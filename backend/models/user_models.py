"""
User Models for both MongoDB and PostgreSQL
Handles user data synchronization between Firebase and databases
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

class ExperienceLevel(Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    EXECUTIVE = "executive"

@dataclass
class UserProfile:
    """User profile data structure"""
    firebase_uid: str
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    skills: List[str] = None
    experience_level: Optional[ExperienceLevel] = None
    preferred_job_types: List[str] = None
    salary_expectation: Optional[int] = None
    availability: Optional[str] = None
    status: UserStatus = UserStatus.ACTIVE
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    profile_completion: Optional[int] = None
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = []
        if self.preferred_job_types is None:
            self.preferred_job_types = []
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.profile_completion is None:
            self.profile_completion = self._calculate_completion()
    
    def _calculate_completion(self) -> int:
        """Calculate profile completion percentage"""
        fields = [
            self.name, self.phone, self.location, self.bio,
            self.skills, self.experience_level, self.preferred_job_types,
            self.salary_expectation, self.availability
        ]
        completed = sum(1 for field in fields if field is not None and field != [])
        return int((completed / len(fields)) * 100)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'firebase_uid': self.firebase_uid,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'location': self.location,
            'bio': self.bio,
            'skills': self.skills,
            'experience_level': self.experience_level.value if self.experience_level else None,
            'preferred_job_types': self.preferred_job_types,
            'salary_expectation': self.salary_expectation,
            'availability': self.availability,
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_login': self.last_login,
            'profile_completion': self.profile_completion
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create UserProfile from dictionary"""
        return cls(
            firebase_uid=data['firebase_uid'],
            email=data['email'],
            name=data.get('name'),
            phone=data.get('phone'),
            location=data.get('location'),
            bio=data.get('bio'),
            skills=data.get('skills', []),
            experience_level=ExperienceLevel(data['experience_level']) if data.get('experience_level') else None,
            preferred_job_types=data.get('preferred_job_types', []),
            salary_expectation=data.get('salary_expectation'),
            availability=data.get('availability'),
            status=UserStatus(data.get('status', 'active')),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            last_login=data.get('last_login'),
            profile_completion=data.get('profile_completion')
        )

@dataclass
class UserPreferences:
    """User job preferences and settings"""
    user_id: str
    job_types: List[str] = None
    locations: List[str] = None
    salary_range_min: Optional[int] = None
    salary_range_max: Optional[int] = None
    remote_work: Optional[bool] = None
    company_size: List[str] = None
    industries: List[str] = None
    experience_level: Optional[str] = None
    work_schedule: List[str] = None
    benefits: List[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.job_types is None:
            self.job_types = []
        if self.locations is None:
            self.locations = []
        if self.company_size is None:
            self.company_size = []
        if self.industries is None:
            self.industries = []
        if self.work_schedule is None:
            self.work_schedule = []
        if self.benefits is None:
            self.benefits = []
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'user_id': self.user_id,
            'job_types': self.job_types,
            'locations': self.locations,
            'salary_range_min': self.salary_range_min,
            'salary_range_max': self.salary_range_max,
            'remote_work': self.remote_work,
            'company_size': self.company_size,
            'industries': self.industries,
            'experience_level': self.experience_level,
            'work_schedule': self.work_schedule,
            'benefits': self.benefits,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

@dataclass
class UserActivity:
    """User activity tracking"""
    user_id: str
    activity_type: str  # login, logout, profile_update, job_apply, etc.
    description: str
    metadata: Dict[str, Any] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'metadata': self.metadata,
            'created_at': self.created_at
        }
