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
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)

    # Similarité cosinus plutôt que le défaut L2 : le modèle est entraîné par
    # perte contrastive, qui optimise la direction des vecteurs, pas leur
    # norme — le cosinus mesure exactement ce que le modèle apprend.
    collection = client.create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

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
