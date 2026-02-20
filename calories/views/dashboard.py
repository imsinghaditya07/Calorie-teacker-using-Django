"""Dashboard view."""
from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import FoodLog, UserProfile, MealType
from ..forms import QuickLogForm


@login_required
def dashboard(request):
    today = date.today()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    logs = FoodLog.objects.filter(user=request.user, date=today).select_related('food_item')

    # Aggregate totals
    totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    meals = {m[0]: [] for m in MealType.choices}
    meal_totals = {m[0]: 0 for m in MealType.choices}

    for log in logs:
        totals['calories'] += log.calories
        totals['protein'] += log.protein
        totals['carbs'] += log.carbs
        totals['fat'] += log.fat
        meals[log.meal_type].append(log)
        meal_totals[log.meal_type] += log.calories

    totals = {k: round(v, 1) for k, v in totals.items()}

    goal = profile.daily_calorie_goal
    pct = min(round(totals['calories'] / goal * 100), 100) if goal else 0
    remaining = max(goal - totals['calories'], 0)

    # Macro percentages (based on caloric contribution)
    total_macro_cals = (totals['protein'] * 4 + totals['carbs'] * 4 + totals['fat'] * 9)
    macro_pct = {
        'protein': round(totals['protein'] * 4 / total_macro_cals * 100) if total_macro_cals else 0,
        'carbs':   round(totals['carbs']   * 4 / total_macro_cals * 100) if total_macro_cals else 0,
        'fat':     round(totals['fat']     * 9 / total_macro_cals * 100) if total_macro_cals else 0,
    }

    context = {
        'today': today,
        'logs': logs,
        'meals': meals,
        'meal_totals': meal_totals,
        'totals': totals,
        'goal': goal,
        'pct': pct,
        'remaining': round(remaining, 1),
        'macro_pct': macro_pct,
        'profile': profile,
        'quick_log_form': QuickLogForm(initial={'date': today}),
        'meal_types': MealType.choices,
    }
    return render(request, 'dashboard.html', context)

# Dashboard display logic
