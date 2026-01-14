import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Menu, SendHorizontal, AlertCircle, Loader2 } from 'lucide-react';
import { api } from './services/api';
import { Session, Message } from './types';
import { Sidebar } from './components/Sidebar';
import { MessageBubble } from './components/MessageBubble';

function App() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Scroll to bottom helper
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Initial Load
  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const data = await api.getSessions();
      // Sort by updated_at descending
      const sorted = data.sort((a, b) => 
        new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
      );
      setSessions(sorted);
    } catch (err) {
      console.error(err);
      setError("Failed to load sessions. Is the backend running?");
    }
  };

  const loadSessionDetails = async (id: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.getSession(id);
      setCurrentSessionId(data.id);
      
      const msgs = Array.isArray(data.messages) ? data.messages : [];
      setMessages(msgs);
    } catch (err) {
      console.error(err);
      setError("Failed to load chat history.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewSession = async () => {
    setIsLoading(true);
    try {
      const newSession = await api.createSession("New Chat");
      setSessions(prev => [newSession, ...prev]);
      setCurrentSessionId(newSession.id);
      setMessages([]);
      if (inputRef.current) inputRef.current.focus();
    } catch (err) {
      setError("Failed to create new session");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || !currentSessionId || isLoading) return;

    const messageText = inputValue;
    setInputValue('');
    setIsLoading(true);
    setError(null);

    // Optimistically add user message for UI responsiveness
    const tempMessage: Message = {
      message: messageText,
      response: '', // Empty response initially
    };
    setMessages(prev => [...prev, tempMessage]);

    try {
      // 1. Send Message
      const req = await api.sendMessage(currentSessionId, messageText);
      
      // 2. Poll for completion
      await api.pollForCompletion(req.id);

      // 3. Fetch updated session to get the full response
      const updatedSession = await api.getSession(currentSessionId);
      
      const msgs = Array.isArray(updatedSession.messages) ? updatedSession.messages : [];
      setMessages(msgs);
      
      // Update session list order (since it was just updated)
      loadSessions();

    } catch (err) {
      console.error(err);
      setError("Failed to send message or receive response.");
      // Remove the optimistic message on failure or show error state
    } finally {
      setIsLoading(false);
      // Keep focus on input
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-900">
      
      {/* Sidebar */}
      <Sidebar 
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={loadSessionDetails}
        onNewSession={handleNewSession}
        isOpen={isSidebarOpen}
        onCloseMobile={() => setIsSidebarOpen(false)}
      />

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative w-full h-full">
        
        {/* Header */}
        <header className="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-200 shadow-sm z-10">
          <div className="flex items-center gap-3">
            <button 
              className="md:hidden p-2 text-gray-500 hover:bg-gray-100 rounded-md"
              onClick={() => setIsSidebarOpen(true)}
            >
              <Menu size={20} />
            </button>
            <h1 className="font-semibold text-gray-700">
              {sessions.find(s => s.id === currentSessionId)?.title || 'Select a chat'}
            </h1>
          </div>
        </header>

        {/* Messages List */}
        <div className="flex-1 overflow-y-auto p-4 md:p-6 scroll-smooth">
          {error && (
            <div className="mx-auto max-w-2xl mb-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg flex items-center gap-2">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          {!currentSessionId ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-400 opacity-60">
               <div className="w-16 h-16 bg-gray-200 rounded-full mb-4 flex items-center justify-center">
                  <SendHorizontal size={32} className="ml-1" />
               </div>
               <p>Select a chat or start a new one</p>
            </div>
          ) : (
            <div className="mx-auto max-w-3xl flex flex-col">
              {messages.map((msg, idx) => (
                <React.Fragment key={idx}>
                  {/* User Bubble */}
                  <MessageBubble isUser={true} content={msg.message} timestamp={msg.created_at} />
                  
                  {/* AI Bubble (only if response exists) */}
                  {msg.response && (
                    <MessageBubble isUser={false} content={msg.response} />
                  )}
                </React.Fragment>
              ))}

              {/* Loading Indicator */}
              {isLoading && (
                <div className="flex w-full mb-6 justify-start">
                   <div className="flex items-end gap-2">
                      <div className="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center mb-1">
                        <Loader2 size={16} className="animate-spin" />
                      </div>
                      <div className="px-4 py-3 bg-white border border-gray-100 rounded-2xl rounded-bl-sm shadow-sm text-gray-400 text-sm">
                        Thinking...
                      </div>
                   </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-white p-4 border-t border-gray-200">
          <div className="mx-auto max-w-3xl">
            <form onSubmit={handleSendMessage} className="relative flex items-center">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder={currentSessionId ? "Type your message..." : "Start a new chat to type..."}
                disabled={!currentSessionId || isLoading}
                className="w-full pl-4 pr-12 py-3.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-inner"
                aria-label="Chat Input"
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || !currentSessionId || isLoading}
                className="absolute right-2 p-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                aria-label="Send Message"
              >
                <SendHorizontal size={18} />
              </button>
            </form>
            <div className="text-center mt-2">
               <p className="text-[10px] text-gray-400">
                 AI can make mistakes. Consider checking important information.
               </p>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}

export default App;