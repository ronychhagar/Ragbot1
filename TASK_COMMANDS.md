# ⚡ Task Commands - Quick Reference Card

## Copy & Paste Commands

### 🤖 Task 1: System Information
```
show system
```
**Shows:** Architecture, LLM, performance, hardware requirements

---

### 📊 Task 2: Type Classification
```
classify types
```
**Requirements:** `data/table_1.csv` + `data/table_2.csv`
**Output:** Accuracy, trained model

---

### 🔍 Task 3: Similar Parts
```
find similar parts
```
**Steps:**
1. Click 📎 to upload CSV with parts data
2. Type the command above
3. Download results from `similar_parts_output.csv`

---

### ⏱️ Task 4: Hour Difference
```
calculate hours from 2022/02/15 08:05 to 2022/02/15 10:00
```
**Format:** `YYYY/MM/DD HH:MM`
**Output:** Number of hours (integer)

---

### 💼 Task 5: Business Hours
```
business hours from 2022/02/14 09:00 to 2022/02/14 17:00
```
**Format:** `YYYY/MM/DD HH:MM`
**Rules:** 09:00-17:00, Mon-Fri only
**Output:** Business hours only (integer)

---

## Command Variations (Work the Same!)

### Task 1
- `show system`
- `system info`
- `system architecture`
- `system specs`

### Task 2
- `classify types`
- `run classification`
- `type classification`

### Task 3
- `find similar parts`
- `similar parts`
- `show similar parts`
- `find alternatives`

### Task 4
- `calculate hours from TIME to TIME`
- `hour difference from TIME to TIME`

### Task 5
- `business hours from TIME to TIME`
- `work hours from TIME to TIME`

---

## 🎯 Most Common Usage Patterns

### Pattern 1: Just Ask
```
You: "system info"
AI: [Shows system details]
```

### Pattern 2: Calculate Time
```
You: "calculate hours from 2022/02/15 08:00 to 2022/02/15 10:00"
AI: 2 hours
```

### Pattern 3: Upload & Analyze
```
You: [Click 📎] [Select CSV]
AI: File uploaded!

You: "find similar parts"
AI: [Processes] ✅ Done! Download results.
```

---

## 💡 Quick Tips

| Tip | Command |
|-----|---------|
| See all tasks | `"help tasks"` |
| Get system info | `"show system"` |
| Time format reminder | `YYYY/MM/DD HH:MM` |
| Upload file | Click 📎 button |
| Download results | Check output files |

---

## 📋 Time Format Examples

### ✅ Correct Format
```
2022/02/15 08:05
2022/12/31 23:59
2022/01/01 00:00
```

### ❌ Wrong Formats
```
2022-02-15 08:05          (wrong separator)
02/15/2022 08:05          (wrong order)
2022/2/15 8:5             (incomplete)
8:05 AM on Feb 15, 2022   (text format)
```

---

## 🎓 5-Minute Tutorial

### Step 1: Start (30 sec)
```bash
chainlit run app.py
# Open: http://localhost:8000
```

### Step 2: System Info (1 min)
```
Type: "show system"
See: Architecture, LLM, performance
```

### Step 3: Calculate Hours (2 min)
```
Type: "calculate hours from 2022/02/15 08:00 to 2022/02/15 10:30"
See: 2 hours
```

### Step 4: Business Hours (1 min)
```
Type: "business hours from 2022/02/14 09:00 to 2022/02/14 17:00"
See: 8 hours (full Monday)
```

### Step 5: Upload & Analyze (2 min)
```
Click 📎 → Select CSV
Type: "find similar parts"
Download results
```

**Total: ~5 minutes to master all tasks!**

---

## 🔧 Quick Setup

### First Time Only
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Prepare data (optional)
mkdir data
# Add your CSV files to data/

# 3. Start Ollama (Terminal 1)
ollama serve

# 4. Start chatbot (Terminal 2)
chainlit run app.py

# 5. Open browser
# http://localhost:8000
```

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| "Command not recognized" | Type `"help tasks"` to see all commands |
| "No file uploaded" | Click 📎 button before asking for similar parts |
| "Data files not found" | Put `table_1.csv`, `table_2.csv` in `data/` |
| "Invalid time format" | Use `YYYY/MM/DD HH:MM` |
| "Ollama not found" | Run `ollama serve` in another terminal |

---

## 📞 Quick Links

- **Full Guide**: [TASKS_IN_CHATBOT.md](TASKS_IN_CHATBOT.md)
- **All Documentation**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **Tasks Overview**: [TASKS_COMPLETE_README.md](TASKS_COMPLETE_README.md)
- **How to Start**: [GETTING_STARTED.md](GETTING_STARTED.md)

---

## 🚀 Ready to Go?

```bash
# 1. Start LLM
ollama serve

# 2. Start chatbot (new terminal)
chainlit run app.py

# 3. Open browser
# http://localhost:8000

# 4. Type command
# "help tasks"

# Enjoy! 🎉
```

---

**Print this page for quick reference!** 📋
