import React from 'react';
import { Upload } from 'lucide-react';

const DocumentUploader = ({ onUpload }) => {
  const handleFileChange = (e) => {
    if (onUpload) {
      onUpload(e);
    }
  };

  return (
    <label className="px-4 py-2 bg-blue-500/30 hover:bg-blue-500/50 text-white rounded-lg cursor-pointer flex items-center gap-2 border border-blue-400/50 transition-all duration-200">
      <Upload className="w-4 h-4" />
      <span className="text-sm">Upload Docs</span>
      <input
        type="file"
        multiple
        className="hidden"
        onChange={handleFileChange}
        accept=".pdf,.txt,.docx"
      />
    </label>
  );
};

export default DocumentUploader;