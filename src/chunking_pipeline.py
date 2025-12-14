from usecases.chunking import apply_chunking
from google_embedding import embed_chunks, save_embeddings
import pandas as pd

df = pd.read_csv("data/articles.csv", delimiter=";", dtype="string")
df["text"] = df["summary"]
df = apply_chunking(df)

all_chunks = df["chunks"].explode().tolist()

embeddings = embed_chunks(all_chunks)
save_embeddings(embeddings, "gemini_embeddings.pkl")

print(len(all_chunks))
print(embeddings.shape)
