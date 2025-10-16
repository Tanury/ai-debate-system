"""
Document Processor Service
Handles PDF, DOCX, TXT file processing and extraction
"""

from typing import Dict, Any, List
import PyPDF2
import docx
from io import BytesIO
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Process uploaded documents and extract text
    """
    
    def __init__(self):
        self.max_file_size = settings.MAX_UPLOAD_SIZE
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
    
    async def process_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process a document and extract text"""
        extension = self._get_extension(filename)
        
        if extension not in self.allowed_extensions:
            raise ValueError(f"Unsupported file type: {extension}")
        
        if len(file_content) > self.max_file_size:
            raise ValueError(f"File too large. Maximum size: {self.max_file_size} bytes")
        
        try:
            if extension == '.pdf':
                text = await self._process_pdf(file_content)
            elif extension in ['.docx', '.doc']:
                text = await self._process_docx(file_content)
            elif extension == '.txt':
                text = file_content.decode('utf-8')
            else:
                raise ValueError(f"Unsupported extension: {extension}")
            
            return {
                "filename": filename,
                "text": text,
                "word_count": len(text.split()),
                "char_count": len(text),
                "success": True
            }
        except Exception as e:
            logger.error(f"Error processing document {filename}: {e}")
            return {
                "filename": filename,
                "error": str(e),
                "success": False
            }
    
    async def _process_pdf(self, content: bytes) -> str:
        """Extract text from PDF"""
        pdf_file = BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    async def _process_docx(self, content: bytes) -> str:
        """Extract text from DOCX"""
        doc_file = BytesIO(content)
        doc = docx.Document(doc_file)
        
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    
    def _get_extension(self, filename: str) -> str:
        """Get file extension"""
        return '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    async def process_multiple_documents(
        self, 
        files: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process multiple documents"""
        results = []
        
        for file_data in files:
            content = file_data.get("content")
            filename = file_data.get("filename")
            
            result = await self.process_document(content, filename)
            results.append(result)
        
        return results