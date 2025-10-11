"""
Information Retrieval Service
Handles document retrieval, vector search, and relevance ranking
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from app.config import settings
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

class InformationRetrieval:
    """
    Vector-based information retrieval system
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.VECTOR_STORE_PATH
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="debate_knowledge",
            metadata={"description": "Knowledge base for debate system"}
        )
        
        self.document_count = 0
    
    async def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector store"""
        try:
            for doc in documents:
                content = doc.get("content", "")
                metadata = doc.get("metadata", {})
                
                # Generate embedding
                embedding = await self.llm_service.embed(content)
                
                # Add to collection
                self.collection.add(
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[metadata],
                    ids=[f"doc_{self.document_count}"]
                )
                self.document_count += 1
                
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
    
    async def retrieve(
        self, 
        query: str, 
        keywords: List[str] = None,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents based on query"""
        try:
            # Enhance query with keywords
            enhanced_query = query
            if keywords:
                enhanced_query = f"{query} {' '.join(keywords[:3])}"
            
            # Generate query embedding
            query_embedding = await self.llm_service.embed(enhanced_query)
            
            # Search collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=max_results
            )
            
            # Format results
            retrieved_docs = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    retrieved_docs.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0,
                        "relevance_score": 1 - (results['distances'][0][i] if results['distances'] else 0)
                    })
            
            return retrieved_docs
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return []
    
    def clear_collection(self) -> None:
        """Clear all documents from collection"""
        try:
            self.client.delete_collection("debate_knowledge")
            self.collection = self.client.create_collection("debate_knowledge")
            self.document_count = 0
            logger.info("Cleared vector store")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
