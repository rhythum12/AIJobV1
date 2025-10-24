/**
 * API Service Layer for Job Recommender Frontend
 * Handles all communication with the Django backend API
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Get authentication headers with Firebase token
   */
  async getAuthHeaders() {
    const token = await this.getFirebaseToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    };
  }

  /**
   * Get Firebase ID token
   */
  async getFirebaseToken() {
    try {
      const { auth } = await import('../Firebase/firebase.js');
      const user = auth.currentUser;
      if (user) {
        return await user.getIdToken();
      }
      return null;
    } catch (error) {
      console.error('Error getting Firebase token:', error);
      return null;
    }
  }

  /**
   * Generic API request method
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        ...options.headers,
        ...(await this.getAuthHeaders()),
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Health and Status Endpoints
  async getHealthStatus() {
    return this.request('/health/');
  }

  async getApiStatus() {
    return this.request('/status/');
  }

  // Job-related Endpoints
  async getJobs(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/jobs/?${queryString}` : '/jobs/';
    return this.request(endpoint);
  }

  async getJobDetail(jobId) {
    return this.request(`/jobs/${jobId}/`);
  }

  async searchJobs(searchParams) {
    const queryString = new URLSearchParams(searchParams).toString();
    return this.request(`/jobs/search/?${queryString}`);
  }

  async getJobRecommendations() {
    return this.request('/jobs/recommendations/');
  }

  // Resume and Profile Endpoints
  async uploadResume(file) {
    const formData = new FormData();
    formData.append('resume', file);
    
    const token = await this.getFirebaseToken();
    const response = await fetch(`${this.baseURL}/resume/upload/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  }

  async analyzeResume() {
    return this.request('/resume/analyze/', { method: 'POST' });
  }

  async updateResume(resumeData) {
    return this.request('/resume/update/', {
      method: 'PUT',
      body: JSON.stringify(resumeData),
    });
  }

  // User Job Interaction Endpoints
  async applyForJob(jobId) {
    return this.request(`/jobs/${jobId}/apply/`, { method: 'POST' });
  }

  async saveJob(jobId) {
    return this.request(`/jobs/${jobId}/save/`, { method: 'POST' });
  }

  async unsaveJob(jobId) {
    return this.request(`/jobs/${jobId}/unsave/`, { method: 'DELETE' });
  }

  async getAppliedJobs() {
    return this.request('/user/applied-jobs/');
  }

  async getSavedJobs() {
    return this.request('/user/saved-jobs/');
  }

  // User Preferences and Settings
  async getUserPreferences() {
    return this.request('/user/preferences/');
  }

  async updateUserPreferences(preferences) {
    return this.request('/user/preferences/', {
      method: 'PUT',
      body: JSON.stringify(preferences),
    });
  }

  async getUserSettings() {
    return this.request('/user/settings/');
  }

  async updateUserSettings(settings) {
    return this.request('/user/settings/', {
      method: 'PUT',
      body: JSON.stringify(settings),
    });
  }

  // Analytics and Insights
  async getDashboardAnalytics() {
    return this.request('/analytics/dashboard/');
  }

  async getJobTrends() {
    return this.request('/analytics/job-trends/');
  }

  // User Profile Endpoints (from user_urls)
  async getUserProfile() {
    return this.request('/users/profile/');
  }

  async updateUserProfile(profileData) {
    return this.request('/users/profile/', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }

  async syncUser() {
    return this.request('/users/sync/', { method: 'POST' });
  }

  async getUserActivities() {
    return this.request('/users/activities/');
  }

  // Skills and Categories
  async getSkills() {
    return this.request('/jobs/skills/');
  }

  async getCategories() {
    return this.request('/jobs/categories/');
  }

  // AI Jobs endpoints
  async getAiJobs(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/jobs/ai/?${queryString}` : '/jobs/ai/';
    return this.request(endpoint);
  }

  async refreshAiJobs(params = {}) {
    return this.request('/jobs/ai/refresh/', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  async saveAiJob(jobData) {
    return this.request('/jobs/ai/save/', {
      method: 'POST',
      body: JSON.stringify(jobData),
    });
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;

