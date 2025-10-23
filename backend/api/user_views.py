"""
User API Views - REST endpoints for user management
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json

from firebase_admin import auth as firebase_auth
from firebase_admin.exceptions import FirebaseError

from services.user_service import user_service
from models.user_models import UserProfile, UserPreferences

logger = logging.getLogger(__name__)

class UserView(View):
    """User management API endpoints"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    async def get(self, request, user_id=None):
        """Get user profile"""
        try:
            # Get Firebase UID from request headers or token
            firebase_uid = await self._get_firebase_uid_from_request(request)
            if not firebase_uid:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            # Get user profile
            user_profile = await user_service.get_user_by_firebase_uid(firebase_uid)
            if not user_profile:
                return JsonResponse({'error': 'User not found'}, status=404)
            
            return JsonResponse({
                'success': True,
                'user': user_profile.to_dict()
            })
            
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    async def post(self, request):
        """Create or sync user from Firebase"""
        try:
            # Get Firebase UID from request
            firebase_uid = await self._get_firebase_uid_from_request(request)
            if not firebase_uid:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            # Sync user from Firebase
            user_profile = await user_service.sync_firebase_user(firebase_uid)
            if not user_profile:
                return JsonResponse({'error': 'Failed to sync user'}, status=400)
            
            return JsonResponse({
                'success': True,
                'message': 'User synced successfully',
                'user': user_profile.to_dict()
            })
            
        except Exception as e:
            logger.error(f"Error syncing user: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    async def put(self, request, user_id=None):
        """Update user profile"""
        try:
            # Get Firebase UID from request
            firebase_uid = await self._get_firebase_uid_from_request(request)
            if not firebase_uid:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            # Parse request data
            try:
                profile_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
            # Update user profile
            success = await user_service.update_user_profile(firebase_uid, profile_data)
            if not success:
                return JsonResponse({'error': 'Failed to update profile'}, status=400)
            
            # Get updated user profile
            updated_user = await user_service.get_user_by_firebase_uid(firebase_uid)
            
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully',
                'user': updated_user.to_dict()
            })
            
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    async def delete(self, request, user_id=None):
        """Delete user account"""
        try:
            # Get Firebase UID from request
            firebase_uid = await self._get_firebase_uid_from_request(request)
            if not firebase_uid:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            # Delete user from databases
            success = await user_service.delete_user(firebase_uid)
            if not success:
                return JsonResponse({'error': 'Failed to delete user'}, status=400)
            
            return JsonResponse({
                'success': True,
                'message': 'User deleted successfully'
            })
            
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    async def _get_firebase_uid_from_request(self, request) -> Optional[str]:
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

class UserActivityView(View):
    """User activity API endpoints"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    async def get(self, request):
        """Get user activities"""
        try:
            # Get Firebase UID from request
            firebase_uid = await self._get_firebase_uid_from_request(request)
            if not firebase_uid:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            # Get limit from query parameters
            limit = int(request.GET.get('limit', 50))
            
            # Get user activities
            activities = await user_service.get_user_activities(firebase_uid, limit)
            
            return JsonResponse({
                'success': True,
                'activities': activities
            })
            
        except Exception as e:
            logger.error(f"Error getting user activities: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    async def _get_firebase_uid_from_request(self, request) -> Optional[str]:
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

# API endpoint functions for Django URL routing
async def user_profile(request, user_id=None):
    """User profile endpoint"""
    view = UserView()
    return await view.dispatch(request, user_id=user_id)

async def user_activities(request):
    """User activities endpoint"""
    view = UserActivityView()
    return await view.dispatch(request)

async def sync_user(request):
    """Sync user from Firebase endpoint"""
    view = UserView()
    return await view.post(request)
