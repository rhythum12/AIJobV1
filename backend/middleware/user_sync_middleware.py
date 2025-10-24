"""
User Sync Middleware - Automatically syncs Firebase users with databases
"""

import logging
from typing import Optional
from django.http import HttpRequest, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from firebase_admin import auth as firebase_auth
from firebase_admin.exceptions import FirebaseError

# Import user_service lazily to avoid database connections at startup

logger = logging.getLogger(__name__)

class UserSyncMiddleware(MiddlewareMixin):
    """Middleware to automatically sync Firebase users with databases"""
    
    def process_request(self, request: HttpRequest):
        """Process request and sync user if authenticated"""
        try:
            # Skip middleware for certain paths
            if self._should_skip_middleware(request.path):
                return None
            
            # Get Firebase UID from request
            firebase_uid = self._get_firebase_uid_from_request(request)
            if not firebase_uid:
                return None
            
            # Check if user exists in database
            user_exists = self._check_user_exists(firebase_uid)
            if not user_exists:
                # Sync user from Firebase
                self._sync_user_from_firebase(firebase_uid)
            
            # Add user info to request for use in views
            request.firebase_uid = firebase_uid
            
        except Exception as e:
            logger.error(f"Error in UserSyncMiddleware: {e}")
            # Don't block the request if middleware fails
        
        return None
    
    def _should_skip_middleware(self, path: str) -> bool:
        """Check if middleware should be skipped for this path"""
        skip_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/api/auth/login',
            '/api/auth/register',
            '/health/',
            '/docs/',
        ]
        
        return any(path.startswith(skip_path) for skip_path in skip_paths)
    
    def _get_firebase_uid_from_request(self, request: HttpRequest) -> Optional[str]:
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
            logger.debug(f"Firebase authentication error: {e}")
            return None
        except Exception as e:
            logger.debug(f"Error extracting Firebase UID: {e}")
            return None
    
    def _check_user_exists(self, firebase_uid: str) -> bool:
        """Check if user exists in database"""
        try:
            # Lazy import to avoid database connections at startup
            from services.user_service import user_service
            # This is a synchronous check, so we'll use a simple approach
            # In production, you might want to cache this information
            return False  # Always sync for now, can be optimized later
        except Exception as e:
            logger.error(f"Error checking user existence: {e}")
            return False
    
    def _sync_user_from_firebase(self, firebase_uid: str):
        """Sync user from Firebase to databases"""
        try:
            # This would typically be async, but middleware is synchronous
            # In a real implementation, you might want to use a task queue
            logger.info(f"User {firebase_uid} needs to be synced")
            # The actual sync will happen when the user makes an API call
        except Exception as e:
            logger.error(f"Error syncing user from Firebase: {e}")

class FirebaseAuthMiddleware(MiddlewareMixin):
    """Middleware to handle Firebase authentication"""
    
    def process_request(self, request: HttpRequest):
        """Process request and add user info if authenticated"""
        try:
            # Get Firebase UID from request
            firebase_uid = self._get_firebase_uid_from_request(request)
            if firebase_uid:
                # Add user info to request
                request.firebase_uid = firebase_uid
                request.is_authenticated = True
            else:
                request.is_authenticated = False
            
        except Exception as e:
            logger.error(f"Error in FirebaseAuthMiddleware: {e}")
            request.is_authenticated = False
        
        return None
    
    def _get_firebase_uid_from_request(self, request: HttpRequest) -> Optional[str]:
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
            logger.debug(f"Firebase authentication error: {e}")
            return None
        except Exception as e:
            logger.debug(f"Error extracting Firebase UID: {e}")
            return None
