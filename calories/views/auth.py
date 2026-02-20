"""Auth views: register, login, logout."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from ..models import UserProfile
from ..forms import RegisterForm


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
            # Validate next URL — prevent open-redirect attacks
            next_url = request.GET.get('next', '')
            if next_url and next_url.startswith('/') and not next_url.startswith('//'):
                return redirect(next_url)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html', {})


def logout_view(request):
    logout(request)
    return redirect('login')
