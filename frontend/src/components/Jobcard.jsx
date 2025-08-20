import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function JobCard({ job, isAuthenticated = false, }) {
  const [isSaved, setIsSaved] = useState(false);
  const [isApplied, setIsApplied] = useState(false);
  const navigate = useNavigate();

  const handleSave = () => {
    if (isAuthenticated) {
      setIsSaved(!isSaved); 
      alert(`Job "${job.title}" ${isSaved ? 'removed from saved' : 'saved'}!`);
    } else {
      alert(`First login, then you can save "${job.title}" job!`);
      if (window.confirm('Do you want to login?')) {
        navigate('/loginpage');
      }
    }
  };

  const handleApply = () => {
    if (isAuthenticated) {
      setIsApplied(true);
      alert(`You have applied to "${job.title}".`);
    } else {
      alert(`First login, then you can apply to "${job.title}".`);
      if (window.confirm('Do you want to login?')) {
        navigate('/loginpage');
      }
    }
  };

  return (
    <>
      <div className="bg-white shadow-md rounded-lg p-4 mb-4 border px-10 hover:shadow-lg transition-shadow duration-200 relative">
        <button
          onClick={handleSave}
          className={`absolute top-4 right-4 p-2 rounded-full transition-colors duration-200 ${
            isSaved 
              ? 'text-red-500 hover:text-red-600 hover:bg-red-50' 
              : 'text-gray-400 hover:text-gray-600 hover:bg-gray-50'
          }`}
          title={isSaved ? "Remove from saved" : "Save job"}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill={isSaved ? "currentColor" : "none"}
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z" />
          </svg>
        </button>

        <div className="flex justify-between items-start pr-12">
          <div className="flex items-start space-x-4 flex-grow">
            <div className="flex-grow">
              <h3 className="text-xl font-semibold text-gray-800 mb-1">{job.title}</h3>
              <p className="text-blue-600 font-medium mb-2">{job.company}</p>
              <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-3">
                <div className="flex items-center">
                  {job.location}
                </div>
                <div className="flex items-center">
                  {job.jobType}
                </div>
                <div className="flex items-center">
                  {job.salary}
                </div>
              </div>
              <p className="text-gray-600 mb-3 line-clamp-2">{job.description}</p>
            </div>
          </div>
        </div>
        {job.match ? <p className="text-sm text-blue-600 font-medium">Match: {job.match}%</p> : null}
        <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
          <div className="mt-4 flex gap-4 flex-col md:flex-row">
            <button
              onClick={handleApply}
              disabled={isApplied}
              className={`px-4 py-2 rounded ${isApplied ? "bg-gray-400 cursor-not-allowed" : "bg-green-500 hover:bg-green-600"} text-white`}
            >
              {isApplied ? "Applied" : "Quick Apply"}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}