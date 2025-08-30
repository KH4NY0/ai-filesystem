# AI Filesystem

An **AI-powered semantic filesystem** built with Python.  
This project adds a smart layer on top of your normal files so you can:

-  Search files semantically (e.g., *“contracts about indemnity signed in 2023”*)  
-  Auto-tag and summarize documents  
-  Perform natural-language actions (*“move all old hero section designs to /Archive/Design”*)  
-  Keep everything up to date with a file watcher
  
---

## Features

- **Multi-format ingestion**: text, markdown, PDFs, images (OCR).  
- **Vector search** with FAISS or Chroma + embeddings.  
- **Metadata storage** in SQLite.  
- **Summarization & auto-tagging** using LLMs or rules.  
- **CLI interface** for quick search and smart actions.  

---

## AI Filesystem

A modular AI-powered filesystem for document indexing, semantic search, and smart file management using FastAPI, Typer CLI, and vector search.

## Features

- **Document Indexing:** Index files in a directory with embeddings and metadata.
- **Semantic Search:** Search indexed documents using natural language queries.
- **API Server:** FastAPI-based REST API for programmatic access.
- **CLI Tool:** Typer-powered command-line interface for indexing, searching, and smart file operations.
- **Pluggable Storage:** Uses FAISS for vector storage and SQLite for metadata.

## Requirements

- Python 3.12+
- [pip](https://pip.pypa.io/)
- Tesseract OCR (for image/PDF text extraction, if needed)

## Installation

```bash
# (Recommended) Create and activate a virtual environment
python3 -m venv ve
source ve/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Index Documents

```bash
python3 -m runtime.cli index my_docs
```
- Replace `my_docs` with the path to your documents directory.

### 2. Search

```bash
python3 -m runtime.cli search "your query"
```

### 3. Run the API Server

```bash
python3 -m runtime.api
```
Or with Uvicorn (recommended for FastAPI):
```bash
uvicorn runtime.api:app --host 0.0.0.0 --port 8000
```

### 4. CLI Help

```bash
python3 -m runtime.cli --help
```

## Project Structure

```
ai-filesystem/
├── ai/                # Embedding, intent, and summarization modules
├── index/             # Indexing and storage logic
├── ingest/            # File readers and content extraction
├── runtime/           # API, CLI, watcher, and executor
├── data/              # Default storage for indexes and metadata
├── my_docs/           # Example directory to index
├── requirements.txt
├── config.py
└── README.md
```

## Configuration

Edit `config.py` to change default paths for data, index, and database files.

## Dependencies

- fastapi
- uvicorn
- typer
- numpy
- sentence-transformers
- faiss-cpu
- pdfplumber
- pytesseract
- pillow

## License

MIT
