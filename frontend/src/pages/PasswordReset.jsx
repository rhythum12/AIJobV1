import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import forgetPasswordImg from './../assets/Images/forget_password.jpg';

export default function PasswordResetPage() {
    const [email, setEmail] = useState("");

    const handlePasswordReset = (e) => {
        e.preventDefault();

        if (!email) {
            alert("Please enter your email.");
            return;
        }
        alert("Link sent to email!")
        setEmail(" ");
    };


    const navigate = useNavigate();

    function loginPagenavigator() {
        navigate('/loginpage');
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
            <div className="max-w-sm w-2/4 bg-white p-8 rounded-xl rounded-r-none my-8 mr-6 hidden md:block">
                <img src={forgetPasswordImg} alt="img" />
            </div>
            <div className="max-w-md w-2/4 bg-white px-10 py-6 rounded-xl rounded-l-none my-12">
                <h2 className="text-2xl font-bold text-center text-gray-800 mb-12">
                    Reset Your Password
                </h2>

                <form onSubmit={handlePasswordReset} className="space-y-8">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Email Address
                        </label>
                        <input
                            type="email"
                            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
                    >
                        Send Reset Link
                    </button>
                </form>

                <p className="mt-24 text-center text-sm text-gray-600">
                    Back to{" "}
                    <span onClick={loginPagenavigator} className="text-blue-600 hover:underline cursor-pointer">Login Page</span>
                </p>
            </div>
        </div>
    );
}
