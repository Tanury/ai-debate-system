import React from 'react';
import { Globe } from 'lucide-react';

const WebScrapeTool = ({ onScrape }) => {
  return (
    <button
      onClick={onScrape}
      className="px-4 py-2 bg-green-500/30 hover:bg-green-500/50 text-white rounded-lg flex items-center gap-2 border border-green-400/50 transition-all duration-200"
    >
      <Globe className="w-4 h-4" />
      <span className="text-sm">Web Scrape</span>
    </button>
  );
};

export default WebScrapeTool;