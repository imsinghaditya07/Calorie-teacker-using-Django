"""Food search & detail JSON API views."""
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from ..models import FoodItem


@login_required
def food_search_api(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 1:
        return JsonResponse({'results': []})

    items = FoodItem.objects.filter(
        Q(name__icontains=q) & (Q(is_custom=False) | Q(created_by=request.user))
    )[:20]

    results = [{
        'id':       item.pk,
        'name':     item.name,
        'calories': item.calories_per_100g,
        'protein':  item.protein_g,
        'carbs':    item.carbs_g,
        'fat':      item.fat_g,
        'category': item.get_category_display(),
    } for item in items]

    return JsonResponse({'results': results})


@login_required
def food_detail_api(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    return JsonResponse({
        'id':               item.pk,
        'name':             item.name,
        'calories_per_100g': item.calories_per_100g,
        'protein_g':        item.protein_g,
        'carbs_g':          item.carbs_g,
        'fat_g':            item.fat_g,
        'fiber_g':          item.fiber_g,
    })
