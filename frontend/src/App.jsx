import './App.css';
import { Navigate, Routes, Route } from 'react-router-dom';
import { useUser } from './context/UserContext.js';
import Home from './pages/Home.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import PasswordResetPage from './pages/PasswordReset.jsx';
import DashboardPage from './pages/Dashboard.jsx';
import JobRecommendationsPage from './pages/JobRecommendations.jsx';
import ResumeAnalysis from './pages/ResumeAnalysis.jsx';
import EditResume from './pages/EditResume.jsx';
import AppliedJobs from './pages/AppliedJobs.jsx';
import SavedJobs from './pages/SavedJobs.jsx';
import Profile from './pages/Profile.jsx';
import About from './pages/About.jsx';
import AboutPageGuest from './pages/AboutPageGuest.jsx';
import Contact from './pages/Contact.jsx';

function App() {
  const { user } = useUser();

  return (
    <Routes>
      <Route index element={<Home />} />
      <Route path="/loginpage" element={<LoginPage />} />
      <Route path="/registration" element={<RegisterPage />} />
      <Route path="/passwordreset" element={<PasswordResetPage />} />
      <Route path="/dashboard" element={user?.email ? <DashboardPage /> : <Navigate to="/loginpage" />} />
      <Route path="/jobs" element={<JobRecommendationsPage />} />
      <Route path="/resumeanalysis" element={<ResumeAnalysis />} />
      <Route path="/editresume" element={<EditResume />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/appliedjobs" element={<AppliedJobs />} />
      <Route path="/savedjobs" element={<SavedJobs />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/aboutpageguest" element={<AboutPageGuest />} />
    </Routes>
  );
}

export default App;
