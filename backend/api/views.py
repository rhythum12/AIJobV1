"""
Comprehensive REST API Views for Job Recommender System
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from firebase_admin import auth as firebase_auth
from firebase_admin.exceptions import FirebaseError

# from services.user_service import user_service
# from models.user_models import UserProfile, UserPreferences

logger = logging.getLogger(__name__)

# Health and Status Endpoints
@api_view(['GET'])
def health_check(request):
    """API health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Job Recommender API is running',
        'timestamp': datetime.now().isoformat()
    })

@api_view(['GET'])
def api_status(request):
    """Detailed API status endpoint"""
    return Response({
        'status': 'operational',
        'version': '1.0.0',
        'services': {
            'database': 'connected',
            'firebase': 'connected',
            'job_scraper': 'active'
        },
        'timestamp': datetime.now().isoformat()
    })

# Job-related Endpoints
@api_view(['GET'])
def job_list(request):
    """Get list of available jobs"""
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        category = request.GET.get('category', '')
        location = request.GET.get('location', '')
        
        # Mock job data - replace with actual database queries
        jobs = [
            {
                'id': 1,
                'title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'salary': '$120,000 - $150,000',
                'description': 'We are looking for a senior software engineer...',
                'requirements': ['Python', 'Django', 'React', 'PostgreSQL'],
                'posted_date': '2024-01-15',
                'application_deadline': '2024-02-15'
            },
            {
                'id': 2,
                'title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'location': 'Remote',
                'salary': '$90,000 - $120,000',
                'description': 'Join our growing team as a full stack developer...',
                'requirements': ['JavaScript', 'Node.js', 'React', 'MongoDB'],
                'posted_date': '2024-01-14',
                'application_deadline': '2024-02-14'
            }
        ]
        
        return Response({
            'success': True,
            'jobs': jobs,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': len(jobs)
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting job list: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def job_detail(request, job_id):
    """Get detailed information about a specific job"""
    try:
        # Mock job detail - replace with actual database query
        job_detail = {
            'id': job_id,
            'title': 'Senior Software Engineer',
            'company': 'Tech Corp',
            'location': 'San Francisco, CA',
            'salary': '$120,000 - $150,000',
            'description': 'We are looking for a senior software engineer to join our team...',
            'requirements': ['Python', 'Django', 'React', 'PostgreSQL', 'AWS'],
            'benefits': ['Health Insurance', '401k', 'Flexible Hours', 'Remote Work'],
            'posted_date': '2024-01-15',
            'application_deadline': '2024-02-15',
            'company_info': {
                'name': 'Tech Corp',
                'size': '100-500 employees',
                'industry': 'Technology',
                'website': 'https://techcorp.com'
            }
        }
        
        return Response({
            'success': True,
            'job': job_detail
        })
        
    except Exception as e:
        logger.error(f"Error getting job detail: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def job_search(request):
    """Search jobs with filters"""
    try:
        query = request.GET.get('q', '')
        location = request.GET.get('location', '')
        category = request.GET.get('category', '')
        salary_min = request.GET.get('salary_min', '')
        salary_max = request.GET.get('salary_max', '')
        
        # Mock search results - replace with actual search logic
        search_results = [
            {
                'id': 1,
                'title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'salary': '$120,000 - $150,000',
                'match_score': 95
            }
        ]
        
        return Response({
            'success': True,
            'results': search_results,
            'filters_applied': {
                'query': query,
                'location': location,
                'category': category,
                'salary_range': f"{salary_min}-{salary_max}"
            }
        })
        
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def job_recommendations(request):
    """Get personalized job recommendations for user"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Mock recommendations - replace with actual ML recommendation logic
        recommendations = [
            {
                'id': 1,
                'title': 'Senior Python Developer',
                'company': 'AI Startup',
                'location': 'San Francisco, CA',
                'salary': '$130,000 - $160,000',
                'match_score': 92,
                'reason': 'Matches your Python and Django experience'
            },
            {
                'id': 2,
                'title': 'Full Stack Developer',
                'company': 'FinTech Corp',
                'location': 'New York, NY',
                'salary': '$110,000 - $140,000',
                'match_score': 88,
                'reason': 'Aligns with your React and JavaScript skills'
            }
        ]
        
        return Response({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        logger.error(f"Error getting job recommendations: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Resume and Profile Endpoints
@api_view(['POST'])
def resume_upload(request):
    """Upload and process user resume"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if 'resume' not in request.FILES:
            return Response({'error': 'No resume file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        resume_file = request.FILES['resume']
        
        # Save file and process
        file_path = default_storage.save(f'resumes/{firebase_uid}_{resume_file.name}', ContentFile(resume_file.read()))
        
        # Mock processing result
        processing_result = {
            'file_path': file_path,
            'status': 'processed',
            'extracted_text': 'Sample extracted text from resume...',
            'skills': ['Python', 'Django', 'React', 'JavaScript', 'PostgreSQL'],
            'experience': '5+ years',
            'education': 'Bachelor of Computer Science'
        }
        
        return Response({
            'success': True,
            'message': 'Resume uploaded and processed successfully',
            'result': processing_result
        })
        
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def resume_analysis(request):
    """Analyze user resume and provide insights"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Mock analysis result
        analysis_result = {
            'overall_score': 85,
            'strengths': [
                'Strong technical skills in Python and Django',
                'Good experience with React and JavaScript',
                'Database knowledge with PostgreSQL'
            ],
            'improvements': [
                'Consider adding cloud technologies (AWS, Azure)',
                'Include more project management experience',
                'Add certifications in relevant technologies'
            ],
            'skill_gaps': [
                'Machine Learning',
                'DevOps',
                'Microservices Architecture'
            ],
            'recommendations': [
                'Focus on cloud certifications',
                'Learn containerization with Docker',
                'Practice system design concepts'
            ]
        }
        
        return Response({
            'success': True,
            'analysis': analysis_result
        })
        
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def resume_update(request):
    """Update user resume information"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Parse request data
        try:
            resume_data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mock update result
        return Response({
            'success': True,
            'message': 'Resume updated successfully',
            'updated_fields': list(resume_data.keys())
        })
        
    except Exception as e:
        logger.error(f"Error updating resume: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Job Interaction Endpoints
@api_view(['POST'])
def apply_job(request, job_id):
    """Apply for a specific job"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Mock application result
        return Response({
            'success': True,
            'message': 'Application submitted successfully',
            'application_id': f'APP_{job_id}_{firebase_uid}',
            'status': 'submitted',
            'applied_date': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error applying for job: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def save_job(request, job_id):
    """Save a job for later"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'success': True,
            'message': 'Job saved successfully',
            'saved_date': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error saving job: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def unsave_job(request, job_id):
    """Remove a job from saved jobs"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'success': True,
            'message': 'Job removed from saved jobs'
        })
        
    except Exception as e:
        logger.error(f"Error unsaving job: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def applied_jobs(request):
    """Get user's applied jobs"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Mock applied jobs data
        applied_jobs = [
            {
                'id': 1,
                'job_title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'applied_date': '2024-01-10',
                'status': 'Under Review',
                'application_id': 'APP_1_12345'
            },
            {
                'id': 2,
                'job_title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'applied_date': '2024-01-08',
                'status': 'Interview Scheduled',
                'application_id': 'APP_2_12345'
            }
        ]
        
        return Response({
            'success': True,
            'applied_jobs': applied_jobs
        })
        
    except Exception as e:
        logger.error(f"Error getting applied jobs: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def saved_jobs(request):
    """Get user's saved jobs"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Mock saved jobs data
        saved_jobs = [
            {
                'id': 3,
                'job_title': 'DevOps Engineer',
                'company': 'CloudTech',
                'saved_date': '2024-01-12',
                'location': 'Remote',
                'salary': '$100,000 - $130,000'
            }
        ]
        
        return Response({
            'success': True,
            'saved_jobs': saved_jobs
        })
        
    except Exception as e:
        logger.error(f"Error getting saved jobs: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Preferences and Settings
@api_view(['GET', 'PUT'])
def user_preferences(request):
    """Get or update user preferences"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.method == 'GET':
            # Mock user preferences
            preferences = {
                'job_categories': ['Software Engineering', 'Data Science'],
                'locations': ['San Francisco', 'Remote'],
                'salary_range': {'min': 80000, 'max': 150000},
                'work_type': ['Full-time', 'Contract'],
                'experience_level': 'Senior',
                'skills': ['Python', 'React', 'Django']
            }
            
            return Response({
                'success': True,
                'preferences': preferences
            })
        
        elif request.method == 'PUT':
            # Parse request data
            try:
                preferences_data = json.loads(request.body)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': True,
                'message': 'Preferences updated successfully',
                'updated_preferences': preferences_data
            })
        
    except Exception as e:
        logger.error(f"Error handling user preferences: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT'])
def user_settings(request):
    """Get or update user settings"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.method == 'GET':
            # Mock user settings
            settings = {
                'notifications': {
                    'email': True,
                    'push': True,
                    'job_alerts': True,
                    'application_updates': True
                },
                'privacy': {
                    'profile_visibility': 'public',
                    'show_salary': True
                },
                'account': {
                    'two_factor_auth': False,
                    'data_retention': '1_year'
                }
            }
            
            return Response({
                'success': True,
                'settings': settings
            })
        
        elif request.method == 'PUT':
            # Parse request data
            try:
                settings_data = json.loads(request.body)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': True,
                'message': 'Settings updated successfully',
                'updated_settings': settings_data
            })
        
    except Exception as e:
        logger.error(f"Error handling user settings: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Analytics and Insights
@api_view(['GET'])
def dashboard_analytics(request):
    """Get dashboard analytics for user"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Mock analytics data
        analytics = {
            'profile_completion': 85,
            'applications_this_month': 12,
            'interviews_scheduled': 3,
            'job_matches': 8,
            'skill_gaps': ['AWS', 'Docker', 'Kubernetes'],
            'recommendation_score': 92,
            'activity_trend': [
                {'date': '2024-01-01', 'applications': 2},
                {'date': '2024-01-02', 'applications': 1},
                {'date': '2024-01-03', 'applications': 3}
            ]
        }
        
        return Response({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        logger.error(f"Error getting dashboard analytics: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def job_trends(request):
    """Get job market trends and insights"""
    try:
        # Mock job trends data
        trends = {
            'popular_skills': [
                {'skill': 'Python', 'demand': 95, 'growth': 15},
                {'skill': 'React', 'demand': 88, 'growth': 12},
                {'skill': 'AWS', 'demand': 82, 'growth': 20}
            ],
            'salary_trends': {
                'software_engineer': {'min': 80000, 'max': 150000, 'avg': 115000},
                'data_scientist': {'min': 90000, 'max': 160000, 'avg': 125000}
            },
            'location_insights': [
                {'location': 'San Francisco', 'job_count': 1250, 'avg_salary': 140000},
                {'location': 'New York', 'job_count': 980, 'avg_salary': 135000},
                {'location': 'Remote', 'job_count': 2100, 'avg_salary': 120000}
            ]
        }
        
        return Response({
            'success': True,
            'trends': trends
        })
        
    except Exception as e:
        logger.error(f"Error getting job trends: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Helper function for Firebase authentication
def _get_firebase_uid_from_request(request) -> Optional[str]:
    """Extract Firebase UID from request headers or token"""
    try:
        # Get Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        # Extract token
        token = auth_header.split(' ')[1]
        
        # Verify token and get UID
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token['uid']
        
    except FirebaseError as e:
        logger.error(f"Firebase authentication error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error extracting Firebase UID: {e}")
        return None