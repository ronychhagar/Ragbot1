# 🚀 Getting Started - Quick Reference

## ⚡ 30-Second Setup

### 1. Start the LLM (Terminal 1)
```bash
ollama serve
```

### 2. Launch the Chatbot (Terminal 2)
```bash
chainlit run app.py
```

### 3. Open Browser
```
http://localhost:8000
```

**Done!** Your AI chatbot is now running. ✅

---

## 📚 Explore All 5 Tasks

### Task 1: Chatbot System
Already running! The UI at http://localhost:8000 is the chatbot.

**Features**:
- 💬 Chat with AI
- 📁 Upload documents
- 🔍 Semantic search
- 💾 Chat history
- ⚡ Query caching

### Task 2: Binary Classification
```bash
python task2_type_classification.py
```
**Trains a model** to classify the Type column from your data.

### Task 3: Similar Parts
```bash
python task3_similar_parts_analysis.py
```
**Or via chatbot**: Ask "Find similar parts" to get results.

### Task 4: Hour Differences
```python
from task4_timestamp_diff import calculate_hour_difference
hours = calculate_hour_difference("2022/02/15 08:05", "2022/02/15 10:00")
print(hours)  # Output: 2
```

### Task 5: Business Hours
```python
from task5_business_hours import calculate_business_hours_difference
hours = calculate_business_hours_difference("2022/02/14 09:00", "2022/02/14 17:00")
print(hours)  # Output: 8 (Monday 9-5 = 8 hours)
```

---

## 📁 Important Files

| File | Purpose | Action |
|------|---------|--------|
| `app.py` | Chatbot UI | `chainlit run app.py` |
| `task1_chatbot_system.py` | System docs | `python task1_chatbot_system.py` |
| `task2_type_classification.py` | ML classifier | `python task2_type_classification.py` |
| `task3_similar_parts_analysis.py` | Similar parts | `python task3_similar_parts_analysis.py` |
| `task4_timestamp_diff.py` | Hour calculator | `python task4_timestamp_diff.py` |
| `task5_business_hours.py` | Business hours | `python task5_business_hours.py` |
| `requirements.txt` | Dependencies | `pip install -r requirements.txt` |
| `.env.example` | Configuration | Copy to `.env` and customize |

---

## ⚙️ Configuration

### Option 1: Use Defaults
Just run it! Default settings work out of the box.

### Option 2: Customize
```bash
# Copy example config
cp .env.example .env

# Edit (optional)
# - Change LLM temperature
# - Adjust chunk size
# - Set logging level
# - Enable/disable cache
```

---

## 🐛 Troubleshooting

### "Ollama not found"
```bash
# Make sure Ollama is installed and running in another terminal
ollama serve
```

### "Port 8000 already in use"
```bash
# Use a different port
chainlit run app.py --port 8001
# Open: http://localhost:8001
```

### "Out of memory"
```bash
# Edit .env
CHUNK_SIZE=256  # Default: 512
MAX_CHUNKS=20   # Default: 50
```

### "Vector store error"
```bash
# Reinitialize from scratch
rm -r chroma_db/
python ingest.py
```

---

## 📊 What Each Task Does

### Task 1: The Chatbot
**What it is**: An AI assistant that answers questions based on your documents

**Example**:
```
You: "What is the company policy?"
AI: "According to your document... [answer]"
```

**How to use**:
1. Run: `chainlit run app.py`
2. Open: http://localhost:8000
3. Upload documents (optional)
4. Ask questions

---

### Task 2: Type Classifier
**What it is**: Automatically classifies items into binary categories

**Example**:
```
Input: Parts data with a "Type" column
Output: Model trained to predict Type for new parts
Accuracy: 85-95% (depending on your data)
```

**How to use**:
```bash
python task2_type_classification.py
```

---

### Task 3: Similar Parts Finder
**What it is**: Finds similar products based on description

**Example**:
```
Part: "M5 Bolt Steel"
Similar: Top 5 similar parts based on meaning
```

**How to use**:
```bash
# Via chatbot:
# 1. Upload Parts.csv
# 2. Ask "find similar parts"
# 3. Download similar_parts_output.csv
```

---

### Task 4: Hour Difference
**What it is**: Calculates hours between two timestamps

**Example**:
```
From: 2022/02/15 08:05
To:   2022/02/15 10:00
Result: 2 hours
```

**How to use**:
```python
from task4_timestamp_diff import calculate_hour_difference
hours = calculate_hour_difference("2022/02/15 08:05", "2022/02/15 10:00")
```

---

### Task 5: Business Hours
**What it is**: Counts hours only during business hours (9-5, weekdays only)

**Example**:
```
Monday 09:00 → Monday 17:00
Result: 8 hours (full business day)

Monday 14:00 → Wednesday 10:00
Result: 11 hours (5h Mon + skip Tue + 1h Wed)
```

**How to use**:
```python
from task5_business_hours import calculate_business_hours_difference
hours = calculate_business_hours_difference("2022/02/14 09:00", "2022/02/14 17:00")
```

---

## 🎓 Learning Paths

### Path 1: Just Chat
```
1. chainlit run app.py
2. Upload documents
3. Ask questions
4. Done!
```

### Path 2: Classify Data
```
1. Prepare CSV with data
2. python task2_type_classification.py
3. Get trained model
4. Use for predictions
```

### Path 3: Find Similarities
```
1. Prepare Parts.csv
2. python task3_similar_parts_analysis.py
3. Get similar_parts_output.csv
4. View results
```

### Path 4: Calculate Dates
```
1. Import from task4 or task5
2. Call function with timestamps
3. Get result in hours
4. Done!
```

### Path 5: Complete System
```
1. Run all tasks
2. Combine results
3. Integrate with workflows
4. Deploy to production
```

---

## 📚 Learn More

### Quick Overview
→ Read: `QUICK_START.md`

### Detailed Guide
→ Read: `TASKS_COMPLETE_README.md`

### Completion Status
→ Read: `COMPLETION_SUMMARY.md`

### System Improvements
→ Read: `IMPROVEMENTS.md`

### Each Task File
→ Read docstrings in:
- `task1_chatbot_system.py`
- `task2_type_classification.py`
- `task3_similar_parts_analysis.py`
- `task4_timestamp_diff.py`
- `task5_business_hours.py`

---

## 🚀 Common Commands

### Start Chatbot
```bash
chainlit run app.py
```

### Start LLM Service
```bash
ollama serve
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Test Classification
```bash
python task2_type_classification.py
```

### Test Similar Parts
```bash
python task3_similar_parts_analysis.py
```

### Test Timestamp Calcs
```bash
python task4_timestamp_diff.py
python task5_business_hours.py
```

### View Logs
```bash
tail -f logs/rag_bot.log
```

### Check Vector Store
```bash
ls -la chroma_db/
```

---

## ✅ Verification

### Everything Works?
```bash
# All these should run without errors

# 1. Check Python
python --version

# 2. Check Ollama
ollama --version

# 3. Check dependencies
pip list | grep chainlit

# 4. Test imports
python -c "import chainlit; import langchain; print('✓ OK')"

# 5. Run chatbot
chainlit run app.py
```

---

## 🎯 Next Steps

1. **First Time?**
   - Read: `QUICK_START.md`
   - Run: `chainlit run app.py`
   - Explore: Upload a document and ask questions

2. **Want to Classify Data?**
   - Prepare: Your CSV file
   - Run: `python task2_type_classification.py`
   - Result: Trained model + metrics

3. **Want to Find Similar Parts?**
   - Upload: Parts.csv to chatbot
   - Ask: "Find similar parts"
   - Download: Results as CSV

4. **Want to Use as API?**
   - Import: `from task4_timestamp_diff import ...`
   - Use: Functions in your code
   - Deploy: Integrate into workflows

5. **Want to Customize?**
   - Edit: `.env` file
   - Change: Settings as needed
   - Restart: Chatbot with new config

---

## 📸 What Each Task Outputs

### Task 1: Chatbot
**Output**: Interactive web UI at http://localhost:8000

### Task 2: Classification
**Output**: 
- Trained model (type_classifier.pkl)
- Accuracy score
- Confusion matrix
- Classification report

### Task 3: Similar Parts
**Output**:
- similar_parts_output.csv
- For each part: top 5 similar items

### Task 4: Hour Difference
**Output**:
- Number of hours (integer)

### Task 5: Business Hours
**Output**:
- Business hours only (integer)

---

## 🏆 Success Indicators

You've successfully set up the system when:

- ✅ Chatbot UI loads at http://localhost:8000
- ✅ You can type a message and get a response
- ✅ Logs show successful operations
- ✅ Vector store initializes without errors
- ✅ All task files run without exceptions

---

## 💡 Pro Tips

1. **Use Caching**: Enable CACHE_ENABLED=true for faster responses
2. **Monitor Logs**: Check logs/rag_bot.log for debugging
3. **Batch Operations**: Run task2 once, use model multiple times
4. **Save Outputs**: Export results from task3 for archival
5. **Git Tracking**: Initialize git to track changes

---

## 🎓 Learning Resources

All task files include:
- Complete source code
- Comprehensive docstrings
- Usage examples
- Test cases
- Integration information

**Read the source code!** It's well-documented and easy to understand.

---

**Ready to start?** Run: `chainlit run app.py` 🚀

**Questions?** Check the documentation files or review task source code.

**Need help?** Review troubleshooting section above.
