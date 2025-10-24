import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_APP_ID = os.getenv('ADZUNA_APP_ID')
API_APP_KEY = os.getenv('ADZUNA_APP_KEY')
API_COUNTRY = 'au'

if not API_APP_ID or not API_APP_KEY:
    print("⚠️ Missing Adzuna API credentials. Using mock data for testing.")
    API_APP_ID = "mock_app_id"
    API_APP_KEY = "mock_app_key"

def load_job_data(query, location, results_per_page=50):
    base_url = f"https://api.adzuna.com/v1/api/jobs/{API_COUNTRY}/search/1"
    params = {
        'app_id': API_APP_ID,
        'app_key': API_APP_KEY,
        'results_per_page': results_per_page,
        'what': query,
        'where': location
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        jobs = []
        for job in data.get('results', []):
            jobs.append({
                'Job Title': job.get('title', 'Unknown'),
                'Company': job.get('company', {}).get('display_name', 'Unknown'),
                'Location': job.get('location', {}).get('display_name', 'Unknown'),
                'Description': job.get('description', 'No description available'),
                'Skills': job.get('category', {}).get('label', 'Unknown'),
                'Salary': job.get('salary_min', 'Not specified')
            })
        return pd.DataFrame(jobs)
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error fetching data: {e.response.status_code} - {e.response.text}")
        return _get_mock_job_data(query, location, results_per_page)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return _get_mock_job_data(query, location, results_per_page)

def _get_mock_job_data(query, location, results_per_page=50):
    """Return mock job data for testing when API is not available"""
    import random
    from datetime import datetime, timedelta
    
    mock_jobs = []
    companies = ['Tech Corp', 'Innovation Labs', 'Digital Solutions', 'Future Systems', 'Smart Technologies']
    skills_list = ['Python', 'JavaScript', 'React', 'Node.js', 'Docker', 'AWS', 'Machine Learning', 'Data Science']
    
    for i in range(min(results_per_page, 10)):  # Limit to 10 mock jobs
        mock_jobs.append({
            'Job Title': f'{query.title()} Developer',
            'Company': random.choice(companies),
            'Location': location,
            'Description': f'We are looking for a skilled {query} to join our team. This role involves working with cutting-edge technologies and contributing to innovative projects.',
            'Skills': random.choice(skills_list),
            'Salary': f'${random.randint(60000, 120000)}'
        })
    
    return pd.DataFrame(mock_jobs)
