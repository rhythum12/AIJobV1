"""
User API URL routing
"""

from django.urls import path
from .simple_user_views import (
    user_profile, 
    user_activities, 
    sync_user,
    user_preferences,
    user_settings,
    list_all_users
)

urlpatterns = [
    # User profile endpoints
    path('profile/', user_profile, name='user_profile'),
    path('profile/<str:user_id>/', user_profile, name='user_profile_detail'),
    
    # User activities
    path('activities/', user_activities, name='user_activities'),
    
    # User sync
    path('sync/', sync_user, name='sync_user'),
    
    # User preferences and settings
    path('preferences/', user_preferences, name='user_preferences'),
    path('settings/', user_settings, name='user_settings'),
    
    # List all users
    path('list/', list_all_users, name='list_all_users'),
]
