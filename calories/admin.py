from django.contrib import admin
from .models import FoodItem, FoodLog, WeightLog, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'daily_calorie_goal', 'gender', 'height_cm', 'weight_kg']
    search_fields = ['user__username', 'user__email']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'calories_per_100g', 'protein_g', 'carbs_g', 'fat_g', 'category', 'is_custom']
    list_filter = ['category', 'is_custom']
    search_fields = ['name']
    list_editable = ['calories_per_100g', 'category']


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'food_item', 'quantity_g', 'meal_type', 'date']
    list_filter = ['meal_type', 'date']
    search_fields = ['user__username', 'food_item__name']
    date_hierarchy = 'date'


@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight_kg', 'date']
    list_filter = ['date']
    search_fields = ['user__username']
    date_hierarchy = 'date'

# Setup admin configurations for the app
