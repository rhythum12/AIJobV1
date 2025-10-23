#!/usr/bin/env python3
"""
Script to insert a test user directly into MongoDB
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

def insert_test_user():
    """Insert a test user directly into MongoDB"""
    try:
        from database.mongodb_connection import get_mongodb
        
        print("🔄 Inserting Test User into MongoDB")
        print("=" * 50)
        
        # Connect to MongoDB
        mongodb = get_mongodb()
        if not mongodb.connect():
            print("❌ Failed to connect to MongoDB")
            return False
        
        # Get users collection
        users_collection = mongodb.get_collection('users')
        
        # Create a simple test user
        test_user = {
            'firebase_uid': 'mongo_express_test_user',
            'email': 'mongo_express_test@example.com',
            'display_name': 'Mongo Express Test User',
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
            'bio': 'This is a test user created specifically for Mongo Express visibility',
            'location': 'San Francisco, CA'
        }
        
        # Insert the user
        result = users_collection.insert_one(test_user)
        print(f"✅ Inserted test user with ID: {result.inserted_id}")
        
        # Verify the user was inserted
        inserted_user = users_collection.find_one({'firebase_uid': 'mongo_express_test_user'})
        if inserted_user:
            print("✅ Test user successfully inserted and verified!")
            print(f"   Firebase UID: {inserted_user['firebase_uid']}")
            print(f"   Email: {inserted_user['email']}")
            print(f"   Display Name: {inserted_user['display_name']}")
            print(f"   Profile Complete: {inserted_user['profile_complete']}")
        else:
            print("❌ Failed to verify user insertion")
            return False
        
        # Count total users
        total_users = users_collection.count_documents({})
        print(f"\n📊 Total users in MongoDB: {total_users}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inserting test user: {e}")
        return False

def main():
    """Main function"""
    success = insert_test_user()
    
    if success:
        print("\n🎉 Test user inserted successfully!")
        print("\n🔗 Now check Mongo Express:")
        print("   URL: http://localhost:8081")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Database: job_recommender")
        print("   Collection: users")
        print("\n💡 Look for user: 'mongo_express_test_user'")
    else:
        print("❌ Failed to insert test user")

if __name__ == "__main__":
    main()
