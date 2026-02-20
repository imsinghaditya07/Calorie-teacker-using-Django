"""User profile view."""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import UserProfile
from ..forms import ProfileForm


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name  = form.cleaned_data.get('last_name', '')
            request.user.email      = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile, initial={
            'first_name': request.user.first_name,
            'last_name':  request.user.last_name,
            'email':      request.user.email,
        })

    return render(request, 'profile.html', {'form': form, 'profile': user_profile})
