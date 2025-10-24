"""
Main API URL routing
"""

from django.urls import path
from . import views

urlpatterns = [
    # Health and status endpoints
    path('health/', views.health_check, name='api_health'),
    path('status/', views.api_status, name='api_status'),
    
    # Job endpoints
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/search/', views.job_search, name='job_search'),
    path('jobs/recommendations/', views.job_recommendations, name='job_recommendations'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('jobs/<int:job_id>/save/', views.save_job, name='save_job'),
    path('jobs/<int:job_id>/unsave/', views.unsave_job, name='unsave_job'),
    path('jobs/skills/', views.get_skills, name='get_skills'),
    path('jobs/categories/', views.get_categories, name='get_categories'),
    
    # AI Job endpoints
    path('jobs/ai/', views.get_ai_jobs, name='get_ai_jobs'),
    path('jobs/ai/refresh/', views.refresh_ai_jobs, name='refresh_ai_jobs'),
    path('jobs/ai/save/', views.save_ai_job, name='save_ai_job'),
    
    # Resume endpoints
    path('resume/upload/', views.resume_upload, name='resume_upload'),
    path('resume/analyze/', views.resume_analysis, name='resume_analysis'),
    path('resume/update/', views.resume_update, name='resume_update'),
    
    # User endpoints
    path('user/applied-jobs/', views.applied_jobs, name='applied_jobs'),
    path('user/saved-jobs/', views.saved_jobs, name='saved_jobs'),
    path('user/preferences/', views.user_preferences, name='user_preferences'),
    path('user/settings/', views.user_settings, name='user_settings'),
    
    # Analytics endpoints
    path('analytics/dashboard/', views.dashboard_analytics, name='dashboard_analytics'),
    path('analytics/job-trends/', views.job_trends, name='job_trends')
]