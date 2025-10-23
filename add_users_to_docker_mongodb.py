#!/usr/bin/env python3
"""
Add users directly to Docker MongoDB using Docker exec
"""

import subprocess
import json
from datetime import datetime

def add_users_to_docker_mongodb():
    """Add users directly to Docker MongoDB"""
    try:
        print("🔄 Adding Users to Docker MongoDB")
        print("=" * 50)
        
        # Sample users data
        users_data = [
            {
                "firebase_uid": "user_001",
                "email": "john.doe@example.com",
                "display_name": "John Doe",
                "profile_complete": True,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "preferences": {
                    "job_categories": ["Software Engineering", "Data Science"],
                    "locations": ["San Francisco", "Remote"],
                    "salary_range": {"min": 80000, "max": 150000},
                    "work_type": ["Full-time"]
                },
                "settings": {
                    "profile_visibility": "public",
                    "email_notifications": True,
                    "push_notifications": True,
                    "job_alerts": True,
                    "newsletter": False,
                    "privacy_level": "standard",
                    "data_sharing": False
                }
            },
            {
                "firebase_uid": "user_002",
                "email": "jane.smith@example.com",
                "display_name": "Jane Smith",
                "profile_complete": True,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "preferences": {
                    "job_categories": ["Product Management", "Design"],
                    "locations": ["New York", "Remote"],
                    "salary_range": {"min": 90000, "max": 140000},
                    "work_type": ["Full-time", "Contract"]
                },
                "settings": {
                    "profile_visibility": "public",
                    "email_notifications": True,
                    "push_notifications": False,
                    "job_alerts": True,
                    "newsletter": True,
                    "privacy_level": "standard",
                    "data_sharing": True
                }
            },
            {
                "firebase_uid": "user_003",
                "email": "mike.johnson@example.com",
                "display_name": "Mike Johnson",
                "profile_complete": False,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "preferences": {
                    "job_categories": ["DevOps", "Cloud Computing"],
                    "locations": ["Austin", "Remote"],
                    "salary_range": {"min": 100000, "max": 160000},
                    "work_type": ["Full-time"]
                },
                "settings": {
                    "profile_visibility": "private",
                    "email_notifications": False,
                    "push_notifications": True,
                    "job_alerts": False,
                    "newsletter": False,
                    "privacy_level": "high",
                    "data_sharing": False
                }
            },
            {
                "firebase_uid": "user_004",
                "email": "sarah.wilson@example.com",
                "display_name": "Sarah Wilson",
                "profile_complete": True,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "preferences": {
                    "job_categories": ["Data Science", "Machine Learning"],
                    "locations": ["Seattle", "Remote"],
                    "salary_range": {"min": 110000, "max": 170000},
                    "work_type": ["Full-time"]
                },
                "settings": {
                    "profile_visibility": "public",
                    "email_notifications": True,
                    "push_notifications": True,
                    "job_alerts": True,
                    "newsletter": True,
                    "privacy_level": "standard",
                    "data_sharing": True
                }
            },
            {
                "firebase_uid": "user_005",
                "email": "alex.brown@example.com",
                "display_name": "Alex Brown",
                "profile_complete": True,
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "preferences": {
                    "job_categories": ["Frontend Development", "UI/UX Design"],
                    "locations": ["Los Angeles", "Remote"],
                    "salary_range": {"min": 70000, "max": 120000},
                    "work_type": ["Full-time", "Part-time"]
                },
                "settings": {
                    "profile_visibility": "public",
                    "email_notifications": True,
                    "push_notifications": True,
                    "job_alerts": True,
                    "newsletter": False,
                    "privacy_level": "standard",
                    "data_sharing": False
                }
            }
        ]
        
        # Add each user to MongoDB
        for user in users_data:
            # Check if user already exists
            check_cmd = [
                'docker', 'exec', 'job_recommender_mongodb',
                'mongosh', 'job_recommender', '--eval', 
                f'db.users.countDocuments({{"firebase_uid": "{user["firebase_uid"]}"}})'
            ]
            
            result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip() == "0":
                # User doesn't exist, add them
                user_json = json.dumps(user)
                insert_cmd = [
                    'docker', 'exec', 'job_recommender_mongodb',
                    'mongosh', 'job_recommender', '--eval',
                    f'db.users.insertOne({user_json})'
                ]
                
                insert_result = subprocess.run(insert_cmd, capture_output=True, text=True, timeout=10)
                
                if insert_result.returncode == 0:
                    print(f"✅ Added user: {user['display_name']} ({user['email']})")
                else:
                    print(f"❌ Failed to add user {user['display_name']}: {insert_result.stderr}")
            else:
                print(f"ℹ️  User already exists: {user['display_name']}")
        
        # Count total users
        count_cmd = [
            'docker', 'exec', 'job_recommender_mongodb',
            'mongosh', 'job_recommender', '--eval', 'db.users.countDocuments({})'
        ]
        
        count_result = subprocess.run(count_cmd, capture_output=True, text=True, timeout=10)
        
        if count_result.returncode == 0:
            total_users = count_result.stdout.strip()
            print(f"\n📊 Total users in MongoDB: {total_users}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding users: {e}")
        return False

def show_mongo_express_instructions():
    """Show instructions for viewing users in Mongo Express"""
    print("\n🌐 How to View All Users in Mongo Express")
    print("=" * 50)
    print("1. Go to: http://localhost:8081")
    print("2. Login with: admin / admin123")
    print("3. Click on 'job_recommender' database")
    print("4. Click on 'users' collection")
    print("5. You should now see multiple users!")
    print("")
    print("💡 If you still see only 1 user:")
    print("   - Clear any search filters")
    print("   - Click 'Find' button to refresh")
    print("   - Make sure you're in the 'users' collection")

def main():
    """Main function"""
    print("🔄 Adding Users to Docker MongoDB")
    print("=" * 60)
    print("Adding sample users directly to Docker MongoDB...")
    print("=" * 60)
    
    # Add users
    success = add_users_to_docker_mongodb()
    
    # Show instructions
    show_mongo_express_instructions()
    
    print("\n" + "=" * 60)
    print("📊 Results:")
    print(f"   Users added: {'✅ Success' if success else '❌ Failed'}")
    
    if success:
        print("\n🎉 Users are now in Docker MongoDB!")
        print("💡 Refresh Mongo Express to see all users")
    else:
        print("\n⚠️  There was an issue adding users")

if __name__ == "__main__":
    main()
