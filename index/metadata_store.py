import sqlite3
from pathlib import Path
from typing import Optional, Iterable

SCHEMA = """
CREATE TABLE IF NOT EXISTS files(
  id TEXT PRIMARY KEY,
  path TEXT UNIQUE,
  mtime REAL,
  size INTEGER,
  mime TEXT,
  title TEXT,
  summary TEXT,
  tags TEXT
);
"""

class MetadataDB:
    def __init__(self, db_path: Path):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(SCHEMA)
        self.conn.commit()

    def upsert_file(self, id: str, **kw):
        cols = ["id"] + list(kw.keys())
        vals = [id] + list(kw.values())
        placeholders = ",".join(["?"]*len(cols))
        updates = ",".join([f"{k}=excluded.{k}" for k in kw.keys()])
        sql = f"INSERT INTO files ({','.join(cols)}) VALUES ({placeholders}) ON CONFLICT(id) DO UPDATE SET {updates}"
        self.conn.execute(sql, vals)
        self.conn.commit()

    def get_by_ids(self, ids: Iterable[str]):
        q = "SELECT * FROM files WHERE id IN ({})".format(",".join(["?"]*len(list(ids))))
        return self.conn.execute(q, list(ids)).fetchall()

    def by_path(self, path: str) -> Optional[tuple]:
        return self.conn.execute("SELECT * FROM files WHERE path=?", (path,)).fetchone()
