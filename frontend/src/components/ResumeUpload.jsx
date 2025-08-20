import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useUser } from './../context/UserContext.js';

export default function ResumeUpload() {

    const { user, updateUser } = useUser();
    const [resume, setResume] = useState(null);
    const [message, setMessage] = useState("");

    const handleResumeUpload = (e) => {
        const file = e.target.files[0];
        if (file && file.type === "application/pdf") {
            setResume(file);
            setMessage("Resume uploaded successfully!");
        } else {
            setMessage("Please upload a PDF file.");
        }
    };

    const navigate = useNavigate();
    function showReport() {
        navigate('/resumeanalysis');
    }
    return (
        <>
            <div className="mb-6">
                <label className="block font-medium mb-2">Upload Resume (PDF)</label>
                <input
                    type="file"
                    accept=".pdf"
                    onChange={handleResumeUpload}
                    className="block w-38 text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer"
                />
                {message && <p className="mt-2 text-sm text-green-600">{message}</p>}
            </div>

            <div className="mb-6">
                <label className="block font-medium mb-2">Edit Skills / Preferences</label>
                <textarea
                    className="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
                    rows="4"
                    defaultValue={user.skills.join(", ") + ", " + user.interests.join(", ")}
                />
            </div>


            <div>
                <label className="block font-medium mb-2">View Resume Parsing Report</label>
                <button onClick={showReport} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                    Show Report
                </button>
            </div>

        </>
    )
}