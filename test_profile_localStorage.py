#!/usr/bin/env python3
"""
Test script to create sample localStorage data for profile page
"""

import json

def create_sample_profile_data():
    """Create sample profile data that would be stored in localStorage"""
    
    sample_data = {
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
            "bio": "Experienced software engineer with 5+ years in full-stack development. Passionate about building scalable web applications and leading development teams."
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
        "skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes", "TypeScript"],
        "job_categories": ["Software Engineering", "DevOps", "Cloud Computing"],
        "preferred_locations": ["San Francisco", "Remote", "New York"],
        "education": [
            {
                "degree": "Bachelor's",
                "field": "Computer Science",
                "school": "Stanford University",
                "graduationYear": "2018",
                "gpa": "3.8"
            },
            {
                "degree": "Master's",
                "field": "Software Engineering",
                "school": "UC Berkeley",
                "graduationYear": "2020",
                "gpa": "3.9"
            }
        ],
        "work_experience": [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp Inc",
                "startDate": "2020-01-01",
                "endDate": "",
                "current": True,
                "description": "Led development of microservices architecture and improved system performance by 40%. Managed a team of 5 developers and implemented CI/CD pipelines."
            },
            {
                "title": "Software Engineer",
                "company": "StartupXYZ",
                "startDate": "2018-06-01",
                "endDate": "2019-12-31",
                "current": False,
                "description": "Developed full-stack web applications using React and Node.js. Implemented automated testing and deployment processes."
            }
        ],
        "languages": ["English", "Spanish", "French"],
        "certifications": ["AWS Solutions Architect", "Google Cloud Professional", "Certified Kubernetes Administrator"],
        "preferences": {
            "job_categories": ["Software Engineering", "DevOps", "Cloud Computing"],
            "locations": ["San Francisco", "Remote", "New York"],
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
        },
        "created_at": "2025-10-23T20:30:00.000Z",
        "last_login": "2025-10-23T20:30:00.000Z",
        "last_sync": "2025-10-23T20:30:00.000Z"
    }
    
    return sample_data

def main():
    print("🧪 Creating Sample Profile Data for Testing")
    print("=" * 60)
    
    # Create sample data
    sample_data = create_sample_profile_data()
    
    # Save to file
    with open('sample_profile_data.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print("✅ Sample profile data created!")
    print(f"📁 Saved to: sample_profile_data.json")
    print(f"📊 Data includes:")
    print(f"   - Personal Info: {sample_data['personal_info']['first_name']} {sample_data['personal_info']['last_name']}")
    print(f"   - Email: {sample_data['email']}")
    print(f"   - Skills: {len(sample_data['skills'])} skills")
    print(f"   - Education: {len(sample_data['education'])} entries")
    print(f"   - Experience: {len(sample_data['work_experience'])} entries")
    print(f"   - Languages: {len(sample_data['languages'])} languages")
    print(f"   - Certifications: {len(sample_data['certifications'])} certifications")
    
    print("\n💡 To test the profile page:")
    print("   1. Open browser console on the profile page")
    print("   2. Run: localStorage.setItem('userProfileData', JSON.stringify(data))")
    print("   3. Refresh the page to see the comprehensive profile data")
    
    print("\n📋 JavaScript code to run in browser console:")
    print("```javascript")
    print("const profileData = " + json.dumps(sample_data, indent=2) + ";")
    print("localStorage.setItem('userProfileData', JSON.stringify(profileData));")
    print("location.reload();")
    print("```")
    
    return sample_data

if __name__ == "__main__":
    main()
