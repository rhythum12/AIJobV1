import React, { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext.js';
import Navbar from '../components/Navbar.jsx';
import Footer from '../components/Footer.jsx';

const SavedJobs = () => {
  const { user } = useUser();
  const isAuthenticated = !!user?.email;
  
  const [savedAiJobs, setSavedAiJobs] = useState([]);
  const [savedRegularJobs, setSavedRegularJobs] = useState([]);

  // Load saved jobs from localStorage on component mount
  useEffect(() => {
    const aiJobs = JSON.parse(localStorage.getItem('savedAiJobs') || '[]');
    const regularJobs = JSON.parse(localStorage.getItem('savedRegularJobs') || '[]');
    setSavedAiJobs(aiJobs);
    setSavedRegularJobs(regularJobs);
  }, []);

  const handleRemoveAiJob = (jobId) => {
    const updatedJobs = savedAiJobs.filter(job => job.id !== jobId);
    setSavedAiJobs(updatedJobs);
    localStorage.setItem('savedAiJobs', JSON.stringify(updatedJobs));
  };

  const handleRemoveRegularJob = (jobId) => {
    const updatedJobs = savedRegularJobs.filter(job => job.id !== jobId);
    setSavedRegularJobs(updatedJobs);
    localStorage.setItem('savedRegularJobs', JSON.stringify(updatedJobs));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar isAuthenticated={isAuthenticated} />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900">Saved Jobs</h1>
          <p className="mt-2 text-gray-600">Your saved job listings.</p>
          
          {/* Saved AI Jobs */}
          {savedAiJobs.length > 0 && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">🤖 Saved AI Jobs</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {savedAiJobs.map((job) => (
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
                      <span className={`text-sm font-medium px-2 py-1 rounded-full ${
                        job.match_score >= 80 ? 'bg-green-100 text-green-800' :
                        job.match_score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        Match: {job.match_score}%
                      </span>
                      <p className="text-xs text-gray-500 mt-1">{job.skills}</p>
                    </div>
                    <p className="text-xs text-gray-400 mt-2">
                      Saved: {new Date(job.saved_date).toLocaleDateString()}
                    </p>
                    <div className="mt-4 flex space-x-2">
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors">
                        Apply Now
                      </button>
                      <button 
                        onClick={() => handleRemoveAiJob(job.id)}
                        className="bg-red-200 text-red-700 px-4 py-2 rounded-md text-sm hover:bg-red-300 transition-colors"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Saved Regular Jobs */}
          {savedRegularJobs.length > 0 && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">📋 Saved Regular Jobs</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {savedRegularJobs.map((job) => (
                  <div key={job.id} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                    <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                    <p className="text-gray-600 text-sm mt-1">{job.company}</p>
                    <p className="text-gray-500 text-sm mt-2">{job.salary}</p>
                    <div className="mt-4 flex space-x-2">
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors">
                        Apply Now
                      </button>
                      <button 
                        onClick={() => handleRemoveRegularJob(job.id)}
                        className="bg-red-200 text-red-700 px-4 py-2 rounded-md text-sm hover:bg-red-300 transition-colors"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* No saved jobs message */}
          {savedAiJobs.length === 0 && savedRegularJobs.length === 0 && (
            <div className="mt-8 text-center py-12">
              <div className="text-gray-400 text-6xl mb-4">📋</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No saved jobs yet</h3>
              <p className="text-gray-500 mb-4">Start saving jobs you're interested in by clicking the "Save" button on job listings.</p>
              <a 
                href="/jobs" 
                className="bg-blue-600 text-white px-6 py-3 rounded-md text-sm hover:bg-blue-700 transition-colors inline-block"
              >
                Browse Jobs
              </a>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default SavedJobs;
