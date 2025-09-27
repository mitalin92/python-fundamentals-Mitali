from typing import List, Optional
from pydantic import BaseModel, ValidationError
import json
from pathlib import Path


# Define Metadata model
class Metadata(BaseModel):
    author: Optional[str] = None
    length: Optional[int] = None  # pages or size


# Define Document model
class Document(BaseModel):
    id: int
    title: str
    tags: List[str]
    published: bool
    metadata: Optional[Metadata] = None
    views: Optional[int] = None


# Function to load JSON file and validate documents
def load_documents(file_path: str) -> List[Document]:
    """Load JSON file and return list of valid Document objects."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    documents: List[Document] = []
    for doc in raw_data:
        try:
            documents.append(Document(**doc))  # validate with Pydantic
        except ValidationError as e:
            print(f"Skipping invalid document: {doc} -> {e}")
    return documents


# Function to display documents
def display_documents(documents: List[Document]) -> None:
    """Print documents, handling missing fields if needed."""
    for doc in documents:
        print(f"ID: {doc.id}, Title: {doc.title}, Published: {doc.published}")
        print(f"Tags: {doc.tags}")
        if doc.metadata:
            print(f"Metadata: {doc.metadata.model_dump()}")
        else:
            print("Metadata: Not available")
        print(f"Views: {doc.views if doc.views is not None else 'Not available'}")
        print("-" * 40)


if __name__ == "__main__":
    file_path = "data/documents.json"
    documents = load_documents(file_path)
    display_documents(documents)
