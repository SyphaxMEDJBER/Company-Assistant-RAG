from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"

COLLECTION_NAME = "company_docs"

# Modèle multilingue : nos documents et les questions des employés sont en français.
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
