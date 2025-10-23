#!/usr/bin/env python3
"""
Script to create more users in MongoDB for Mongo Express visibility
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.working_settings')
django.setup()

def create_more_users():
    """Create more users in MongoDB"""
    try:
        from database.mongodb_connection import get_mongodb
        
        print("🔄 Creating More Users in MongoDB")
        print("=" * 50)
        
        # Connect to MongoDB
        mongodb = get_mongodb()
        if not mongodb.connect():
            print("❌ Failed to connect to MongoDB")
            return False
        
        users_collection = mongodb.get_collection('users')
        
        # Create additional users
        additional_users = [
            {
                'firebase_uid': 'mongo_express_user_1',
                'email': 'mongo_express_user_1@example.com',
                'display_name': 'Mongo Express User 1',
                'profile_complete': True,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'preferences': {
                    'job_categories': ['Software Engineering', 'DevOps'],
                    'locations': ['San Francisco', 'Remote'],
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
                'skills': ['Python', 'AWS', 'Docker', 'Kubernetes'],
                'experience_level': 'senior',
                'bio': 'Senior software engineer with DevOps expertise',
                'location': 'San Francisco, CA'
            },
            {
                'firebase_uid': 'mongo_express_user_2',
                'email': 'mongo_express_user_2@example.com',
                'display_name': 'Mongo Express User 2',
                'profile_complete': True,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'preferences': {
                    'job_categories': ['Data Science', 'Machine Learning'],
                    'locations': ['New York', 'Remote'],
                    'salary_range': {'min': 100000, 'max': 150000},
                    'work_type': ['Full-time', 'Contract']
                },
                'settings': {
                    'profile_visibility': 'public',
                    'email_notifications': True,
                    'push_notifications': False,
                    'job_alerts': True,
                    'newsletter': False,
                    'privacy_level': 'standard',
                    'data_sharing': False
                },
                'skills': ['Python', 'R', 'TensorFlow', 'Pandas'],
                'experience_level': 'mid',
                'bio': 'Data scientist specializing in machine learning',
                'location': 'New York, NY'
            },
            {
                'firebase_uid': 'mongo_express_user_3',
                'email': 'mongo_express_user_3@example.com',
                'display_name': 'Mongo Express User 3',
                'profile_complete': False,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'preferences': {
                    'job_categories': ['Frontend Development'],
                    'locations': ['Remote'],
                    'salary_range': {'min': 70000, 'max': 100000},
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
                'experience_level': 'entry',
                'bio': 'Frontend developer learning modern web technologies',
                'location': 'Remote'
            }
        ]
        
        # Insert users
        for user in additional_users:
            result = users_collection.insert_one(user)
            print(f"✅ Inserted user: {user['display_name']} (ID: {result.inserted_id})")
        
        # Count total users
        total_users = users_collection.count_documents({})
        print(f"\n📊 Total users in MongoDB: {total_users}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating more users: {e}")
        return False

def main():
    """Main function"""
    success = create_more_users()
    
    if success:
        print("\n🎉 More users created successfully!")
        print("\n🔗 Now check Mongo Express:")
        print("   URL: http://localhost:8081")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Database: job_recommender")
        print("   Collection: users")
        print("\n💡 You should now see multiple users in Mongo Express!")
    else:
        print("❌ Failed to create more users")

if __name__ == "__main__":
    main()
