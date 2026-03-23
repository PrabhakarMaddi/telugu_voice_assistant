import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  return (
    <Router>
      <div className="min-h-screen">
        <Routes>
          <Route path="/login" element={token ? <Navigate to="/" /> : <Login setToken={setToken} />} />
          <Route path="/register" element={token ? <Navigate to="/" /> : <Register />} />
          <Route 
            path="/" 
            element={token ? <Dashboard token={token} setToken={setToken} /> : <Navigate to="/login" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
