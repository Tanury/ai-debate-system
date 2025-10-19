"""
Document Upload and Processing Routes
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from app.services.document_processor import DocumentProcessor
from app.services.information_retrieval import InformationRetrieval
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload")
async def upload_documents(
    files: List[UploadFile] = File(...),
    processor: DocumentProcessor = Depends(),
    ir_service: InformationRetrieval = Depends()
):
    """Upload and process documents for debate knowledge base"""
    
    results = []
    
    for file in files:
        try:
            content = await file.read()
            
            # Process document
            result = await processor.process_document(content, file.filename)
            
            if result["success"]:
                # Add to vector store
                await ir_service.add_documents([{
                    "content": result["text"],
                    "metadata": {
                        "filename": file.filename,
                        "word_count": result["word_count"]
                    }
                }])
            
            results.append(result)
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {e}")
            results.append({
                "filename": file.filename,
                "error": str(e),
                "success": False
            })
    
    return {"results": results, "total": len(files), "successful": sum(1 for r in results if r["success"])}

