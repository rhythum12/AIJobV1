import { useState, useEffect } from 'react';
import Navbar from './../components/Navbar.jsx';
import { NavLink, useNavigate } from 'react-router-dom';
import { Bookmark, Send } from 'lucide-react';
import Footer from './../components/Footer.jsx';
export default function SavedJobs() {
    const [appliedJobs, setAppliedJobs] = useState(new Set());
    const [savedJobs, setSavedJobs] = useState([
        {
            id: 1,
            title: "Frontend Developer",
            company: "TechCorp",
            location: "New York, NY",
            jobType: "Full-Time",
            industry: "Tech",
            match: 92,
            salary: "$120,000 - $150,000",
            dateSaved: "2024-01-15",
            description: "We are looking for a Senior Frontend Developer to join our team..."
        },
        {
            id: 2,
            title: "Full Stack Engineer",
            company: "CodeMasters",
            location: "New York",
            jobType: "Part-Time",
            industry: "Tech",
            match: 85,
            salary: "$80,000 - $100,000",
            dateSaved: "2024-01-10",
            description: "Join our creative team as a UX/UI Designer..."
        },
        {
            id: 3,
            title: "Data Scientist",
            company: "Analytics Pro",
            location: "Remote",
            type: "Full-time",
            salary: "$130,000 - $160,000",
            dateSaved: "2024-01-08",
            description: "We're seeking a Data Scientist to help drive insights..."
        }
    ]);

    const removeSavedJob = (jobId) => {
        if (window.confirm('Are you sure you want to remove this application?')) {
            setSavedJobs(savedJobs.filter(job => job.id !== jobId));
            alert('Application removed successfully!');
        }
    };
    const applySavedJob = (jobId) => {
        if (window.confirm('Are you sure you want to apply on this application?')) {
            setAppliedJobs((prev) => new Set(prev).add(jobId));
            alert('Application applied successfully!');
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };


    const navLinkClass = ({ isActive }) => {
        return `px-4 py-2 font-medium transition-all duration-200 hover:text-gray-600 relative  
      ${isActive
                ? 'text-blue-600 after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-blue-600'
                : 'text-gray-500'}`;
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar isAuthenticated={true} />

            <div className="container mx-auto px-4 py-8">
                <div className="text-3xl font-bold text-gray-800 my-3">Activity</div>
                <div className='my-6'>
                    <nav className="flex space-x-8 px-6">
                        <NavLink
                            className={navLinkClass}
                            to='/savedjobs'
                        >
                            <div className="flex items-center">
                                <Bookmark className="w-4 h-4 mr-2" />
                                <span>Saved</span>
                            </div>
                        </NavLink>
                        <NavLink
                            className={navLinkClass}
                            to='/appliedjobs'
                        >
                            <div className="flex items-center">
                                <Send className="w-4 h-4 mr-2" />
                                <span>Applied</span>
                            </div>
                        </NavLink>
                    </nav>
                </div>


                {savedJobs.length === 0 ? (
                    <div className="text-center py-16">
                        <h3 className="text-lg font-medium text-gray-900 mb-2">No saved jobs yet</h3>
                        <p className="text-gray-600 mb-6">
                            Start saving jobs you're interested in to keep track of them here.
                        </p>
                        <NavLink
                            to="/jobs"
                            className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors duration-200"
                        >
                            Browse Jobs
                        </NavLink>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {savedJobs.map((job) => {
                            const isApplied = appliedJobs.has(job.id);
                            return (
                                <div key={job.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
                                    <div className="flex justify-between items-start">
                                        <div className="flex items-start space-x-4 flex-grow">
                                            <div className="flex-grow">
                                                <h3 className="text-xl font-semibold text-gray-800 mb-1">{job.title}</h3>
                                                <p className="text-blue-600 font-medium mb-2">{job.company}</p>
                                                <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-3">
                                                    <div className="flex items-center">
                                                        {job.location}
                                                    </div>
                                                    <div className="flex items-center">
                                                        {job.type}
                                                    </div>
                                                    <div className="flex items-center">
                                                        {job.salary}
                                                    </div>
                                                </div>
                                                <p className="text-gray-600 mb-3 line-clamp-2">{job.description}</p>
                                                <p className="text-sm text-gray-500">Saved on {formatDate(job.dateSaved)}</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
                                        <div className="flex space-x-3">
                                            <button
                                                onClick={() => applySavedJob(job.id)}
                                                disabled={isApplied}
                                                className={`px-4 py-2 rounded ${isApplied ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"} text-white`}
                                            >
                                                Apply Now
                                            </button>
                                            <button
                                                onClick={() => removeSavedJob(job.id)}
                                                className="hover:bg-red-600 bg-red-500 text-white px-4 py-2 rounded-md  transition-colors duration-200"
                                                title="Remove from saved jobs"
                                            >
                                                Remove
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            );
                        }
                        )}
                    </div>
                )}
            </div>
            <Footer />
        </div >
    );
}