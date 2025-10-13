"""
Vector Store Service
Wrapper around ChromaDB for embeddings and similarity search
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    """
    Vector database operations using ChromaDB
    """
    
    def __init__(self, collection_name: str = "debate_knowledge"):
        """Initialize vector store"""
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.VECTOR_STORE_PATH
        ))
        
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Knowledge base for AI debate system"}
        )
        
        logger.info(f"Vector store initialized: {collection_name}")
    
    def add_documents(
        self, 
        documents: List[str], 
        embeddings: List[List[float]], 
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """
        Add documents with embeddings to the vector store
        
        Args:
            documents: List of text documents
            embeddings: List of embedding vectors
            metadatas: List of metadata dicts
            ids: List of unique document IDs
        """
        try:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def query(
        self, 
        query_embeddings: List[List[float]], 
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query the vector store for similar documents
        
        Args:
            query_embeddings: Query embedding vectors
            n_results: Number of results to return
            where: Metadata filter conditions
            
        Returns:
            Query results with documents, distances, metadatas
        """
        try:
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=where
            )
            return results
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")
            return {"documents": [], "distances": [], "metadatas": []}
    
    def delete(self, ids: List[str]) -> None:
        """Delete documents by IDs"""
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents")
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
    
    def count(self) -> int:
        """Get total document count"""
        return self.collection.count()
    
    def clear(self) -> None:
        """Clear all documents from collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(self.collection_name)
            logger.info("Vector store cleared")
        except Exception as e:
            logger.error(f"Error clearing vector store: {e}")