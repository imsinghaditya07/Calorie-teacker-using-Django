from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    avatar_color = models.CharField(max_length=7, default='#38bdf8')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def get_tdee(self):
        """Calculate Total Daily Energy Expenditure (Mifflin-St Jeor)."""
        if not (self.height_cm and self.weight_kg and self.date_of_birth and self.gender):
            return self.daily_calorie_goal
        age = self.age
        if self.gender == 'M':
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * age + 5
        else:
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * age - 161
        return round(bmr * 1.55)  # Moderate activity


class FoodCategory(models.TextChoices):
    VEGETABLES = 'vegetables', 'Vegetables'
    FRUITS = 'fruits', 'Fruits'
    GRAINS = 'grains', 'Grains & Cereals'
    PROTEIN = 'protein', 'Protein & Meat'
    DAIRY = 'dairy', 'Dairy'
    SNACKS = 'snacks', 'Snacks & Fast Food'
    BEVERAGES = 'beverages', 'Beverages'
    LEGUMES = 'legumes', 'Legumes & Beans'
    NUTS = 'nuts', 'Nuts & Seeds'
    OILS = 'oils', 'Oils & Fats'
    OTHER = 'other', 'Other'


class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    calories_per_100g = models.FloatField()
    protein_g = models.FloatField(default=0)
    carbs_g = models.FloatField(default=0)
    fat_g = models.FloatField(default=0)
    fiber_g = models.FloatField(default=0)
    category = models.CharField(
        max_length=20,
        choices=FoodCategory.choices,
        default=FoodCategory.OTHER
    )
    is_custom = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='custom_foods'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.calories_per_100g} kcal/100g)"

    def calories_for_quantity(self, quantity_g):
        return round(self.calories_per_100g * quantity_g / 100, 1)

    def protein_for_quantity(self, quantity_g):
        return round(self.protein_g * quantity_g / 100, 1)

    def carbs_for_quantity(self, quantity_g):
        return round(self.carbs_g * quantity_g / 100, 1)

    def fat_for_quantity(self, quantity_g):
        return round(self.fat_g * quantity_g / 100, 1)


class MealType(models.TextChoices):
    BREAKFAST = 'breakfast', 'Breakfast'
    LUNCH = 'lunch', 'Lunch'
    DINNER = 'dinner', 'Dinner'
    SNACK = 'snack', 'Snack'


class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_logs')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity_g = models.FloatField(default=100)
    date = models.DateField(default=timezone.now)
    meal_type = models.CharField(
        max_length=15,
        choices=MealType.choices,
        default=MealType.LUNCH
    )
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['meal_type', 'created_at']

    def __str__(self):
        return f"{self.user.username} – {self.food_item.name} on {self.date}"

    @property
    def calories(self):
        return round(self.food_item.calories_per_100g * self.quantity_g / 100, 1)

    @property
    def protein(self):
        return round(self.food_item.protein_g * self.quantity_g / 100, 1)

    @property
    def carbs(self):
        return round(self.food_item.carbs_g * self.quantity_g / 100, 1)

    @property
    def fat(self):
        return round(self.food_item.fat_g * self.quantity_g / 100, 1)


class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    weight_kg = models.FloatField()
    date = models.DateField(default=timezone.now)
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} – {self.weight_kg}kg on {self.date}"
