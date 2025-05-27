import './App.css';
import { Navigate } from 'react-router-dom';
import Home from './pages/Home.jsx';
import LoginPage from './pages/LoginPage.jsx';
import RegisterPage from './pages/RegisterPage.jsx';
import { useUser } from './context/UserContext.js';
import { BrowserRouter } from 'react-router-dom'
import { Route, Router, Routes } from 'react-router-dom'
function App() {
  const { user } = useUser();

  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Home />} />
        <Route path='/loginpage' element={<LoginPage />} />
        <Route path='/registration' element={<RegisterPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
