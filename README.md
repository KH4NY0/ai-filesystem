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
- **API (FastAPI)** for building UIs.  
- **FUSE integration** for mounting AI-driven virtual folders.  

---

## Tech Stack

- **Language**: Python 3.10+  
- **Embeddings**: [sentence-transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`)  
- **Vector DB**: FAISS / Chroma  
- **Database**: SQLite  
- **OCR**: Tesseract via `pytesseract`  
- **API**: FastAPI + Uvicorn  
- **CLI**: Typer  

---

## Installation

Clone the repo:

```bash
git clone https://github.com/KH4NY0/ai-filesystem.git
cd ai-filesystem
```
