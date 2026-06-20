# 📋 Task 2 - Quick Reference Card

## 🎯 Run Classification in 3 Steps

```
STEP 1: [Optional] Click 📎 to upload CSV
        ↓
STEP 2: Type "classify types"
        ↓
STEP 3: Get results! ✅
```

---

## 📊 Two Ways to Provide Data

### Method A: Upload File (Fastest ⚡)
```
1. Click 📎 button
2. Select CSV file
3. Type: classify types
```

### Method B: Use data/ Directory (Standard 📂)
```
1. Put file in: data/table_1.csv
2. Put file in: data/table_2.csv
3. Type: classify types
```

---

## 🔑 Magic Commands

| Command | What It Does |
|---------|-------------|
| `classify types` | Run classification |
| `classification` | Run classification |
| `type classification` | Run classification |
| `run classification` | Run classification |

---

## 📁 File Setup (Method B)

```
Your Project/
├── data/
│   ├── table_1.csv  ← Put here
│   └── table_2.csv  ← Put here
└── app.py
```

**File Format:** Standard CSV with headers
```csv
ID,Name,Description,Type
1,Part_A,Bearing,A
2,Part_B,Shaft,B
```

---

## ✅ What Happens

```
✓ Merges table_1 + table_2 (by ID)
✓ Trains classification model
✓ Shows accuracy metrics
✓ Saves model for reuse
✓ Displays predictions
```

---

## 📈 Expected Output

```
Data Source: [uploaded file / data/ directory]
Total Records: 500
Classes: 3

Model Performance:
- Accuracy: 87%
- F1 Score: 0.86
- Precision: 0.88
- Recall: 0.84

✓ Model saved: type_classifier.pkl
```

---

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| "File not found" | Upload CSV or add to data/ |
| "Invalid CSV" | Check format, remove special chars |
| "Column error" | Ensure "Type" column exists |

---

## 🚀 Fastest Start

```
1. Click 📎
2. Pick any CSV
3. Type: "classify types"
4. Done! 🎉
```

No setup needed. Files in data/ optional!

---

## 💾 Model Persistence

**Where:** Project root
**File:** `type_classifier.pkl`
**Use:** Load in Python with joblib

```python
from joblib import load
classifier = load('type_classifier.pkl')
prediction = classifier.predict(new_data)
```

---

## 📞 Need Help?

- **For detailed guide:** Read TASK2_FILE_UPLOAD_GUIDE.md
- **For all commands:** Type "help tasks"
- **For file requirements:** Check [TASK_COMMANDS.md](TASK_COMMANDS.md)

---

**TL;DR:** Upload CSV or use data/ folder → Type "classify types" → Get results! ✨
