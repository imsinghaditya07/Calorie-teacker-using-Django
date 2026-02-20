"""History view — 30-day calorie & macro chart."""
import json
from datetime import date, timedelta
from collections import defaultdict

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import FoodLog, UserProfile


@login_required
def history(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    end   = date.today()
    start = end - timedelta(days=29)

    logs = FoodLog.objects.filter(
        user=request.user, date__range=(start, end)
    ).select_related('food_item')

    daily = defaultdict(lambda: {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0})
    for log in logs:
        key = str(log.date)
        daily[key]['calories'] += log.calories
        daily[key]['protein']  += log.protein
        daily[key]['carbs']    += log.carbs
        daily[key]['fat']      += log.fat

    labels, cal_data, protein_data, carb_data, fat_data = [], [], [], [], []

    for i in range(30):
        d = str(start + timedelta(days=i))
        labels.append(d[5:])  # MM-DD
        cal_data.append(round(daily[d]['calories'], 1))
        protein_data.append(round(daily[d]['protein'], 1))
        carb_data.append(round(daily[d]['carbs'], 1))
        fat_data.append(round(daily[d]['fat'], 1))

    avg_calories = round(sum(cal_data) / max(sum(1 for c in cal_data if c > 0), 1), 1)

    return render(request, 'history.html', {
        'labels':       json.dumps(labels),
        'cal_data':     json.dumps(cal_data),
        'protein_data': json.dumps(protein_data),
        'carb_data':    json.dumps(carb_data),
        'fat_data':     json.dumps(fat_data),
        'avg_calories': avg_calories,
        'goal':         profile.daily_calorie_goal,
    })

# Historical data viewing logic
