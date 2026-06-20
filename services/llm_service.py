"""
Enhanced LLM Service with Retry Logic and Streaming
- Automatic retry with exponential backoff
- Streaming support for long responses
- Error handling and logging
- Response validation
"""

import time
from typing import Generator, Optional
from langchain_ollama import ChatOllama
from langchain_core.exceptions import LangChainException
from config import (
    LLM_MODEL, LLM_TEMPERATURE, LLM_TOP_P, 
    LLM_MAX_TOKENS, LLM_TIMEOUT, LLM_RETRY_ATTEMPTS
)
from utils.logger import log_error, log_info, log_exception


class LLMService:
    """Enhanced LLM service with retry logic and streaming"""
    
    def __init__(self):
        """Initialize LLM service"""
        self.llm = ChatOllama(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            top_p=LLM_TOP_P,
            num_predict=LLM_MAX_TOKENS,
            timeout=LLM_TIMEOUT
        )
        self.retry_attempts = LLM_RETRY_ATTEMPTS
        self.base_backoff = 1  # seconds
        log_info(f"LLM Service initialized with model: {LLM_MODEL}")
    
    def _invoke_with_retry(self, prompt: str, attempt: int = 0) -> Optional[str]:
        """Invoke LLM with exponential backoff retry logic"""
        try:
            response = self.llm.invoke(prompt)
            return response.content
        
        except LangChainException as e:
            log_error(f"LLM error (attempt {attempt + 1}/{self.retry_attempts}): {str(e)}")
            
            if attempt < self.retry_attempts - 1:
                wait_time = self.base_backoff * (2 ** attempt)
                log_info(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
                return self._invoke_with_retry(prompt, attempt + 1)
            else:
                log_exception("Max retry attempts reached")
                raise
        
        except Exception as e:
            log_exception(f"Unexpected error during LLM invocation: {str(e)}")
            raise
    
    def invoke(self, prompt: str) -> str:
        """Synchronous LLM invocation"""
        try:
            response = self._invoke_with_retry(prompt)
            
            if not response or response.strip() == "":
                log_error("Empty response from LLM")
                return "I couldn't generate a response. Please try again."
            
            return response
        
        except Exception as e:
            log_error(f"Failed to invoke LLM: {str(e)}")
            return f"Error: Unable to process your request. {str(e)}"
    
    def stream(self, prompt: str) -> Generator[str, None, None]:
        """Stream LLM response tokens"""
        try:
            for chunk in self.llm.stream(prompt):
                if hasattr(chunk, 'content'):
                    yield chunk.content
                else:
                    yield str(chunk)
        
        except Exception as e:
            log_exception(f"Error during streaming: {str(e)}")
            yield f"Error: {str(e)}"
    
    def batch_invoke(self, prompts: list[str]) -> list[str]:
        """Batch invocation for multiple prompts"""
        results = []
        for i, prompt in enumerate(prompts):
            try:
                log_info(f"Processing batch {i + 1}/{len(prompts)}")
                result = self.invoke(prompt)
                results.append(result)
            except Exception as e:
                log_error(f"Batch processing error for item {i}: {str(e)}")
                results.append(f"Error: {str(e)}")
        
        return results


# Global LLM service instance
_llm_service = None


def get_llm() -> LLMService:
    """Get or create LLM service instance (singleton)"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def invoke_llm(prompt: str) -> str:
    """Convenience function to invoke LLM"""
    service = get_llm()
    return service.invoke(prompt)


def stream_llm(prompt: str) -> Generator[str, None, None]:
    """Convenience function to stream LLM response"""
    service = get_llm()
    return service.stream(prompt)
