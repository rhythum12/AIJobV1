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
        from api.models import Job, Company, JobCategory
        
        # Get query parameters
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        category = request.GET.get('category', '')
        location = request.GET.get('location', '')
        job_type = request.GET.get('job_type', '')
        work_location = request.GET.get('work_location', '')
        
        # Build query
        jobs_query = Job.objects.filter(is_active=True).select_related('company', 'category')
        
        # Apply filters
        if category:
            jobs_query = jobs_query.filter(category__name__icontains=category)
        if location:
            jobs_query = jobs_query.filter(location__icontains=location)
        if job_type:
            jobs_query = jobs_query.filter(job_type=job_type)
        if work_location:
            jobs_query = jobs_query.filter(work_location=work_location)
        
        # Get total count
        total_jobs = jobs_query.count()
        
        # Apply pagination
        start = (page - 1) * limit
        end = start + limit
        jobs = jobs_query[start:end]
        
        # Serialize jobs
        jobs_data = []
        for job in jobs:
            # Get required skills
            required_skills = list(job.skill_requirements.filter(is_required=True).values_list('skill__name', flat=True))
            
            job_data = {
                'id': job.id,
                'title': job.title,
                'company': job.company.name,
                'company_id': job.company.id,
                'location': job.location,
                'salary': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Salary not specified",
                'description': job.description,
                'requirements': required_skills,
                'job_type': job.job_type,
                'work_location': job.work_location,
                'category': job.category.name if job.category else None,
                'posted_date': job.posted_date.isoformat(),
                'application_deadline': job.application_deadline.isoformat() if job.application_deadline else None,
                'is_featured': job.is_featured,
                'views_count': job.views_count,
                'applications_count': job.applications_count
            }
            jobs_data.append(job_data)
        
        return Response({
            'success': True,
            'jobs': jobs_data,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_jobs,
                'pages': (total_jobs + limit - 1) // limit
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting job list: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def job_detail(request, job_id):
    """Get detailed information about a specific job"""
    try:
        from api.models import Job
        
        # Get job from database
        try:
            job = Job.objects.select_related('company', 'category').get(id=job_id, is_active=True)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Increment view count
        job.views_count += 1
        job.save(update_fields=['views_count'])
        
        # Get required skills
        required_skills = list(job.skill_requirements.filter(is_required=True).values_list('skill__name', flat=True))
        
        # Serialize job detail
        job_detail = {
            'id': job.id,
            'title': job.title,
            'company': job.company.name,
            'company_id': job.company.id,
            'location': job.location,
            'salary': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Salary not specified",
            'description': job.description,
            'requirements': job.requirements,
            'responsibilities': job.responsibilities,
            'benefits': job.benefits,
            'required_skills': required_skills,
            'job_type': job.job_type,
            'work_location': job.work_location,
            'category': job.category.name if job.category else None,
            'posted_date': job.posted_date.isoformat(),
            'application_deadline': job.application_deadline.isoformat() if job.application_deadline else None,
            'application_url': job.application_url,
            'application_email': job.application_email,
            'is_featured': job.is_featured,
            'views_count': job.views_count,
            'applications_count': job.applications_count,
            'company_info': {
                'name': job.company.name,
                'description': job.company.description,
                'website': job.company.website,
                'industry': job.company.industry,
                'size': job.company.size,
                'location': job.company.location,
                'logo_url': job.company.logo_url
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
        from api.models import Job
        from django.db.models import Q
        
        query = request.GET.get('q', '')
        location = request.GET.get('location', '')
        category = request.GET.get('category', '')
        salary_min = request.GET.get('salary_min', '')
        salary_max = request.GET.get('salary_max', '')
        job_type = request.GET.get('job_type', '')
        work_location = request.GET.get('work_location', '')
        
        # Build search query
        jobs_query = Job.objects.filter(is_active=True).select_related('company', 'category')
        
        # Text search
        if query:
            jobs_query = jobs_query.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(requirements__icontains=query) |
                Q(company__name__icontains=query)
            )
        
        # Location filter
        if location:
            jobs_query = jobs_query.filter(location__icontains=location)
        
        # Category filter
        if category:
            jobs_query = jobs_query.filter(category__name__icontains=category)
        
        # Job type filter
        if job_type:
            jobs_query = jobs_query.filter(job_type=job_type)
        
        # Work location filter
        if work_location:
            jobs_query = jobs_query.filter(work_location=work_location)
        
        # Salary filters
        if salary_min:
            try:
                salary_min_val = float(salary_min)
                jobs_query = jobs_query.filter(salary_max__gte=salary_min_val)
            except ValueError:
                pass
        
        if salary_max:
            try:
                salary_max_val = float(salary_max)
                jobs_query = jobs_query.filter(salary_min__lte=salary_max_val)
            except ValueError:
                pass
        
        # Get results
        jobs = jobs_query.order_by('-is_featured', '-posted_date')[:50]  # Limit to 50 results
        
        # Serialize results
        search_results = []
        for job in jobs:
            # Calculate match score based on query relevance
            match_score = 100
            if query:
                if query.lower() in job.title.lower():
                    match_score = 95
                elif query.lower() in job.description.lower():
                    match_score = 85
                elif query.lower() in job.company.name.lower():
                    match_score = 80
                else:
                    match_score = 70
            
            job_data = {
                'id': job.id,
                'title': job.title,
                'company': job.company.name,
                'location': job.location,
                'salary': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Salary not specified",
                'job_type': job.job_type,
                'work_location': job.work_location,
                'category': job.category.name if job.category else None,
                'posted_date': job.posted_date.isoformat(),
                'is_featured': job.is_featured,
                'match_score': match_score
            }
            search_results.append(job_data)
        
        return Response({
            'success': True,
            'results': search_results,
            'total_results': len(search_results),
            'filters_applied': {
                'query': query,
                'location': location,
                'category': category,
                'salary_range': f"{salary_min}-{salary_max}",
                'job_type': job_type,
                'work_location': work_location
            }
        })
        
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def job_recommendations(request):
    """Get personalized job recommendations for user"""
    try:
        # Get Firebase UID from request (optional for now)
        firebase_uid = _get_firebase_uid_from_request(request)
        # For now, we'll allow access without authentication for testing
        # In a production environment, you'd want to require authentication
        
        # Mock job recommendations for testing
        recommendations = [
            {
                'id': 1,
                'title': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'salary': '$120,000 - $150,000',
                'description': 'We are looking for a senior software engineer to join our team...',
                'match_score': 95,
                'reason': 'Excellent match based on your Python and React skills',
                'posted_date': '2024-01-15T10:00:00Z',
                'job_type': 'Full-time',
                'work_location': 'Hybrid'
            },
            {
                'id': 2,
                'title': 'Full Stack Developer',
                'company': 'Innovation Labs',
                'location': 'Remote',
                'salary': '$100,000 - $130,000',
                'description': 'Join our dynamic team as a full stack developer...',
                'match_score': 88,
                'reason': 'Strong match for your JavaScript and Django experience',
                'posted_date': '2024-01-14T14:30:00Z',
                'job_type': 'Full-time',
                'work_location': 'Remote'
            },
            {
                'id': 3,
                'title': 'Python Developer',
                'company': 'Data Solutions Inc',
                'location': 'Austin, TX',
                'salary': '$90,000 - $120,000',
                'description': 'We need a skilled Python developer for our data team...',
                'match_score': 82,
                'reason': 'Good match based on your Python and data science background',
                'posted_date': '2024-01-13T09:15:00Z',
                'job_type': 'Full-time',
                'work_location': 'On-site'
            }
        ]
        
        return Response({
            'success': True,
            'recommendations': recommendations,
            'total_recommendations': len(recommendations)
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
        # Get Firebase UID from request (optional for now)
        firebase_uid = _get_firebase_uid_from_request(request)
        # For now, we'll allow saving without authentication since we're using localStorage
        
        return Response({
            'success': True,
            'message': 'Job saved successfully',
            'saved_date': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error saving job: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_ai_jobs(request):
    """Get AI-scraped jobs with recommendations"""
    try:
        # Get parameters from request
        query = request.GET.get('query', 'software engineer')
        location = request.GET.get('location', 'Perth')
        limit = int(request.GET.get('limit', 20))
        skills = request.GET.get('skills', '')
        experience = request.GET.get('experience', '')
        resume_text = request.GET.get('resume_text', '')
        
        # Import AI modules
        import sys
        import os
        ai_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'AI')
        if ai_folder_path not in sys.path:
            sys.path.append(ai_folder_path)
        
        try:
            from job_scraper import load_job_data
            from recommender.job_recommender import JobRecommender
            import pandas as pd
            
            # Fetch job data from AI scraper
            job_df = load_job_data(query, location, results_per_page=limit)
            
            if job_df.empty:
                return Response({
                    'success': True,
                    'jobs': [],
                    'message': 'No jobs found for the given criteria'
                })
            
            # Prepare data for recommender - map the correct column names from job scraper
            df = pd.DataFrame({
                'title': job_df['Job Title'],
                'description': job_df['Description'],
                'skills': job_df.get('Skills', ''),
                'location': job_df['Location'],
                'salary': job_df.get('Salary', ''),
                'company': job_df['Company']
            })
            
            # Initialize and fit recommender
            rec = JobRecommender().fit(df)
            
            # Build user profile
            user_vec = rec.build_user_profile(
                target_title=query,
                skills=skills,
                resume_text=resume_text
            )
            
            # Get recommendations
            recommendations = rec.recommend(
                user_vector=user_vec,
                k=len(df),
                user_location=location
            )
            
            # Convert to API format
            jobs = []
            for _, job in recommendations.iterrows():
                jobs.append({
                    'id': str(job.get('id', '')),
                    'title': job.get('title', 'Unknown'),
                    'company': job.get('company', 'Unknown'),
                    'location': job.get('location', 'Unknown'),
                    'salary': job.get('salary', 'Not specified'),
                    'description': job.get('description', 'No description available'),
                    'skills': job.get('skills', 'Unknown'),
                    'source': 'AI_SCRAPER',
                    'match_score': round(job.get('score', 0) * 100, 1),
                    'posted_date': job.get('created', datetime.now().isoformat()),
                    'url': job.get('redirect_url', '#')
                })
            
        except Exception as e:
            logger.error(f"AI recommendation error: {e}")
            # Fallback to basic job data without recommendations
            jobs = []
            for _, job in job_df.iterrows():
                jobs.append({
                    'id': f"mock_{len(jobs)}",
                    'title': job.get('Job Title', 'Unknown'),
                    'company': job.get('Company', 'Unknown'),
                    'location': job.get('Location', 'Unknown'),
                    'salary': job.get('Salary', 'Not specified'),
                    'description': job.get('Description', 'No description available'),
                    'skills': job.get('Skills', 'Unknown'),
                    'source': 'AI_SCRAPER',
                    'match_score': 75.0,  # Fallback score
                    'posted_date': datetime.now().isoformat(),
                    'url': '#'
                })
        
        return Response({
            'success': True,
            'jobs': jobs,
            'total': len(jobs),
            'query': query,
            'location': location
        })
        
    except Exception as e:
        logger.error(f"Error fetching AI jobs: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def refresh_ai_jobs(request):
    """Refresh AI jobs (same as get_ai_jobs but POST method)"""
    return get_ai_jobs(request)

@api_view(['POST'])
def save_ai_job(request):
    """Save an AI job for later"""
    try:
        # Parse request data
        try:
            job_data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract job information
        job_id = job_data.get('id', '')
        job_title = job_data.get('title', 'Unknown')
        company = job_data.get('company', 'Unknown')
        location = job_data.get('location', 'Unknown')
        salary = job_data.get('salary', 'Not specified')
        description = job_data.get('description', 'No description available')
        skills = job_data.get('skills', 'Unknown')
        source = job_data.get('source', 'AI_SCRAPER')
        match_score = job_data.get('match_score', 0)
        
        # For Docker setup with PostgreSQL/MongoDB, we'll store in the database
        # For now, we'll use a simple approach and return success
        # In a full implementation, you'd save to your PostgreSQL database
        
        logger.info(f"Saving AI job: {job_title} at {company}")
        
        return Response({
            'success': True,
            'message': 'AI job saved successfully',
            'saved_date': datetime.now().isoformat(),
            'job_data': {
                'id': job_id,
                'title': job_title,
                'company': company,
                'location': location,
                'salary': salary,
                'description': description,
                'skills': skills,
                'source': source,
                'match_score': match_score
            }
        })
        
    except Exception as e:
        logger.error(f"Error saving AI job: {e}")
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
        from api.models import SavedJob, Job, Company
        
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        
        # For testing purposes, if no authentication, return sample data
        if not firebase_uid:
            # Return sample saved jobs for testing
            sample_saved_jobs = [
                {
                    'id': 1,
                    'job_title': 'Senior Software Engineer',
                    'company': 'TechCorp Solutions',
                    'saved_date': '2024-01-12',
                    'location': 'San Francisco, CA',
                    'salary': '$120,000 - $160,000',
                    'job_type': 'full-time',
                    'work_location': 'hybrid'
                },
                {
                    'id': 2,
                    'job_title': 'Data Scientist',
                    'company': 'DataFlow Inc',
                    'saved_date': '2024-01-10',
                    'location': 'New York, NY',
                    'salary': '$100,000 - $140,000',
                    'job_type': 'full-time',
                    'work_location': 'remote'
                }
            ]
            
            return Response({
                'success': True,
                'saved_jobs': sample_saved_jobs,
                'message': 'Sample data (authentication required for real user data)'
            })
        
        # Get or create user
        try:
            from api.models import FirebaseUser
            user = FirebaseUser.objects.get(uid=firebase_uid)
        except FirebaseUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get saved jobs from database
        saved_jobs_query = SavedJob.objects.filter(user=user).select_related('job', 'job__company')
        
        # Serialize saved jobs
        saved_jobs = []
        for saved_job in saved_jobs_query:
            job = saved_job.job
            saved_job_data = {
                'id': job.id,
                'job_title': job.title,
                'company': job.company.name,
                'saved_date': saved_job.saved_date.isoformat(),
                'location': job.location,
                'salary': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Salary not specified",
                'job_type': job.job_type,
                'work_location': job.work_location,
                'notes': saved_job.notes
            }
            saved_jobs.append(saved_job_data)
        
        return Response({
            'success': True,
            'saved_jobs': saved_jobs,
            'total_saved': len(saved_jobs)
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
        # Get Firebase UID from request (optional for now)
        firebase_uid = _get_firebase_uid_from_request(request)
        # For now, we'll allow access without authentication for testing
        # In a production environment, you'd want to require authentication
        
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

@api_view(['GET'])
def get_skills(request):
    """Get all available skills"""
    try:
        from api.models import JobSkill
        
        skills = JobSkill.objects.all().values_list('name', flat=True)
        
        return Response({
            'success': True,
            'skills': list(skills)
        })
        
    except Exception as e:
        logger.error(f"Error getting skills: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_categories(request):
    """Get all available job categories"""
    try:
        from api.models import JobCategory
        
        categories = JobCategory.objects.all().values_list('name', flat=True)
        
        return Response({
            'success': True,
            'categories': list(categories)
        })
        
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)