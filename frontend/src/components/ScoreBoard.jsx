import React from 'react';
import { Trophy, Bot } from 'lucide-react';

const ScoreBoard = ({ score, roundNumber }) => {
  return (
    <div className="flex gap-4 text-white items-center">
      <div className="text-center bg-white/10 px-4 py-2 rounded-lg">
        <div className="text-xs text-purple-300">Round</div>
        <div className="text-2xl font-bold">{roundNumber}</div>
      </div>
      <div className="text-center">
        <Trophy className="w-6 h-6 mx-auto text-yellow-400" />
        <div className="text-2xl font-bold">{score.human}</div>
        <div className="text-xs">Human</div>
      </div>
      <div className="text-center">
        <Bot className="w-6 h-6 mx-auto text-blue-400" />
        <div className="text-2xl font-bold">{score.ai}</div>
        <div className="text-xs">AI</div>
      </div>
    </div>
  );
};

export default ScoreBoard;