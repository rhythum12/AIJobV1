import { useState } from "react";
import googleIcon from '../assets/Icons/google-icon.svg'
import linkedinIcon from '../assets/Icons/linkedin-icon.svg'
import loginUserImg from './../assets/Images/login_user.jpg';
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
    const navigate = useNavigate();
    const handleLogin = (e) => {
        e.preventDefault();
        navigate('/dashboard');
    };


    function registerpage() {
        navigate('/registration');
    }

    function passwordresetpage() {
        navigate('/passwordreset');
    }



    return (
        <div className="min-h-screen h-screen flex items-center justify-center bg-gray-100 py-4 px-4 box-border">
            <div className="max-w-full w-2/4 h-full rounded-xl max-h-full rounded-r-none hidden md:block">
                <img src={loginUserImg} alt="img" className="h-full rounded-xl rounded-r-none " />
            </div>
            <div className="max-w-md md:w-2/4 h-full bg-white py-6 px-14 md:py-6 rounded-xl md:rounded-l-none ">
                <h2 className="text-xl font-bold text-center text-gray-800">
                    Login to Your Account
                </h2>

                <form onSubmit={handleLogin} className="space-y-5">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Email
                        </label>
                        <input
                            type="email"
                            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Password
                        </label>
                        <input
                            type="password"
                            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
                    >
                        Login
                    </button>
                </form>

                <div className="text-center mt-3 text-sm">
                    <span onClick={passwordresetpage} className="text-blue-600 hover:underline cursor-pointer">Forget Password</span>
                </div>

                <div className="my-6 flex items-center justify-between">
                    <span className="border-b w-1/5 lg:w-1/4"></span>
                    <span className="text-xs text-gray-500 uppercase">or login with</span>
                    <span className="border-b w-1/5 lg:w-1/4"></span>
                </div>

                <div className="flex flex-col gap-3">
                    <button
                        className="flex items-center justify-center w-full bg-white border py-2 rounded-md hover:bg-gray-100"
                    >
                        <img src={googleIcon} alt="Google" className="w-5 h-5 mr-2" />
                        Continue with Google
                    </button>

                    <button
                        className="flex items-center justify-center w-full bg-white border py-2 rounded-md hover:bg-gray-100"
                    >
                        <img src={linkedinIcon} alt="LinkedIn" className="w-5 h-5 mr-2" />
                        Continue with LinkedIn
                    </button>
                </div>

                <p className="mt-4 text-center text-sm text-gray-600">
                    Don’t have an account?{" "}
                    <span onClick={registerpage} className="text-blue-600 hover:underline cursor-pointer">Register here</span>
                </p>
            </div>
        </div>
    );
}