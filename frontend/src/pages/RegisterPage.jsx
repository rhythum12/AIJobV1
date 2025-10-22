import React, { useState } from "react";
import googleIcon from '../assets/Icons/google-icon.svg'
import linkedinIcon from '../assets/Icons/linkedin-icon.svg'
import { useNavigate } from "react-router-dom";
import registerUserImg from './../assets/Images/register_user.jpg';
import { createUserWithEmailAndPassword, signInWithPopup } from 'firebase/auth';
import { auth, googleProvider } from '../Firebase/firebase.js';
import { toast } from 'react-toastify';
export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      toast.error("Passwords do not match");
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      toast.error("Password must be at least 6 characters");
      setLoading(false);
      return;
    }

    try {
      await createUserWithEmailAndPassword(auth, email, password);
      toast.success('Account created successfully! Please login to continue.');
      navigate('/loginpage');
    } catch (error) {
      setError(error.message);
      toast.error('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleRegister = async () => {
    setLoading(true);
    setError("");

    try {
      await signInWithPopup(auth, googleProvider);
      toast.success('Google account linked successfully! Welcome to Job Recommender!');
      navigate('/dashboard');
    } catch (error) {
      setError(error.message);
      toast.error('Google registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  function loginPage(){
    navigate('/loginpage');
  }

  return (
    <div className="min-h-screen h-screen flex items-center justify-center bg-gray-100 py-4 px-4 box-border">
      <div className="max-w-full w-2/4 h-full rounded-xl max-h-full rounded-r-none hidden md:block">
        <img src={registerUserImg} alt="img" className="h-full rounded-xl rounded-r-none " />
      </div>
      <div className="max-w-md md:w-2/4 h-full bg-white py-6 px-14 md:py-6 rounded-xl md:rounded-l-none ">
        <h2 className="text-xl font-bold text-center text-gray-800 mb-2">
          Create Your Account
        </h2>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Confirm Password
            </label>
            <input
              type="password"
              className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition disabled:opacity-50"
          >
            {loading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <div className="my-6 flex items-center justify-between">
          <span className="border-b w-1/5 lg:w-1/4"></span>
          <span className="text-xs text-gray-500 uppercase">or sign up with</span>
          <span className="border-b w-1/5 lg:w-1/4"></span>
        </div>

        <div className="flex flex-col gap-3">
          <button
            onClick={handleGoogleRegister}
            disabled={loading}
            className="flex items-center justify-center w-full bg-white border py-2 rounded-md hover:bg-gray-100 disabled:opacity-50"
          >
            <img src={googleIcon} alt="Google" className="w-5 h-5 mr-2" />
            Sign up with Google
          </button>

          <button
            disabled={loading}
            className="flex items-center justify-center w-full bg-white border py-2 rounded-md hover:bg-gray-100 disabled:opacity-50"
          >
            <img src={linkedinIcon} alt="LinkedIn" className="w-5 h-5 mr-2" />
            Sign up with LinkedIn
          </button>
        </div>

        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{" "}
          <span onClick={loginPage} className="text-blue-600 hover:underline cursor-pointer">Login here</span>
        </p>
      </div>
    </div>
  );
}
