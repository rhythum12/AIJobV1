import { NavLink } from 'react-router-dom'


export default function Footer() {
    return (
        <>
            <footer className="bg-neutral-700 text-white mt-10">
                <div className="max-w-6xl mx-auto px-4 py-8 flex flex-col md:flex-row justify-between items-center">
                    <div className="text-center md:text-left mb-4 md:mb-0">
                        <h1 className="text-lg font-semibold">Job Recommender</h1>
                        <p className="text-sm">Connecting you to your dream job.</p>
                    </div>
                    <div className="flex gap-6">
                        <NavLink className="text-xl hover:underline " to="/about">About</NavLink>
                        <NavLink className="text-xl hover:underline" to="/Contact">Contact</NavLink>
                    </div>
                </div>
                <div className="text-center text-sm text-gray-400 py-4 border-t border-white">
                    &copy; {new Date().getFullYear()} Job Recommender. All rights reserved.
                </div>
            </footer>

        </>
    )
}