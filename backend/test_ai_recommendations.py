#!/usr/bin/env python3
"""
Test script to verify AI recommendation system is working
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

import requests
import json

def test_ai_recommendations():
    """Test the AI recommendation system"""
    
    print("🧪 Testing AI Recommendation System...")
    print("=" * 50)
    
    # Test parameters
    test_params = {
        'query': 'software engineer',
        'location': 'Perth',
        'limit': 5,
        'skills': 'Python,React,Django',
        'experience': '3 years',
        'resume_text': 'Full-stack developer with React and Python experience'
    }
    
    try:
        # Test the AI jobs endpoint
        print("📡 Fetching AI jobs with recommendations...")
        response = requests.get('http://localhost:8000/api/jobs/ai/', params=test_params)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                jobs = data.get('jobs', [])
                print(f"✅ Successfully fetched {len(jobs)} AI jobs")
                print(f"🤖 AI Recommendations Active: {data.get('ai_recommendations', False)}")
                print()
                
                # Display job recommendations with match scores
                for i, job in enumerate(jobs[:3], 1):
                    print(f"Job {i}:")
                    print(f"  Title: {job.get('title', 'Unknown')}")
                    print(f"  Company: {job.get('company', 'Unknown')}")
                    print(f"  Match Score: {job.get('match_score', 0)}%")
                    print(f"  AI Recommended: {job.get('ai_recommendation', False)}")
                    print(f"  Skills: {job.get('skills', 'Unknown')}")
                    print()
                
                # Check if match scores are varied (not all the same)
                match_scores = [job.get('match_score', 0) for job in jobs]
                unique_scores = set(match_scores)
                
                if len(unique_scores) > 1:
                    print("✅ AI Recommendation System Working!")
                    print(f"   Match scores are varied: {sorted(unique_scores, reverse=True)}")
                else:
                    print("⚠️  AI Recommendation System may not be working properly")
                    print(f"   All match scores are the same: {unique_scores}")
                
            else:
                print("❌ API returned error:", data.get('error', 'Unknown error'))
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print("Response:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running on localhost:8000")
        print("   Run: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=" * 50)

def test_refresh_ai_jobs():
    """Test the refresh AI jobs endpoint"""
    
    print("🔄 Testing AI Jobs Refresh...")
    print("=" * 50)
    
    try:
        # Test the refresh endpoint
        refresh_data = {
            'query': 'data scientist',
            'location': 'Perth',
            'limit': 3
        }
        
        print("📡 Refreshing AI jobs...")
        response = requests.post(
            'http://localhost:8000/api/jobs/ai/refresh/',
            json=refresh_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                jobs = data.get('jobs', [])
                print(f"✅ Successfully refreshed {len(jobs)} AI jobs")
                print(f"🤖 AI Recommendations Active: {data.get('ai_recommendations', False)}")
                
                # Display refreshed jobs
                for i, job in enumerate(jobs[:2], 1):
                    print(f"Refreshed Job {i}:")
                    print(f"  Title: {job.get('title', 'Unknown')}")
                    print(f"  Match Score: {job.get('match_score', 0)}%")
                    print(f"  AI Recommended: {job.get('ai_recommendation', False)}")
                    print()
                    
            else:
                print("❌ Refresh failed:", data.get('error', 'Unknown error'))
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print("Response:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    print("🚀 AI Recommendation System Test Suite")
    print()
    
    test_ai_recommendations()
    print()
    test_refresh_ai_jobs()
    
    print("🎉 Test completed!")
    print()
    print("📝 Notes:")
    print("- Make sure your Django server is running: python manage.py runserver")
    print("- Ensure your AI folder has the required dependencies installed")
    print("- Check that your Adzuna API credentials are properly configured")
