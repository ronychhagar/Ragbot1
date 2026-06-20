"""
Parts Similarity Solution
------------------------------------
Goal:
Find 5 alternative similar parts based on DESCRIPTION column.

Features:
✔ Robust CSV loading
✔ Data quality analysis
✔ Text preprocessing
✔ Semantic similarity using embeddings
✔ TF-IDF fallback (no torch / GPU dependency)
✔ Saves similarity output
✔ Production-style logging
"""

import pandas as pd
import numpy as np
import re
import logging
from sklearn.metrics.pairwise import cosine_similarity

# TF-IDF fallback
from sklearn.feature_extraction.text import TfidfVectorizer

# Try transformer embeddings (optional)
USE_TRANSFORMER = True

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    USE_TRANSFORMER = False


# -----------------------------
# CONFIG
# -----------------------------
FILE_PATH = "Parts.csv"
TOP_K = 5
OUTPUT_FILE = "similar_parts_output.csv"


# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Robust CSV Loader
# -----------------------------
def load_dataset(filepath):

    logging.info("Loading dataset...")

    # Try multiple delimiters automatically
    for sep in [",", ";", "|", "\t"]:
        try:
            df = pd.read_csv(
                filepath,
                sep=sep,
                encoding="utf-8",
                engine="python",
                on_bad_lines="skip"
            )

            if len(df.columns) > 1:
                logging.info(f"Loaded using separator: '{sep}'")
                break

        except Exception:
            continue

    logging.info(f"Dataset Shape: {df.shape}")
    logging.info(f"Columns Found: {df.columns.tolist()}")

    # Normalize column names
    df.columns = df.columns.str.strip().str.upper()

    # If only one column exists → assume entire row is description
    if "DESCRIPTION" not in df.columns:

        if len(df.columns) == 1:
            logging.warning("Single column detected — treating as DESCRIPTION")
            df.rename(columns={df.columns[0]: "DESCRIPTION"}, inplace=True)
        else:
            raise ValueError("DESCRIPTION column not found")

    df = df.dropna(subset=["DESCRIPTION"])

    return df



# -----------------------------
# Data Cleaning
# -----------------------------
def clean_text(text):

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# -----------------------------
# Descriptive Analysis
# -----------------------------
def descriptive_analysis(df):

    logging.info("Running descriptive analysis...")

    desc_lengths = df["DESCRIPTION"].astype(str).apply(len)

    logging.info(f"Total Parts: {len(df)}")
    logging.info(f"Unique Descriptions: {df['DESCRIPTION'].nunique()}")
    logging.info(f"Average Description Length: {desc_lengths.mean():.2f}")
    logging.info(f"Missing Description Count: {df['DESCRIPTION'].isna().sum()}")

    # Findings
    print("\n===== DATA FINDINGS =====")

    print("\n1. Description length variability:")
    print("   -> Long descriptions may include additional specs")

    print("\n2. Potential noisy text:")
    print("   -> Special characters, units, abbreviations")

    print("\n3. Duplicate or near duplicate parts likely exist:")
    print("   -> Requires semantic similarity vs keyword match")


# -----------------------------
# Embedding Generator
# -----------------------------
def generate_embeddings(text_list):

    if USE_TRANSFORMER:
        try:
            logging.info("Using Sentence Transformer Embeddings...")
            model = SentenceTransformer("all-MiniLM-L6-v2")
            return model.encode(text_list, show_progress_bar=True)
        except Exception as e:
            logging.warning("Transformer failed. Falling back to TF-IDF")
    
    logging.info("Using TF-IDF embeddings...")
    vectorizer = TfidfVectorizer(stop_words="english")
    return vectorizer.fit_transform(text_list).toarray()


# -----------------------------
# Similarity Search
# -----------------------------
def find_similar_parts(df, embeddings):

    logging.info("Calculating cosine similarity matrix...")

    similarity_matrix = cosine_similarity(embeddings)

    results = []

    for idx in range(len(df)):

        sim_scores = similarity_matrix[idx]
        sim_indices = np.argsort(sim_scores)[::-1][1:TOP_K + 1]

        base_part = df.iloc[idx]

        for alt_idx in sim_indices:

            alt_part = df.iloc[alt_idx]

            results.append({
                "BASE_PART_DESC": base_part["DESCRIPTION"],
                "ALT_PART_DESC": alt_part["DESCRIPTION"],
                "SIMILARITY_SCORE": sim_scores[alt_idx]
            })

    return pd.DataFrame(results)


# -----------------------------
# Main Pipeline
# -----------------------------
def main():

    # Load Data
    df = load_dataset(FILE_PATH)

    # Descriptive Analysis
    descriptive_analysis(df)

    # Clean Text
    logging.info("Cleaning text descriptions...")
    df["DESCRIPTION_CLEAN"] = df["DESCRIPTION"].apply(clean_text)

    # Generate Embeddings
    embeddings = generate_embeddings(df["DESCRIPTION_CLEAN"].tolist())

    # Find Similar Parts
    result_df = find_similar_parts(df, embeddings)

    # Save Output
    result_df.to_csv(OUTPUT_FILE, index=False)

    logging.info(f"Similarity results saved to {OUTPUT_FILE}")

    print("\nSample Output:")
    print(result_df.head())


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
