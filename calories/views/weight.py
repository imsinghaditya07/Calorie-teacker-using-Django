"""Weight tracker views: log, list, delete."""
import json
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import WeightLog, UserProfile
from ..forms import WeightLogForm


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
    chart_data   = [l.weight_kg for l in logs]

    return render(request, 'weight_tracker.html', {
        'form':         form,
        'logs':         WeightLog.objects.filter(user=request.user)[:10],
        'chart_labels': json.dumps(chart_labels),
        'chart_data':   json.dumps(chart_data),
        'profile':      profile,
    })


@login_required
def delete_weight_log(request, pk):
    log = get_object_or_404(WeightLog, pk=pk, user=request.user)
    if request.method == 'POST':
        log.delete()
        messages.success(request, 'Weight entry deleted.')
    return redirect('weight_tracker')

# Weight tracking logic and views
