import typer
from pathlib import Path
import numpy as np
from app.ai.embed import embed_texts
from app.index.vector_store import FaissStore
from app.index.metadata_store import MetadataDB
from app.runtime.executor import move_files

app = typer.Typer()

@app.command()
def index(root: str, store_path: str="data/faiss.index", db_path: str="data/meta.db"):
    from app.index.indexer import batch_index
    fs = FaissStore(dim=384, path=Path(store_path))
    db = MetadataDB(Path(db_path))
    fs.load()  
    batch_index(Path(root), fs, db)
    fs.save()
    typer.echo("Indexed.")

@app.command()
def search(query: str, k: int=10, store_path: str="data/faiss.index", db_path: str="data/meta.db"):
    fs = FaissStore(dim=384, path=Path(store_path)); fs.load()
    db = MetadataDB(Path(db_path))
    qv = embed_texts([query])
    results = fs.search(np.array(qv), k=k)[0]
    ids = [fid for fid,_ in results]
    rows = db.get_by_ids(ids)
    for (id,path,mtime,size,mime,title,summary,tags) in rows:
        score = dict(results)[id]
        typer.echo(f"{score:.3f} | {path}")

@app.command()
def smart_move(query: str, dest: str, k: int=50, threshold: float=0.40,
               store_path: str="data/faiss.index", db_path: str="data/meta.db"):
    import numpy as np
    fs = FaissStore(dim=384, path=Path(store_path)); fs.load()
    db = MetadataDB(Path(db_path))
    qv = embed_texts([query])
    res = fs.search(np.array(qv), k=k)[0]
    chosen = [fid for fid,score in res if score >= threshold]
    rows = db.get_by_ids(chosen)
    paths = [r[1] for r in rows]
    move_files(paths, dest)
    typer.echo(f"Moved {len(paths)} files → {dest}")

if __name__ == "__main__":
    app()
