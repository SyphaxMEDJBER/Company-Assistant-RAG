import chromadb
from sentence_transformers import SentenceTransformer

from src.chunking import chunk_documents_dir
from src.config import (
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    DOCUMENTS_DIR,
    EMBEDDING_MODEL_NAME,
)


def build_index() -> None:
    chunks = chunk_documents_dir(DOCUMENTS_DIR)
    print(f"{len(chunks)} chunks extraits depuis {DOCUMENTS_DIR}")

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embeddings = model.encode([c.text for c in chunks], show_progress_bar=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
    client.delete_collection(COLLECTION_NAME) if COLLECTION_NAME in [
        c.name for c in client.list_collections()
    ] else None
    collection = client.create_collection(COLLECTION_NAME)

    collection.add(
        ids=[f"{c.source}::{i}" for i, c in enumerate(chunks)],
        embeddings=embeddings.tolist(),
        documents=[c.text for c in chunks],
        metadatas=[
            {"source": c.source, "document_title": c.document_title, "section": c.section}
            for c in chunks
        ],
    )
    print(f"Index construit : {collection.count()} chunks stockés dans {CHROMA_DB_DIR}")


if __name__ == "__main__":
    build_index()
