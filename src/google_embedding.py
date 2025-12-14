from google import genai
from google.genai import types
import pickle
from typing import cast, Any

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

api_key = "AIzaSyCjUeuznP2FKv21EuRhXs5okEn53LoIEjQ"

client = genai.Client(api_key=api_key)

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[  # type: ignore[arg-type, union-attr]
        "proton collision",
        "proton collision happens in LHC",
        "proton collision is an operation between two protons",
        "London is the capital of the United Kingdom",
    ],
    config=types.EmbedContentConfig(output_dimensionality=768, task_type="SEMANTIC_SIMILARITY"),
)

print(result.embeddings)

vectors = [embedding.values for embedding in result.embeddings]  # type: ignore[arg-type, union-attr]

embeddings_matrix = np.array(vectors)

similarity_matrix = cosine_similarity(embeddings_matrix)

print(similarity_matrix)


def embed_chunks(chunks: list[str]) -> np.ndarray:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=cast(Any, chunks),
        config=types.EmbedContentConfig(
            output_dimensionality=768,
            task_type="SEMANTIC_SIMILARITY",
        ),
    )

    embeddings = result.embeddings
    if embeddings is None:
        raise RuntimeError("No embeddings returned from Gemini API")

    vectors = [embedding.values for embedding in embeddings]
    return np.array(vectors)


def save_embeddings(embeddings: np.ndarray, path: str) -> None:
    with open(path, "wb") as f:
        pickle.dump(embeddings, f)
