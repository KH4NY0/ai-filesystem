from pathlib import Path

class Config:
    # Root directory to watch / index
    ROOT_DIR: Path = Path("./my_docs")

    # Storage locations
    DATA_DIR: Path = Path("./data")
    VECTOR_INDEX: Path = DATA_DIR / "faiss.index"
    META_DB: Path = DATA_DIR / "meta.db"

    # Embedding model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_DIM: int = 384   # matches the embedding model

    # Watchdog settings
    WATCH_PATTERNS = ["*.txt", "*.md", "*.pdf", "*.png", "*.jpg", "*.jpeg"]
    WATCH_IGNORE_DIRS = [".git", "__pycache__", "node_modules"]

    # Search defaults
    TOP_K: int = 10
    SCORE_THRESHOLD: float = 0.40

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Misc
    SUMMARY_MAX_CHARS: int = 400
