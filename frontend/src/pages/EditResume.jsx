import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from './../components/Navbar.jsx';
import Footer from './../components/Footer.jsx';


export default function EditResume() {
  const navigate = useNavigate();

  const [resumeData, setResumeData] = useState({
    skills: "Python, Machine Learning, NLP",
    experience: "3 Years at XYZ Corp",
    education: "BSc Computer Science",
  });

  const handleChange = (e) => {
    setResumeData({
      ...resumeData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSave = () => {
    alert("Resume updated successfully!");
    navigate("/resumeanalysis");
  };

  return (
    <div className="min-h-screen bg-stone-100">
      <Navbar isAuthenticated={true}/>
      <div className="max-w-2xl mx-auto mt-10 p-6 bg-white shadow-md rounded-md">
        <h2 className="text-2xl font-bold mb-6">Edit Resume</h2>

        <div className="mb-4">
          <label className="block font-semibold mb-1">Skills</label>
          <input
            type="text"
            name="skills"
            value={resumeData.skills}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="e.g., Python, React, SQL"
          />
        </div>

        <div className="mb-4">
          <label className="block font-semibold mb-1">Experience</label>
          <input
            type="text"
            name="experience"
            value={resumeData.experience}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="e.g., 3 Years at XYZ"
          />
        </div>

        <div className="mb-4">
          <label className="block font-semibold mb-1">Education</label>
          <input
            type="text"
            name="education"
            value={resumeData.education}
            onChange={handleChange}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="e.g., BSc Computer Science"
          />
        </div>

        <button
          onClick={handleSave}
          className="mt-4 px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Save
        </button>
      </div>
      <Footer />
    </div>
  );
}
