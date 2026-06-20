"""
Enhanced Memory Service with Session Management
- Configurable max history
- Context length management
- Memory cleanup
"""

from typing import List, Dict
from config import MAX_CHAT_HISTORY, MAX_CONTEXT_LENGTH
from utils.logger import log_info, log_warning


class ConversationMemory:
    """Enhanced conversation memory with limits"""
    
    def __init__(self, max_history: int = MAX_CHAT_HISTORY):
        """Initialize conversation memory"""
        self.history: List[Dict[str, str]] = []
        self.max_history = max_history
        log_info(f"Chat memory initialized with max_history={max_history}")
    
    def add_message(self, role: str, content: str):
        """Add a message to history"""
        if not content or not content.strip():
            log_warning("Attempted to add empty message")
            return
        
        self.history.append({
            "role": role,
            "content": content.strip()
        })
        
        # Maintain max history limit
        if len(self.history) > self.max_history:
            removed = self.history.pop(0)
            log_warning(f"Removed oldest message due to history limit. Removed: {removed['role']}")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.history.copy()
    
    def get_context_string(self, max_length: int = MAX_CONTEXT_LENGTH) -> str:
        """Get formatted context string with length limit"""
        context_lines = []
        total_length = 0
        
        for message in reversed(self.history):
            line = f"{message['role'].upper()}: {message['content']}"
            line_length = len(line) + 1
            
            if total_length + line_length > max_length:
                log_warning(f"Context truncated at {total_length} chars (limit: {max_length})")
                break
            
            context_lines.insert(0, line)
            total_length += line_length
        
        return "\n".join(context_lines)
    
    def get_last_messages(self, count: int = 5) -> List[Dict[str, str]]:
        """Get last N messages"""
        return self.history[-count:] if self.history else []
    
    def clear(self):
        """Clear all history"""
        self.history = []
        log_info("Chat history cleared")
    
    def get_summary(self) -> Dict:
        """Get memory summary stats"""
        return {
            "total_messages": len(self.history),
            "context_length": len(self.get_context_string()),
            "user_messages": sum(1 for m in self.history if m['role'] == 'user'),
            "assistant_messages": sum(1 for m in self.history if m['role'] == 'assistant')
        }


# Session-based memory management
_session_memories: Dict[str, ConversationMemory] = {}


def get_session_memory(session_id: str) -> ConversationMemory:
    """Get or create memory for a session"""
    if session_id not in _session_memories:
        _session_memories[session_id] = ConversationMemory()
        log_info(f"Created new memory for session: {session_id}")
    return _session_memories[session_id]


def add_message_to_session(session_id: str, role: str, content: str):
    """Add message to session memory"""
    memory = get_session_memory(session_id)
    memory.add_message(role, content)


def get_session_history(session_id: str) -> List[Dict[str, str]]:
    """Get conversation history for session"""
    memory = get_session_memory(session_id)
    return memory.get_history()


def get_session_context(session_id: str) -> str:
    """Get context string for session"""
    memory = get_session_memory(session_id)
    return memory.get_context_string()


def clear_session(session_id: str):
    """Clear history for a session"""
    if session_id in _session_memories:
        _session_memories[session_id].clear()
        del _session_memories[session_id]
        log_info(f"Cleared memory for session: {session_id}")


def cleanup_old_sessions(max_sessions: int = 100):
    """Clean up old sessions if too many exist"""
    if len(_session_memories) > max_sessions:
        keys_to_remove = list(_session_memories.keys())[:-max_sessions]
        for key in keys_to_remove:
            del _session_memories[key]
        log_warning(f"Cleaned up {len(keys_to_remove)} old sessions")


# Legacy support - global memory
global_memory = ConversationMemory()


def add_message(role: str, content: str):
    """Legacy: Add message to global memory"""
    global_memory.add_message(role, content)


def get_history() -> List[Dict[str, str]]:
    """Legacy: Get global history"""
    return global_memory.get_history()
