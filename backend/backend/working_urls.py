# """
# Working URL Configuration - Simple endpoints without database dependencies
# """

# from django.contrib import admin
# from django.urls import path
# from django.http import JsonResponse

# def health_check(request):
#     """Health check endpoint"""
#     return JsonResponse({
#         'status': 'healthy',
#         'message': 'Job Recommender API is running',
#         'version': '1.0.0',
#         'database_status': 'MongoDB and PostgreSQL containers running',
#         'endpoints': [
#             '/health/',
#             '/api/users/profile/',
#             '/api/users/sync/',
#             '/api/users/activities/'
#         ]
#     })

# def user_profile(request):
#     """User profile endpoint"""
#     return JsonResponse({
#         'message': 'User profile endpoint - ready for authentication',
#         'status': 'ready',
#         'note': 'This endpoint will sync users with MongoDB and PostgreSQL when authentication is implemented'
#     })

# def user_sync(request):
#     """User sync endpoint"""
#     return JsonResponse({
#         'message': 'User sync endpoint - ready for Firebase integration',
#         'status': 'ready',
#         'note': 'This endpoint will sync Firebase users with both databases'
#     })

# def user_activities(request):
#     """User activities endpoint"""
#     return JsonResponse({
#         'message': 'User activities endpoint - ready for activity tracking',
#         'status': 'ready',
#         'note': 'This endpoint will track user activities in MongoDB'
#     })

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('health/', health_check, name='health_check'),
#     path('api/users/profile/', user_profile, name='user_profile'),
#     path('api/users/sync/', user_sync, name='user_sync'),
#     path('api/users/activities/', user_activities, name='user_activities'),
# ]

"""
Page URL routing - Backend URLs matching frontend page routes
"""

from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({'status': 'healthy', 'message': 'Job Recommender API is running'})

from .page_views import (
    home_page,
    login_page,
    registration_page,
    password_reset_page,
    dashboard_page,
    jobs_page,
    resume_analysis_page,
    edit_resume_page,
    applied_jobs_page,
    saved_jobs_page,
    profile_page,
    about_page,
    about_guest_page,
    contact_page
)

urlpatterns = [
    # API endpoints
    path('api/', include('api.urls')),
    path('api/users/', include('api.user_urls')),
    path('health/', health_check, name='health_check'),
    
    # Home page
    path('', home_page, name='home_page'),
    
    # Authentication pages
    path('loginpage/', login_page, name='login_page'),
    path('registration/', registration_page, name='registration_page'),
    path('passwordreset/', password_reset_page, name='password_reset_page'),
    
    # Main application pages
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('jobs/', jobs_page, name='jobs_page'),
    path('resumeanalysis/', resume_analysis_page, name='resume_analysis_page'),
    path('editresume/', edit_resume_page, name='edit_resume_page'),
    path('appliedjobs/', applied_jobs_page, name='applied_jobs_page'),
    path('savedjobs/', saved_jobs_page, name='saved_jobs_page'),
    path('profile/', profile_page, name='profile_page'),
    
    # Public pages
    path('about/', about_page, name='about_page'),
    path('aboutpageguest/', about_guest_page, name='about_guest_page'),
    path('contact/', contact_page, name='contact_page'),
]
