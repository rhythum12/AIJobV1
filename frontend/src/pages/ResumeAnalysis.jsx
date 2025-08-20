import React, { useState } from "react";
import Navbar from './../components/Navbar.jsx';
import { useUser } from './../context/UserContext.js';
import { useNavigate } from "react-router-dom";
import Footer from './../components/Footer.jsx';

export default function ResumeAnalysis() {

    const { user, updateUser } = useUser();


    const navigate = useNavigate();
    const handleEdit = () => {
        navigate('/editresume');
    };

    return (
        <div className=" bg-stone-100 mx-auto min-h-screen">
            <Navbar isAuthenticated={true}/>
            <div className="h-screen">
                <div className="max-w-2xl mx-auto mt-8 p-6 bg-white shadow-lg rounded-lg">
                    <h2 className="text-2xl font-bold mb-4 text-center">Resume Summary</h2>
                    <div className="space-y-4">
                        <div>
                            <strong>Skills:</strong>
                            <p className="text-gray-700 mx-4 my-2">{user.skills.join(", ")}</p>
                        </div>
                        <div>
                            <strong>Experience:</strong>
                            <p className="text-gray-700 mx-4 my-2">{user.experience}</p>
                        </div>
                        <div>
                            <strong>Education:</strong>
                            <p className="text-gray-700 mx-4 my-2">{user.education}</p>
                        </div>
                        <button
                            onClick={handleEdit}
                            className="mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded"
                        >
                            Edit
                        </button>
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    );
}
