import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify environment variables
app_id = os.getenv('ADZUNA_APP_ID')
app_key = os.getenv('ADZUNA_APP_KEY')

print(f"App ID: {app_id}")
print(f"App Key: {app_key}")

# Set your Adzuna API credentials
API_APP_ID = os.getenv('ADZUNA_APP_ID')
API_APP_KEY = os.getenv('ADZUNA_APP_KEY')
API_COUNTRY = 'au'  

# Verify API credentials
if not API_APP_ID or not API_APP_KEY:
    raise ValueError("❌ Missing Adzuna API credentials. Please check your .env file.")

# Fetch job data from Adzuna API
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
        print(f"❌ Error fetching data from Adzuna API: {e.response.status_code} - {e.response.text}")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return pd.DataFrame()

# Main function
def main():
    # Collect user inputs
    query = input("Enter the job title (e.g., data scientist): ").strip()
    location = input("Enter your preferred job location: ").strip()
    
    # Fetch job data
    job_df = load_job_data(query, location)
    if job_df.empty:
        print("No jobs found. Please try different parameters.")
        return
    
    # Display job data
    print("\nAvailable Jobs:\n")
    print(job_df[['Job Title', 'Company', 'Location', 'Skills', 'Salary']])

   


