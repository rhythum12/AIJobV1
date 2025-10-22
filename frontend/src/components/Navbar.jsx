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
        <nav className="bg-white shadow-md">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex items-center">
                        <button
                            onClick={() => navigate('/')}
                            className="font-bold text-xl text-blue-600 hover:text-blue-800 transition-colors"
                        >
                            Job Recommender
                        </button>
                    </div>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-8">
                        {isAuthenticated ? (
                            <>
                                {authNavItems.map((item) => (
                                    <button
                                        key={item.name}
                                        onClick={() => navigate(item.path)}
                                        className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                    >
                                        {item.name}
                                    </button>
                                ))}
                                <button
                                    onClick={handleLogout}
                                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                                >
                                    Sign Out
                                </button>
                            </>
                        ) : (
                            <>
                                {navItems.map((item) => (
                                    <button
                                        key={item.name}
                                        onClick={() => navigate(item.path)}
                                        className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                    >
                                        {item.name}
                                    </button>
                                ))}
                                <button
                                    onClick={() => navigate('/loginpage')}
                                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                                >
                                    Sign In
                                </button>
                                <button
                                    onClick={() => navigate('/registration')}
                                    className="bg-white text-blue-600 border border-blue-600 px-4 py-2 rounded-md hover:bg-blue-50 transition-colors"
                                >
                                    Sign Up
                                </button>
                            </>
                        )}
                    </div>

                    {/* Mobile menu button */}
                    <div className="md:hidden flex items-center">
                        <button
                            onClick={toggleMenu}
                            className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
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
                <div className="md:hidden">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t">
                        {isAuthenticated ? (
                            <>
                                {authNavItems.map((item) => (
                                    <button
                                        key={item.name}
                                        onClick={() => {
                                            navigate(item.path);
                                            setIsOpen(false);
                                        }}
                                        className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                                    >
                                        {item.name}
                                    </button>
                                ))}
                                <button
                                    onClick={() => {
                                        handleLogout();
                                        setIsOpen(false);
                                    }}
                                    className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-red-600 hover:bg-red-50"
                                >
                                    Sign Out
                                </button>
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
                                        className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                                    >
                                        {item.name}
                                    </button>
                                ))}
                                <button
                                    onClick={() => {
                                        navigate('/loginpage');
                                        setIsOpen(false);
                                    }}
                                    className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-blue-600 hover:bg-blue-50"
                                >
                                    Sign In
                                </button>
                                <button
                                    onClick={() => {
                                        navigate('/registration');
                                        setIsOpen(false);
                                    }}
                                    className="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-blue-600 hover:bg-blue-50"
                                >
                                    Sign Up
                                </button>
                            </>
                        )}
                    </div>
                </div>
            )}
        </nav>
    );
}
