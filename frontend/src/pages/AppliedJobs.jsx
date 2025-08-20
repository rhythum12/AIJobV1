import { useState } from 'react';
import Navbar from './../components/Navbar.jsx';
import Footer from './../components/Footer.jsx';
import { Bookmark, Send } from 'lucide-react';
import { NavLink } from 'react-router-dom';


export default function AppliedJobs() {
    const [filterStatus, setFilterStatus] = useState('all');
    const [appliedJobs, setAppliedJobs] = useState([{
        id: 1,
        title: "Frontend Developer",
        company: "TechCorp",
        location: "New York, NY",
        jobType: "Full-Time",
        industry: "Tech",
        match: 92,
        appliedDate: "2024-01-20",
        status: "interview"
    },
    {
        id: 2,
        title: "Full Stack Engineer",
        company: "CodeMasters",
        location: "Remote",
        jobType: "Part-Time",
        industry: "Tech",
        match: 85,
        appliedDate: "2024-01-18",
        status: "under_review"
    },
    {
        id: 3,
        title: "Finance Analyst",
        company: "MoneyWise",
        location: "New York, NY",
        jobType: "Full-Time",
        industry: "Finance",
        match: 78,
        appliedDate: "2024-01-15",
        status: "rejected"
    },
    {
        id: 4,
        title: "React Developer",
        company: "InnoSoft",
        location: "San Francisco, CA",
        jobType: "Internship",
        industry: "Tech",
        match: 88,
        appliedDate: "2024-01-12",
        status: "applied"
    },
    {
        id: 5,
        title: "Backend Developer",
        company: "DataFlow",
        location: "Austin, TX",
        jobType: "Full-Time",
        industry: "Tech",
        match: 91,
        appliedDate: "2024-01-10",
        status: "offered"
    }]);

    const getStatusColor = (status) => {
        switch (status) {
            case 'applied':
                return 'bg-blue-500 text-white';
            case 'under_review':
                return 'bg-yellow-500 text-white';
            case 'interview':
                return 'bg-green-500 text-white';
            case 'rejected':
                return 'bg-red-500 text-white';
            case 'offered':
                return 'bg-purple-500 text-white';
            default:
                return 'bg-gray-500 text-white';
        }
    };

    const getStatusText = (status) => {
        switch (status) {
            case 'applied':
                return 'Applied';
            case 'under_review':
                return 'Under Review';
            case 'interview':
                return 'Interview';
            case 'rejected':
                return 'Rejected';
            case 'offered':
                return 'Job Offered';
            default:
                return 'Unknown';
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    const handleRemoveApplication = (jobId) => {
        if (window.confirm('Are you sure you want to remove this application?')) {
            setAppliedJobs(prev => prev.filter(job => job.id !== jobId));
            alert('Application removed successfully!');
        }
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

                <div className="space-y-4">
                    {appliedJobs.length === 0 ? (
                        <div className="text-center py-12">

                            <h3 className="text-lg font-medium text-gray-600 mb-2">
                                No applications found
                            </h3>
                            <p className="text-gray-500">
                                {filterStatus === 'all'
                                    ? "You haven't applied to any jobs yet."
                                    : `No applications with "${getStatusText(filterStatus)}" status.`}
                            </p>
                        </div>
                    ) : (
                        appliedJobs.map(job => (
                            <div key={job.id} className="bg-white shadow-md rounded-lg p-4 mb-4 border px-10 hover:shadow-lg transition-shadow duration-200">
                                <div className="flex justify-between items-start mb-2">
                                    <div>
                                        <h3 className="text-xl font-semibold">{job.title}</h3>
                                        <p className="text-gray-600">{job.company} – {job.location}</p>
                                        <p className="text-sm text-blue-600 font-medium">Match: {job.match}%</p>
                                    </div>
                                    <span className={`px-3 py-1 rounded text-sm font-medium ${getStatusColor(job.status)}`}>
                                        {getStatusText(job.status)}
                                    </span>
                                </div>

                                <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                                    <div className="flex items-center">

                                        {job.jobType}
                                    </div>
                                    <div className="flex items-center">

                                        {job.industry}
                                    </div>
                                    <div className="flex items-center">

                                        Applied {formatDate(job.appliedDate)}
                                    </div>
                                </div>
                                <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
                                    <div className="flex gap-4 flex-col md:flex-row">
                                        <button className="px-4 py-2 rounded bg-gray-400 text-white cursor-not-allowed">
                                            Applied
                                        </button>
                                        <button
                                            onClick={() => handleRemoveApplication(job.id)}
                                            className="px-4 py-2 rounded bg-red-500 hover:bg-red-600 text-white flex items-center gap-2"
                                        >
                                            Remove
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
            <Footer />
        </div>
    );
}