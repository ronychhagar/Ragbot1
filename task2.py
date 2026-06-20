import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------
# Load Data
# ---------------------------------------
df = pd.read_csv("Parts.csv")

df = df.dropna(subset=["DESCRIPTION"])
df.reset_index(drop=True, inplace=True)


# ---------------------------------------
# Basic Cleaning
# ---------------------------------------
def clean_text(text):
    text = str(text).lower()
    text = text.replace("-", " ")
    return text


df["clean_description"] = df["DESCRIPTION"].apply(clean_text)


# ---------------------------------------
# Generate Embeddings
# ---------------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    df["clean_description"].tolist(),
    show_progress_bar=True
)


# ---------------------------------------
# Compute Similarity Matrix
# ---------------------------------------
similarity_matrix = cosine_similarity(embeddings)


# ---------------------------------------
# Find Top 5 Similar Parts
# ---------------------------------------
def find_top_similar(idx, top_n=5):
    sim_scores = list(enumerate(similarity_matrix[idx]))
    
    # Remove self match
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]
    
    results = []
    for i, score in sim_scores:
        results.append({
            "PART_INDEX": i,
            "DESCRIPTION": df.loc[i, "DESCRIPTION"],
            "SIMILARITY": score
        })
        
    return results


# ---------------------------------------
# Generate Output
# ---------------------------------------
results = []

for i in range(len(df)):
    similar_parts = find_top_similar(i)

    for part in similar_parts:
        results.append({
            "SOURCE_PART": df.loc[i, "DESCRIPTION"],
            "SIMILAR_PART": part["DESCRIPTION"],
            "SIMILARITY": part["SIMILARITY"]
        })


output_df = pd.DataFrame(results)
output_df.to_csv("similar_parts_output.csv", index=False)

print("✅ Similar parts file generated.")
