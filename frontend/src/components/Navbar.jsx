
import { useNavigate } from "react-router-dom";
import { NavLink, Link } from 'react-router-dom';
import { useState, useRef, useEffect } from "react";
import { useUser } from './../context/UserContext.js';

export default function Navbar({ isAuthenticated = false }) {
    const { user, updateUser } = useUser();
    const [isOpen, setIsOpen] = useState(false);
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    const navigate = useNavigate();
    
    const handleLogout = () => {
        updateUser({ name: "", email: "", skills: [], interests: [], resume: null });
        navigate("/");
        setIsDropdownOpen(false);
    };


    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsDropdownOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const navLinkClass = ({ isActive }) => {
        return `px-4 py-2 font-medium transition-all duration-200 hover:text-blue-600 relative  hover:bg-stone-100 transition-colors duration-200 rounded-md
      ${isActive
                ? 'text-blue-600 after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-blue-600'
                : 'text-gray-700'}`;
    }

    function toggleMenu() {
        setIsOpen(!isOpen);
    }

    function toggleDropdown() {
        setIsDropdownOpen(!isDropdownOpen);
    }

    return (
        <nav className="bg-white shadow-md px-6 py-4">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="w-full flex items-center justify-between">
                        <Link to="/" className="font-bold text-xl text-blue-600">Job Recommender</Link>
                        
                        
                        <div className="hidden md:block">
                            {isAuthenticated ? (
                                <div className="flex items-center gap-4">
                                    <NavLink className={navLinkClass} to="/dashboard">Resume</NavLink>
                                    <NavLink className={navLinkClass} to="/jobs">Jobs</NavLink>
                                    <NavLink className={navLinkClass} to="/resumeanalysis">Resume Analysis</NavLink>
                                    
                                    <div className="relative" ref={dropdownRef}>
                                        <button
                                            onClick={toggleDropdown}
                                            className="flex items-center space-x-2 px-3 py-2 rounded-md hover:bg-stone-100 transition-colors duration-200"
                                        >
                                            
                                            <span className="font-medium text-gray-700">{user?.name || 'User'}</span>
                                            <svg
                                                className={`w-4 h-4 text-gray-500 transition-transform duration-200 ${isDropdownOpen ? 'rotate-180' : ''}`}
                                                fill="none"
                                                stroke="currentColor"
                                                viewBox="0 0 24 24"
                                            >
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                            </svg>
                                        </button>

                                        {isDropdownOpen && (
                                            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-50">
                                                <Link
                                                    to="/savedjobs"
                                                    className="block px-4 py-2 font-medium  text-gray-700 hover:bg-stone-100 transition-colors duration-200"
                                                    onClick={() => setIsDropdownOpen(false)}
                                                >
                                                    <div className="flex items-center space-x-2">
                                                        <span>Saved Jobs</span>
                                                    </div>
                                                </Link>
                                                <Link
                                                    to="/appliedjobs"
                                                    className="block px-4 py-2 font-medium text-gray-700 hover:bg-stone-100 transition-colors duration-200"
                                                    onClick={() => setIsDropdownOpen(false)}
                                                >
                                                    <div className="flex items-center space-x-2">
                                                    
                                                        <span>Applied Jobs</span>
                                                    </div>
                                                </Link>
                                                <Link
                                                    to="/profile"
                                                    className="block px-4 py-2 font-medium  text-gray-700 hover:bg-stone-100 transition-colors duration-200"
                                                    onClick={() => setIsDropdownOpen(false)}
                                                >
                                                    <div className="flex items-center space-x-2">
                                                        
                                                        <span>Profile</span>
                                                    </div>
                                                </Link>
                                                <hr className="my-1" />
                                                <button
                                                    onClick={handleLogout}
                                                    className="block w-full text-left px-4 py-2 font-medium  text-red-600 hover:bg-red-50 transition-colors duration-200"
                                                >
                                                    <div className="flex items-center space-x-2">
                                                        
                                                        <span>Sign Out</span>
                                                    </div>
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ) : (
                                <div className="flex flex-col sm:flex-row gap-4 mt-2 sm:mt-0">
                                    <NavLink className={navLinkClass} to="/">Browse Jobs</NavLink>
                                    <NavLink className={navLinkClass} to="/aboutpageguest">About Us</NavLink>
                                    <NavLink className={navLinkClass} to="/loginpage">Sign In</NavLink>
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="flex items-center md:hidden">
                        <button
                            onClick={toggleMenu}
                            className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
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
            {isOpen && (
                <div className="md:hidden">
                    
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        {isAuthenticated ? (
                            <>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/dashboard">Resume</NavLink>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/jobs">Jobs</NavLink>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/resumeanalysis">Resume Analysis</NavLink>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/savedjobs">Saved Jobs</NavLink>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/appliedjobs">Applied Jobs</NavLink>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/profile">Profile</NavLink>
                                <button onClick={handleLogout} className="hover:text-red-500 bg-stone-100 px-4 w-full text-left py-2 font-medium transition-all duration-200 relative text-red-500">Sign Out</button>
                            </>
                        ) : (
                            <>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/">Browse Jobs</NavLink>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/aboutpageguest">About Us</NavLink>
                                <NavLink className="block px-3 py-2 rounded-md text-base font-medium text-blue-600 bg-stone-100" to="/">Sign In</NavLink>
                            </>
                        )}
                    </div>
                </div>
            )}
        </nav>
    );
}