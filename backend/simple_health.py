#!/usr/bin/env python3
"""
Simple Health Check Server
Minimal Django server for testing
"""

import os
import sys
import django
from django.http import JsonResponse
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.simple_settings')

# Initialize Django
django.setup()

from django.urls import path
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Job Recommender API is running',
        'version': '1.0.0',
        'endpoints': [
            '/health/',
            '/api/users/profile/',
            '/api/users/sync/',
            '/api/users/activities/'
        ]
    })

def user_profile(request):
    """User profile endpoint"""
    return JsonResponse({
        'message': 'User profile endpoint - requires authentication',
        'status': 'ready'
    })

def user_sync(request):
    """User sync endpoint"""
    return JsonResponse({
        'message': 'User sync endpoint - requires authentication',
        'status': 'ready'
    })

def user_activities(request):
    """User activities endpoint"""
    return JsonResponse({
        'message': 'User activities endpoint - requires authentication',
        'status': 'ready'
    })

# URL patterns
urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('api/users/profile/', user_profile, name='user_profile'),
    path('api/users/sync/', user_sync, name='user_sync'),
    path('api/users/activities/', user_activities, name='user_activities'),
]

# Create WSGI application
application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    print("🚀 Starting Simple Health Check Server...")
    print("=" * 50)
    print("✅ Django initialized successfully")
    print("📊 API endpoints available at:")
    print("   • http://localhost:8000/health/")
    print("   • http://localhost:8000/api/users/profile/")
    print("   • http://localhost:8000/api/users/sync/")
    print("   • http://localhost:8000/api/users/activities/")
    print("=" * 50)
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
