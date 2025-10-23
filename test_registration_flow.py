#!/usr/bin/env python3
"""
Test script to verify registration and profile data flow
"""

import requests
import json
import time

def test_registration_flow():
    """Test the complete registration flow"""
    print("🧪 Testing Registration and Profile Data Flow")
    print("=" * 60)
    
    # Test data
    test_user_data = {
        "firebase_uid": "test_user_comprehensive_123",
        "email": "john.doe@example.com",
        "display_name": "John Doe",
        "profile_complete": True,
        "personal_info": {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1-555-0123",
            "location": "San Francisco, CA",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "portfolio_url": "https://johndoe.dev",
            "bio": "Experienced software engineer with 5+ years in full-stack development."
        },
        "professional_info": {
            "current_job_title": "Senior Software Engineer",
            "current_company": "TechCorp Inc",
            "experience_level": "senior",
            "desired_job_title": "Lead Software Engineer",
            "desired_salary": "120000-150000",
            "work_type": "full-time",
            "work_location": "hybrid"
        },
        "skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker"],
        "job_categories": ["Software Engineering", "DevOps"],
        "preferred_locations": ["San Francisco", "Remote"],
        "education": [
            {
                "degree": "Bachelor's",
                "field": "Computer Science",
                "school": "Stanford University",
                "graduationYear": "2018",
                "gpa": "3.8"
            }
        ],
        "work_experience": [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp Inc",
                "startDate": "2020-01-01",
                "endDate": "",
                "current": True,
                "description": "Led development of microservices architecture and improved system performance by 40%."
            }
        ],
        "languages": ["English", "Spanish"],
        "certifications": ["AWS Solutions Architect", "Google Cloud Professional"],
        "preferences": {
            "job_categories": ["Software Engineering", "DevOps"],
            "locations": ["San Francisco", "Remote"],
            "salary_range": {"min": 120000, "max": 150000},
            "work_type": ["full-time"],
            "experience_level": "senior"
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
    
    # Test 1: Check backend health
    print("1. Testing backend health...")
    try:
        response = requests.get("http://localhost:8000/health/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend is running")
        else:
            print(f"   ❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Backend is not running: {e}")
        return False
    
    # Test 2: Send comprehensive user data to sync endpoint
    print("\n2. Testing user sync with comprehensive data...")
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test_user_comprehensive_123'
        }
        response = requests.post(
            "http://localhost:8000/api/users/sync/",
            json=test_user_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ User sync successful")
            print(f"   📊 Response: {result.get('message', 'No message')}")
        else:
            print(f"   ❌ User sync failed: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ User sync request failed: {e}")
        return False
    
    # Test 3: Retrieve user profile
    print("\n3. Testing user profile retrieval...")
    try:
        headers = {
            'Authorization': 'Bearer test_user_comprehensive_123'
        }
        response = requests.get(
            "http://localhost:8000/api/users/profile/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                user_data = result.get('user', {})
                print("   ✅ User profile retrieved successfully")
                print(f"   👤 Name: {user_data.get('display_name', 'N/A')}")
                print(f"   📧 Email: {user_data.get('email', 'N/A')}")
                print(f"   📱 Phone: {user_data.get('personal_info', {}).get('phone', 'N/A')}")
                print(f"   🏢 Company: {user_data.get('professional_info', {}).get('current_company', 'N/A')}")
                print(f"   🎯 Skills: {', '.join(user_data.get('skills', []))}")
                print(f"   🎓 Education: {len(user_data.get('education', []))} entries")
                print(f"   💼 Experience: {len(user_data.get('work_experience', []))} entries")
            else:
                print("   ❌ User profile retrieval failed")
                return False
        else:
            print(f"   ❌ User profile request failed: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ User profile request failed: {e}")
        return False
    
    # Test 4: Check MongoDB directly
    print("\n4. Testing MongoDB data storage...")
    try:
        import subprocess
        result = subprocess.run([
            'docker', 'exec', 'job_recommender_mongodb', 
            'mongosh', 'job_recommender', 
            '--eval', 'db.users.countDocuments({})'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            user_count = result.stdout.strip().split('\n')[-1]
            print(f"   📊 Total users in MongoDB: {user_count}")
        else:
            print("   ⚠️ Could not check MongoDB directly")
    except Exception as e:
        print(f"   ⚠️ MongoDB check failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Registration and Profile Flow Test Complete!")
    print("\n💡 Next Steps:")
    print("   1. Register a new user through the frontend")
    print("   2. Check the profile page to see all user data")
    print("   3. Verify data is stored in MongoDB via Mongo Express")
    print("\n🌐 URLs:")
    print("   - Frontend: http://localhost:3000")
    print("   - Backend: http://localhost:8000")
    print("   - Mongo Express: http://localhost:8081")
    
    return True

if __name__ == "__main__":
    test_registration_flow()
