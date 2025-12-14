from pathlib import Path
import pandas as pd


def load_articles(folder: str) -> pd.DataFrame:
    records = []

    for file in Path(folder).glob("*.txt"):
        records.append(
            {
                "article_id": file.stem,
                "text": file.read_text(encoding="utf-8"),
            }
        )

    return pd.DataFrame(records)


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            last_period = chunk.rfind(".")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks


def apply_chunking(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["chunks"] = df["text"].apply(chunk_text)
    return df
