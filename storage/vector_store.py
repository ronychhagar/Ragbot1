"""
Enhanced Vector Store with Metadata and Filtering
- Metadata support for document tracking
- Similarity filtering
- Batch operations
"""

from typing import List, Optional
try:
    # Try newer langchain-chroma first
    from langchain_chroma import Chroma
except ImportError:
    # Fallback to older langchain-community version
    from langchain_community.vectorstores import Chroma

from langchain_core.documents import Document
from config import VECTOR_DB_PATH, TOP_K, SIMILARITY_THRESHOLD
from services.embedding_service import get_embeddings
from utils.logger import log_info, log_warning, log_error


class EnhancedVectorStore:
    """Enhanced vector store with metadata and filtering"""
    
    def __init__(self):
        """Initialize vector store"""
        self.db = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=get_embeddings()
        )
        log_info(f"Vector store initialized at {VECTOR_DB_PATH}")
    
    def add_documents(self, documents: List[Document], metadata: Optional[dict] = None):
        """Add documents with metadata"""
        try:
            # Add metadata to documents if provided
            if metadata:
                for doc in documents:
                    if not doc.metadata:
                        doc.metadata = {}
                    doc.metadata.update(metadata)
            
            self.db.add_documents(documents)
            self.db.persist()
            log_info(f"Added {len(documents)} documents to vector store")
        
        except Exception as e:
            log_error(f"Error adding documents: {str(e)}")
            raise
    
    def similarity_search(
        self,
        query: str,
        k: int = TOP_K,
        filter_metadata: Optional[dict] = None
    ) -> List[Document]:
        """Search with optional metadata filtering"""
        try:
            # Perform similarity search
            docs = self.db.similarity_search(query, k=k * 2)  # Get more to filter
            
            # Filter by metadata if provided
            if filter_metadata:
                filtered_docs = []
                for doc in docs:
                    if self._matches_metadata(doc, filter_metadata):
                        filtered_docs.append(doc)
                docs = filtered_docs[:k]
            else:
                docs = docs[:k]
            
            if not docs:
                log_warning(f"No documents found for query: {query}")
            
            return docs
        
        except Exception as e:
            log_error(f"Error during similarity search: {str(e)}")
            return []
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = TOP_K,
        score_threshold: float = SIMILARITY_THRESHOLD
    ) -> List[tuple[Document, float]]:
        """Search with similarity scores and threshold filtering"""
        try:
            results = self.db.similarity_search_with_relevance_scores(query, k=k * 2)
            
            # Filter by score threshold
            filtered = [(doc, score) for doc, score in results if score >= score_threshold]
            
            if not filtered:
                log_warning(f"No documents above score threshold ({score_threshold})")
            
            return filtered[:k]
        
        except Exception as e:
            log_error(f"Error during scored search: {str(e)}")
            return []
    
    def get_as_retriever(self, k: int = TOP_K, **kwargs):
        """Get retriever object"""
        search_kwargs = {"k": k}
        search_kwargs.update(kwargs)
        return self.db.as_retriever(search_kwargs=search_kwargs)
    
    def _matches_metadata(self, doc: Document, filter_metadata: dict) -> bool:
        """Check if document matches metadata filter"""
        if not doc.metadata:
            return False
        
        for key, value in filter_metadata.items():
            if key not in doc.metadata or doc.metadata[key] != value:
                return False
        
        return True
    
    def delete_documents(self, ids: List[str]):
        """Delete documents by ID"""
        try:
            self.db.delete(ids)
            self.db.persist()
            log_info(f"Deleted {len(ids)} documents from vector store")
        
        except Exception as e:
            log_error(f"Error deleting documents: {str(e)}")
            raise
    
    def get_collection_info(self) -> dict:
        """Get vector store collection info"""
        try:
            collection = self.db._collection if hasattr(self.db, '_collection') else None
            if collection:
                return {
                    "count": collection.count(),
                    "name": collection.name if hasattr(collection, 'name') else "unknown"
                }
            return {"count": 0, "name": "unknown"}
        except Exception as e:
            log_warning(f"Could not get collection info: {str(e)}")
            return {"count": 0, "name": "unknown"}


# Global vector store instance
_vector_store = None


def get_vector_store() -> EnhancedVectorStore:
    """Get or create vector store instance (singleton)"""
    global _vector_store
    if _vector_store is None:
        _vector_store = EnhancedVectorStore()
    return _vector_store


def get_retriever(k: int = TOP_K, **kwargs):
    """Get retriever from vector store"""
    store = get_vector_store()
    return store.get_as_retriever(k=k, **kwargs)
