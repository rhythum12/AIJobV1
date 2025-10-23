"""
User API URL routing
"""

from django.urls import path
from .user_views import user_profile, user_activities, sync_user

urlpatterns = [
    # User profile endpoints
    path('profile/', user_profile, name='user_profile'),
    path('profile/<str:user_id>/', user_profile, name='user_profile_detail'),
    
    # User activities
    path('activities/', user_activities, name='user_activities'),
    
    # User sync
    path('sync/', sync_user, name='sync_user'),
]
