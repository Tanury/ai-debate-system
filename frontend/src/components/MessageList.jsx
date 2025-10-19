import React, { useRef, useEffect } from 'react';
import { Send, User, Bot, Trophy, MessageSquare } from 'lucide-react';

const MessageList = ({
  messages,
  loading,
  debateActive,
  input,
  setInput,
  handleSendMessage,
  handleAdmitDefeat
}) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  return (
    <div className="card h-[600px] flex flex-col">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.type === 'human' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[80%] rounded-xl p-4 ${
                msg.type === 'human'
                  ? 'bg-gradient-to-r from-blue-500 to-blue-600'
                  : msg.type === 'ai'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500'
                  : msg.type === 'evaluation'
                  ? 'bg-gradient-to-r from-yellow-500 to-orange-500'
                  : 'bg-white/10'
              }`}
            >
              <div className="flex items-start gap-2 mb-2">
                {msg.type === 'human' ? (
                  <User className="w-5 h-5 text-white" />
                ) : msg.type === 'ai' ? (
                  <Bot className="w-5 h-5 text-white" />
                ) : msg.type === 'evaluation' ? (
                  <Trophy className="w-5 h-5 text-white" />
                ) : (
                  <MessageSquare className="w-5 h-5 text-white" />
                )}
                <span className="text-white/70 text-xs">{msg.timestamp}</span>
                {msg.round && (
                  <span className="ml-auto text-white/90 text-xs font-semibold px-2 py-1 bg-white/20 rounded">
                    Round {msg.round}
                  </span>
                )}
              </div>
              <p className="text-white whitespace-pre-wrap">{msg.content}</p>
              {msg.keywords && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {msg.keywords.map((kw, i) => (
                    <span key={i} className="px-2 py-1 bg-white/20 rounded text-xs text-white">
                      {kw}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] rounded-xl p-4 bg-gradient-to-r from-purple-500 to-pink-500">
              <div className="flex items-center gap-2">
                <Bot className="w-5 h-5 text-white animate-pulse" />
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
                <span className="text-white text-sm">AI analyzing your argument...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-white/20 p-4">
        <div className="flex gap-2 mb-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder={debateActive ? 'Present your argument...' : 'Start a debate first'}
            disabled={!debateActive || loading}
            className="flex-1 input-field disabled:opacity-50"
          />
          <button
            onClick={handleSendMessage}
            disabled={!debateActive || loading}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        {debateActive && (
          <div className="flex gap-2">
            <button
              onClick={() => handleAdmitDefeat('ai')}
              className="flex-1 px-4 py-2 bg-red-500/30 hover:bg-red-500/50 text-white rounded-lg text-sm border border-red-400/50"
            >
              I Admit Defeat
            </button>
            <button
              onClick={() => handleAdmitDefeat('human')}
              className="flex-1 px-4 py-2 bg-green-500/30 hover:bg-green-500/50 text-white rounded-lg text-sm border border-green-400/50"
            >
              AI Admits Defeat
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageList;
