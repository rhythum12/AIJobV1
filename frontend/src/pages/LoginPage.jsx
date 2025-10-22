import { useState } from "react";
import googleIcon from '../assets/Icons/google-icon.svg'
import linkedinIcon from '../assets/Icons/linkedin-icon.svg'
import loginUserImg from './../assets/Images/login_user.jpg';
import { useNavigate } from "react-router-dom";
import { signInWithEmailAndPassword, signInWithPopup } from 'firebase/auth';
import { auth, googleProvider } from '../Firebase/firebase.js';
import { useUser } from '../context/UserContext.js';
import { toast } from 'react-toastify';

export default function LoginPage() {
    const navigate = useNavigate();
    const { user } = useUser();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await signInWithEmailAndPassword(auth, email, password);
            toast.success('Login successful! Welcome back!');
            navigate('/dashboard');
        } catch (error) {
            setError(error.message);
            toast.error('Login failed. Please check your credentials.');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = async () => {
        setLoading(true);
        setError('');

        try {
            await signInWithPopup(auth, googleProvider);
            toast.success('Google login successful! Welcome!');
            navigate('/dashboard');
        } catch (error) {
            setError(error.message);
            toast.error('Google login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };


    function registerpage() {
        navigate('/registration');
    }

    function passwordresetpage() {
        navigate('/passwordreset');
    }

    function goHome() {
        navigate('/');
    }



    return (
        <div className="min-h-screen h-screen flex items-center justify-center bg-gray-100 py-4 px-4 box-border">
            <div className="max-w-full w-2/4 h-full rounded-xl max-h-full rounded-r-none hidden md:block">
                <img src={loginUserImg} alt="img" className="h-full rounded-xl rounded-r-none " />
            </div>
            <div className="max-w-md md:w-2/4 h-full bg-white py-6 px-14 md:py-6 rounded-xl md:rounded-l-none ">
                <div className="flex items-center mb-4">
                    <button
                        onClick={goHome}
                        className="flex items-center text-gray-600 hover:text-gray-800 transition-colors"
                    >
                        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Back to Home
                    </button>
                </div>
                <h2 className="text-xl font-bold text-center text-gray-800">
                    Login to Your Account
                </h2>

                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin} className="space-y-5">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Email
                        </label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
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
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
                    >
                        {loading ? 'Signing In...' : 'Login'}
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
                        onClick={handleGoogleLogin}
                        disabled={loading}
                        className="flex items-center justify-center w-full bg-white border py-2 rounded-md hover:bg-gray-100 disabled:opacity-50"
                    >
                        <img src={googleIcon} alt="Google" className="w-5 h-5 mr-2" />
                        Continue with Google
                    </button>

                    <button
                        disabled={loading}
                        className="flex items-center justify-center w-full bg-white border py-2 rounded-md hover:bg-gray-100 disabled:opacity-50"
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