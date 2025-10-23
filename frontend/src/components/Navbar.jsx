import { useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import { useUser } from '../context/UserContext.js';
import { toast } from 'react-toastify';

export default function Navbar({ isAuthenticated = false }) {
    const [isOpen, setIsOpen] = useState(false);
    const navigate = useNavigate();
    const { logout } = useUser();

    const handleLogout = async () => {
        await logout();
        toast.success('Logged out successfully! See you soon!');
        navigate('/');
    };

    function toggleMenu() {
        setIsOpen(!isOpen);
    }

    const navItems = [
        { name: 'Home', path: '/' },
        { name: 'Browse Jobs', path: '/jobs' },
        { name: 'About Us', path: '/aboutpageguest' },
        { name: 'Contact', path: '/contact' },
    ];

    const authNavItems = [
        { name: 'Dashboard', path: '/dashboard' },
        { name: 'Jobs', path: '/jobs' },
        { name: 'Resume Analysis', path: '/resumeanalysis' },
        { name: 'Edit Resume', path: '/editresume' },
        { name: 'Saved Jobs', path: '/savedjobs' },
        { name: 'Applied Jobs', path: '/appliedjobs' },
        { name: 'Profile', path: '/profile' },
        { name: 'About Us', path: '/about' },
        { name: 'Contact', path: '/contact' },
    ];

    return (
        <nav className="bg-white shadow-lg border-b border-gray-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <div className="flex items-center">
                        <button
                            onClick={() => navigate('/')}
                            className="font-bold text-xl text-blue-600 hover:text-blue-800 transition-all duration-200 hover:scale-105"
                        >
                            Job Recommender
                        </button>
                    </div>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-1">
                        {isAuthenticated ? (
                            <>
                                {authNavItems.map((item) => (
                                    <button
                                        key={item.name}
                                        onClick={() => navigate(item.path)}
                                        className="relative text-gray-700 hover:text-blue-600 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-blue-50 hover:shadow-sm group"
                                    >
                                        <span className="relative z-10">{item.name}</span>
                                        <span className="absolute inset-0 bg-blue-100 rounded-lg scale-0 group-hover:scale-100 transition-transform duration-200 opacity-0 group-hover:opacity-100"></span>
                                    </button>
                                ))}
                                <div className="ml-4 pl-4 border-l border-gray-200">
                                    <button
                                        onClick={handleLogout}
                                        className="bg-blue-600 text-white px-6 py-2.5 rounded-lg hover:bg-blue-700 hover:shadow-md transition-all duration-200 font-medium text-sm hover:scale-105"
                                    >
                                        Sign Out
                                    </button>
                                </div>
                            </>
                        ) : (
                            <>
                                {navItems.map((item) => (
                                    <button
                                        key={item.name}
                                        onClick={() => navigate(item.path)}
                                        className="relative text-gray-700 hover:text-blue-600 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 hover:bg-blue-50 hover:shadow-sm group"
                                    >
                                        <span className="relative z-10">{item.name}</span>
                                        <span className="absolute inset-0 bg-blue-100 rounded-lg scale-0 group-hover:scale-100 transition-transform duration-200 opacity-0 group-hover:opacity-100"></span>
                                    </button>
                                ))}
                                <div className="ml-4 pl-4 border-l border-gray-200 flex space-x-3">
                                    <button
                                        onClick={() => navigate('/loginpage')}
                                        className="bg-blue-600 text-white px-6 py-2.5 rounded-lg hover:bg-blue-700 hover:shadow-md transition-all duration-200 font-medium text-sm hover:scale-105"
                                    >
                                        Sign In
                                    </button>
                                    <button
                                        onClick={() => navigate('/registration')}
                                        className="bg-white text-blue-600 border-2 border-blue-600 px-6 py-2.5 rounded-lg hover:bg-blue-50 hover:border-blue-700 hover:shadow-md transition-all duration-200 font-medium text-sm hover:scale-105"
                                    >
                                        Sign Up
                                    </button>
                                </div>
                            </>
                        )}
                    </div>

                    {/* Mobile menu button */}
                    <div className="md:hidden flex items-center">
                        <button
                            onClick={toggleMenu}
                            className="inline-flex items-center justify-center p-3 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 transition-all duration-200"
                        >
                            <svg
                                className="h-6 w-6"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    d="M4 6h16M4 12h16M4 18h16"
                                />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Navigation */}
            {isOpen && (
                <div className="md:hidden bg-white border-t border-gray-200 shadow-lg">
                    <div className="px-4 pt-4 pb-6 space-y-2">
                        {isAuthenticated ? (
                            <>
                                {authNavItems.map((item) => (
                                    <button
                                        key={item.name}
                                        onClick={() => {
                                            navigate(item.path);
                                            setIsOpen(false);
                                        }}
                                        className="block w-full text-left px-4 py-3 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 hover:shadow-sm"
                                    >
                                        {item.name}
                                    </button>
                                ))}
                                <div className="pt-4 border-t border-gray-200 mt-4">
                                    <button
                                        onClick={() => {
                                            handleLogout();
                                            setIsOpen(false);
                                        }}
                                        className="block w-full text-left px-4 py-3 rounded-lg text-base font-medium text-red-600 hover:bg-red-50 transition-all duration-200 hover:shadow-sm"
                                    >
                                        Sign Out
                                    </button>
                                </div>
                            </>
                        ) : (
                            <>
                                {navItems.map((item) => (
                                    <button
                                        key={item.name}
                                        onClick={() => {
                                            navigate(item.path);
                                            setIsOpen(false);
                                        }}
                                        className="block w-full text-left px-4 py-3 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 hover:shadow-sm"
                                    >
                                        {item.name}
                                    </button>
                                ))}
                                <div className="pt-4 border-t border-gray-200 mt-4 space-y-2">
                                    <button
                                        onClick={() => {
                                            navigate('/loginpage');
                                            setIsOpen(false);
                                        }}
                                        className="block w-full text-left px-4 py-3 rounded-lg text-base font-medium text-blue-600 hover:bg-blue-50 transition-all duration-200 hover:shadow-sm"
                                    >
                                        Sign In
                                    </button>
                                    <button
                                        onClick={() => {
                                            navigate('/registration');
                                            setIsOpen(false);
                                        }}
                                        className="block w-full text-left px-4 py-3 rounded-lg text-base font-medium text-blue-600 hover:bg-blue-50 transition-all duration-200 hover:shadow-sm"
                                    >
                                        Sign Up
                                    </button>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            )}
        </nav>
    );
}
