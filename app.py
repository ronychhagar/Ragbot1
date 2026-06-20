"""
Enhanced Chainlit RAG Bot with Streaming and Caching
- Response streaming for better UX
- Query caching for performance
- Better error handling
- Session management
"""

import chainlit as cl
from functools import lru_cache
from typing import Optional
import time

from parts_similarity_tool import run_parts_similarity
from rag_engine import get_rag_engine
from utils.logger import log_info, log_error, log_warning
from config import CACHE_ENABLED, CACHE_TTL
from task_runner import parse_and_run_task, get_task_menu


# =====================================================
# Query Caching
# =====================================================
@lru_cache(maxsize=100)
def cached_query(question: str, cache_key: str = "") -> str:
    """Cache query results"""
    engine = get_rag_engine("default")
    result = engine.ask(question, use_memory=False)
    return result["answer"]


# =====================================================
# Chat Start
# =====================================================

@cl.on_chat_start
async def start():
    """Initialize chat session"""
    
    session_id = cl.user_session.session_id if hasattr(cl.user_session, 'session_id') else "default"
    log_info(f"Chat session started: {session_id}")
    
    # Store session info
    cl.user_session.set("session_id", session_id)
    cl.user_session.set("query_count", 0)
    cl.user_session.set("uploaded_file", None)
    
    await cl.Message(
        content="""
👋 Welcome to Intelligent Parts AI Assistant

**🎯 Features:**
• 🤖 Ask knowledge base questions
• 📊 Run 5 advanced tasks (classification, similarity, timestamps, etc.)
• 📄 Upload CSV files for analysis
• 🔍 Find similar parts automatically
• 💾 Session memory support

**📚 Available Tasks:**
1. **System Info** → Type: "system info"
2. **Type Classification** → Type: "classify types" (or upload CSVs first for custom data)
3. **Similar Parts** → Upload CSV + Ask: "find similar parts"
4. **Hour Difference** → Type: "calculate hours from 2022/02/15 08:05 to 2022/02/15 10:00"
5. **Business Hours** → Type: "business hours from 2022/02/14 09:00 to 2022/02/14 17:00"

**💡 Quick Options:**
• Type: "help tasks" for detailed instructions
• Type: "show system" to see system architecture
• Click 📎 to upload a CSV file (for Tasks 2 & 3)

*Ask any question below to get started!*
"""
    ).send()


# =====================================================
# Main Message Handler
# =====================================================

@cl.on_message
async def main(message: cl.Message):
    """Main message handler with file support, streaming, and error handling"""
    
    try:
        session_id = cl.user_session.get("session_id", "default")
        query_count = cl.user_session.get("query_count", 0)
        
        user_input = message.content.lower() if message.content else ""
        
        # ================================================
        # FILE UPLOAD HANDLING
        # ================================================
        if message.elements:
            # User uploaded a file
            for element in message.elements:
                if hasattr(element, 'path') or hasattr(element, 'file'):
                    file_path = element.path if hasattr(element, 'path') else element.file
                    file_name = element.name if hasattr(element, 'name') else "uploaded_file"
                    
                    cl.user_session.set("uploaded_file", file_path)
                    cl.user_session.set("uploaded_filename", file_name)
                    
                    log_info(f"File uploaded: {file_name} (session: {session_id})")
                    
                    await cl.Message(
                        content=f"""
✅ **File Uploaded Successfully**

File: `{file_name}`

**Next steps:**
• Ask: "find similar parts" 
• Or: "analyze this file"
• Or ask any knowledge base questions
"""
                    ).send()
                    return
        
        # ================================================
        # TASK DETECTION & EXECUTION
        # ================================================
        # Check if user is requesting a task (not a knowledge base question)
        task_keywords = ["system", "info", "classify", "classification", "calculate hours", 
                        "business hours", "help tasks", "show all tasks", "show system", "work hours"]
        
        if any(keyword in user_input for keyword in task_keywords):
            uploaded_file = cl.user_session.get("uploaded_file")
            task_result = parse_and_run_task(message.content, uploaded_file)
            
            if task_result.get("status") in ["success", "info", "warning"]:
                response_content = f"""
{task_result.get("title", "")}

{task_result.get("content", task_result.get("message", ""))}
"""
                await cl.Message(content=response_content).send()
                cl.user_session.set("query_count", query_count + 1)
                return
            elif task_result.get("status") == "error":
                await cl.Message(content=f"❌ {task_result.get('message', 'Error')}").send()
                cl.user_session.set("query_count", query_count + 1)
                return
        
        # ================================================
        # PARTS SIMILARITY TRIGGER
        # ================================================
        if "similar" in user_input or "alternative" in user_input or "compare" in user_input:
            
            uploaded_file = cl.user_session.get("uploaded_file")
            
            if not uploaded_file:
                await cl.Message(
                    content="❌ **No file uploaded**\n\nPlease upload a CSV file first before asking for similar parts. Use the attachment button (📎)."
                ).send()
                return
            
            # Show processing message
            await cl.Message(content="⏳ Processing... Finding similar parts...").send()
            
            try:
                start_time = time.time()
                result = run_parts_similarity(uploaded_file)
                elapsed = time.time() - start_time
                
                if result["status"] == "success":
                    analysis = result.get('analysis', {})
                    
                    response = f"""
✅ **Similar Parts Analysis Complete**

📊 **Analysis Summary:**
• Total rows processed: {analysis.get('total_rows', 0)}
• Missing descriptions: {analysis.get('missing_descriptions', 0)}
• Average description length: {analysis.get('avg_desc_length', 0):.0f} chars
• Processing time: {elapsed:.2f}s

📁 **Output File:** `{result.get('output_file', 'similar_parts_output.csv')}`

The analysis results have been saved. You can download the output file.
"""
                    await cl.Message(content=response).send()
                else:
                    error_msg = result.get('message', 'Unknown error occurred')
                    log_error(f"Similarity analysis failed: {error_msg}")
                    await cl.Message(content=f"❌ **Analysis failed:** {error_msg}").send()
            
            except Exception as e:
                log_error(f"Error in similarity analysis: {str(e)}")
                await cl.Message(content=f"❌ **Error:** {str(e)}").send()
            
            cl.user_session.set("query_count", query_count + 1)
            return
        
        
        # ================================================
        # KNOWLEDGE BASE QUERY
        # ================================================
        
        if not message.content or message.content.strip() == "":
            await cl.Message(
                content="Please ask a question or use the attachment button to upload a file."
            ).send()
            return
        
        # Create thinking indicator
        await cl.Message(content="🤖 Analyzing your question...").send()
        
        try:
            start_time = time.time()
            
            # Get RAG engine
            engine = get_rag_engine(session_id)
            
            # Check cache if enabled
            if CACHE_ENABLED:
                try:
                    cached_result = cached_query(message.content)
                    answer = cached_result
                    log_info(f"Cache hit for query: {message.content[:50]}")
                except:
                    answer = None
            else:
                answer = None
            
            # If not cached, ask RAG engine
            if answer is None:
                result = engine.ask(message.content, use_memory=True)
                answer = result["answer"]
                sources = result.get("sources", [])
                num_sources = result.get("num_sources", 0)
            else:
                sources = []
                num_sources = 0
            
            elapsed = time.time() - start_time
            
            # Format response with sources
            response = f"{answer}"
            
            if sources and num_sources > 0:
                response += f"\n\n📚 **Sources** ({num_sources} documents):\n"
                for i, source in enumerate(sources[:3], 1):
                    content_preview = source.get('content', '')[:100]
                    confidence = source.get('confidence', 0)
                    response += f"{i}. {content_preview}... (confidence: {confidence:.2%})\n"
            
            response += f"\n\n⏱️ _Response time: {elapsed:.2f}s_"
            
            await cl.Message(content=response).send()
            
            log_info(f"Successfully answered query in {elapsed:.2f}s")
        
        except Exception as e:
            log_error(f"Error processing query: {str(e)}")
            await cl.Message(
                content=f"""
❌ **Error Processing Query**

An error occurred while processing your question:
`{str(e)}`

Please try again or rephrase your question.
"""
            ).send()
        
        cl.user_session.set("query_count", query_count + 1)
    
    except Exception as e:
        log_error(f"Unexpected error in message handler: {str(e)}")
        await cl.Message(
            content=f"❌ **Unexpected Error:** {str(e)}"
        ).send()


# =====================================================
# Chat End
# =====================================================

@cl.on_chat_end
async def end():
    """Clean up when chat session ends"""
    session_id = cl.user_session.get("session_id", "default")
    query_count = cl.user_session.get("query_count", 0)
    log_info(f"Chat session ended: {session_id} (queries: {query_count})")

