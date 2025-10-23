#!/usr/bin/env python3
"""
Script to check users stored in MongoDB
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.working_settings')
django.setup()

def check_mongodb_users():
    """Check users in MongoDB"""
    try:
        from database.mongodb_connection import get_mongodb
        
        print("🔍 Checking MongoDB Users")
        print("=" * 50)
        
        # Connect to MongoDB
        mongodb = get_mongodb()
        if not mongodb.connect():
            print("❌ Failed to connect to MongoDB")
            return False
        
        # Get users collection
        users_collection = mongodb.get_collection('users')
        
        # Count total users
        total_users = users_collection.count_documents({})
        print(f"📊 Total Users in MongoDB: {total_users}")
        
        if total_users == 0:
            print("⚠️  No users found in MongoDB")
            print("💡 Try accessing the user API endpoints to create users:")
            print("   - http://localhost:8000/api/users/profile/")
            print("   - http://localhost:8000/api/users/sync/")
            return False
        
        # Get all users
        users = list(users_collection.find({}))
        
        print(f"\n👥 Users in MongoDB:")
        print("-" * 30)
        
        for i, user in enumerate(users, 1):
            print(f"{i}. User ID: {user.get('firebase_uid', 'N/A')}")
            print(f"   Email: {user.get('email', 'N/A')}")
            print(f"   Display Name: {user.get('display_name', 'N/A')}")
            print(f"   Profile Complete: {user.get('profile_complete', False)}")
            print(f"   Created: {user.get('created_at', 'N/A')}")
            print(f"   Last Login: {user.get('last_login', 'N/A')}")
            
            # Show preferences
            preferences = user.get('preferences', {})
            if preferences:
                print(f"   Job Categories: {preferences.get('job_categories', [])}")
                print(f"   Locations: {preferences.get('locations', [])}")
                salary_range = preferences.get('salary_range', {})
                if salary_range:
                    print(f"   Salary Range: ${salary_range.get('min', 0):,} - ${salary_range.get('max', 0):,}")
            
            # Show settings
            settings = user.get('settings', {})
            if settings:
                print(f"   Notifications: Email={settings.get('email_notifications', False)}, Push={settings.get('push_notifications', False)}")
                print(f"   Privacy: {settings.get('privacy_level', 'N/A')}")
            
            print()
        
        print("✅ MongoDB users check completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error checking MongoDB users: {e}")
        return False

def main():
    """Main function"""
    success = check_mongodb_users()
    
    if success:
        print("\n🎉 Users are now stored in MongoDB!")
        print("🔗 You can view them in Mongo Express: http://localhost:8081")
        print("📊 Database: job_recommender")
        print("📋 Collection: users")
    else:
        print("\n⚠️  No users found. Try accessing the API endpoints to create users.")

if __name__ == "__main__":
    main()
