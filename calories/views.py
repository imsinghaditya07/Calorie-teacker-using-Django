import json
from datetime import date, timedelta
from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.utils import timezone

from .models import FoodItem, FoodLog, WeightLog, UserProfile, MealType
from .forms import (
    RegisterForm, ProfileForm, QuickLogForm,
    FoodLogForm, WeightLogForm, CustomFoodForm
)


# ────────────────────────────────────── AUTH ──────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name or user.username}! Your account is ready.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Validate next URL to prevent open-redirect attacks
            next_url = request.GET.get('next', '')
            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                return redirect(next_url)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html', {})


def logout_view(request):
    logout(request)
    return redirect('login')


# ────────────────────────────────────── DASHBOARD ─────────────────────────────────

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

    # Macro percentages
    total_macro_cals = (totals['protein'] * 4 + totals['carbs'] * 4 + totals['fat'] * 9)
    macro_pct = {
        'protein': round(totals['protein'] * 4 / total_macro_cals * 100) if total_macro_cals else 0,
        'carbs': round(totals['carbs'] * 4 / total_macro_cals * 100) if total_macro_cals else 0,
        'fat': round(totals['fat'] * 9 / total_macro_cals * 100) if total_macro_cals else 0,
    }

    quick_log_form = QuickLogForm(initial={'date': today})

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
        'quick_log_form': quick_log_form,
        'meal_types': MealType.choices,
    }
    return render(request, 'dashboard.html', context)


# ────────────────────────────────────── FOOD LOG ──────────────────────────────────

@login_required
def add_food_log(request):
    if request.method == 'POST':
        form = QuickLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, f'Added {log.food_item.name} to your log!')
            return redirect('dashboard')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = QuickLogForm(initial={'date': date.today()})
    return render(request, 'food_log_form.html', {'form': form, 'title': 'Add Food'})


@login_required
def edit_food_log(request, pk):
    log = get_object_or_404(FoodLog, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FoodLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Log entry updated.')
            return redirect('dashboard')
    else:
        form = FoodLogForm(instance=log)
    return render(request, 'food_log_form.html', {'form': form, 'title': 'Edit Entry', 'log': log})


@login_required
def delete_food_log(request, pk):
    log = get_object_or_404(FoodLog, pk=pk, user=request.user)
    if request.method == 'POST':
        name = log.food_item.name
        log.delete()
        messages.success(request, f'Removed {name} from your log.')
    return redirect('dashboard')


# ────────────────────────────────────── FOOD SEARCH API ───────────────────────────

@login_required
def food_search_api(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 1:
        return JsonResponse({'results': []})

    items = FoodItem.objects.filter(
        Q(name__icontains=q) & (Q(is_custom=False) | Q(created_by=request.user))
    )[:20]

    results = [{
        'id': item.pk,
        'name': item.name,
        'calories': item.calories_per_100g,
        'protein': item.protein_g,
        'carbs': item.carbs_g,
        'fat': item.fat_g,
        'category': item.get_category_display(),
    } for item in items]

    return JsonResponse({'results': results})


@login_required
def food_detail_api(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    return JsonResponse({
        'id': item.pk,
        'name': item.name,
        'calories_per_100g': item.calories_per_100g,
        'protein_g': item.protein_g,
        'carbs_g': item.carbs_g,
        'fat_g': item.fat_g,
        'fiber_g': item.fiber_g,
    })


# ────────────────────────────────────── CUSTOM FOOD ───────────────────────────────

@login_required
def create_custom_food(request):
    if request.method == 'POST':
        form = CustomFoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.is_custom = True
            food.created_by = request.user
            food.save()
            messages.success(request, f'Custom food "{food.name}" added!')
            return redirect('dashboard')
    else:
        form = CustomFoodForm()
    return render(request, 'custom_food.html', {'form': form})


# ────────────────────────────────────── WEIGHT TRACKER ────────────────────────────

@login_required
def weight_tracker(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            entry, created = WeightLog.objects.update_or_create(
                user=request.user,
                date=form.cleaned_data['date'],
                defaults={
                    'weight_kg': form.cleaned_data['weight_kg'],
                    'notes': form.cleaned_data.get('notes', ''),
                }
            )
            messages.success(request, 'Weight logged!' if created else 'Weight updated!')
            return redirect('weight_tracker')
    else:
        form = WeightLogForm(initial={'date': date.today()})

    logs = WeightLog.objects.filter(user=request.user).order_by('date')[:90]
    chart_labels = [str(l.date) for l in logs]
    chart_data = [l.weight_kg for l in logs]

    recent_logs = WeightLog.objects.filter(user=request.user)[:10]

    return render(request, 'weight_tracker.html', {
        'form': form,
        'logs': recent_logs,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'profile': profile,
    })


@login_required
def delete_weight_log(request, pk):
    log = get_object_or_404(WeightLog, pk=pk, user=request.user)
    if request.method == 'POST':
        log.delete()
        messages.success(request, 'Weight entry deleted.')
    return redirect('weight_tracker')


# ────────────────────────────────────── HISTORY ───────────────────────────────────

@login_required
def history(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    end = date.today()
    start = end - timedelta(days=29)

    logs = FoodLog.objects.filter(
        user=request.user, date__range=(start, end)
    ).select_related('food_item')

    daily = defaultdict(lambda: {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0})
    for log in logs:
        key = str(log.date)
        daily[key]['calories'] += log.calories
        daily[key]['protein'] += log.protein
        daily[key]['carbs'] += log.carbs
        daily[key]['fat'] += log.fat

    labels = []
    cal_data = []
    protein_data = []
    carb_data = []
    fat_data = []

    for i in range(30):
        d = str(start + timedelta(days=i))
        labels.append(d[5:])  # MM-DD
        cal_data.append(round(daily[d]['calories'], 1))
        protein_data.append(round(daily[d]['protein'], 1))
        carb_data.append(round(daily[d]['carbs'], 1))
        fat_data.append(round(daily[d]['fat'], 1))

    avg_calories = round(sum(cal_data) / max(sum(1 for c in cal_data if c > 0), 1), 1)

    return render(request, 'history.html', {
        'labels': json.dumps(labels),
        'cal_data': json.dumps(cal_data),
        'protein_data': json.dumps(protein_data),
        'carb_data': json.dumps(carb_data),
        'fat_data': json.dumps(fat_data),
        'avg_calories': avg_calories,
        'goal': profile.daily_calorie_goal,
    })


# ────────────────────────────────────── PROFILE ───────────────────────────────────

@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            # Update User model fields too
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileForm(instance=user_profile, initial=initial)

    return render(request, 'profile.html', {'form': form, 'profile': user_profile})


# ────────────────────────────────────── FOOD CALCULATOR ───────────────────────────

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

