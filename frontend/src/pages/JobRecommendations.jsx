import React, { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext.js';
import { useJobs, useJobRecommendations, useApi } from '../hooks/useApi.js';
import apiService from '../services/api.js';
import Navbar from '../components/Navbar.jsx';
import Footer from '../components/Footer.jsx';

const JobRecommendations = () => {
  const { user } = useUser();
  const isAuthenticated = !!user?.email;
  const [searchParams, setSearchParams] = useState({
    category: '',
    location: '',
    salary_min: '',
    salary_max: ''
  });

  const [aiSearchParams, setAiSearchParams] = useState({
    query: 'software engineer',
    location: 'Perth',
    limit: 20,
    skills: '',
    experience: '',
    resume_text: ''
  });

  // Fetch job recommendations, regular jobs, and AI jobs
  const { data: recommendations, loading: recommendationsLoading, error: recommendationsError } = useJobRecommendations();
  const { execute: applyForJob } = useApi();
  const { execute: saveJob } = useApi();
  const { execute: refreshAiJobs } = useApi();
  
  // AI jobs state - manually managed to prevent auto-refresh
  const [aiJobs, setAiJobs] = useState(null);
  const [aiJobsLoading, setAiJobsLoading] = useState(false);
  const [aiJobsError, setAiJobsError] = useState(null);
  
  // Regular jobs state - manually managed to prevent auto-refresh
  const [jobs, setJobs] = useState(null);
  const [jobsLoading, setJobsLoading] = useState(false);
  const [jobsError, setJobsError] = useState(null);

  // Load initial data only once when component mounts
  useEffect(() => {
    // Load initial AI jobs
    const initialAiParams = {
      query: 'software engineer',
      location: 'Perth',
      limit: 20
    };
    fetchAiJobs(initialAiParams);
    
    // Load initial regular jobs
    fetchRegularJobs({});
  }, []); // Empty dependency array means this runs only once

  const handleApply = async (jobId) => {
    try {
      await applyForJob(apiService.applyForJob, jobId);
      alert('Application submitted successfully!');
    } catch (error) {
      alert('Failed to apply for job: ' + error.message);
    }
  };

  const handleSave = async (jobId) => {
    try {
      await saveJob(apiService.saveJob, jobId);
      alert('Job saved successfully!');
    } catch (error) {
      alert('Failed to save job: ' + error.message);
    }
  };

  const handleSaveAiJob = async (jobData) => {
    try {
      await apiService.saveAiJob(jobData);
      alert('AI job saved successfully!');
      
      // Also save to localStorage for immediate display
      const savedJobs = JSON.parse(localStorage.getItem('savedAiJobs') || '[]');
      const existingJob = savedJobs.find(job => job.id === jobData.id);
      
      if (!existingJob) {
        savedJobs.push({
          ...jobData,
          saved_date: new Date().toISOString()
        });
        localStorage.setItem('savedAiJobs', JSON.stringify(savedJobs));
      }
    } catch (error) {
      alert('Failed to save AI job: ' + error.message);
    }
  };

  const fetchAiJobs = async (params) => {
    setAiJobsLoading(true);
    setAiJobsError(null);
    
    try {
      const result = await apiService.getAiJobs(params);
      setAiJobs(result);
    } catch (error) {
      setAiJobsError(error.message);
    } finally {
      setAiJobsLoading(false);
    }
  };

  const fetchRegularJobs = async (params) => {
    setJobsLoading(true);
    setJobsError(null);
    
    try {
      const result = await apiService.getJobs(params);
      setJobs(result);
    } catch (error) {
      setJobsError(error.message);
    } finally {
      setJobsLoading(false);
    }
  };

  const handleSearch = (e) => {
    if (e) e.preventDefault();
    fetchRegularJobs(searchParams);
  };

  const handleAiSearch = (e) => {
    if (e) e.preventDefault();
    fetchAiJobs(aiSearchParams);
  };

  const handleInputChange = (field, value) => {
    console.log(`Updating ${field} to: ${value}`); // Debug log
    setAiSearchParams(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      fetchAiJobs(aiSearchParams);
    }
  };

  const handleRefreshAiJobs = async () => {
    try {
      await refreshAiJobs(apiService.refreshAiJobs, aiSearchParams);
      fetchAiJobs(aiSearchParams);
      alert('AI jobs refreshed successfully!');
    } catch (error) {
      alert('Failed to refresh AI jobs: ' + error.message);
    }
  };

  if (recommendationsLoading || jobsLoading || aiJobsLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading jobs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar isAuthenticated={isAuthenticated} />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900">Job Recommendations</h1>
          <p className="mt-2 text-gray-600">Find your next job opportunity.</p>
          
          {/* Search Filters */}


          {/* AI Jobs Search */}
          <div className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg shadow-sm border border-blue-200">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-900">🤖 Real-Time AI Job Search</h2>
              <button
                onClick={handleRefreshAiJobs}
                className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <span>🔄</span>
                Refresh AI Jobs
              </button>
            </div>
            <form onSubmit={handleAiSearch} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input
                  type="text"
                  placeholder="Job Title (e.g., software engineer)"
                  value={aiSearchParams.query}
                  onChange={(e) => handleInputChange('query', e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="border border-gray-300 rounded-md px-3 py-2"
                />
                <input
                  type="text"
                  placeholder="Location (e.g., Perth)"
                  value={aiSearchParams.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="border border-gray-300 rounded-md px-3 py-2"
                />
                <input
                  type="number"
                  placeholder="Limit (max jobs to fetch)"
                  value={aiSearchParams.limit}
                  onChange={(e) => handleInputChange('limit', parseInt(e.target.value) || 20)}
                  onKeyPress={handleKeyPress}
                  className="border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Your Skills (comma-separated, e.g., Python, React, Django)"
                  value={aiSearchParams.skills}
                  onChange={(e) => handleInputChange('skills', e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="border border-gray-300 rounded-md px-3 py-2"
                />
                <input
                  type="text"
                  placeholder="Experience Level (e.g., 3 years, Senior, Entry-level)"
                  value={aiSearchParams.experience}
                  onChange={(e) => handleInputChange('experience', e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="border border-gray-300 rounded-md px-3 py-2"
                />
              </div>
              <div>
                <textarea
                  placeholder="Brief description of your background (optional, helps AI provide better recommendations)"
                  value={aiSearchParams.resume_text}
                  onChange={(e) => handleInputChange('resume_text', e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="border border-gray-300 rounded-md px-3 py-2 w-full h-20 resize-none"
                />
              </div>
              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={handleAiSearch}
                  className="bg-indigo-600 text-white px-6 py-2 rounded-md text-sm hover:bg-indigo-700 transition-colors"
                >
                  🤖 Search AI Jobs
                </button>
              </div>
            </form>
            <p className="text-sm text-gray-600 mt-2">
              💡 Powered by AI job scraping and machine learning recommendations - fetches real-time job listings and calculates personalized match scores based on your skills and experience
            </p>
          </div>

          {/* Job Recommendations */}
          {recommendationsError ? (
            <div className="mt-8 bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-red-600">Error loading recommendations: {recommendationsError}</p>
            </div>
          ) : (
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Recommended for You</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations?.recommendations?.map((job) => (
                  <div key={job.id} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                    <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                    <p className="text-gray-600 text-sm mt-1">{job.company}</p>
                    <p className="text-gray-500 text-sm mt-2">{job.salary}</p>
                    <p className="text-gray-600 text-sm mt-3">{job.location}</p>
                    <div className="mt-2">
                      <span className="text-sm text-blue-600 font-medium">Match: {job.match_score}%</span>
                      <p className="text-xs text-gray-500 mt-1">{job.reason}</p>
                    </div>
                    <div className="mt-4 flex space-x-2">
                      <button 
                        onClick={() => handleApply(job.id)}
                        className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors"
                      >
                        Apply Now
                      </button>
                      <button 
                        onClick={() => handleSave(job.id)}
                        className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300 transition-colors"
                      >
                        Save
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* AI Jobs Section */}
          {aiJobsError ? (
            <div className="mt-8 bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-red-600">Error loading AI jobs: {aiJobsError}</p>
            </div>
          ) : (
            <div className="mt-8">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">🤖 Real-Time AI Jobs</h2>
                  {aiJobs?.ai_recommendations && (
                    <p className="text-sm text-green-600 mt-1">
                      ✨ AI-powered recommendations active - match scores calculated using machine learning
                    </p>
                  )}
                </div>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                  {aiJobs?.total_jobs || 0} jobs found
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {aiJobs?.jobs?.map((job) => (
                  <div key={job.id} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow border-l-4 border-blue-500">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                        AI Scraped
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm mt-1">{job.company}</p>
                    <p className="text-gray-500 text-sm mt-2">{job.salary}</p>
                    <p className="text-gray-600 text-sm mt-3">{job.location}</p>
                    <div className="mt-2">
                      <div className="flex items-center gap-2">
                        <span className={`text-sm font-medium px-2 py-1 rounded-full ${
                          job.match_score >= 80 ? 'bg-green-100 text-green-800' :
                          job.match_score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          Match: {job.match_score}%
                        </span>
                        {job.ai_recommendation && (
                          <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded-full">
                            AI Recommended
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-gray-500 mt-1">{job.skills}</p>
                    </div>
                    <div className="mt-4 flex space-x-2">
                      <button 
                        onClick={() => handleApply(job.id)}
                        className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors"
                      >
                        Apply Now
                      </button>
                      <button 
                        onClick={() => handleSaveAiJob(job)}
                        className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300 transition-colors"
                      >
                        Save
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              {aiJobs?.jobs?.length === 0 && (
                <div className="text-center py-8">
                  <p className="text-gray-500">No AI jobs found. Try adjusting your search criteria.</p>
                </div>
              )}
            </div>
          )}

          {/* All Jobs */}
          {jobsError ? (
            <div className="mt-8 bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-red-600">Error loading jobs: {jobsError}</p>
            </div>
          ) : (
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">All Jobs</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {jobs?.jobs?.map((job) => (
                  <div key={job.id} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                    <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                    <p className="text-gray-600 text-sm mt-1">{job.company}</p>
                    <p className="text-gray-500 text-sm mt-2">{job.salary}</p>
                    <p className="text-gray-600 text-sm mt-3">{job.location}</p>
                    <div className="mt-4 flex space-x-2">
                      <button 
                        onClick={() => handleApply(job.id)}
                        className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors"
                      >
                        Apply Now
                      </button>
                      <button 
                        onClick={() => handleSave(job.id)}
                        className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300 transition-colors"
                      >
                        Save
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default JobRecommendations;
