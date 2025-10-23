#!/usr/bin/env python3
"""
Script to create users in the authenticated MongoDB database
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime
from pymongo import MongoClient

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.working_settings')
django.setup()

def create_authenticated_users():
    """Create users in the authenticated MongoDB database"""
    try:
        print("🔄 Creating Users in Authenticated MongoDB")
        print("=" * 50)
        
        # Connect to MongoDB with authentication
        client = MongoClient('mongodb://admin:password123@localhost:27017/')
        db = client['job_recommender']
        users_collection = db['users']
        
        # Clear existing users
        users_collection.drop()
        print("✅ Cleared existing users")
        
        # Create test users
        test_users = [
            {
                'firebase_uid': 'auth_user_1',
                'email': 'auth_user_1@example.com',
                'display_name': 'Authenticated User 1',
                'profile_complete': True,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'preferences': {
                    'job_categories': ['Software Engineering', 'Data Science'],
                    'locations': ['San Francisco', 'Remote'],
                    'salary_range': {'min': 100000, 'max': 200000},
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
                },
                'skills': ['Python', 'JavaScript', 'React', 'MongoDB'],
                'experience_level': 'senior',
                'bio': 'This is an authenticated user for Mongo Express visibility',
                'location': 'San Francisco, CA'
            },
            {
                'firebase_uid': 'auth_user_2',
                'email': 'auth_user_2@example.com',
                'display_name': 'Authenticated User 2',
                'profile_complete': True,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'preferences': {
                    'job_categories': ['DevOps', 'Cloud Computing'],
                    'locations': ['New York', 'Remote'],
                    'salary_range': {'min': 120000, 'max': 180000},
                    'work_type': ['Full-time']
                },
                'settings': {
                    'profile_visibility': 'public',
                    'email_notifications': True,
                    'push_notifications': True,
                    'job_alerts': True,
                    'newsletter': True,
                    'privacy_level': 'standard',
                    'data_sharing': True
                },
                'skills': ['AWS', 'Docker', 'Kubernetes', 'Terraform'],
                'experience_level': 'senior',
                'bio': 'DevOps engineer with cloud expertise',
                'location': 'New York, NY'
            },
            {
                'firebase_uid': 'auth_user_3',
                'email': 'auth_user_3@example.com',
                'display_name': 'Authenticated User 3',
                'profile_complete': False,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'preferences': {
                    'job_categories': ['Frontend Development'],
                    'locations': ['Remote'],
                    'salary_range': {'min': 80000, 'max': 120000},
                    'work_type': ['Full-time', 'Part-time']
                },
                'settings': {
                    'profile_visibility': 'private',
                    'email_notifications': False,
                    'push_notifications': True,
                    'job_alerts': False,
                    'newsletter': False,
                    'privacy_level': 'high',
                    'data_sharing': False
                },
                'skills': ['React', 'Vue.js', 'TypeScript', 'CSS'],
                'experience_level': 'mid',
                'bio': 'Frontend developer specializing in modern web technologies',
                'location': 'Remote'
            }
        ]
        
        # Insert users
        result = users_collection.insert_many(test_users)
        print(f"✅ Inserted {len(result.inserted_ids)} users")
        
        # Verify users were inserted
        count = users_collection.count_documents({})
        print(f"📊 Total users in authenticated database: {count}")
        
        # Show inserted users
        users = list(users_collection.find({}))
        for i, user in enumerate(users, 1):
            print(f"\n👤 User {i}:")
            print(f"   Firebase UID: {user['firebase_uid']}")
            print(f"   Email: {user['email']}")
            print(f"   Display Name: {user['display_name']}")
            print(f"   Profile Complete: {user['profile_complete']}")
            print(f"   Skills: {user['skills']}")
            print(f"   Experience: {user['experience_level']}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating authenticated users: {e}")
        return False

def main():
    """Main function"""
    success = create_authenticated_users()
    
    if success:
        print("\n🎉 Users created in authenticated MongoDB!")
        print("\n🔗 Now check Mongo Express:")
        print("   URL: http://localhost:8081")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Database: job_recommender")
        print("   Collection: users")
        print("\n💡 You should now see 3 authenticated users!")
    else:
        print("❌ Failed to create authenticated users")

if __name__ == "__main__":
    main()
