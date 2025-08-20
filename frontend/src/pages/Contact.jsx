import React, { useState } from 'react';
import Navbar from './../components/Navbar.jsx';
import Footer from './../components/Footer.jsx';

export default function Contact() {

    const [form, setForm] = useState({ name: '', email: '', message: '' });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        alert('Message sent!');
        setForm({ name: '', email: '', message: '' });
    };

    return (
        <div className='min-h-screen bg-stone-100'>
            <Navbar isAuthenticated={true}/>
            <div className="max-w-2xl mx-auto px-4 py-10 mt-10 p-6 bg-white shadow-md rounded-xl">
                <h1 className="text-3xl font-bold mb-6 text-center">Contact Us</h1>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-lg font-medium text-gray-700">Name</label>
                        <input
                            type="text"
                            name="name"
                            value={form.name}
                            onChange={handleChange}
                            required
                            className="mt-3 w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
                        />
                    </div>
                    <div>
                        <label className="block text-lg font-medium text-gray-700">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={form.email}
                            onChange={handleChange}
                            required
                            className="mt-3 w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
                        />
                    </div>
                    <div>
                        <label className="block text-lg font-medium text-gray-700">Message</label>
                        <textarea
                            name="message"
                            rows="4"
                            value={form.message}
                            onChange={handleChange}
                            required
                            className="mt-3 w-full px-4 py-2 border rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-400"
                        ></textarea>
                    </div>
                    <button
                        type="submit"
                        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    >
                        Send Message
                    </button>
                </form>
            </div>
            <Footer />
        </div>
    );

}