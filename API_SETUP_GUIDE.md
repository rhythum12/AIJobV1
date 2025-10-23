# REST API Setup Guide

This guide explains how to set up and use the REST API for the Job Recommender system.

## 🚀 Quick Start

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Start the Backend Server**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/api/`

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the Frontend Server**
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

## 📡 API Endpoints

### Health & Status
- `GET /api/health/` - Health check
- `GET /api/status/` - Detailed API status

### Jobs
- `GET /api/jobs/` - List all jobs
- `GET /api/jobs/{id}/` - Get job details
- `GET /api/jobs/search/` - Search jobs with filters
- `GET /api/jobs/recommendations/` - Get personalized job recommendations

### Resume & Profile
- `POST /api/resume/upload/` - Upload resume file
- `POST /api/resume/analyze/` - Analyze resume
- `PUT /api/resume/update/` - Update resume information

### User Job Interactions
- `POST /api/jobs/{id}/apply/` - Apply for a job
- `POST /api/jobs/{id}/save/` - Save a job
- `DELETE /api/jobs/{id}/unsave/` - Remove saved job
- `GET /api/user/applied-jobs/` - Get applied jobs
- `GET /api/user/saved-jobs/` - Get saved jobs

### User Preferences & Settings
- `GET /api/user/preferences/` - Get user preferences
- `PUT /api/user/preferences/` - Update user preferences
- `GET /api/user/settings/` - Get user settings
- `PUT /api/user/settings/` - Update user settings

### Analytics
- `GET /api/analytics/dashboard/` - Get dashboard analytics
- `GET /api/analytics/job-trends/` - Get job market trends

### User Management
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile
- `POST /api/users/sync/` - Sync user from Firebase
- `GET /api/users/activities/` - Get user activities

## 🔐 Authentication

The API uses Firebase authentication. Include the Firebase ID token in the Authorization header:

```javascript
headers: {
  'Authorization': `Bearer ${firebaseToken}`,
  'Content-Type': 'application/json'
}
```

## 🎯 Frontend Integration

### Using the API Service

```javascript
import apiService from './services/api';

// Get job recommendations
const recommendations = await apiService.getJobRecommendations();

// Apply for a job
await apiService.applyForJob(jobId);

// Upload resume
const formData = new FormData();
formData.append('resume', file);
await apiService.uploadResume(file);
```

### Using React Hooks

```javascript
import { useJobs, useJobRecommendations } from './hooks/useApi';

function JobList() {
  const { data: jobs, loading, error } = useJobs();
  const { data: recommendations } = useJobRecommendations();
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      {jobs?.jobs?.map(job => (
        <div key={job.id}>{job.title}</div>
      ))}
    </div>
  );
}
```

## 🧪 Testing

Run the API connectivity test:

```bash
python test_api_connectivity.py
```

This will test:
- Health endpoints
- Job endpoints
- CORS configuration
- API status

## 🔧 Configuration

### Backend Configuration

The backend is configured in `backend/backend/settings.py`:

- **CORS Settings**: Configured for `localhost:3000` and `localhost:8000`
- **Database**: PostgreSQL (configurable via environment variables)
- **Firebase**: Authentication and user management

### Frontend Configuration

The frontend API service is configured in `frontend/src/services/api.js`:

- **API Base URL**: `http://localhost:8000/api` (configurable via `REACT_APP_API_URL`)
- **Authentication**: Automatic Firebase token handling
- **Error Handling**: Comprehensive error handling and logging

## 📊 Example API Responses

### Job List Response
```json
{
  "success": true,
  "jobs": [
    {
      "id": 1,
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "salary": "$120,000 - $150,000",
      "description": "We are looking for...",
      "requirements": ["Python", "Django", "React"],
      "posted_date": "2024-01-15"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1
  }
}
```

### Dashboard Analytics Response
```json
{
  "success": true,
  "analytics": {
    "profile_completion": 85,
    "applications_this_month": 12,
    "interviews_scheduled": 3,
    "job_matches": 8,
    "skill_gaps": ["AWS", "Docker", "Kubernetes"],
    "recommendation_score": 92
  }
}
```

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure CORS is properly configured in Django settings
   - Check that the frontend URL is in `CORS_ALLOWED_ORIGINS`

2. **Authentication Errors**
   - Verify Firebase configuration
   - Check that the Firebase token is valid and not expired

3. **Database Connection**
   - Ensure PostgreSQL is running
   - Check database credentials in settings

4. **API Not Responding**
   - Verify Django server is running on port 8000
   - Check for any error messages in the Django logs

### Debug Mode

Enable debug logging by setting `DEBUG = True` in Django settings and check the console for detailed error messages.

## 🔄 Development Workflow

1. **Backend Changes**: Modify API endpoints in `backend/api/views.py`
2. **Frontend Changes**: Update components to use new API endpoints
3. **Testing**: Run the connectivity test to verify changes
4. **Deployment**: Ensure both servers are running and accessible

## 📝 Next Steps

- Implement real database models instead of mock data
- Add comprehensive error handling
- Implement rate limiting
- Add API documentation with Swagger/OpenAPI
- Set up monitoring and logging
- Implement caching for better performance

