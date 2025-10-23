#!/usr/bin/env python3
"""
Debug script to help identify why frontend registration isn't syncing to MongoDB
"""

import requests
import json
from datetime import datetime

def check_current_users():
    """Check current users in MongoDB"""
    try:
        print("🔍 Checking Current Users in MongoDB")
        print("=" * 50)
        
        import os
        import sys
        from pathlib import Path
        
        # Add the backend directory to Python path
        backend_dir = Path(__file__).parent / 'backend'
        sys.path.insert(0, str(backend_dir))
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.working_settings')
        import django
        django.setup()
        
        from database.mongodb_connection import get_mongodb
        
        mongodb = get_mongodb()
        if mongodb.connect():
            users_collection = mongodb.get_collection('users')
            
            # Count total users
            total_users = users_collection.count_documents({})
            print(f"📊 Total users in MongoDB: {total_users}")
            
            # Get recent users (last 5)
            recent_users = list(users_collection.find().sort('created_at', -1).limit(5))
            
            print("\n🕒 Recent Users (Last 5):")
            for i, user in enumerate(recent_users, 1):
                print(f"   {i}. {user.get('display_name', 'N/A')} ({user.get('email', 'N/A')})")
                print(f"      🆔 UID: {user.get('firebase_uid', 'N/A')}")
                print(f"      📅 Created: {user.get('created_at', 'N/A')}")
                print(f"      🔄 Last Sync: {user.get('last_sync', 'N/A')}")
                print()
            
            return True
        else:
            print("❌ Failed to connect to MongoDB")
            return False
            
    except Exception as e:
        print(f"❌ Error checking users: {e}")
        return False

def test_user_sync_with_different_tokens():
    """Test user sync with different token patterns"""
    try:
        print("\n🔄 Testing User Sync with Different Tokens")
        print("=" * 50)
        
        # Test with different token patterns that might be used by frontend
        test_tokens = [
            "Bearer mock_firebase_token_123",
            "mock_firebase_token_123",
            "Bearer test_token_456",
            "test_token_456"
        ]
        
        for i, token in enumerate(test_tokens, 1):
            print(f"\n{i}. Testing token: {token}")
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': token
            }
            
            response = requests.post("http://localhost:8000/api/users/sync/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data.get('success', False)}")
                print(f"   📧 Email: {data.get('user', {}).get('email', 'N/A')}")
                print(f"   🆔 UID: {data.get('user', {}).get('firebase_uid', 'N/A')}")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing tokens: {e}")
        return False

def create_test_user_for_frontend():
    """Create a test user that simulates frontend registration"""
    try:
        print("\n🔄 Creating Test User (Frontend Simulation)")
        print("=" * 50)
        
        # Generate a unique user ID
        timestamp = int(datetime.now().timestamp())
        test_uid = f"frontend_test_user_{timestamp}"
        
        print(f"📝 Creating user: {test_uid}")
        
        # Test user sync
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {test_uid}'
        }
        
        response = requests.post("http://localhost:8000/api/users/sync/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User created successfully!")
            print(f"   📧 Email: {data.get('user', {}).get('email', 'N/A')}")
            print(f"   🆔 UID: {data.get('user', {}).get('firebase_uid', 'N/A')}")
            print(f"   👤 Display Name: {data.get('user', {}).get('display_name', 'N/A')}")
            
            # Verify user was stored in MongoDB
            print("\n🔍 Verifying user in MongoDB...")
            import os
            import sys
            from pathlib import Path
            
            backend_dir = Path(__file__).parent / 'backend'
            sys.path.insert(0, str(backend_dir))
            
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.working_settings')
            import django
            django.setup()
            
            from database.mongodb_connection import get_mongodb
            
            mongodb = get_mongodb()
            if mongodb.connect():
                users_collection = mongodb.get_collection('users')
                
                # Check if user exists
                user_exists = users_collection.find_one({'firebase_uid': test_uid})
                if user_exists:
                    print(f"✅ User found in MongoDB!")
                    print(f"   📧 Email: {user_exists.get('email', 'N/A')}")
                    print(f"   📅 Created: {user_exists.get('created_at', 'N/A')}")
                else:
                    print(f"❌ User not found in MongoDB")
            
            return True
        else:
            print(f"❌ Failed to create user: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Debugging Frontend Registration Issue")
    print("=" * 60)
    print("This script helps identify why frontend registration isn't syncing to MongoDB")
    print("=" * 60)
    
    # Check current users
    check_current_users()
    
    # Test different token patterns
    test_user_sync_with_different_tokens()
    
    # Create a test user
    create_test_user_for_frontend()
    
    print("\n" + "=" * 60)
    print("💡 Troubleshooting Tips:")
    print("1. Check browser console for JavaScript errors")
    print("2. Verify UserContext is triggering sync on auth state change")
    print("3. Check if frontend is making API calls to /api/users/sync/")
    print("4. Ensure backend server is running on port 8000")
    print("5. Check CORS configuration allows frontend origin")
    print("\n🔗 To test manually:")
    print("1. Open browser developer tools")
    print("2. Go to Network tab")
    print("3. Register a new user in your app")
    print("4. Look for API calls to /api/users/sync/")
    print("5. Check if calls are successful (200 status)")

if __name__ == "__main__":
    main()
