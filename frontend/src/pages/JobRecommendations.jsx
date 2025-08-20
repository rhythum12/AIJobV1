import React, { useState } from "react";
import JobCard from './../components/Jobcard.jsx';
import Navbar from './../components/Navbar.jsx';
import Footer from './../components/Footer.jsx';
const mockJobs = [
  {
    id: 1,
    title: "Frontend Developer",
    company: "TechCorp",
    location: "New York, NY",
    jobType: "Full-Time",
    industry: "Tech",
    match: 92,
    salary: "$90,000",
    description: "Join our dynamic team to build intuitive user interfaces for web apps..."
  },
  {
    id: 2,
    title: "Full Stack Engineer",
    company: "CodeMasters",
    location: "New York",
    jobType: "Part-Time",
    industry: "Tech",
    match: 85,
    salary: "$75,000",
    description: "Work across frontend and backend to deliver full-featured applications..."
  },
  {
    id: 3,
    title: "Finance Analyst",
    company: "MoneyWise",
    location: "New York, NY",
    jobType: "Full-Time",
    industry: "Finance",
    match: 78,
    salary: "$80,000",
    description: "Analyze financial data to guide business decisions and investments..."
  },
  {
    id: 4,
    title: "React Developer",
    company: "InnoSoft",
    location: "San Francisco, CA",
    jobType: "Internship",
    industry: "Tech",
    match: 88,
    salary: "$30,000",
    description: "Build modern React-based components in a fast-paced development team..."
  },
];


export default function JobRecommendationsPage() {
  const [filters, setFilters] = useState({
    location: "",
    jobType: "",
    industry: "",
  });

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const filteredJobs = mockJobs.filter((job) => {
    return (
      (filters.location === "" || job.location === filters.location) &&
      (filters.jobType === "" || job.jobType === filters.jobType) &&
      (filters.industry === "" || job.industry === filters.industry)
    );
  });

  return (
    <>
      <div className="min-h-screen bg-stone-100">
        <Navbar isAuthenticated={true} />
        <div className="min-h-screen max-h-max">
          <h2 className="text-2xl font-bold mb-4 p-4">Job Recommendation Results</h2>
          <div className="flex gap-4 mb-6 flex-wrap px-10 justify-center">
            <select
              name="location"
              value={filters.location}
              onChange={handleFilterChange}
              className="p-2 border rounded-md"
            >
              <option value="" disabled>Location</option>
              <option value="New York, NY">New York, NY</option>
              <option value="Remote">Remote</option>
              <option value="San Francisco, CA">San Francisco, CA</option>
            </select>

            <select
              name="jobType"
              value={filters.jobType}
              onChange={handleFilterChange}
              className="p-2 border rounded-md"
            >
              <option value="" disabled>Job Type</option>
              <option value="Full-Time">Full-Time</option>
              <option value="Part-Time">Part-Time</option>
              <option value="Internship">Internship</option>
            </select>

            <select
              name="industry"
              value={filters.industry}
              onChange={handleFilterChange}
              className="p-2 border rounded-md"
            >
              <option value="" disabled>Industry</option>
              <option value="Tech">Tech</option>
              <option value="Finance">Finance</option>
              <option value="Education">Education</option>
            </select>
          </div>
          <div className="w-full flex justify-center">
            <div className="px-12 md:w-3/4 flex justify-center flex-col">
              {filteredJobs.length > 0 ? (
                filteredJobs.map((job) => <JobCard key={job.id} job={job} isAuthenticated={true}/>)
              ) : (
                <div className="mt-12">
                  <p className="text-gray-600 text-xl text-center">No jobs match your filters.Try adjusting the filters</p>
                </div>
              )}
            </div>
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}
