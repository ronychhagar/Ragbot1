"""
Enhanced RAG Engine with Improved Prompting and Error Handling
- Better system prompts
- Multi-strategy retrieval
- Answer validation
- Source attribution
"""

from typing import Dict, List, Tuple, Optional
from langchain_core.prompts import ChatPromptTemplate
from storage.vector_store import get_vector_store
from services.llm_service import get_llm
from services.memory_service import get_session_memory
from config import TOP_K, SIMILARITY_THRESHOLD, MAX_CONTEXT_LENGTH
from utils.logger import log_info, log_warning, log_error


# =====================================================
# System Prompts
# =====================================================
SYSTEM_PROMPT = """You are an intelligent AI assistant with access to a knowledge base.

Guidelines:
1. Always consider the provided context when answering questions
2. Be accurate and cite sources when available
3. If the context doesn't contain relevant information, say so clearly
4. Provide clear, concise, and helpful answers
5. If unsure, ask clarifying questions rather than guessing
6. Structure your response with headings and bullet points when appropriate"""

RAG_PROMPT = ChatPromptTemplate.from_template("""
{system_prompt}

Context from knowledge base:
{context}

Previous conversation context:
{history}

User Query:
{question}

Answer based on the provided context. If the context is insufficient, acknowledge this and provide general knowledge if applicable.
""")

SUMMARY_PROMPT = ChatPromptTemplate.from_template("""
Summarize the following information in 2-3 sentences:

{text}
""")


class RAGEngine:
    """Enhanced RAG Engine with multiple retrieval strategies"""
    
    def __init__(self, session_id: str = "default"):
        """Initialize RAG engine"""
        self.session_id = session_id
        self.vector_store = get_vector_store()
        self.llm = get_llm()
        self.memory = get_session_memory(session_id)
        log_info(f"RAG Engine initialized for session: {session_id}")
    
    def retrieve_context(
        self,
        query: str,
        k: int = TOP_K,
        use_scoring: bool = True
    ) -> Tuple[List, List[Tuple[float, str]]]:
        """
        Retrieve relevant documents with confidence scores
        Returns: (documents, scores_with_sources)
        """
        try:
            if use_scoring:
                # Use similarity scoring with threshold filtering
                results = self.vector_store.similarity_search_with_score(query, k=k)
                
                if not results:
                    log_warning(f"No documents found above threshold for: {query}")
                    return [], []
                
                scores = [(score, doc.page_content[:100]) for doc, score in results]
                docs = [doc for doc, _ in results]
            else:
                # Simple similarity search
                docs = self.vector_store.similarity_search(query, k=k)
                scores = [(0.8, doc.page_content[:100]) for doc in docs]
            
            log_info(f"Retrieved {len(docs)} documents for query")
            return docs, scores
        
        except Exception as e:
            log_error(f"Error retrieving context: {str(e)}")
            return [], []
    
    def format_context(self, documents: List) -> str:
        """Format retrieved documents as context"""
        if not documents:
            return "No relevant documents found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Unknown") if doc.metadata else "Unknown"
            context_parts.append(f"Source {i} ({source}):\n{doc.page_content}")
        
        # Limit total context length
        context = "\n\n".join(context_parts)
        if len(context) > MAX_CONTEXT_LENGTH:
            context = context[:MAX_CONTEXT_LENGTH] + "..."
            log_warning(f"Context truncated to {MAX_CONTEXT_LENGTH} characters")
        
        return context
    
    def ask(self, question: str, use_memory: bool = True) -> Dict:
        """
        Ask a question using RAG
        Returns: {answer, sources, confidence}
        """
        try:
            log_info(f"Processing question: {question}")
            
            # Retrieve context
            documents, scores = self.retrieve_context(question)
            context = self.format_context(documents)
            
            # Get conversation history
            history = self.memory.get_context_string() if use_memory else ""
            
            # Format and invoke prompt
            prompt = RAG_PROMPT.format(
                system_prompt=SYSTEM_PROMPT,
                context=context,
                history=history,
                question=question
            )
            
            # Get response
            response = self.llm.invoke(prompt)
            
            # Store in memory
            if use_memory:
                self.memory.add_message("user", question)
                self.memory.add_message("assistant", response)
            
            # Prepare result
            result = {
                "answer": response,
                "sources": [
                    {"content": score[1], "confidence": float(score[0])}
                    for score in scores
                ],
                "num_sources": len(documents),
                "success": True
            }
            
            log_info("Successfully answered question")
            return result
        
        except Exception as e:
            log_error(f"Error in ask: {str(e)}")
            return {
                "answer": f"Error processing question: {str(e)}",
                "sources": [],
                "success": False
            }
    
    def ask_follow_up(self, question: str) -> Dict:
        """Ask a follow-up question with conversation context"""
        return self.ask(question, use_memory=True)
    
    def summarize(self, text: str) -> str:
        """Summarize text using LLM"""
        try:
            prompt = SUMMARY_PROMPT.format(text=text[:2000])  # Limit input
            summary = self.llm.invoke(prompt)
            return summary
        except Exception as e:
            log_error(f"Error summarizing: {str(e)}")
            return f"Error summarizing: {str(e)}"
    
    def clear_memory(self):
        """Clear session memory"""
        self.memory.clear()
        log_info(f"Cleared memory for session: {self.session_id}")
    
    def get_memory_summary(self) -> Dict:
        """Get memory statistics"""
        return self.memory.get_summary()


# Global RAG engine instances per session
_rag_engines: Dict[str, RAGEngine] = {}


def get_rag_engine(session_id: str = "default") -> RAGEngine:
    """Get or create RAG engine for session"""
    if session_id not in _rag_engines:
        _rag_engines[session_id] = RAGEngine(session_id)
    return _rag_engines[session_id]


# Convenience functions for backward compatibility
def ask_hybrid(question: str, session_id: str = "default") -> str:
    """Ask a question using hybrid RAG (backward compatible)"""
    engine = get_rag_engine(session_id)
    result = engine.ask(question)
    return result["answer"]


def ask_with_sources(question: str, session_id: str = "default") -> Dict:
    """Ask a question and get sources"""
    engine = get_rag_engine(session_id)
    return engine.ask(question)


def clear_session(session_id: str = "default"):
    """Clear session memory"""
    if session_id in _rag_engines:
        _rag_engines[session_id].clear_memory()
