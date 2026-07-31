import chromadb
from sentence_transformers import SentenceTransformer

from src.config import CHROMA_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL_NAME

# Chargés une seule fois au niveau module : recharger le modèle ou rouvrir
# la connexion à chaque appel de retrieve() coûterait plusieurs secondes.
_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
_collection = _client.get_collection(COLLECTION_NAME)


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Retourne les `top_k` chunks les plus pertinents pour `query`.

    top_k > 1 par défaut : une question peut concerner plusieurs sections ou
    documents à la fois, on laisse donc de la marge pour le LLM en aval.
    """
    # Même modèle que pour l'indexation : obligatoire, question et documents
    # doivent vivre dans le même espace vectoriel pour être comparables.
    query_embedding = _model.encode([query]).tolist()

    results = _collection.query(query_embeddings=query_embedding, n_results=top_k)

    # ChromaDB renvoie une liste par requête envoyée ; on n'en a envoyé qu'une.
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved_chunks = []
    for text, metadata, distance in zip(documents, metadatas, distances):
        retrieved_chunks.append(
            {
                "text": text,
                "source": metadata["source"],
                "section": metadata["section"],
                "distance": distance,  # plus petit = plus pertinent
            }
        )

    return retrieved_chunks


if __name__ == "__main__":
    # Petit test manuel : lance `python -m src.retrieval` pour essayer
    # une question et voir les chunks retrouvés.
    question = "comment configurer le VPN pour travailler depuis chez moi ?"
    for chunk in retrieve(question, top_k=3):
        print(f"[{chunk['distance']:.4f}] {chunk['source']} > {chunk['section']}")
        print(chunk["text"][:150].replace("\n", " "))
        print()
