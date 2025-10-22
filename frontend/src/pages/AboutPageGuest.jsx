import React from 'react';
import { useUser } from '../context/UserContext.js';
import Navbar from '../components/Navbar.jsx';
import Footer from '../components/Footer.jsx';

const AboutPageGuest = () => {
  const { user } = useUser();
  const isAuthenticated = !!user?.email;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar isAuthenticated={isAuthenticated} />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900">About Us</h1>
          <p className="mt-2 text-gray-600">Learn more about our platform.</p>
          
          {/* About content for guests */}
          <div className="mt-8 space-y-8">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Welcome to Job Recommender</h2>
              <p className="text-gray-600 leading-relaxed">
                We're revolutionizing the job search process by leveraging artificial intelligence to match 
                talented individuals with their perfect career opportunities. Our platform analyzes your skills, 
                experience, and preferences to provide personalized job recommendations that align with your 
                career goals.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Get Started Today</h2>
              <div className="flex flex-col sm:flex-row gap-4">
                <button className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors">
                  Create Free Account
                </button>
                <button className="bg-white text-blue-600 border border-blue-600 px-6 py-3 rounded-md hover:bg-blue-50 transition-colors">
                  Learn More
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

export default AboutPageGuest;
