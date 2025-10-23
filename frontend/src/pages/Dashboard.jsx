import React from 'react';
import { useUser } from '../context/UserContext.js';
import { useDashboardAnalytics, useJobRecommendations } from '../hooks/useApi.js';
import Navbar from '../components/Navbar.jsx';
import Footer from '../components/Footer.jsx';

const Dashboard = () => {
  const { user } = useUser();
  const isAuthenticated = !!user?.email;
  
  // Fetch dashboard analytics and job recommendations
  const { data: analytics, loading: analyticsLoading, error: analyticsError } = useDashboardAnalytics();
  const { data: recommendations, loading: recommendationsLoading, error: recommendationsError } = useJobRecommendations();

  if (analyticsLoading || recommendationsLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar isAuthenticated={isAuthenticated} />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">Welcome to your dashboard!</p>
          
          {/* Dashboard content */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900">Applications</h3>
              <p className="text-3xl font-bold text-blue-600 mt-2">
                {analytics?.analytics?.applications_this_month || 0}
              </p>
              <p className="text-gray-600">This Month</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900">Interviews</h3>
              <p className="text-3xl font-bold text-green-600 mt-2">
                {analytics?.analytics?.interviews_scheduled || 0}
              </p>
              <p className="text-gray-600">Scheduled</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900">Job Matches</h3>
              <p className="text-3xl font-bold text-yellow-600 mt-2">
                {analytics?.analytics?.job_matches || 0}
              </p>
              <p className="text-gray-600">New Matches</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900">Profile Score</h3>
              <p className="text-3xl font-bold text-purple-600 mt-2">
                {analytics?.analytics?.profile_completion || 0}%
              </p>
              <p className="text-gray-600">Complete</p>
            </div>
          </div>

          {/* Job Recommendations Section */}
          <div className="mt-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Recommended Jobs</h2>
            {recommendationsError ? (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <p className="text-red-600">Error loading recommendations: {recommendationsError}</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations?.recommendations?.map((job) => (
                  <div key={job.id} className="bg-white p-6 rounded-lg shadow-sm border">
                    <h3 className="text-lg font-semibold text-gray-900">{job.title}</h3>
                    <p className="text-gray-600">{job.company}</p>
                    <p className="text-gray-500 text-sm">{job.location}</p>
                    <p className="text-green-600 font-semibold mt-2">{job.salary}</p>
                    <div className="mt-4 flex items-center justify-between">
                      <span className="text-sm text-gray-500">Match: {job.match_score}%</span>
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700">
                        Apply
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Skill Gaps Section */}
          {analytics?.analytics?.skill_gaps && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Skill Development</h2>
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended Skills to Learn</h3>
                <div className="flex flex-wrap gap-2">
                  {analytics.analytics.skill_gaps.map((skill, index) => (
                    <span key={index} className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Dashboard;
