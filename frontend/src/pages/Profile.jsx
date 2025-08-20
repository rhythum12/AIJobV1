
import React, { useState, useEffect, useRef } from 'react';
import { useUser } from './../context/UserContext.js';
import Navbar from './../components/Navbar.jsx';
import Footer from './../components/Footer.jsx';

export default function Profile() {
    const { user, updateUser } = useUser();
    const [isEditing, setIsEditing] = useState(false);
    const formRef = useRef(null);
    const [formData, setFormData] = useState({
        firstName: user.name?.split(' ')[0] || '',
        lastName: user.name?.split(' ').slice(1).join(' ') || '',
        address: user.address || '',
        phone: user.phone || '',
        location: user.location || ''
    });

    const analytics = {
        profileViews: 47,
        jobsApplied: 12,
        interviews: 5,
        offers: 2,
        matchRate: 78
    };


    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSave = () => {
        const updatedUser = {
            ...user,
            name: `${formData.firstName} ${formData.lastName}`.trim(),
            address: formData.address,
            phone: formData.phone,
            location: formData.location
        };

        updateUser(updatedUser);
        setIsEditing(false);
    };

    const handleCancel = () => {
        if (window.confirm('Do you want to discard changes?')) {
            setFormData({
                firstName: user.name?.split(' ')[0] || '',
                lastName: user.name?.split(' ').slice(1).join(' ') || '',
                address: user.address || '',
                phone: user.phone || '',
                location: user.location || ''
            });
            setIsEditing(false);
        }
    };

    useEffect(() => {
        if (isEditing && formRef.current) {
            setTimeout(() => {
                formRef.current.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start',
                    inline: 'nearest'
                });
            }, 100);
        }
    }, [isEditing]);

    return (
        <div className="min-h-screen bg-gray-50">
            <Navbar isAuthenticated={true} />

            <div className="max-w-6xl mx-auto px-4 py-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-1">
                        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
                            <div className="text-center mb-6">
                                <img
                                    src={user.avatar}
                                    alt="Profile Pic"
                                    className="w-24 h-24 rounded-full mx-auto mb-4 border-4 border-blue-100"
                                />
                                <h2 className="text-xl font-bold text-gray-900">{user.name}</h2>
                                <p className="text-gray-600 mb-2">{user.title}</p>
                                <div className="flex items-center justify-center text-sm text-gray-500 mb-2">
                                    {user.location}
                                </div>
                                {user.email && (
                                    <div className="text-sm text-gray-500 mb-2">
                                        {user.email}
                                    </div>
                                )}

                                <button
                                    onClick={() => setIsEditing(!isEditing)}
                                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                                >
                                    {isEditing ? 'Cancel Edit' : 'Edit Profile'}
                                </button>
                            </div>

                            <div className="space-y-4">
                                <div className="flex items-center text-sm">
                                    <span className="text-gray-600">Experience: {user.experience}</span>
                                </div>
                                <div className="flex items-center text-sm">
                                    <span className="text-gray-600">Salary: {user.preferences.salary}</span>
                                </div>
                                <div className="flex items-center text-sm">
                                    <span className="text-gray-600">Type: {user.preferences.jobType}</span>
                                </div>
                            </div>
                        </div>

                        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Skills</h3>
                            <div className="flex flex-wrap gap-2">
                                {user.skills.map((skill, index) => (
                                    <span
                                        key={index}
                                        className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>

                        <div className="bg-white rounded-xl shadow-sm p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile Analytics</h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600">Profile Views</span>
                                    <span className="font-semibold text-gray-900">{analytics.profileViews}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600">Jobs Applied</span>
                                    <span className="font-semibold text-gray-900">{analytics.jobsApplied}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600">Interviews</span>
                                    <span className="font-semibold text-gray-900">{analytics.interviews}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600">Offers</span>
                                    <span className="font-semibold text-green-600">{analytics.offers}</span>
                                </div>
                                <div className="flex justify-between items-center pt-2 border-t">
                                    <span className="text-gray-600">Match Rate</span>
                                    <span className="font-semibold text-blue-600">{analytics.matchRate}%</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="lg:col-span-2">
                        <div className="bg-white rounded-xl shadow-sm mb-6">
                            <div className="border-b p-4 text-center text-xl font-medium text-blue-500">
                                Overview
                            </div>
                            <div className="p-6">
                                <div className="space-y-6">
                                    <div>
                                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Job Preferences</h3>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div className="p-4 bg-gray-50 rounded-lg">
                                                <h4 className="font-medium text-gray-900 mb-2">Work Style</h4>
                                                <p className="text-gray-600">{user.preferences.remote}</p>
                                            </div>
                                            <div className="p-4 bg-gray-50 rounded-lg">
                                                <h4 className="font-medium text-gray-900 mb-2">Industries</h4>
                                                <p className="text-gray-600">{user.preferences.industries.join(', ')}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {isEditing && (
                            <div ref={formRef} className="bg-white rounded-xl shadow-sm mb-6">
                                <div className="border-b p-4 text-center text-xl font-medium text-blue-500">
                                    Edit Profile Information
                                </div>
                                <div className="p-6">
                                    <div className="space-y-6">
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                                    First Name
                                                </label>
                                                <input
                                                    type="text"
                                                    name="firstName"
                                                    value={formData.firstName}
                                                    onChange={handleInputChange}
                                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                                    placeholder="Enter first name"
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-sm font-medium text-gray-700 mb-2">
                                                    Last Name
                                                </label>
                                                <input
                                                    type="text"
                                                    name="lastName"
                                                    value={formData.lastName}
                                                    onChange={handleInputChange}
                                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                                    placeholder="Enter last name"
                                                />
                                            </div>
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                                Location
                                            </label>
                                            <input
                                                type="text"
                                                name="location"
                                                value={formData.location}
                                                onChange={handleInputChange}
                                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                                placeholder="City, State/Country"
                                            />
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                                Full Address
                                            </label>
                                            <textarea
                                                name="address"
                                                value={formData.address}
                                                onChange={handleInputChange}
                                                rows="4"
                                                className="w-full px-4 py-3 border resize-none border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                                placeholder="Enter your complete address"
                                            />
                                        </div>


                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                                Phone Number
                                            </label>
                                            <div className="flex gap-2">
                                                <select
                                                    name="countryCode"
                                                    value={formData.countryCode}
                                                    onChange={(e) => {
                                                        handleInputChange(e);
                                                        const newCountryCode = e.target.value;
                                                        const currentPhone = formData.phone;
                                                        let phoneWithoutCode = currentPhone;
                                                        if (currentPhone.startsWith('+')) {
                                                            const match = currentPhone.match(/^\+\d+\s?(.*)$/);
                                                            if (match) {
                                                                phoneWithoutCode = match[1];
                                                            }
                                                        }

                                                        const newPhoneValue = phoneWithoutCode ? `${newCountryCode} ${phoneWithoutCode}` : newCountryCode + ' ';

                                                        handleInputChange({
                                                            target: {
                                                                name: 'phone',
                                                                value: newPhoneValue
                                                            }
                                                        });
                                                    }}
                                                    className="px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white min-w-[120px]"
                                                >
                                                    <option value="+1">🇺🇸 +1</option>
                                                    <option value="+1">🇨🇦 +1</option>
                                                    <option value="+44">🇬🇧 +44</option>
                                                    <option value="+33">🇫🇷 +33</option>
                                                    <option value="+49">🇩🇪 +49</option>
                                                    <option value="+39">🇮🇹 +39</option>
                                                    <option value="+34">🇪🇸 +34</option>
                                                    <option value="+31">🇳🇱 +31</option>
                                                    <option value="+32">🇧🇪 +32</option>
                                                    <option value="+41">🇨🇭 +41</option>
                                                    <option value="+43">🇦🇹 +43</option>
                                                    <option value="+45">🇩🇰 +45</option>
                                                    <option value="+46">🇸🇪 +46</option>
                                                    <option value="+47">🇳🇴 +47</option>
                                                    <option value="+358">🇫🇮 +358</option>
                                                    <option value="+91">🇮🇳 +91</option>
                                                    <option value="+86">🇨🇳 +86</option>
                                                    <option value="+81">🇯🇵 +81</option>
                                                    <option value="+82">🇰🇷 +82</option>
                                                    <option value="+61">🇦🇺 +61</option>
                                                    <option value="+64">🇳🇿 +64</option>
                                                    <option value="+55">🇧🇷 +55</option>
                                                    <option value="+52">🇲🇽 +52</option>
                                                    <option value="+54">🇦🇷 +54</option>
                                                    <option value="+56">🇨🇱 +56</option>
                                                    <option value="+57">🇨🇴 +57</option>
                                                    <option value="+351">🇵🇹 +351</option>
                                                    <option value="+7">🇷🇺 +7</option>
                                                    <option value="+27">🇿🇦 +27</option>
                                                    <option value="+234">🇳🇬 +234</option>
                                                    <option value="+20">🇪🇬 +20</option>
                                                    <option value="+971">🇦🇪 +971</option>
                                                    <option value="+966">🇸🇦 +966</option>
                                                    <option value="+65">🇸🇬 +65</option>
                                                    <option value="+60">🇲🇾 +60</option>
                                                    <option value="+66">🇹🇭 +66</option>
                                                    <option value="+84">🇻🇳 +84</option>
                                                    <option value="+63">🇵🇭 +63</option>
                                                    <option value="+62">🇮🇩 +62</option>
                                                </select>
                                                <input
                                                    type="tel"
                                                    name="phone"
                                                    value={formData.phone}
                                                    onChange={handleInputChange}
                                                    className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                                    placeholder="Enter phone number"
                                                />
                                            </div>
                                        </div>


                                        <div className="flex gap-4 pt-4 justify-center">
                                            <button
                                                onClick={handleSave}
                                                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
                                            >
                                                Save Changes
                                            </button>
                                            <button
                                                onClick={handleCancel}
                                                className="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors font-medium"
                                            >
                                                Cancel
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
            <Footer />
        </div >
    );
}