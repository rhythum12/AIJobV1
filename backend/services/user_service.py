"""
User Service - Handles user synchronization between Firebase and databases
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from firebase_admin import auth as firebase_auth
from firebase_admin.exceptions import FirebaseError

from models.user_models import UserProfile, UserPreferences, UserActivity, UserStatus
from database.mongodb_connection import get_mongodb_collection
from database.postgresql_connection import get_postgresql

logger = logging.getLogger(__name__)

class UserService:
    """Service for managing user data across Firebase, MongoDB, and PostgreSQL"""
    
    def __init__(self):
        # Lazy initialization - don't connect to databases until needed
        self._mongodb_users = None
        self._mongodb_activities = None
        self._postgresql = None
    
    @property
    def mongodb_users(self):
        """Lazy load MongoDB users collection"""
        if self._mongodb_users is None:
            self._mongodb_users = get_mongodb_collection('users')
        return self._mongodb_users
    
    @property
    def mongodb_activities(self):
        """Lazy load MongoDB activities collection"""
        if self._mongodb_activities is None:
            self._mongodb_activities = get_mongodb_collection('user_activities')
        return self._mongodb_activities
    
    @property
    def postgresql(self):
        """Lazy load PostgreSQL connection"""
        if self._postgresql is None:
            self._postgresql = get_postgresql()
        return self._postgresql
    
    async def create_or_update_user(self, firebase_uid: str, firebase_user_data: Dict[str, Any]) -> UserProfile:
        """Create or update user in both databases from Firebase data"""
        try:
            # Create user profile from Firebase data
            user_profile = UserProfile(
                firebase_uid=firebase_uid,
                email=firebase_user_data.get('email', ''),
                name=firebase_user_data.get('display_name'),
                phone=firebase_user_data.get('phone_number'),
                last_login=datetime.utcnow()
            )
            
            # Check if user exists in MongoDB
            existing_user = self.mongodb_users.find_one({'firebase_uid': firebase_uid})
            
            if existing_user:
                # Update existing user
                user_profile.created_at = existing_user.get('created_at')
                user_profile.updated_at = datetime.utcnow()
                
                # Update MongoDB
                self.mongodb_users.update_one(
                    {'firebase_uid': firebase_uid},
                    {'$set': user_profile.to_dict()}
                )
                
                # Update PostgreSQL
                self._update_postgresql_user(user_profile)
                
                logger.info(f"Updated user {firebase_uid} in both databases")
            else:
                # Create new user
                # Insert into MongoDB
                self.mongodb_users.insert_one(user_profile.to_dict())
                
                # Insert into PostgreSQL
                self._create_postgresql_user(user_profile)
                
                # Log user creation activity
                await self._log_user_activity(
                    firebase_uid, 
                    'user_created', 
                    'User account created from Firebase authentication'
                )
                
                logger.info(f"Created new user {firebase_uid} in both databases")
            
            return user_profile
            
        except Exception as e:
            logger.error(f"Error creating/updating user {firebase_uid}: {e}")
            raise
    
    def _create_postgresql_user(self, user_profile: UserProfile):
        """Create user in PostgreSQL"""
        try:
            query = """
                INSERT INTO users (firebase_uid, email, name, phone, location, bio, skills, 
                                 experience_level, preferred_job_types, salary_expectation, 
                                 availability, status, created_at, updated_at, last_login, profile_completion)
                VALUES (%(firebase_uid)s, %(email)s, %(name)s, %(phone)s, %(location)s, %(bio)s, 
                        %(skills)s, %(experience_level)s, %(preferred_job_types)s, %(salary_expectation)s, 
                        %(availability)s, %(status)s, %(created_at)s, %(updated_at)s, %(last_login)s, %(profile_completion)s)
                ON CONFLICT (firebase_uid) DO UPDATE SET
                    email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    phone = EXCLUDED.phone,
                    last_login = EXCLUDED.last_login,
                    updated_at = EXCLUDED.updated_at
            """
            
            self.postgresql.execute_insert(query, user_profile.to_dict())
            
        except Exception as e:
            logger.error(f"Error creating PostgreSQL user: {e}")
            raise
    
    def _update_postgresql_user(self, user_profile: UserProfile):
        """Update user in PostgreSQL"""
        try:
            query = """
                UPDATE users SET 
                    email = %(email)s,
                    name = %(name)s,
                    phone = %(phone)s,
                    location = %(location)s,
                    bio = %(bio)s,
                    skills = %(skills)s,
                    experience_level = %(experience_level)s,
                    preferred_job_types = %(preferred_job_types)s,
                    salary_expectation = %(salary_expectation)s,
                    availability = %(availability)s,
                    status = %(status)s,
                    last_login = %(last_login)s,
                    profile_completion = %(profile_completion)s,
                    updated_at = %(updated_at)s
                WHERE firebase_uid = %(firebase_uid)s
            """
            
            self.postgresql.execute_update(query, user_profile.to_dict())
            
        except Exception as e:
            logger.error(f"Error updating PostgreSQL user: {e}")
            raise
    
    async def get_user_by_firebase_uid(self, firebase_uid: str) -> Optional[UserProfile]:
        """Get user by Firebase UID from MongoDB"""
        try:
            user_data = self.mongodb_users.find_one({'firebase_uid': firebase_uid})
            if user_data:
                return UserProfile.from_dict(user_data)
            return None
        except Exception as e:
            logger.error(f"Error getting user {firebase_uid}: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserProfile]:
        """Get user by email from MongoDB"""
        try:
            user_data = self.mongodb_users.find_one({'email': email})
            if user_data:
                return UserProfile.from_dict(user_data)
            return None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    async def update_user_profile(self, firebase_uid: str, profile_data: Dict[str, Any]) -> bool:
        """Update user profile in both databases"""
        try:
            # Get existing user
            existing_user = await self.get_user_by_firebase_uid(firebase_uid)
            if not existing_user:
                return False
            
            # Update profile data
            for key, value in profile_data.items():
                if hasattr(existing_user, key):
                    setattr(existing_user, key, value)
            
            existing_user.updated_at = datetime.utcnow()
            existing_user.profile_completion = existing_user._calculate_completion()
            
            # Update MongoDB
            self.mongodb_users.update_one(
                {'firebase_uid': firebase_uid},
                {'$set': existing_user.to_dict()}
            )
            
            # Update PostgreSQL
            self._update_postgresql_user(existing_user)
            
            # Log profile update activity
            await self._log_user_activity(
                firebase_uid,
                'profile_updated',
                'User profile updated',
                {'updated_fields': list(profile_data.keys())}
            )
            
            logger.info(f"Updated profile for user {firebase_uid}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating user profile {firebase_uid}: {e}")
            return False
    
    async def _log_user_activity(self, user_id: str, activity_type: str, description: str, metadata: Dict[str, Any] = None):
        """Log user activity to MongoDB"""
        try:
            activity = UserActivity(
                user_id=user_id,
                activity_type=activity_type,
                description=description,
                metadata=metadata or {}
            )
            
            self.mongodb_activities.insert_one(activity.to_dict())
            
        except Exception as e:
            logger.error(f"Error logging user activity: {e}")
    
    async def get_user_activities(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user activities from MongoDB"""
        try:
            activities = list(self.mongodb_activities.find(
                {'user_id': user_id}
            ).sort('created_at', -1).limit(limit))
            
            return activities
            
        except Exception as e:
            logger.error(f"Error getting user activities: {e}")
            return []
    
    async def delete_user(self, firebase_uid: str) -> bool:
        """Delete user from both databases"""
        try:
            # Delete from MongoDB
            self.mongodb_users.delete_one({'firebase_uid': firebase_uid})
            self.mongodb_activities.delete_many({'user_id': firebase_uid})
            
            # Delete from PostgreSQL
            self.postgresql.execute_delete(
                "DELETE FROM users WHERE firebase_uid = %s",
                (firebase_uid,)
            )
            
            logger.info(f"Deleted user {firebase_uid} from both databases")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting user {firebase_uid}: {e}")
            return False
    
    async def sync_firebase_user(self, firebase_uid: str) -> Optional[UserProfile]:
        """Sync user data from Firebase to databases"""
        try:
            # Get user data from Firebase
            firebase_user = firebase_auth.get_user(firebase_uid)
            
            firebase_data = {
                'email': firebase_user.email,
                'display_name': firebase_user.display_name,
                'phone_number': firebase_user.phone_number,
                'email_verified': firebase_user.email_verified,
                'disabled': firebase_user.disabled
            }
            
            # Create or update user in databases
            user_profile = await self.create_or_update_user(firebase_uid, firebase_data)
            
            return user_profile
            
        except FirebaseError as e:
            logger.error(f"Firebase error syncing user {firebase_uid}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error syncing user {firebase_uid}: {e}")
            return None

# Global user service instance
user_service = UserService()
