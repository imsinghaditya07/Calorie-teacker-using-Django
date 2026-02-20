from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, FoodLog, WeightLog, FoodItem, MealType


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Choose a username',
            'first_name': 'Your first name',
            'last_name': 'Your last name',
            'email': 'your@email.com',
            'password1': 'Create a strong password',
            'password2': 'Repeat your password',
        }
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'afc-input'
            field.widget.attrs['autocomplete'] = 'off'
            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]
        # Remove verbose help text
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = 'Min 8 characters, not too common.'
        self.fields['password2'].help_text = ''


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['daily_calorie_goal', 'height_cm', 'weight_kg', 'date_of_birth', 'gender', 'avatar_color']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'avatar_color': forms.TextInput(attrs={'type': 'color'}),
            'daily_calorie_goal': forms.NumberInput(attrs={'min': '500', 'max': '10000'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        fields = ['food_item', 'quantity_g', 'meal_type', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'quantity_g': forms.NumberInput(attrs={'min': '1', 'max': '5000', 'step': '0.5'}),
            'notes': forms.TextInput(attrs={'placeholder': 'Optional note...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['food_item'].widget.attrs['class'] = 'form-control food-select'


class QuickLogForm(forms.ModelForm):
    """Simplified form used from dashboard – food_item set via search."""
    class Meta:
        model = FoodLog
        fields = ['food_item', 'quantity_g', 'meal_type', 'date', 'notes']
        widgets = {
            'food_item': forms.HiddenInput(),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'quantity_g': forms.NumberInput(attrs={'min': '1', 'max': '5000', 'step': '0.5', 'value': '100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'food_item':
                field.widget.attrs['class'] = 'form-control'


class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['weight_kg', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'weight_kg': forms.NumberInput(attrs={'min': '20', 'max': '500', 'step': '0.1'}),
            'notes': forms.TextInput(attrs={'placeholder': 'Optional note...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CustomFoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'calories_per_100g', 'protein_g', 'carbs_g', 'fat_g', 'fiber_g', 'category']
        widgets = {
            'calories_per_100g': forms.NumberInput(attrs={'min': '0', 'step': '0.1'}),
            'protein_g': forms.NumberInput(attrs={'min': '0', 'step': '0.1'}),
            'carbs_g': forms.NumberInput(attrs={'min': '0', 'step': '0.1'}),
            'fat_g': forms.NumberInput(attrs={'min': '0', 'step': '0.1'}),
            'fiber_g': forms.NumberInput(attrs={'min': '0', 'step': '0.1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# Form classes for data validation
