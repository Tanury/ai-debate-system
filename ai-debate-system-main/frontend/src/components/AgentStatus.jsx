import React from 'react';
import { Shield } from 'lucide-react';

const AgentStatus = ({ currentAgent }) => {
  const agents = [
    'Keyword Extractor',
    'Argument Generator',
    'Counter-Argument Generator',
    'Evaluation Agent'
  ];

  return (
    <div className="lg:col-span-1 space-y-4">
      <div className="card">
        <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
          <Shield className="w-5 h-5 text-green-400" />
          Active Agents
        </h3>
        {agents.map((agent, idx) => (
          <div
            key={idx}
            className={`p-3 mb-2 rounded-lg transition-all ${
              currentAgent === agent
                ? 'bg-purple-500/50 border-2 border-purple-400'
                : 'bg-white/5'
            }`}
          >
            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  currentAgent === agent ? 'bg-green-400 animate-pulse' : 'bg-gray-500'
                }`}
              />
              <span className="text-white text-sm">{agent}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3 className="text-white font-semibold mb-3">Security Features</h3>
        <div className="space-y-2 text-sm text-white/70">
          {['Input Sanitization', 'Rate Limiting', 'Content Moderation', 'Encrypted Storage'].map(
            (feature, idx) => (
              <div key={idx} className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full" />
                <span>{feature}</span>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentStatus;