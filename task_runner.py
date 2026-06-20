"""
Task Runner - Unified interface for all 5 tasks callable from chatbot
This module provides a simple interface to call any of the 5 tasks from the Chainlit UI
"""

import os
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime

from utils.logger import log_info, log_error, log_warning


# =====================================================
# Task 1: Chatbot System Info
# =====================================================

def run_task1_chatbot_info() -> Dict[str, Any]:
    """Task 1: Return chatbot system information"""
    try:
        return {
            "status": "success",
            "title": "🤖 Chatbot System Information",
            "content": """
## System Architecture

**LLM Model**: Mistral 7B (via Ollama)
**Vector DB**: Chroma with Sentence Transformers
**Interface**: Chainlit Web UI
**Architecture**: Modular RAG system

### Key Features:
- ✅ Local LLM inference (100% offline/private)
- ✅ Semantic search with embeddings
- ✅ Session-based conversation memory
- ✅ Query caching for performance
- ✅ Multi-format document support
- ✅ Source attribution

### Hardware Requirements:
- **RAM**: 16GB minimum (8GB with GPU)
- **CPU**: 4+ cores
- **Storage**: 5-10GB for models
- **GPU**: Optional (NVIDIA/AMD/Apple Silicon)

### Performance:
- Query latency: 100-1000ms (depends on hardware)
- Vector search: 50-200ms
- Memory per session: ~10MB

### Deployment:
Start with: `chainlit run app.py`
Requires: Ollama running (`ollama serve`)

See `task1_chatbot_system.py` for full documentation.
"""
        }
    except Exception as e:
        log_error(f"Error in task1_chatbot_info: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to get system info: {str(e)}"
        }


# =====================================================
# Task 2: Type Classification
# =====================================================

def run_task2_classification(data_path: str = "data/", uploaded_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Task 2: Run binary type classification on CSV data
    
    Can use either:
    1. Files from data/ directory (table_1.csv + table_2.csv)
    2. Single uploaded CSV file (will be used as merged data)
    3. Check if user has uploaded files in session
    """
    try:
        import pandas as pd
        from task2_type_classification import TypeClassifier
        
        log_info("Starting Task 2: Type Classification")
        
        classifier = TypeClassifier(data_path)
        
        # Try to load and analyze data
        try:
            # If uploaded file provided, use it directly
            if uploaded_file:
                log_info(f"Using uploaded file: {uploaded_file}")
                try:
                    df = pd.read_csv(uploaded_file)
                    log_info(f"Loaded uploaded CSV: {len(df)} rows")
                except Exception as e:
                    return {
                        "status": "error",
                        "message": f"Could not read uploaded file: {str(e)}\n\nPlease upload a valid CSV file."
                    }
            else:
                # Try to load from data/ directory
                df = classifier.load_and_merge_data("table_1.csv", "table_2.csv")
                log_info(f"Loaded files from data/: {len(df)} rows")
            
            analysis = classifier.analyze_type_column(df)
            
            # Prepare data
            X_train, X_test, y_train, y_test = classifier.prepare_data(df)
            
            # Train classifier
            classifier.train_classifier(X_train, y_train)
            
            # Evaluate
            metrics = classifier.evaluate_classifier(X_test, y_test)
            
            # Save model
            classifier.save_model("type_classifier.pkl")
            
            data_source = "uploaded file" if uploaded_file else "data/ directory"
            
            return {
                "status": "success",
                "title": "✅ Type Classification Complete",
                "content": f"""
### Classification Results:

**Data Source:** {data_source}

**Data Summary:**
- Total rows: {len(df)}
- Type distribution: {analysis.get('type_distribution', {})}
- Missing values: {analysis.get('missing_count', 0)}
- Is binary: {analysis.get('is_binary', False)}

**Model Performance:**
- Accuracy: {metrics['accuracy']:.2%}
- Precision: {metrics['precision']:.2%}
- Recall: {metrics['recall']:.2%}
- F1 Score: {metrics['f1']:.2%}

**Model Saved:** `type_classifier.pkl`

See `task2_type_classification.py` for details.
"""
            }
        except FileNotFoundError as e:
            return {
                "status": "warning",
                "title": "💡 Data Files Not Found (But You Can Upload!)",
                "message": f"""Please choose one of these options:

**Option 1: Upload CSV Files**
1. Click 📎 attachment button
2. Upload your CSV files (table_1.csv and table_2.csv)
3. Type: "classify types"
4. The chatbot will use your uploaded files

**Option 2: Add Files to Directory**
Place these files in the `{data_path}` directory:
- table_1.csv
- table_2.csv

Then type: "classify types"
"""
            }
    
    except Exception as e:
        log_error(f"Error in task2_classification: {str(e)}")
        return {
            "status": "error",
            "message": f"Classification failed: {str(e)}"
        }


# =====================================================
# Task 3: Similar Parts (already integrated)
# =====================================================

def run_task3_similar_parts(file_path: str) -> Dict[str, Any]:
    """Task 3: Find similar parts from uploaded CSV"""
    try:
        from task3_similar_parts_analysis import run_task3_documentation
        from parts_similarity_tool import run_parts_similarity
        
        log_info(f"Starting Task 3: Similar Parts Analysis on {file_path}")
        
        result = run_parts_similarity(file_path)
        
        if result["status"] == "success":
            analysis = result.get('analysis', {})
            return {
                "status": "success",
                "title": "✅ Similar Parts Found",
                "content": f"""
### Analysis Results:

**Data Processed:**
- Total rows: {analysis.get('total_rows', 0)}
- Missing descriptions: {analysis.get('missing_descriptions', 0)}
- Average description: {analysis.get('avg_desc_length', 0):.0f} chars

**Key Findings:**
1. **Incomplete Descriptions**: Some parts have short descriptions (< 50 chars)
2. **Text Inconsistency**: Mixed case and formatting variations
3. **Semantic Similarity**: Using embeddings to find meaning-based matches

**Output File:** `similar_parts_output.csv`
- Contains top 5 similar parts per item
- Includes similarity scores

See `task3_similar_parts_analysis.py` for details.
"""
            }
        else:
            return {
                "status": "error",
                "message": result.get('message', 'Analysis failed')
            }
    
    except Exception as e:
        log_error(f"Error in task3_similar_parts: {str(e)}")
        return {
            "status": "error",
            "message": f"Similar parts analysis failed: {str(e)}"
        }


# =====================================================
# Task 4: Timestamp Difference
# =====================================================

def run_task4_timestamp_calc(dt1: str, dt2: str) -> Dict[str, Any]:
    """Task 4: Calculate hour difference between two timestamps"""
    try:
        from task4_timestamp_diff import calculate_hour_difference
        
        log_info(f"Task 4: Calculating hours between {dt1} and {dt2}")
        
        hours = calculate_hour_difference(dt1, dt2)
        
        return {
            "status": "success",
            "title": "⏱️ Timestamp Difference",
            "content": f"""
### Time Calculation:

**From**: `{dt1}`
**To**: `{dt2}`

**Difference**: `{hours} hours` ⏰

### How it works:
- Parses timestamps in format: `YYYY/MM/DD HH:MM`
- Calculates total difference
- Returns full hours (rounded)
- Handles both directions automatically

See `task4_timestamp_diff.py` for details.
"""
        }
    
    except Exception as e:
        log_error(f"Error in task4_timestamp_calc: {str(e)}")
        return {
            "status": "error",
            "message": f"Timestamp calculation failed: {str(e)}"
        }


# =====================================================
# Task 5: Business Hours Calculation
# =====================================================

def run_task5_business_hours(dt1: str, dt2: str) -> Dict[str, Any]:
    """Task 5: Calculate business hours between two timestamps (9-17, weekdays only)"""
    try:
        from task5_business_hours import calculate_business_hours_difference
        
        log_info(f"Task 5: Calculating business hours between {dt1} and {dt2}")
        
        hours = calculate_business_hours_difference(dt1, dt2)
        
        return {
            "status": "success",
            "title": "💼 Business Hours Calculation",
            "content": f"""
### Business Hours Calculation:

**From**: `{dt1}`
**To**: `{dt2}`

**Business Hours**: `{hours} hours` 💼

### Rules:
- Only counts hours between **09:00 - 17:00**
- Only **Monday - Friday** (weekends skipped)
- Handles multi-day calculations
- Precise to the hour

### Examples:
- Monday 09:00 → Monday 17:00 = 8 hours ✓
- Friday 14:00 → Monday 10:00 = 10 hours (3h Fri + 1h Mon) ✓
- Saturday → Sunday = 0 hours ✓

See `task5_business_hours.py` for details.
"""
        }
    
    except Exception as e:
        log_error(f"Error in task5_business_hours: {str(e)}")
        return {
            "status": "error",
            "message": f"Business hours calculation failed: {str(e)}"
        }


# =====================================================
# Task Menu & Help
# =====================================================

def get_task_menu() -> str:
    """Return formatted task menu"""
    return """
## 📋 Available Tasks

**Task 1: Chatbot System** 🤖
  → Ask: "system info" or "show system"
  → Shows: Architecture, performance, requirements
  
**Task 2: Type Classification** 📊
  → Ask: "classify types" or "run classification"
  → Option 1: Upload CSV files (click 📎 button first)
  → Option 2: Place `data/table_1.csv` and `data/table_2.csv` in data/ folder
  → Returns: Model accuracy, metrics, trained model
  
**Task 3: Similar Parts** 🔍
  → Ask: "find similar parts" 
  → Needs: Upload a CSV file first
  → Returns: Similarity scores, top 5 matches per part
  
**Task 4: Timestamp Difference** ⏱️
  → Ask: "calculate hours from 2022/02/15 08:05 to 2022/02/15 10:00"
  → Calculates: Exact hours between timestamps
  
**Task 5: Business Hours** 💼
  → Ask: "business hours from 2022/02/14 09:00 to 2022/02/14 17:00"
  → Calculates: Hours only during business times (9-17, weekdays)

**Or type:** "help tasks" for commands
"""


def parse_and_run_task(user_input: str, uploaded_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse user input and run appropriate task
    
    Returns: Dict with status, title, and content
    """
    user_input_lower = user_input.lower()
    
    # Task Help
    if "help" in user_input_lower or "show all tasks" in user_input_lower:
        return {
            "status": "info",
            "title": "📚 Task Commands",
            "content": get_task_menu()
        }
    
    # Task 1: System Info
    if any(word in user_input_lower for word in ["system", "info", "architecture", "specs"]):
        return run_task1_chatbot_info()
    
    # Task 2: Classification
    if any(word in user_input_lower for word in ["classify", "classification", "type"]) and \
       not any(word in user_input_lower for word in ["similar", "part"]):
        return run_task2_classification(uploaded_file=uploaded_file)
    
    # Task 3: Similar Parts
    if any(word in user_input_lower for word in ["similar", "alternative", "compare", "parts"]):
        if uploaded_file:
            return run_task3_similar_parts(uploaded_file)
        else:
            return {
                "status": "warning",
                "title": "⚠️ No File Uploaded",
                "message": "Please upload a CSV file first before finding similar parts."
            }
    
    # Task 4: Timestamp Difference
    if "calculate hours" in user_input_lower or "hour difference" in user_input_lower:
        # Try to extract timestamps
        tokens = user_input.split()
        date_parts = [t for t in tokens if "/" in t]
        
        if len(date_parts) >= 2:
            dt1 = date_parts[0]
            dt2 = date_parts[1]
            return run_task4_timestamp_calc(dt1, dt2)
        else:
            return {
                "status": "error",
                "message": "Format: 'calculate hours from YYYY/MM/DD HH:MM to YYYY/MM/DD HH:MM'\n\nExample: 'calculate hours from 2022/02/15 08:05 to 2022/02/15 10:00'"
            }
    
    # Task 5: Business Hours
    if "business hours" in user_input_lower or "work hours" in user_input_lower:
        # Try to extract timestamps
        tokens = user_input.split()
        date_parts = [t for t in tokens if "/" in t]
        
        if len(date_parts) >= 2:
            dt1 = date_parts[0]
            dt2 = date_parts[1]
            return run_task5_business_hours(dt1, dt2)
        else:
            return {
                "status": "error",
                "message": "Format: 'business hours from YYYY/MM/DD HH:MM to YYYY/MM/DD HH:MM'\n\nExample: 'business hours from 2022/02/14 09:00 to 2022/02/14 17:00'"
            }
    
    # No task matched
    return {
        "status": "info",
        "title": "💡 Did you mean?",
        "content": "I didn't recognize that task. Type 'help tasks' to see available commands."
    }
