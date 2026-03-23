import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Mic, Lock, User as UserIcon, ArrowRight, Waves } from 'lucide-react';
import { motion } from 'framer-motion';

const API_URL = 'http://localhost:8000';

function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API_URL}/token`, { username, password });
      setToken(response.data.access_token);
      navigate('/');
    } catch (err) {
      setError('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 relative overflow-hidden">
      {/* Decorative blobs */}
      <div className="absolute top-[-80px] right-[-80px] w-[360px] h-[360px] bg-aqua-200/50 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-[-80px] left-[-80px] w-[360px] h-[360px] bg-aqua-100/60 rounded-full blur-3xl pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md glass shadow-xl shadow-aqua-100/60 rounded-3xl p-8 z-10"
      >
        <div className="flex flex-col items-center mb-8">
          <div className="p-4 bg-aqua-500 rounded-2xl shadow-lg shadow-aqua-300/40 mb-4 animate-float">
            <Mic className="text-white w-8 h-8" />
          </div>
          <h1 className="text-3xl font-bold text-aqua-900 mb-1">Welcome Back</h1>
          <p className="text-aqua-600 text-sm">Sign in to Telugu Assistant</p>
        </div>

        {error && (
          <div className="mb-5 p-3 bg-red-50 border border-red-200 text-red-600 rounded-2xl text-center text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="relative group">
            <UserIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-aqua-400 w-5 h-5 group-focus-within:text-aqua-600 transition-colors" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full pl-12 pr-4 py-3.5 bg-white border border-aqua-200 rounded-2xl focus:border-aqua-500 focus:ring-2 focus:ring-aqua-100 outline-none transition-all placeholder:text-gray-300 text-gray-700"
            />
          </div>
          <div className="relative group">
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-aqua-400 w-5 h-5 group-focus-within:text-aqua-600 transition-colors" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full pl-12 pr-4 py-3.5 bg-white border border-aqua-200 rounded-2xl focus:border-aqua-500 focus:ring-2 focus:ring-aqua-100 outline-none transition-all placeholder:text-gray-300 text-gray-700"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-aqua-500 hover:bg-aqua-600 text-white py-3.5 rounded-2xl font-semibold flex items-center justify-center gap-2 transition-all active:scale-[0.98] shadow-lg shadow-aqua-200/60 mt-2"
          >
            {loading ? 'Signing in...' : (<>Sign In <ArrowRight className="w-5 h-5" /></>)}
          </button>
        </form>

        <p className="mt-8 text-center text-gray-400 text-sm">
          Don't have an account?{' '}
          <Link to="/register" className="text-aqua-500 hover:text-aqua-700 font-semibold transition-colors">
            Sign Up
          </Link>
        </p>
      </motion.div>
    </div>
  );
}

export default Login;
