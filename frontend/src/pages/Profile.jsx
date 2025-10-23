import React, { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext.js';
import Navbar from '../components/Navbar.jsx';
import Footer from '../components/Footer.jsx';
import apiService from '../services/api';

const Profile = () => {
  const { user } = useUser();
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('personal');

  const isAuthenticated = !!user?.email;

  useEffect(() => {
    if (isAuthenticated) {
      loadUserProfile();
    }
  }, [isAuthenticated]);

  const loadUserProfile = async () => {
    try {
      setLoading(true);
      
      // First, check if we have comprehensive profile data in localStorage
      const storedProfileData = localStorage.getItem('userProfileData');
      if (storedProfileData) {
        const profileData = JSON.parse(storedProfileData);
        setUserProfile(profileData);
        setLoading(false);
        return;
      }
      
      // Fallback to API if no localStorage data
      const response = await apiService.getUserProfile();
      if (response.success) {
        setUserProfile(response.user);
      } else {
        setError('Failed to load profile data');
      }
    } catch (err) {
      console.error('Error loading profile:', err);
      setError('Error loading profile data');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not specified';
    return new Date(dateString).toLocaleDateString();
  };

  const formatSalary = (salary) => {
    if (!salary) return 'Not specified';
    if (typeof salary === 'string') return salary;
    if (typeof salary === 'object' && salary.min && salary.max) {
      return `$${salary.min.toLocaleString()} - $${salary.max.toLocaleString()}`;
    }
    return 'Not specified';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar isAuthenticated={isAuthenticated} />
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <div className="space-y-4">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                  <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar isAuthenticated={isAuthenticated} />
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{error}</p>
                  </div>
                  <div className="mt-4">
                    <button
                      onClick={loadUserProfile}
                      className="bg-red-100 text-red-800 px-3 py-2 rounded-md text-sm font-medium hover:bg-red-200"
                    >
                      Try Again
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (!userProfile) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar isAuthenticated={isAuthenticated} />
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-yellow-800">No Profile Data</h3>
                  <div className="mt-2 text-sm text-yellow-700">
                    <p>No profile data found. Please complete your registration or contact support.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  const tabs = [
    { id: 'personal', name: 'Personal Info', icon: '👤' },
    { id: 'professional', name: 'Professional', icon: '💼' },
    { id: 'skills', name: 'Skills & Interests', icon: '🎯' },
    { id: 'education', name: 'Education', icon: '🎓' },
    { id: 'experience', name: 'Experience', icon: '💼' },
    { id: 'preferences', name: 'Preferences', icon: '⚙️' }
  ];

  const renderPersonalInfo = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.personal_info?.first_name && userProfile.personal_info?.last_name 
              ? `${userProfile.personal_info.first_name} ${userProfile.personal_info.last_name}`
              : userProfile.display_name || 'Not provided'
            }
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.email || 'Not provided'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.personal_info?.phone || 'Not provided'}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.personal_info?.location || 'Not provided'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">LinkedIn</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.personal_info?.linkedin_url ? (
              <a href={userProfile.personal_info.linkedin_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                {userProfile.personal_info.linkedin_url}
              </a>
            ) : 'Not provided'}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Portfolio</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.personal_info?.portfolio_url ? (
              <a href={userProfile.personal_info.portfolio_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                {userProfile.personal_info.portfolio_url}
              </a>
            ) : 'Not provided'}
          </div>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
        <div className="p-3 bg-gray-50 rounded-md min-h-[100px]">
          {userProfile.personal_info?.bio || 'No bio provided'}
        </div>
      </div>
    </div>
  );

  const renderProfessionalInfo = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Current Job Title</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.professional_info?.current_job_title || 'Not provided'}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Current Company</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.professional_info?.current_company || 'Not provided'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Experience Level</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.professional_info?.experience_level || 'Not provided'}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Desired Job Title</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.professional_info?.desired_job_title || 'Not provided'}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Desired Salary</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {formatSalary(userProfile.professional_info?.desired_salary)}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Work Type</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.professional_info?.work_type || 'Not provided'}
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Work Location</label>
          <div className="p-3 bg-gray-50 rounded-md">
            {userProfile.professional_info?.work_location || 'Not provided'}
          </div>
        </div>
      </div>
    </div>
  );

  const renderSkillsAndInterests = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Skills</label>
        <div className="p-3 bg-gray-50 rounded-md">
          {userProfile.skills && userProfile.skills.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {userProfile.skills.map((skill, index) => (
                <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <span className="text-gray-500">No skills added</span>
          )}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Job Categories of Interest</label>
        <div className="p-3 bg-gray-50 rounded-md">
          {userProfile.job_categories && userProfile.job_categories.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {userProfile.job_categories.map((category, index) => (
                <span key={index} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                  {category}
                </span>
              ))}
            </div>
          ) : (
            <span className="text-gray-500">No categories selected</span>
          )}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Job Locations</label>
        <div className="p-3 bg-gray-50 rounded-md">
          {userProfile.preferred_locations && userProfile.preferred_locations.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {userProfile.preferred_locations.map((location, index) => (
                <span key={index} className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
                  {location}
                </span>
              ))}
            </div>
          ) : (
            <span className="text-gray-500">No preferred locations set</span>
          )}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Languages</label>
        <div className="p-3 bg-gray-50 rounded-md">
          {userProfile.languages && userProfile.languages.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {userProfile.languages.map((language, index) => (
                <span key={index} className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                  {language}
                </span>
              ))}
            </div>
          ) : (
            <span className="text-gray-500">No languages added</span>
          )}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Certifications</label>
        <div className="p-3 bg-gray-50 rounded-md">
          {userProfile.certifications && userProfile.certifications.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {userProfile.certifications.map((cert, index) => (
                <span key={index} className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm">
                  {cert}
                </span>
              ))}
            </div>
          ) : (
            <span className="text-gray-500">No certifications added</span>
          )}
        </div>
      </div>
    </div>
  );

  const renderEducation = () => (
    <div className="space-y-6">
      {userProfile.education && userProfile.education.length > 0 ? (
        userProfile.education.map((edu, index) => (
          <div key={index} className="border rounded-lg p-4 bg-white">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Degree</label>
                <div className="p-2 bg-gray-50 rounded">
                  {edu.degree || 'Not specified'}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Field of Study</label>
                <div className="p-2 bg-gray-50 rounded">
                  {edu.field || 'Not specified'}
                </div>
              </div>
            </div>
            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">School/University</label>
              <div className="p-2 bg-gray-50 rounded">
                {edu.school || 'Not specified'}
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Graduation Year</label>
                <div className="p-2 bg-gray-50 rounded">
                  {edu.graduationYear || 'Not specified'}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">GPA</label>
                <div className="p-2 bg-gray-50 rounded">
                  {edu.gpa || 'Not specified'}
                </div>
              </div>
            </div>
          </div>
        ))
      ) : (
        <div className="text-center py-8 text-gray-500">
          No education information provided
        </div>
      )}
    </div>
  );

  const renderExperience = () => (
    <div className="space-y-6">
      {userProfile.work_experience && userProfile.work_experience.length > 0 ? (
        userProfile.work_experience.map((exp, index) => (
          <div key={index} className="border rounded-lg p-4 bg-white">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
                <div className="p-2 bg-gray-50 rounded">
                  {exp.title || 'Not specified'}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
                <div className="p-2 bg-gray-50 rounded">
                  {exp.company || 'Not specified'}
                </div>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                <div className="p-2 bg-gray-50 rounded">
                  {formatDate(exp.startDate)}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                <div className="p-2 bg-gray-50 rounded">
                  {exp.current ? 'Current' : formatDate(exp.endDate)}
                </div>
              </div>
            </div>
            {exp.description && (
              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <div className="p-2 bg-gray-50 rounded">
                  {exp.description}
                </div>
              </div>
            )}
          </div>
        ))
      ) : (
        <div className="text-center py-8 text-gray-500">
          No work experience provided
        </div>
      )}
    </div>
  );

  const renderPreferences = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Job Preferences</label>
        <div className="p-4 bg-gray-50 rounded-md">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <span className="text-sm font-medium text-gray-600">Salary Range:</span>
              <div className="mt-1">
                {formatSalary(userProfile.preferences?.salary_range)}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Work Type:</span>
              <div className="mt-1">
                {userProfile.preferences?.work_type?.join(', ') || 'Not specified'}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Experience Level:</span>
              <div className="mt-1">
                {userProfile.preferences?.experience_level || 'Not specified'}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Job Categories:</span>
              <div className="mt-1">
                {userProfile.preferences?.job_categories?.join(', ') || 'Not specified'}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Account Settings</label>
        <div className="p-4 bg-gray-50 rounded-md">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <span className="text-sm font-medium text-gray-600">Profile Visibility:</span>
              <div className="mt-1">
                {userProfile.settings?.profile_visibility || 'Not specified'}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Email Notifications:</span>
              <div className="mt-1">
                {userProfile.settings?.email_notifications ? 'Enabled' : 'Disabled'}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Push Notifications:</span>
              <div className="mt-1">
                {userProfile.settings?.push_notifications ? 'Enabled' : 'Disabled'}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Job Alerts:</span>
              <div className="mt-1">
                {userProfile.settings?.job_alerts ? 'Enabled' : 'Disabled'}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Newsletter:</span>
              <div className="mt-1">
                {userProfile.settings?.newsletter ? 'Subscribed' : 'Not subscribed'}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Privacy Level:</span>
              <div className="mt-1">
                {userProfile.settings?.privacy_level || 'Not specified'}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Account Information</label>
        <div className="p-4 bg-gray-50 rounded-md">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <span className="text-sm font-medium text-gray-600">Profile Complete:</span>
              <div className="mt-1">
                <span className={`px-2 py-1 rounded-full text-xs ${
                  userProfile.profile_complete 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {userProfile.profile_complete ? 'Complete' : 'Incomplete'}
                </span>
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Last Login:</span>
              <div className="mt-1">
                {formatDate(userProfile.last_login)}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Account Created:</span>
              <div className="mt-1">
                {formatDate(userProfile.created_at)}
              </div>
            </div>
            <div>
              <span className="text-sm font-medium text-gray-600">Last Sync:</span>
              <div className="mt-1">
                {formatDate(userProfile.last_sync)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'personal':
        return renderPersonalInfo();
      case 'professional':
        return renderProfessionalInfo();
      case 'skills':
        return renderSkillsAndInterests();
      case 'education':
        return renderEducation();
      case 'experience':
        return renderExperience();
      case 'preferences':
        return renderPreferences();
      default:
        return renderPersonalInfo();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar isAuthenticated={isAuthenticated} />
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
            <p className="mt-2 text-gray-600">View and manage your profile information.</p>
          </div>

          {/* Tab Navigation */}
          <div className="border-b border-gray-200 mb-6">
            <nav className="-mb-px flex space-x-8 overflow-x-auto">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.name}
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="bg-white rounded-lg shadow-sm">
            <div className="p-6">
              {renderTabContent()}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-6 flex justify-end space-x-4">
            <button
              onClick={loadUserProfile}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Refresh
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
              Edit Profile
            </button>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Profile;