import React, { useState, useRef, useEffect, useCallback } from 'react';
import { MessageBubble } from './MessageBubble';
import { ChatHistory } from './ChatHistory';
import { MCPServerConfig } from './MCPServerConfig';
import { Message, ChatSession, MCPServer } from '../types/chat';
import { Send, Settings, Menu, X, Sparkles } from 'lucide-react';

export const ChatInterface: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [inputMessage, setInputMessage] = useState('');
  const [mcpServers, setMcpServers] = useState<MCPServer[]>([]); // Assuming MCP servers are managed client-side for now
  const [showMcpConfig, setShowMcpConfig] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const activeSession = sessions.find(s => s.id === activeSessionId);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [activeSession?.messages, isTyping]);

  const generateId = () => Math.random().toString(36).substr(2, 9);

  const createNewSession = useCallback(() => {
    const newSession: ChatSession = {
      id: generateId(),
      title: 'New Chat', // Default title, will be updated by summary
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date()
    };

    setSessions(prev => [newSession, ...prev]);
    setActiveSessionId(newSession.id);
  }, []);

  const summarizeAndSetTitle = useCallback(async (sessionId: string, messages: Message[]) => {
    if (messages.length === 0) return;

    try {
      // Send only the necessary parts of messages for summarization
      const messagesForSummary = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const response = await fetch('/api/summarize_chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: messagesForSummary }),
      });

      if (!response.ok) {
        throw new Error(`Summary API error! status: ${response.status}`);
      }

      const data = await response.json();
      const summary = data.summary || "Untitled Chat"; // Fallback summary

      setSessions(prev => prev.map(session =>
        session.id === sessionId
          ? { ...session, title: summary }
          : session
      ));

    } catch (error) {
      console.error('Error getting chat summary:', error);
      setSessions(prev => prev.map(session =>
        session.id === sessionId
          ? { ...session, title: 'Untitled Chat' } // Fallback on error
          : session
      ));
    }
  }, []);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    let currentSessionId = activeSessionId;
    let isNewSession = false;

    // Create new session if none exists
    if (!currentSessionId) {
      const newSessionId = generateId();
      const newSession: ChatSession = {
        id: newSessionId,
        title: 'New Chat', // Temporary title
        messages: [],
        createdAt: new Date(),
        updatedAt: new Date()
      };

      setSessions(prev => [newSession, ...prev]);
      currentSessionId = newSessionId;
      setActiveSessionId(currentSessionId);
      isNewSession = true;
    }

    const userMessage: Message = {
      id: generateId(),
      content: inputMessage,
      role: 'user',
      timestamp: new Date()
    };

    // Add user message immediately
    setSessions(prev => prev.map(session => {
        if (session.id === currentSessionId) {
            return {
                ...session,
                messages: [...session.messages, userMessage],
                updatedAt: new Date()
            };
        }
        return session;
    }));

    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: currentSessionId,
          message: userMessage.content,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const aiResponseContent = data.response || "No response from AI.";

      const aiMessage: Message = {
        id: generateId(),
        content: aiResponseContent,
        role: 'assistant',
        timestamp: new Date()
      };

      // Update session with AI message
      setSessions(prev => prev.map(session => {
        if (session.id === currentSessionId) {
          return {
            ...session,
            messages: [...session.messages, aiMessage],
            updatedAt: new Date()
          };
        }
        return session;
      }));

      // Trigger summarization if this is a new session or after a few messages
      if (isNewSession || (activeSession?.messages.length === 2)) {
          summarizeAndSetTitle(currentSessionId, activeSession?.messages || []);
      }

    } catch (error) {
      console.error('Error sending message to backend:', error);
      const errorMessage: Message = {
        id: generateId(),
        content: `Error: Could not get response from AI. ${error instanceof Error ? error.message : String(error)}`,
        role: 'assistant',
        timestamp: new Date()
      };
      setSessions(prev => prev.map(session =>
        session.id === currentSessionId
          ? {
              ...session,
              messages: [...session.messages, errorMessage],
              updatedAt: new Date()
            }
          : session
      ));
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const deleteSession = (sessionId: string) => {
    setSessions(prev => {
      const updatedSessions = prev.filter(s => s.id !== sessionId);
      if (activeSessionId === sessionId) {
        // Select the first remaining session or null if no sessions left
        setActiveSessionId(updatedSessions.length > 0 ? updatedSessions[0].id : null);
      }
      return updatedSessions;
    });
  };


  const addMcpServer = (server: Omit<MCPServer, 'id'>) => {
    const newServer: MCPServer = {
      ...server,
      id: generateId(),
      isActive: true // New servers are active by default
    };
    setMcpServers(prev => [...prev, newServer]);
  };

  const deleteMcpServer = (serverId: string) => {
    setMcpServers(prev => prev.filter(s => s.id !== serverId));
  };

  const toggleMcpServer = (serverId: string) => {
    setMcpServers(prev => prev.map(server =>
      server.id === serverId
        ? { ...server, isActive: !server.isActive }
        : server
    ));
  };

  // Initialize with a default session if none exist
  useEffect(() => {
    if (sessions.length === 0 && !activeSessionId) {
      createNewSession();
    }
  }, [sessions.length, activeSessionId, createNewSession]);

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Sidebar */}
      {showSidebar && (
        <ChatHistory
          sessions={sessions}
          activeSessionId={activeSessionId}
          onSelectSession={setActiveSessionId}
          onDeleteSession={deleteSession}
          onNewChat={createNewSession}
        />
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col backdrop-blur-sm">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600/20 via-purple-600/20 to-pink-600/20 backdrop-blur-md border-b border-white/10 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowSidebar(!showSidebar)}
              className="p-2 hover:bg-white/10 rounded-xl transition-all duration-300 lg:hidden backdrop-blur-sm"
            >
              {showSidebar ? <X size={20} className="text-white" /> : <Menu size={20} className="text-white" />}
            </button>

            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Axiom AI
                </h1>
                <p className="text-sm text-white/70">
                  {activeSession ? activeSession.title : 'Select or start a new chat'}
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={() => setShowMcpConfig(true)}
            className="p-3 hover:bg-white/10 rounded-xl transition-all duration-300 backdrop-blur-sm group"
            title="Configure MCP Servers"
          >
            <Settings size={20} className="text-white/80 group-hover:text-white group-hover:rotate-90 transition-all duration-300" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-transparent to-black/20">
          {activeSession ? (
            <>
              {activeSession.messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}

              {isTyping && (
                <MessageBubble
                  message={{
                    id: 'typing',
                    content: '',
                    role: 'assistant',
                    timestamp: new Date(),
                    isTyping: true
                  }}
                />
              )}

              <div ref={messagesEndRef} />
            </>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-2xl">
                  <Sparkles className="text-white w-8 h-8" />
                </div>
                <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent mb-3">
                  Welcome to Axiom AI
                </h2>
                <p className="text-white/70 mb-6 text-lg">Start a conversation to explore infinite possibilities</p>
                <button
                  onClick={createNewSession}
                  className="px-8 py-4 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-600 text-white rounded-xl hover:from-cyan-400 hover:via-blue-400 hover:to-purple-500 transition-all duration-300 shadow-xl hover:shadow-2xl hover:scale-105 font-medium"
                >
                  Start New Chat
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        {activeSession && (
          <div className="border-t border-white/10 bg-gradient-to-r from-indigo-600/10 via-purple-600/10 to-pink-600/10 backdrop-blur-md p-6">
            <div className="max-w-4xl mx-auto">
              <div className="relative">
                <textarea
                  ref={inputRef}
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask Axiom AI anything..."
                  className="w-full resize-none bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl px-6 py-4 pr-16 focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-400/50 min-h-[60px] max-h-32 text-white placeholder-white/50 transition-all duration-300 break-words overflow-hidden"
                  rows={1}
                  style={{ wordWrap: 'break-word', overflowWrap: 'break-word' }}
                />

                <button
                  onClick={sendMessage}
                  disabled={!inputMessage.trim() || isTyping}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 p-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-xl hover:from-cyan-400 hover:to-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105"
                >
                  <Send size={18} />
                </button>
              </div>

              <div className="flex items-center justify-between mt-3 text-sm text-white/60">
                <span>Press Enter to send, Shift+Enter for new line</span>
                <span className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full animate-pulse"></div>
                  {mcpServers.filter(s => s.isActive).length} MCP server(s) connected
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* MCP Server Configuration Modal */}
      <MCPServerConfig
        servers={mcpServers}
        onAddServer={addMcpServer}
        onDeleteServer={deleteMcpServer}
        onToggleServer={toggleMcpServer}
        isOpen={showMcpConfig}
        onClose={() => setShowMcpConfig(false)}
      />
    </div>
  );
};