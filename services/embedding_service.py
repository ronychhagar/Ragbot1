"""
Embeddings Service using Sentence Transformers
- Supports multiple embedding models
- Caching of embeddings
"""

from functools import lru_cache

try:
    # Try the newer langchain-huggingface package first
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    # Fallback to the deprecated package (will show warning)
    from langchain_community.embeddings import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL
from utils.logger import log_info

# Initialize embeddings with explicit model
_embeddings = None


def get_embeddings():
    """Get or create embeddings instance (singleton with caching)"""
    global _embeddings
    if _embeddings is None:
        log_info(f"Initializing embeddings with model: {EMBEDDING_MODEL}")
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings

