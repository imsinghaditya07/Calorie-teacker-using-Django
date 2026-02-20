from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # Dashboard — accessible at both / and /dashboard/
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_alias'),

    # Food Log
    path('log/add/', views.add_food_log, name='add_food_log'),
    path('log/<int:pk>/edit/', views.edit_food_log, name='edit_food_log'),
    path('log/<int:pk>/delete/', views.delete_food_log, name='delete_food_log'),

    # Food Search API
    path('api/food/search/', views.food_search_api, name='food_search_api'),
    path('api/food/<int:pk>/', views.food_detail_api, name='food_detail_api'),

    # Custom Food
    path('food/create/', views.create_custom_food, name='create_custom_food'),

    # Weight Tracker
    path('weight/', views.weight_tracker, name='weight_tracker'),
    path('weight/<int:pk>/delete/', views.delete_weight_log, name='delete_weight_log'),

    # History
    path('history/', views.history, name='history'),

    # Food Calculator
    path('calculator/', views.food_calculator, name='food_calculator'),
    path('log/bulk/', views.bulk_food_log, name='bulk_food_log'),

    # Profile
    path('profile/', views.profile, name='profile'),
]
