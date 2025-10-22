import React from 'react';
import { useUser } from '../context/UserContext.js';
import Navbar from '../components/Navbar.jsx';
import Footer from '../components/Footer.jsx';

const JobRecommendations = () => {
  const { user } = useUser();
  const isAuthenticated = !!user?.email;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar isAuthenticated={isAuthenticated} />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900">Job Recommendations</h1>
          <p className="mt-2 text-gray-600">Find your next job opportunity.</p>
          
          {/* Job recommendations */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <h3 className="text-lg font-semibold text-gray-900">Frontend Developer</h3>
              <p className="text-gray-600 text-sm mt-1">WebTech Solutions</p>
              <p className="text-gray-500 text-sm mt-2">$70,000 - $100,000</p>
              <p className="text-gray-600 text-sm mt-3">Remote • Full-time</p>
              <div className="mt-4 flex space-x-2">
                <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors">
                  Apply Now
                </button>
                <button className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300 transition-colors">
                  Save
                </button>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <h3 className="text-lg font-semibold text-gray-900">Backend Engineer</h3>
              <p className="text-gray-600 text-sm mt-1">CloudTech Inc.</p>
              <p className="text-gray-500 text-sm mt-2">$80,000 - $120,000</p>
              <p className="text-gray-600 text-sm mt-3">Hybrid • Full-time</p>
              <div className="mt-4 flex space-x-2">
                <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors">
                  Apply Now
                </button>
                <button className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300 transition-colors">
                  Save
                </button>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <h3 className="text-lg font-semibold text-gray-900">Full Stack Developer</h3>
              <p className="text-gray-600 text-sm mt-1">StartupXYZ</p>
              <p className="text-gray-500 text-sm mt-2">$75,000 - $110,000</p>
              <p className="text-gray-600 text-sm mt-3">On-site • Full-time</p>
              <div className="mt-4 flex space-x-2">
                <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700 transition-colors">
                  Apply Now
                </button>
                <button className="bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-300 transition-colors">
                  Save
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default JobRecommendations;
