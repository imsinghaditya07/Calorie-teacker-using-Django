"""Food log CRUD views: add, edit, delete."""
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import FoodLog
from ..forms import QuickLogForm, FoodLogForm


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

# Views for logging food intake
