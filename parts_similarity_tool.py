"""
=========================================================
Production Grade Parts Similarity Tool
=========================================================

Features:
---------
✔ Robust CSV ingestion
✔ Auto delimiter detection
✔ Auto encoding detection
✔ Auto DESCRIPTION column detection
✔ Industrial logging
✔ Fault tolerant parsing
✔ Chatbot callable interface
✔ Semantic similarity using Sentence Transformers
✔ Returns output file + summary

Author: Production Version
"""

import os
import re
import logging
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# Logging Configuration
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================================================
# CSV INGESTION
# =========================================================

def detect_encoding(file_path):
    """Try detecting encoding"""
    try:
        import chardet

        with open(file_path, "rb") as f:
            result = chardet.detect(f.read(50000))
            return result["encoding"]

    except Exception:
        return "utf-8"


def load_csv_robust(file_path):
    """Industrial grade CSV loader"""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    logging.info("Detecting encoding...")
    encoding = detect_encoding(file_path)

    logging.info(f"Detected Encoding: {encoding}")

    try:
        df = pd.read_csv(file_path, encoding=encoding)

    except Exception:
        logging.warning("Standard CSV parsing failed. Trying fallback parser...")

        df = pd.read_csv(
            file_path,
            sep=None,
            engine="python",
            encoding=encoding,
            quoting=3,
            on_bad_lines="skip"
        )

    logging.info(f"Dataset Loaded Shape: {df.shape}")
    return df


# =========================================================
# DESCRIPTION COLUMN DETECTION
# =========================================================

def find_description_column(df):

    candidates = [
        "DESCRIPTION",
        "Description",
        "description",
        "PART_DESCRIPTION",
        "DESC",
        "PART_DESC"
    ]

    for col in candidates:
        if col in df.columns:
            logging.info(f"Using description column: {col}")
            return col

    # fallback heuristic
    longest_text_col = max(df.columns, key=lambda c: df[c].astype(str).str.len().mean())
    logging.warning(f"No DESCRIPTION column found. Using heuristic column: {longest_text_col}")
    return longest_text_col


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# =========================================================
# DATA ANALYSIS
# =========================================================

def perform_analysis(df):

    logging.info("Running descriptive analysis...")

    missing = df["DESCRIPTION"].isna().sum()

    df["desc_length"] = df["DESCRIPTION"].astype(str).apply(lambda x: len(x.split()))

    analysis_summary = {
        "total_rows": len(df),
        "missing_descriptions": int(missing),
        "avg_desc_length": float(df["desc_length"].mean()),
        "short_descriptions": int((df["desc_length"] <= 2).sum()),
        "unique_descriptions": int(df["DESCRIPTION"].nunique())
    }

    return analysis_summary


# =========================================================
# EMBEDDING + SIMILARITY
# =========================================================

def generate_similarity(df):

    logging.info("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    logging.info("Generating embeddings...")

    embeddings = model.encode(
        df["clean_description"].tolist(),
        show_progress_bar=True
    )

    logging.info("Computing similarity matrix...")

    similarity_matrix = cosine_similarity(embeddings)

    return similarity_matrix


# =========================================================
# FIND SIMILAR PARTS
# =========================================================

def find_top_similar(df, similarity_matrix, index, top_n=5):

    scores = list(enumerate(similarity_matrix[index]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1: top_n + 1]

    results = []

    for idx, score in scores:
        results.append({
            "Similar_Description": df.loc[idx, "DESCRIPTION"],
            "Similarity_Score": round(float(score), 4)
        })

    return results


# =========================================================
# MAIN TOOL FUNCTION (CHATBOT ENTRY POINT)
# =========================================================

def run_parts_similarity(file_path):

    try:

        # Load dataset
        df = load_csv_robust(file_path)

        # Detect description column
        desc_col = find_description_column(df)

        df["DESCRIPTION"] = df[desc_col]

        # Drop missing
        df = df.dropna(subset=["DESCRIPTION"]).reset_index(drop=True)

        # Clean text
        df["clean_description"] = df["DESCRIPTION"].apply(clean_text)

        # Analysis
        analysis = perform_analysis(df)

        # Similarity
        similarity_matrix = generate_similarity(df)

        logging.info("Finding similar parts...")

        output_rows = []

        for i in range(len(df)):

            source_desc = df.loc[i, "DESCRIPTION"]

            similar_parts = find_top_similar(df, similarity_matrix, i)

            for part in similar_parts:
                output_rows.append({
                    "Source_Part": source_desc,
                    "Alternative_Part": part["Similar_Description"],
                    "Similarity": part["Similarity_Score"]
                })

        output_df = pd.DataFrame(output_rows)

        output_file = "similar_parts_output.csv"
        output_df.to_csv(output_file, index=False)

        return {
            "status": "success",
            "output_file": output_file,
            "analysis": analysis
        }

    except Exception as e:

        logging.error(str(e))

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# CLI EXECUTION
# =========================================================

if __name__ == "__main__":

    FILE_PATH = "Parts.csv"

    result = run_parts_similarity(FILE_PATH)

    print(result)
