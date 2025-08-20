import React, { useState } from "react";
import { useUser } from './../context/UserContext.js';
import { useNavigate } from "react-router-dom";
import Navbar from './../components/Navbar.jsx';
import Footer from './../components/Footer.jsx';
import ResumeUpload from './../components/ResumeUpload.jsx';


export default function DashboardPage() { 
    const { user, updateUser } = useUser();


    return (
        <div className="min-h-screen bg-stone-100">
            <Navbar isAuthenticated={true}/>
            <h2 className="text-3xl font-semibold m-6">Welcome, {user.name}</h2>
            <div className="max-w-3xl mx-auto mt-10 bg-white p-8 rounded-lg shadow">
            <ResumeUpload />
            </div>
            <Footer/>
        </div>
    );
 } 


