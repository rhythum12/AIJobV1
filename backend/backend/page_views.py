"""
Page views for serving React application
"""

from django.http import HttpResponse
from django.shortcuts import render
import os

def serve_react_app(request):
    """Serve the React application"""
    try:
        # Path to the React build directory
        build_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'frontend', 'build')
        index_path = os.path.join(build_path, 'index.html')
        
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HttpResponse(content, content_type='text/html')
        else:
            return HttpResponse("React app not built. Please run 'npm run build' in the frontend directory.", status=404)
    except Exception as e:
        return HttpResponse(f"Error serving React app: {str(e)}", status=500)

# All page routes serve the React app
home_page = serve_react_app
login_page = serve_react_app
registration_page = serve_react_app
password_reset_page = serve_react_app
dashboard_page = serve_react_app
jobs_page = serve_react_app
resume_analysis_page = serve_react_app
edit_resume_page = serve_react_app
applied_jobs_page = serve_react_app
saved_jobs_page = serve_react_app
profile_page = serve_react_app
about_page = serve_react_app
about_guest_page = serve_react_app
contact_page = serve_react_app

