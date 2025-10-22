import React from 'react';
import { useUser } from '../context/UserContext.js';
import Navbar from '../components/Navbar.jsx';
import Footer from '../components/Footer.jsx';

const About = () => {
  const { user } = useUser();
  const isAuthenticated = !!user?.email;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar isAuthenticated={isAuthenticated} />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900">About Us</h1>
          <p className="mt-2 text-gray-600">Learn more about our platform.</p>
          
          {/* About content */}
          <div className="mt-8 space-y-8">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Our Mission</h2>
              <p className="text-gray-600 leading-relaxed">
                We're revolutionizing the job search process by leveraging artificial intelligence to match 
                talented individuals with their perfect career opportunities. Our platform analyzes your skills, 
                experience, and preferences to provide personalized job recommendations that align with your 
                career goals.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">How We Work</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-blue-600 font-bold text-xl">1</span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Upload Resume</h3>
                  <p className="text-gray-600 text-sm">Upload your resume or create your profile</p>
                </div>
                <div className="text-center">
                  <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-blue-600 font-bold text-xl">2</span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
                  <p className="text-gray-600 text-sm">Our AI analyzes your skills and preferences</p>
                </div>
                <div className="text-center">
                  <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-blue-600 font-bold text-xl">3</span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2">Get Matches</h3>
                  <p className="text-gray-600 text-sm">Receive personalized job recommendations</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Our Team</h2>
              <p className="text-gray-600 leading-relaxed">
                We're a team of passionate developers, data scientists, and career experts dedicated to 
                making job searching more efficient and successful. Our diverse backgrounds in technology, 
                HR, and career development help us create the most effective job matching platform.
              </p>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default About;
