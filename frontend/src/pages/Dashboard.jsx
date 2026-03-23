import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  Mic, Send, Volume2, History, LogOut, User as UserIcon, Square, X
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_URL = 'http://localhost:8000';

function Dashboard({ token, setToken }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [voice, setVoice] = useState('te-IN-ShrutiNeural');
  const [username, setUsername] = useState('');
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const scrollRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => { fetchProfile(); fetchHistory(); }, []);
  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  const stopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
    }
  };

  const playAudio = (url) => {
    stopAudio();
    const audio = new Audio(url);
    audioRef.current = audio;
    audio.onplay = () => setIsPlaying(true);
    audio.onended = () => setIsPlaying(false);
    audio.onpause = () => setIsPlaying(false);
    audio.play().catch(e => console.error('Audio play failed', e));
  };

  const fetchProfile = async () => {
    try {
      const res = await axios.get(`${API_URL}/me`, { headers: { Authorization: `Bearer ${token}` } });
      setUsername(res.data.username);
      setVoice(res.data.preferred_voice);
    } catch { handleLogout(); }
  };

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_URL}/history`, { headers: { Authorization: `Bearer ${token}` } });
      setHistory(res.data);
    } catch { console.error('History fetch failed'); }
  };

  const handleLogout = () => { setToken(null); localStorage.removeItem('token'); };

  const handleVoiceChange = async (newVoice) => {
    setVoice(newVoice);
    try {
      await axios.post(`${API_URL}/settings/voice`, { voice: newVoice }, {
        headers: { Authorization: `Bearer ${token}` }
      });
    } catch { console.error('Voice update failed'); }
  };

  const startConversation = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) { alert('Your browser does not support Speech Recognition.'); return; }
    const recognition = new SpeechRecognition();
    recognition.lang = 'te-IN';
    recognition.interimResults = false;
    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (e) => sendMessage(e.results[0][0].transcript);
    recognition.start();
  };

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    setMessages(prev => [...prev, { role: 'user', text }]);
    setLoading(true);
    setInputText('');
    try {
      const res = await axios.post(`${API_URL}/chat`, { text }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const assistantMsg = {
        role: 'assistant',
        text: res.data.assistant_text,
        audio: `${API_URL}${res.data.audio_url}`
      };
      setMessages(prev => [...prev, assistantMsg]);
      playAudio(assistantMsg.audio);
      fetchHistory();
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', text: 'నమస్కారం, ఏదో పొరపాటు జరిగింది. మళ్ళీ ప్రయత్నించండి.' }]);
    } finally {
      setLoading(false);
    }
  };

  const formatText = (text) => {
    if (!text) return null;
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="font-bold">{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  const loadHistoryItem = (h) => {
    setMessages([
      { role: 'user', text: h.user_text },
      { role: 'assistant', text: h.assistant_text, audio: h.audio_url ? `${API_URL}${h.audio_url}` : null }
    ]);
    if (h.audio_url) playAudio(`${API_URL}${h.audio_url}`);
    setShowHistory(false);
  };

  const startNewChat = () => {
    setMessages([]);
    stopAudio();
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 glass border-b border-aqua-100 sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-aqua-500 rounded-2xl shadow-md shadow-aqua-200/50">
            <Mic className="text-white w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-aqua-900 leading-tight">Telugu Assistant</h1>
            <p className="text-xs text-aqua-400 font-medium">Online & Ready</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <button
              onClick={startNewChat}
              className="px-3 py-1.5 text-xs font-semibold text-aqua-600 hover:bg-aqua-50 rounded-lg transition-colors border border-aqua-100 mr-2"
            >
              + New Chat
            </button>
          )}
          <button
            onClick={() => setShowHistory(!showHistory)}
            className={`p-2 rounded-xl transition-all ${
              showHistory ? 'bg-aqua-100 text-aqua-600' : 'hover:bg-aqua-50 text-aqua-400'
            }`}
            title="History"
          >
            <History className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-2 bg-white border border-aqua-100 px-3 py-2 rounded-full shadow-sm">
            <UserIcon className="w-4 h-4 text-aqua-400" />
            <span className="text-sm font-medium text-aqua-800">{username}</span>
            <button onClick={handleLogout} className="ml-1 p-0.5 hover:text-red-400 text-gray-300 transition-colors">
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 flex overflow-hidden relative">
        {/* Chat area */}
        <div className="flex-1 flex flex-col min-w-0">
          <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="h-full flex flex-col items-center justify-center text-center py-20">
                <div className="p-6 bg-aqua-50 border-2 border-aqua-100 rounded-3xl mb-5 animate-float">
                  <Mic className="w-12 h-12 text-aqua-400" />
                </div>
                <h2 className="text-xl font-bold text-aqua-800 mb-1">How can I help you?</h2>
                <p className="text-aqua-400 text-sm max-w-xs">
                  Click <strong>Start Conversation</strong> to speak in Telugu, or type below.
                </p>
              </div>
            )}

            <AnimatePresence initial={false}>
              {messages.map((msg, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 8, scale: 0.97 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[78%] px-4 py-3 rounded-2xl shadow-sm ${
                    msg.role === 'user'
                      ? 'bg-aqua-500 text-white rounded-tr-sm shadow-aqua-200/60'
                      : 'bg-white text-gray-700 rounded-tl-sm border border-aqua-100'
                  }`}>
                    <p className="text-sm leading-relaxed telugu-font">{formatText(msg.text)}</p>
                    {msg.audio && (
                      <button
                        onClick={() => playAudio(msg.audio)}
                        className="mt-1.5 text-xs flex items-center gap-1 opacity-50 hover:opacity-100 transition-opacity"
                      >
                        <Volume2 className="w-3 h-3" /> Replay
                      </button>
                    )}
                  </div>
                </motion.div>
              ))}
              {loading && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                  <div className="bg-white border border-aqua-100 px-5 py-3.5 rounded-2xl rounded-tl-sm shadow-sm">
                    <div className="flex gap-1.5">
                      {[0, 1, 2].map(i => (
                        <div key={i} className={`w-2 h-2 bg-aqua-400 rounded-full animate-bounce`}
                          style={{ animationDelay: `${i * 0.15}s` }} />
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Controls */}
          <div className="px-5 pb-5 pt-3 glass border-t border-aqua-100">
            {/* Voice toggle */}
            <div className="flex items-center gap-2 mb-3">
              <span className="text-xs font-semibold text-aqua-500 uppercase tracking-wider">Voice:</span>
              {['te-IN-ShrutiNeural', 'te-IN-MohanNeural'].map((v) => (
                <button
                  key={v}
                  onClick={() => handleVoiceChange(v)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                    voice === v
                      ? 'bg-aqua-500 text-white shadow shadow-aqua-300/40'
                      : 'bg-aqua-50 text-aqua-500 hover:bg-aqua-100 border border-aqua-100'
                  }`}
                >
                  {v.includes('Shruti') ? '♀ Shruti' : '♂ Mohan'}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-3">
              {/* Mic button */}
              <div className="relative">
                <button
                  onClick={startConversation}
                  className={`flex-none p-4 rounded-2xl transition-all active:scale-95 shadow-md ${
                    isListening
                      ? 'bg-red-500 text-white shadow-red-200/60 animate-pulse'
                      : 'bg-aqua-500 hover:bg-aqua-600 text-white shadow-aqua-200/60'
                  }`}
                  title="Start Conversation"
                  disabled={isPlaying}
                >
                  {isListening ? <Square className="w-6 h-6 fill-current" /> : <Mic className="w-6 h-6" />}
                </button>
                
                {isPlaying && (
                  <motion.button
                    initial={{ scale: 0, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    onClick={stopAudio}
                    className="absolute -top-2 -right-2 p-2 bg-white border border-red-100 text-red-500 rounded-full shadow-lg hover:bg-red-50 transition-colors z-20"
                    title="Stop Speaking"
                  >
                    <Square className="w-3 h-3 fill-current" />
                  </motion.button>
                )}
              </div>

              {/* Text input */}
              <div className="flex-1 relative flex items-center">
                <input
                  type="text"
                  placeholder={isPlaying ? "Assistant is speaking..." : "Type in Telugu or English..."}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendMessage(inputText)}
                  disabled={isPlaying}
                  className="w-full bg-white border border-aqua-200 rounded-2xl pl-4 pr-12 py-3.5 text-gray-700 placeholder:text-gray-300 outline-none focus:border-aqua-500 focus:ring-2 focus:ring-aqua-100 transition-all disabled:bg-gray-50 disabled:cursor-not-allowed"
                />
                <button
                  onClick={() => sendMessage(inputText)}
                  disabled={isPlaying || !inputText.trim()}
                  className="absolute right-3 text-aqua-400 hover:text-aqua-600 transition-colors disabled:opacity-30"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
            <p className="text-[10px] text-aqua-300 mt-2 text-center">
              Conversations are stored for the last 10 days only.
            </p>
          </div>
        </div>

        {/* History sidebar */}
        <AnimatePresence>
          {showHistory && (
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="absolute right-0 top-0 bottom-0 w-80 bg-white border-l border-aqua-100 shadow-xl z-20 flex flex-col"
            >
              <div className="p-4 border-b border-aqua-100 flex items-center justify-between">
                <h3 className="font-bold text-aqua-800 flex items-center gap-2">
                  <History className="w-4 h-4 text-aqua-400" /> Recent History
                </h3>
                <button onClick={() => setShowHistory(false)} className="text-gray-300 hover:text-aqua-500 transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {history.length === 0 && (
                  <p className="text-center text-gray-300 text-sm mt-10">No recent conversations.</p>
                )}
                {history.map((h, i) => (
                  <button
                    key={i}
                    onClick={() => loadHistoryItem(h)}
                    className="w-full text-left bg-aqua-50 hover:bg-aqua-100 border border-aqua-100 p-3 rounded-2xl transition-all active:scale-[0.98] group"
                  >
                    <div className="flex justify-between items-start mb-1">
                      <p className="text-[10px] text-aqua-400 font-medium">
                        {new Date(h.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                      </p>
                      {h.audio_url && <Volume2 className="w-3 h-3 text-aqua-300 group-hover:text-aqua-500" />}
                    </div>
                    <p className="text-sm font-semibold text-aqua-800 truncate telugu-font">{formatText(h.user_text)}</p>
                    <p className="text-xs text-gray-400 line-clamp-2 telugu-font mt-0.5">{formatText(h.assistant_text)}</p>
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default Dashboard;
