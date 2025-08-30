from fastapi import FastAPI, Query
from pydantic import BaseModel
from pathlib import Path
import numpy as np

from ai.embed import embed_texts
from index.vector_store import FaissStore
from index.metadata_store import MetadataDB
from ai.intent import parse_intent
from runtime.executor import move_files

app = FastAPI(title="AI Filesystem API")

STORE_PATH = Path("data/faiss.index")
DB_PATH = Path("data/meta.db")

fs = FaissStore(dim=384, path=STORE_PATH)
fs.load()
db = MetadataDB(DB_PATH)

class IntentResponse(BaseModel):
    action: str
    query: str | None = None
    dest: str | None = None
    tags: list[str] | None = []

@app.get("/")
def root():
    return {"status": "AI Filesystem API is running 🚀"}

@app.get("/search")
def search(query: str = Query(..., description="Semantic search query"), k: int = 10):
    qv = embed_texts([query])
    results = fs.search(np.array(qv), k=k)[0]
    ids = [fid for fid, _ in results]
    rows = db.get_by_ids(ids)
    return [
        {"score": dict(results)[fid], "path": row[1], "title": row[6] or Path(row[1]).stem}
        for fid, row in zip(ids, rows)
    ]

@app.post("/intent", response_model=IntentResponse)
def intent(user_input: str):
    return parse_intent(user_input)

@app.post("/action/move")
def action_move(query: str, dest: str, k: int = 20, threshold: float = 0.4):
    qv = embed_texts([query])
    res = fs.search(np.array(qv), k=k)[0]
    chosen = [fid for fid, score in res if score >= threshold]
    rows = db.get_by_ids(chosen)
    paths = [r[1] for r in rows]
    move_files(paths, dest)
    return {"moved": len(paths), "dest": dest, "files": paths}
