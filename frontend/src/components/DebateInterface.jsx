import React, { useState } from 'react';
import { Brain } from 'lucide-react';
import AgentStatus from './AgentStatus';
import ScoreBoard from './ScoreBoard';
import MessageList from './MessageList';
import DocumentUploader from './DocumentUploader';
import WebScrapeTool from './WebScrapeTool';
import { useDebate } from '../hooks/useDebate';

const DebateInterface = () => {
  const [topic, setTopic] = useState('');
  
  const {
    messages,
    input,
    setInput,
    debateActive,
    score,
    loading,
    roundNumber,
    currentAgent,
    uploadedDocs,
    startDebate,
    handleSendMessage,
    handleAdmitDefeat,
    handleFileUpload,
    simulateWebScrape
  } = useDebate(topic);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="card mb-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Brain className="w-10 h-10 text-purple-400" />
              <div>
                <h1 className="text-3xl font-bold text-white">AI Debate System</h1>
                <p className="text-purple-300 text-sm">Multi-Round Collaborative Argumentation Platform</p>
              </div>
            </div>
            <ScoreBoard score={score} roundNumber={roundNumber} />
          </div>

          {/* Topic Input */}
          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter debate topic (e.g., 'Climate change requires immediate action')"
              className="flex-1 input-field"
              disabled={debateActive}
            />
            <button
              onClick={() => startDebate(topic)}
              disabled={debateActive}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Start Debate
            </button>
          </div>

          {/* Tools */}
          <div className="flex gap-2">
            <DocumentUploader onUpload={handleFileUpload} />
            <WebScrapeTool onScrape={() => simulateWebScrape(topic)} />
            {uploadedDocs.length > 0 && (
              <div className="px-4 py-2 bg-white/10 text-white rounded-lg flex items-center gap-2 border border-white/30">
                <span className="text-sm">{uploadedDocs.length} docs loaded</span>
              </div>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          {/* Agent Status Panel */}
          <AgentStatus currentAgent={currentAgent} />

          {/* Chat Area */}
          <div className="lg:col-span-3">
            <MessageList 
              messages={messages}
              loading={loading}
              debateActive={debateActive}
              input={input}
              setInput={setInput}
              handleSendMessage={handleSendMessage}
              handleAdmitDefeat={handleAdmitDefeat}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DebateInterface;
