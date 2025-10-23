"""
Page URL routing - Backend URLs matching frontend page routes
"""

from django.urls import path
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

