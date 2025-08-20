import React, { createContext, useContext, useState } from "react";

const UserContext = createContext();

export const useUser = () => useContext(UserContext);


export const UserProvider = ({ children }) => {
  const [user, setUser] = useState({
    name: "John Doe",
    email: "john@example.com",
    title: "Senior Software Engineer",
    avatar: "/userPicture/120/120",
    location: "San Francisco, CA",
    address: "1234 Elm Street, Apt 56, San Francisco, CA 94107, USA",
    phone: "+1 (415) 555-1234",
    skills: ["React", "Node.js", "Python", "Machine Learning", "AWS", "Docker"],
    interests: ["Web Development"],
    experience: "3 Years at XYZ Corp",
    education: "BSc Computer Science",
    preferences: {
      salary: "$120,000 - $180,000",
      jobType: "Full-time",
      remote: "Hybrid preferred",
      industries: ["Technology", "Healthcare", "Fintech"]
    },
    resume: null,
  });

  const updateUser = (updates) => {
    setUser((prev) => ({ ...prev, ...updates }));
  };

  return (
    <UserContext.Provider value={{ user, updateUser }}>
      {children}
    </UserContext.Provider>
  );
};
