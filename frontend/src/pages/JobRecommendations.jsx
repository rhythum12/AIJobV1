import React, { useState } from 'react';
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

  // Fetch job recommendations and regular jobs
  const { data: recommendations, loading: recommendationsLoading, error: recommendationsError } = useJobRecommendations();
  const { data: jobs, loading: jobsLoading, error: jobsError } = useJobs(searchParams);
  const { execute: applyForJob } = useApi();
  const { execute: saveJob } = useApi();

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

  const handleSearch = (e) => {
    e.preventDefault();
    // The useJobs hook will automatically refetch when searchParams change
  };

  if (recommendationsLoading || jobsLoading) {
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
          <div className="mt-8 bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Search Jobs</h2>
            <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <input
                type="text"
                placeholder="Category"
                value={searchParams.category}
                onChange={(e) => setSearchParams({...searchParams, category: e.target.value})}
                className="border border-gray-300 rounded-md px-3 py-2"
              />
              <input
                type="text"
                placeholder="Location"
                value={searchParams.location}
                onChange={(e) => setSearchParams({...searchParams, location: e.target.value})}
                className="border border-gray-300 rounded-md px-3 py-2"
              />
              <input
                type="number"
                placeholder="Min Salary"
                value={searchParams.salary_min}
                onChange={(e) => setSearchParams({...searchParams, salary_min: e.target.value})}
                className="border border-gray-300 rounded-md px-3 py-2"
              />
              <input
                type="number"
                placeholder="Max Salary"
                value={searchParams.salary_max}
                onChange={(e) => setSearchParams({...searchParams, salary_max: e.target.value})}
                className="border border-gray-300 rounded-md px-3 py-2"
              />
            </form>
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
