# """
# URL configuration for job_recommender project.
# """

# from django.contrib import admin
# from django.urls import path, include
# from django.http import JsonResponse

# def health_check(request):
#     """Health check endpoint"""
#     return JsonResponse({'status': 'healthy', 'message': 'Job Recommender API is running'})

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('health/', health_check, name='health_check'),
#     path('api/users/', include('api.user_urls')),
#     path('api/', include('api.user_urls')),  # Fallback for API calls
 
# ]
"""
Main URL configuration for job_recommender project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({'status': 'healthy', 'message': 'Job Recommender API is running'})

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', health_check, name='health_check'),
    
    # API endpoints
    path('api/', include('api.urls')),
    path('api/users/', include('api.user_urls')),
    
    # Page routing (for serving React app)
    path('', include('backend.page_urls')),
]
