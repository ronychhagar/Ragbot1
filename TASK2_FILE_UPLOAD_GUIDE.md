# 📊 Task 2: Classification with File Upload - Guide

## ✨ New Feature: Upload CSVs for Task 2

You can now run **Task 2 (Type Classification)** in two ways:

---

## 🚀 Option 1: Upload Files (NEW!)

### Steps:
1. **Click 📎 attachment button** at the bottom of chat
2. **Select a CSV file** (or multiple files)
3. **Type:** `"classify types"` or `"run classification"`
4. **Get results** with model accuracy and metrics

### Perfect For:
- Quick testing with your own data
- No need to organize files in directories
- Multi-user scenarios (each user uploads their own data)

### Example Workflow:
```
You: [Click 📎] [Select: my_data.csv]
AI: ✅ File uploaded successfully

You: "classify types"
AI: 📊 Running classification on your data...
AI: ✅ Accuracy: 87%, F1: 0.86
AI: ✓ Model saved: type_classifier.pkl
```

---

## 📂 Option 2: Use Files in data/ Directory

### Setup:
1. Place `table_1.csv` in the `data/` folder
2. Place `table_2.csv` in the `data/` folder
3. **Type:** `"classify types"` in chat

### Perfect For:
- Production deployments
- Pre-set default datasets
- Consistent analysis

### Example:
```
data/
├── table_1.csv
└── table_2.csv
```

Then in chat:
```
You: "classify types"
AI: ✅ Loaded table_1.csv + table_2.csv
AI: ✅ Model trained successfully
```

---

## 🎯 Which Option to Choose?

| Option | Best For | Speed | Flexibility |
|--------|----------|-------|-------------|
| **Upload Files** | Quick tests, custom data | ⚡ Instant | 🎯 Very high |
| **data/ Directory** | Production, presets | ⚡ Instant | 📁 Fixed |

---

## 📊 How It Works

### Upload Path
```
1. Click 📎
   ↓
2. Select CSV
   ↓
3. File stored in session
   ↓
4. Type "classify types"
   ↓
5. Task 2 loads uploaded file
   ↓
6. Trains classifier
   ↓
7. Returns results
```

### Directory Path
```
1. table_1.csv + table_2.csv in data/
   ↓
2. Type "classify types"
   ↓
3. Task 2 loads from data/
   ↓
4. Automatically merges on ID
   ↓
5. Trains classifier
   ↓
6. Returns results
```

---

## 💡 Tips & Tricks

### Tip 1: Multiple Files
- Upload ONE merged CSV for direct use
- Or upload multiple CSVs (first one will be used)

### Tip 2: File Naming
CSV files should have columns for analysis:
- Ideally a "Type" or "Label" column for classification
- Keep headers in first row

### Tip 3: Mix & Match
```
Session 1:
- Upload my_data.csv
- Type "classify types"
- Get results

Session 2:
- Don't upload anything
- Type "classify types"
- Uses data/table_1.csv + table_2.csv
```

### Tip 4: Save Your Models
Task 2 automatically saves trained models:
- **File:** `type_classifier.pkl`
- **Use later:** `from joblib import load`

---

## 🔍 File Format Requirements

### CSV Requirements:
- **Format:** Standard CSV with headers
- **Encoding:** UTF-8
- **Type Column:** Should have "Type" or similar column
- **No special characters** in headers (use underscores: `Type_A`, not `Type-A`)

### Good Example:
```csv
ID,Name,Description,Type
1,Part_A,Bearing assembly,A
2,Part_B,Shaft connection,B
3,Part_C,Mounting bracket,A
```

### Not Good:
```csv
Id - Name | Description @ Type
1 - Part A | Bearing assembly ! A
```

---

## ⚠️ Troubleshooting

### "File upload failed"
- Check file is valid CSV
- File name should not have spaces
- Try: `table_1.csv` instead of `table 1.csv`

### "Classification failed"
- Check CSV has appropriate column names
- Ensure data has Type/Label column
- Check for missing values

### "Using files from data/ instead"
- If upload fails, system falls back to data/
- Check logs: `logs/rag_bot.log`

---

## 🎯 When to Use Each Option

### Use Upload When:
```
✅ Testing new datasets
✅ Ad-hoc analysis
✅ Different users, different data
✅ Quick iterations
✅ Mobile/remote work
```

### Use data/ Directory When:
```
✅ Standard workflow
✅ Same data everytime
✅ Production deployment
✅ Shared/team data
✅ Consistent results
```

---

## 📈 Example Use Cases

### Case 1: Quick Test
```
Boss: "Can you classify these parts?"
You: Click 📎 → Upload their CSV
You: Type "classify types"
You: Get results in seconds ✓
```

### Case 2: Regular Analysis
```
You: Set up table_1.csv + table_2.csv in data/
Team: Every day, type "classify types"
System: Uses same data, consistent results ✓
```

### Case 3: Batch Processing
```
Monday: Upload Week1_parts.csv → Classify
Tuesday: Upload Week2_parts.csv → Classify
Wednesday: Upload Week3_parts.csv → Classify
Log: All results saved with timestamps ✓
```

---

## 🚀 Quick Start

### Option 1 (Fastest):
```
1. Click 📎
2. Upload any CSV
3. Type "classify types"
4. Done! 🎉
```

### Option 2 (Standard):
```
1. Put files in data/
2. Type "classify types"
3. Done! 🎉
```

---

## 📞 Support

### Error Messages:
- **"File not found"** → Upload a file or put CSVs in data/
- **"Invalid CSV"** → Check file format
- **"No data"** → Ensure CSV has content

### For Help:
- Type: `"help tasks"`
- Read: [TASK_COMMANDS.md](TASK_COMMANDS.md)
- Check: Logs in `logs/rag_bot.log`

---

## ✅ Summary

**Task 2 now supports:**
- ✅ Upload your own CSV files
- ✅ Use presets from data/ directory
- ✅ Automatic fallback if files missing
- ✅ Full error messages with guidance

**Choose what works best for you!** 🎯

Start with: `"classify types"` 
System will guide you if files are needed!
