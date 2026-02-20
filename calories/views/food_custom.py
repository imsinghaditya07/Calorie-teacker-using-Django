"""Custom food creation view."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..forms import CustomFoodForm


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
