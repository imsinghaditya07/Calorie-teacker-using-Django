"""Food calculator and bulk log views."""
import json
from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import FoodItem, FoodLog, MealType


@login_required
def food_calculator(request):
    return render(request, 'food_calculator.html', {
        'meal_types': MealType.choices,
    })


@login_required
def bulk_food_log(request):
    """Accept a JSON list of {id, qty} items from the Food Calculator and log them all."""
    if request.method != 'POST':
        return redirect('food_calculator')

    raw = request.POST.get('bulk_data', '[]')
    meal_type = request.POST.get('meal_type', MealType.LUNCH)
    today = date.today()

    try:
        items = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        messages.error(request, 'Invalid data. Please try again.')
        return redirect('food_calculator')

    logged = 0
    for item in items:
        food_id = item.get('id')
        qty = float(item.get('qty', 100))
        try:
            food = FoodItem.objects.get(pk=food_id)
            FoodLog.objects.create(
                user=request.user,
                food_item=food,
                quantity_g=qty,
                meal_type=meal_type,
                date=today,
            )
            logged += 1
        except (FoodItem.DoesNotExist, ValueError, TypeError):
            continue

    if logged:
        messages.success(request, f'✅ {logged} food item{"s" if logged > 1 else ""} logged to today\'s diary!')
    else:
        messages.error(request, 'No valid items were logged.')

    return redirect('dashboard')

# Logic for calorie calculation
