import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import Config
from index.vector_store import FaissStore
from index.metadata_store import MetadataDB
from ingest.readers import extract_content
from ai.embed import embed_texts
from index.indexer import file_id

class IndexUpdateHandler(FileSystemEventHandler):
    def __init__(self, fs: FaissStore, db: MetadataDB):
        self.fs = fs
        self.db = db

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        self._index_file(path)

    def on_modified(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        self._index_file(path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        # For simplicity: just remove from DB (vector pruning is trickier)
        fid = file_id(Path(event.src_path))
        self.db.conn.execute("DELETE FROM files WHERE id=?", (fid,))
        self.db.conn.commit()
        print(f"🗑 Removed {event.src_path} from index")

    def _index_file(self, path: Path):
        try:
            text = extract_content(path)
            vec = embed_texts([text])
            fid = file_id(path)
            stat = path.stat()
            self.fs.add([fid], vec)
            self.db.upsert_file(
                fid,
                path=str(path),
                mtime=stat.st_mtime,
                size=stat.st_size,
                mime=path.suffix.lower(),
                title=path.stem
            )
            self.fs.save()
            print(f"📥 Indexed {path}")
        except Exception as e:
            print(f"⚠️ Failed to index {path}: {e}")

def start_watcher():
    fs = FaissStore(dim=Config.VECTOR_DIM, path=Config.VECTOR_INDEX)
    fs.load()
    db = MetadataDB(Config.META_DB)

    event_handler = IndexUpdateHandler(fs, db)
    observer = Observer()
    observer.schedule(event_handler, str(Config.ROOT_DIR), recursive=True)

    observer.start()
    print(f"👀 Watching {Config.ROOT_DIR} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()
