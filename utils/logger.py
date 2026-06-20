"""
Enhanced Structured Logging for RAG Bot
- File and console logging
- Structured log formatting
- Performance tracking
"""

import logging
import os
import json
from pathlib import Path
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE, ENABLE_FILE_LOGGING


# Create logs directory
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)

# =====================================================
# Structured Formatter
# =====================================================
class StructuredFormatter(logging.Formatter):
    """Structured JSON logging formatter"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


# =====================================================
# Logger Configuration
# =====================================================
def get_logger(name: str) -> logging.Logger:
    """Get or create a logger with structured formatting"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if enabled)
    if ENABLE_FILE_LOGGING:
        file_path = log_dir / LOG_FILE
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        file_formatter = StructuredFormatter()
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


# Main logger instance
logger = get_logger("rag_bot")


# =====================================================
# Convenience functions
# =====================================================
def log_debug(msg: str, **kwargs):
    """Log debug message"""
    logger.debug(msg, extra=kwargs)

def log_info(msg: str, **kwargs):
    """Log info message"""
    logger.info(msg, extra=kwargs)

def log_warning(msg: str, **kwargs):
    """Log warning message"""
    logger.warning(msg, extra=kwargs)

def log_error(msg: str, **kwargs):
    """Log error message"""
    logger.error(msg, extra=kwargs)

def log_exception(msg: str, **kwargs):
    """Log exception message"""
    logger.exception(msg, extra=kwargs)
