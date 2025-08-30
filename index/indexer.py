import hashlib, os, time
from pathlib import Path
import numpy as np
from app.ai.embed import embed_texts
from app.index.vector_store import FaissStore
from app.index.metadata_store import MetadataDB
from app.ingest.readers import extract_content

def file_id(path: Path) -> str:
    return hashlib.sha1(str(path.resolve()).encode()).hexdigest()

def batch_index(root: Path, store: FaissStore, db: MetadataDB, batch_size=64):
    docs, ids, metas = [], [], []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            p = Path(dirpath) / fn
            try:
                text = extract_content(p)
            except Exception:
                text = ""
            fid = file_id(p)
            stat = p.stat()
            docs.append(text[:4000])  # truncate for speed; chunk later
            ids.append(fid)
            metas.append(dict(
                path=str(p),
                mtime=stat.st_mtime,
                size=stat.st_size,
                mime=p.suffix.lower(),
                title=p.stem
            ))
            if len(docs) >= batch_size:
                vecs = embed_texts(docs)
                store.add(ids, vecs)
                for fid, meta in zip(ids, metas):
                    db.upsert_file(fid, **meta)
                docs, ids, metas = [], [], []
    if docs:
        vecs = embed_texts(docs)
        store.add(ids, vecs)
        for fid, meta in zip(ids, metas):
            db.upsert_file(fid, **meta)
