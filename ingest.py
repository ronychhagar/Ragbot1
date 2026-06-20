"""
Enhanced Document Ingestion
- Better error handling
- Progress tracking
- Batch processing
- Document metadata
"""

import os
from pathlib import Path
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import DOCS_PATH, CHUNK_SIZE, CHUNK_OVERLAP, SEPARATOR, SUPPORTED_FORMATS
from storage.vector_store import get_vector_store
from utils.logger import log_info, log_warning, log_error


def load_documents(docs_path: str = DOCS_PATH) -> List[Document]:
    """Load documents from directory with error handling"""
    docs = []
    docs_dir = Path(docs_path)
    
    if not docs_dir.exists():
        log_warning(f"Documents directory not found: {docs_path}")
        return []
    
    log_info(f"Loading documents from {docs_path}")
    
    for file_path in sorted(docs_dir.iterdir()):
        if not file_path.is_file():
            continue
        
        file_ext = file_path.suffix.lower()
        
        try:
            if file_ext == ".pdf":
                log_info(f"Loading PDF: {file_path.name}")
                loader = PyPDFLoader(str(file_path))
                file_docs = loader.load()
                
                # Add metadata
                for doc in file_docs:
                    doc.metadata["source"] = file_path.name
                    doc.metadata["type"] = "pdf"
                
                docs.extend(file_docs)
            
            elif file_ext in [".txt", ".md"]:
                log_info(f"Loading text file: {file_path.name}")
                loader = TextLoader(str(file_path), encoding='utf-8')
                file_docs = loader.load()
                
                # Add metadata
                for doc in file_docs:
                    doc.metadata["source"] = file_path.name
                    doc.metadata["type"] = file_ext[1:]
                
                docs.extend(file_docs)
        
        except Exception as e:
            log_error(f"Error loading {file_path.name}: {str(e)}")
            continue
    
    log_info(f"Successfully loaded {len(docs)} documents")
    return docs


def chunk_documents(
    documents: List[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[Document]:
    """Split documents into chunks with metadata"""
    
    if not documents:
        log_warning("No documents to chunk")
        return []
    
    log_info(f"Chunking {len(documents)} documents (size={chunk_size}, overlap={chunk_overlap})")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[SEPARATOR, "\n", " ", ""]
    )
    
    try:
        chunks = splitter.split_documents(documents)
        log_info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        return chunks
    
    except Exception as e:
        log_error(f"Error chunking documents: {str(e)}")
        return []


def ingest_documents(docs_path: str = DOCS_PATH) -> dict:
    """
    Complete ingestion pipeline
    Returns summary of ingestion process
    """
    
    log_info("=" * 50)
    log_info("Starting document ingestion pipeline")
    log_info("=" * 50)
    
    # Load documents
    documents = load_documents(docs_path)
    
    if not documents:
        log_warning("No documents found to ingest")
        return {
            "status": "warning",
            "message": "No documents found",
            "documents_loaded": 0,
            "chunks_created": 0,
            "chunks_ingested": 0
        }
    
    # Chunk documents
    chunks = chunk_documents(documents)
    
    if not chunks:
        log_error("Failed to create chunks")
        return {
            "status": "error",
            "message": "Failed to create chunks",
            "documents_loaded": len(documents),
            "chunks_created": 0,
            "chunks_ingested": 0
        }
    
    # Ingest into vector store
    try:
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        
        log_info("=" * 50)
        log_info("✅ Document ingestion completed successfully")
        log_info(f"   - Documents loaded: {len(documents)}")
        log_info(f"   - Chunks created: {len(chunks)}")
        log_info("=" * 50)
        
        return {
            "status": "success",
            "message": "Documents ingested successfully",
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "chunks_ingested": len(chunks)
        }
    
    except Exception as e:
        log_error(f"Failed to ingest documents: {str(e)}")
        return {
            "status": "error",
            "message": f"Ingestion failed: {str(e)}",
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "chunks_ingested": 0
        }


def ingest_single_document(file_path: str) -> dict:
    """Ingest a single document"""
    
    log_info(f"Ingesting single document: {file_path}")
    
    try:
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            log_error(f"File not found: {file_path}")
            return {"status": "error", "message": "File not found"}
        
        # Load document
        if file_path_obj.suffix.lower() == ".pdf":
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        docs = loader.load()
        
        # Add metadata
        for doc in docs:
            doc.metadata["source"] = file_path_obj.name
        
        # Chunk
        chunks = chunk_documents(docs)
        
        # Ingest
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        
        log_info(f"✅ Successfully ingested {file_path}")
        
        return {
            "status": "success",
            "message": f"Ingested {file_path}",
            "chunks": len(chunks)
        }
    
    except Exception as e:
        log_error(f"Error ingesting document: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    result = ingest_documents()
    print(f"\nResult: {result}")
