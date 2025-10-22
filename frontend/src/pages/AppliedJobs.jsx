import React from 'react';
import { useUser } from '../context/UserContext.js';
import Navbar from '../components/Navbar.jsx';
import Footer from '../components/Footer.jsx';

const AppliedJobs = () => {
  const { user } = useUser();
  const isAuthenticated = !!user?.email;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar isAuthenticated={isAuthenticated} />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900">Applied Jobs</h1>
          <p className="mt-2 text-gray-600">Track your job applications.</p>
          
          {/* Applied jobs list */}
          <div className="mt-8 space-y-4">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Software Engineer</h3>
                  <p className="text-gray-600">TechCorp Inc.</p>
                  <p className="text-gray-500 text-sm">Applied on Dec 15, 2024</p>
                </div>
                <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
                  Under Review
                </span>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Data Analyst</h3>
                  <p className="text-gray-600">DataCorp Solutions</p>
                  <p className="text-gray-500 text-sm">Applied on Dec 12, 2024</p>
                </div>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                  Interview Scheduled
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default AppliedJobs;
