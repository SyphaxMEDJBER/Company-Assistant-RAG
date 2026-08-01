from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"

COLLECTION_NAME = "company_docs"

# Modèle multilingue : nos documents et les questions des employés sont en français.
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

GENERATION_MODEL_NAME = "llama3.2:3b"

# Distance cosinus au-delà de laquelle on considère qu'aucun chunk récupéré
# n'est vraiment pertinent (calibré empiriquement : ~0.2-0.5 sur des questions
# dans le sujet, ~0.8 sur des questions hors-sujet, voir notes/CONCEPTS.md).
RELEVANCE_THRESHOLD = 0.6
