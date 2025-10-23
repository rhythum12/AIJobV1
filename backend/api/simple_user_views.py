"""
Simple User API Views - REST endpoints for user management
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

# Import MongoDB connection
from database.mongodb_connection import get_mongodb

logger = logging.getLogger(__name__)

def _get_firebase_uid_from_request(request) -> Optional[str]:
    """Extract Firebase UID from request headers or token"""
    try:
        # Get Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        # Extract token from "Bearer <token>"
        token = auth_header.split(' ')[1]
        
        # For now, use the token as the UID (in production, verify Firebase token)
        # This allows different tokens to create different users
        return token
        
    except Exception as e:
        logger.error(f"Error extracting Firebase UID: {e}")
        return None

@api_view(['GET'])
def user_profile(request, user_id=None):
    """Get user profile"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            # Create a test user and store in MongoDB
            firebase_uid = 'test_user_123'
            
            # Connect to MongoDB
            mongodb = get_mongodb()
            if not mongodb.connect():
                return Response({'error': 'Database connection failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Get users collection
            users_collection = mongodb.get_collection('users')
            
            # Check if user exists, if not create one
            existing_user = users_collection.find_one({'firebase_uid': firebase_uid})
            if not existing_user:
                # Create new user
                user_data = {
                    'firebase_uid': firebase_uid,
                    'email': 'user@example.com',
                    'display_name': 'Test User',
                    'profile_complete': True,
                    'created_at': datetime.now().isoformat(),
                    'last_login': datetime.now().isoformat(),
                    'preferences': {
                        'job_categories': ['Software Engineering', 'Data Science'],
                        'locations': ['San Francisco', 'Remote'],
                        'salary_range': {'min': 80000, 'max': 150000},
                        'work_type': ['Full-time', 'Contract']
                    },
                    'settings': {
                        'profile_visibility': 'public',
                        'email_notifications': True,
                        'push_notifications': True,
                        'job_alerts': True,
                        'newsletter': False,
                        'privacy_level': 'standard',
                        'data_sharing': False
                    }
                }
                users_collection.insert_one(user_data)
                logger.info(f"Created new user in MongoDB: {firebase_uid}")
            else:
                # Update last login
                users_collection.update_one(
                    {'firebase_uid': firebase_uid},
                    {'$set': {'last_login': datetime.now().isoformat()}}
                )
                logger.info(f"Updated last login for user: {firebase_uid}")
            
            # Get user data
            user_data = users_collection.find_one({'firebase_uid': firebase_uid})
            if user_data:
                # Remove MongoDB _id field
                user_data.pop('_id', None)
                return Response({
                    'success': True,
                    'user': user_data,
                    'message': 'User data from MongoDB'
                })
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # For authenticated users, get real user data from MongoDB
        mongodb = get_mongodb()
        if not mongodb.connect():
            return Response({'error': 'Database connection failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        users_collection = mongodb.get_collection('users')
        user_data = users_collection.find_one({'firebase_uid': firebase_uid})
        
        if user_data:
            user_data.pop('_id', None)
            return Response({
                'success': True,
                'user': user_data
            })
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def sync_user(request):
    """Sync user from Firebase"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            # For testing, create a test user
            firebase_uid = 'test_user_sync_' + str(int(datetime.now().timestamp()))
        
        # Connect to MongoDB
        mongodb = get_mongodb()
        if not mongodb.connect():
            return Response({'error': 'Database connection failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        users_collection = mongodb.get_collection('users')
        
        # Check if user already exists
        existing_user = users_collection.find_one({'firebase_uid': firebase_uid})
        
        if existing_user:
            # Update existing user
            users_collection.update_one(
                {'firebase_uid': firebase_uid},
                {
                    '$set': {
                        'last_sync': datetime.now().isoformat(),
                        'last_login': datetime.now().isoformat()
                    }
                }
            )
            logger.info(f"Updated existing user in MongoDB: {firebase_uid}")
            user_data = users_collection.find_one({'firebase_uid': firebase_uid})
        else:
            # Create new user
            user_data = {
                'firebase_uid': firebase_uid,
                'email': f'user_{firebase_uid}@example.com',
                'display_name': f'User {firebase_uid}',
                'profile_complete': False,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'last_sync': datetime.now().isoformat(),
                'preferences': {
                    'job_categories': [],
                    'locations': [],
                    'salary_range': {'min': 0, 'max': 0},
                    'work_type': []
                },
                'settings': {
                    'profile_visibility': 'public',
                    'email_notifications': True,
                    'push_notifications': True,
                    'job_alerts': True,
                    'newsletter': False,
                    'privacy_level': 'standard',
                    'data_sharing': False
                }
            }
            users_collection.insert_one(user_data)
            logger.info(f"Created new user in MongoDB: {firebase_uid}")
        
        # Remove MongoDB _id field
        if user_data:
            user_data.pop('_id', None)
        
        return Response({
            'success': True,
            'message': 'User synced successfully with MongoDB',
            'user': user_data
        })
        
    except Exception as e:
        logger.error(f"Error syncing user: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def user_activities(request):
    """Get user activities"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            # Return sample activities for testing
            activities = [
                {
                    'id': 1,
                    'type': 'job_view',
                    'description': 'Viewed Senior Software Engineer at TechCorp',
                    'timestamp': '2024-01-15T10:30:00Z',
                    'job_id': 1
                },
                {
                    'id': 2,
                    'type': 'job_save',
                    'description': 'Saved Data Scientist position',
                    'timestamp': '2024-01-14T15:45:00Z',
                    'job_id': 2
                },
                {
                    'id': 3,
                    'type': 'application',
                    'description': 'Applied for DevOps Engineer role',
                    'timestamp': '2024-01-13T09:20:00Z',
                    'job_id': 3
                }
            ]
            
            return Response({
                'success': True,
                'activities': activities,
                'message': 'Sample activities (authentication required for real user data)'
            })
        
        # In production, get real user activities from database
        return Response({
            'success': True,
            'activities': []
        })
        
    except Exception as e:
        logger.error(f"Error getting user activities: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT'])
def user_preferences(request):
    """Get or update user preferences"""
    try:
        # Get Firebase UID from request
        firebase_uid = _get_firebase_uid_from_request(request)
        if not firebase_uid:
            # Return sample preferences for testing
            preferences = {
                'job_categories': ['Software Engineering', 'Data Science'],
                'locations': ['San Francisco', 'Remote'],
                'salary_range': {'min': 80000, 'max': 150000},
                'work_type': ['Full-time', 'Contract'],
                'experience_level': 'Senior',
                'skills': ['Python', 'React', 'Django'],
                'notifications': {
                    'email': True,
                    'push': True,
                    'job_alerts': True
                }
            }
            
            return Response({
                'success': True,
                'preferences': preferences,
                'message': 'Sample preferences (authentication required for real user data)'
            })
        
        if request.method == 'GET':
            # Get user preferences from database
            return Response({
                'success': True,
                'preferences': {}
            })
        
        elif request.method == 'PUT':
            # Update user preferences
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
            # Return sample settings for testing
            settings = {
                'profile_visibility': 'public',
                'email_notifications': True,
                'push_notifications': True,
                'job_alerts': True,
                'newsletter': False,
                'privacy_level': 'standard',
                'data_sharing': False
            }
            
            return Response({
                'success': True,
                'settings': settings,
                'message': 'Sample settings (authentication required for real user data)'
            })
        
        if request.method == 'GET':
            # Get user settings from database
            return Response({
                'success': True,
                'settings': {}
            })
        
        elif request.method == 'PUT':
            # Update user settings
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

@api_view(['GET'])
def list_all_users(request):
    """List all users in the system"""
    try:
        mongodb = get_mongodb()
        if not mongodb.connect():
            return Response({'error': 'Database connection failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        users_collection = mongodb.get_collection('users')
        users = list(users_collection.find().sort('created_at', -1))
        
        # Remove _id field from each user
        for user in users:
            user.pop('_id', None)
        
        return Response({
            'success': True,
            'users': users,
            'total': len(users),
            'message': f'Found {len(users)} users in the system'
        })
        
    except Exception as e:
        logger.error(f"Error listing all users: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
