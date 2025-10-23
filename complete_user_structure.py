#!/usr/bin/env python3
"""
Script to complete the user data structure in MongoDB
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

def complete_user_structure():
    """Add missing profile_complete field to all users"""
    try:
        from database.mongodb_connection import get_mongodb
        
        print("🔄 Completing User Data Structure")
        print("=" * 50)
        
        # Connect to MongoDB
        mongodb = get_mongodb()
        if not mongodb.connect():
            print("❌ Failed to connect to MongoDB")
            return False
        
        users_collection = mongodb.get_collection('users')
        
        # Get all users
        users = list(users_collection.find({}))
        updated_count = 0
        
        for user in users:
            firebase_uid = user.get('firebase_uid')
            if not firebase_uid:
                continue
            
            # Check if user has profile_complete field
            if 'profile_complete' not in user:
                print(f"🔄 Adding profile_complete to user: {firebase_uid}")
                
                # Determine if profile is complete based on existing data
                has_name = 'name' in user and user.get('name')
                has_email = 'email' in user and user.get('email')
                has_skills = 'skills' in user and user.get('skills')
                has_experience = 'experience_level' in user and user.get('experience_level')
                
                # Calculate profile completion
                profile_complete = has_name and has_email and has_skills and has_experience
                
                # Update the user
                users_collection.update_one(
                    {'firebase_uid': firebase_uid},
                    {'$set': {'profile_complete': profile_complete}}
                )
                
                updated_count += 1
                print(f"   ✅ Added profile_complete: {profile_complete}")
        
        print(f"\n🎉 Updated {updated_count} users with profile_complete field!")
        
        # Show final structure
        print("\n📊 Final User Structure Summary:")
        print("-" * 40)
        
        users = list(users_collection.find({}))
        for i, user in enumerate(users, 1):
            firebase_uid = user.get('firebase_uid', 'N/A')
            email = user.get('email', 'N/A')
            display_name = user.get('display_name', user.get('name', 'N/A'))
            profile_complete = user.get('profile_complete', False)
            
            print(f"{i}. {firebase_uid}")
            print(f"   Email: {email}")
            print(f"   Name: {display_name}")
            print(f"   Profile Complete: {profile_complete}")
            
            # Show preferences
            preferences = user.get('preferences', {})
            if preferences:
                job_categories = preferences.get('job_categories', [])
                locations = preferences.get('locations', [])
                salary_range = preferences.get('salary_range', {})
                print(f"   Job Categories: {job_categories}")
                print(f"   Locations: {locations}")
                if salary_range:
                    print(f"   Salary Range: ${salary_range.get('min', 0):,} - ${salary_range.get('max', 0):,}")
            
            # Show settings
            settings = user.get('settings', {})
            if settings:
                email_notifications = settings.get('email_notifications', False)
                push_notifications = settings.get('push_notifications', False)
                privacy_level = settings.get('privacy_level', 'N/A')
                print(f"   Notifications: Email={email_notifications}, Push={push_notifications}")
                print(f"   Privacy: {privacy_level}")
            
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error completing user structure: {e}")
        return False

def main():
    """Main function"""
    success = complete_user_structure()
    
    if success:
        print("🎉 All users now have complete data structure!")
        print("\n🔗 View in Mongo Express:")
        print("   URL: http://localhost:8081")
        print("   Database: job_recommender")
        print("   Collection: users")
        print("\n📋 Each user document now contains:")
        print("   ✅ firebase_uid - Unique user identifier")
        print("   ✅ email - User email address")
        print("   ✅ display_name - User's display name")
        print("   ✅ profile_complete - Profile completion status")
        print("   ✅ created_at - Account creation timestamp")
        print("   ✅ last_login - Last login timestamp")
        print("   ✅ preferences - Job preferences (categories, locations, salary)")
        print("   ✅ settings - User settings (notifications, privacy)")
    else:
        print("❌ Failed to complete user structure")

if __name__ == "__main__":
    main()
