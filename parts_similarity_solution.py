import pandas as pd
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------
# Load Model Once (Production Optimization)
# -------------------------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------------------------------
# Text Cleaning
# -------------------------------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -------------------------------------------------
# Main Similarity Function
# -------------------------------------------------
def run_similarity_analysis(csv_file):

    df = pd.read_csv(csv_file)

    if "DESCRIPTION" not in df.columns:
        raise ValueError("CSV must contain DESCRIPTION column")

    # Remove missing
    df = df.dropna(subset=["DESCRIPTION"]).reset_index(drop=True)

    df["clean_description"] = df["DESCRIPTION"].apply(clean_text)

    # Generate embeddings
    embeddings = model.encode(df["clean_description"].tolist())

    similarity_matrix = cosine_similarity(embeddings)

    # ----------------------------
    # Find Top 5 Similar
    # ----------------------------
    output_rows = []

    for i in range(len(df)):
        scores = list(enumerate(similarity_matrix[i]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

        for idx, score in scores:
            output_rows.append(
                {
                    "Source_Part": df.loc[i, "DESCRIPTION"],
                    "Alternative_Part": df.loc[idx, "DESCRIPTION"],
                    "Similarity": round(float(score), 4)
                }
            )

    output_df = pd.DataFrame(output_rows)

    return df, output_df
