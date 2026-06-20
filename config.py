"""
Enhanced Configuration Management for RAG Bot
- Environment variable support
- Type validation
- Sensible defaults
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =====================================================
# LLM Configuration
# =====================================================
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
LLM_TOP_P = float(os.getenv("LLM_TOP_P", 0.9))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 2048))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", 60))
LLM_RETRY_ATTEMPTS = int(os.getenv("LLM_RETRY_ATTEMPTS", 3))

# =====================================================
# Vector Database Configuration
# =====================================================
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", 384))

# =====================================================
# RAG Configuration
# =====================================================
TOP_K = int(os.getenv("TOP_K", 5))  # Number of documents to retrieve
TOP_K_RERANK = int(os.getenv("TOP_K_RERANK", 3))  # After reranking
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.5))

# Document chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1024))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
SEPARATOR = os.getenv("CHUNK_SEPARATOR", "\n\n")

# =====================================================
# Document Loading Configuration
# =====================================================
DOCS_PATH = os.getenv("DOCS_PATH", "data")
SUPPORTED_FORMATS = [".pdf", ".txt", ".md", ".docx"]

# =====================================================
# Chat Configuration
# =====================================================
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", 20))
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", 4000))
ENABLE_MEMORY = os.getenv("ENABLE_MEMORY", "true").lower() == "true"

# =====================================================
# Performance Configuration
# =====================================================
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # Cache TTL in seconds
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 32))

# =====================================================
# Logging Configuration
# =====================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "rag_bot.log")
ENABLE_FILE_LOGGING = os.getenv("ENABLE_FILE_LOGGING", "true").lower() == "true"

# =====================================================
# Validation
# =====================================================
def validate_config():
    """Validate configuration values"""
    assert 0 <= LLM_TEMPERATURE <= 2, "LLM_TEMPERATURE must be between 0 and 2"
    assert 0 <= LLM_TOP_P <= 1, "LLM_TOP_P must be between 0 and 1"
    assert CHUNK_SIZE > 0, "CHUNK_SIZE must be positive"
    assert CHUNK_OVERLAP < CHUNK_SIZE, "CHUNK_OVERLAP must be less than CHUNK_SIZE"
    assert TOP_K > 0, "TOP_K must be positive"
    assert MAX_CHAT_HISTORY > 0, "MAX_CHAT_HISTORY must be positive"
    
    # Create necessary directories
    Path(VECTOR_DB_PATH).mkdir(parents=True, exist_ok=True)
    Path(DOCS_PATH).mkdir(parents=True, exist_ok=True)

# Validate on import
validate_config()
