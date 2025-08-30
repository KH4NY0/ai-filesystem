import faiss
import numpy as np
from pathlib import Path
import pickle

class FaissStore:
    def __init__(self, dim: int, path: Path):
        self.dim = dim
        self.path = path
        self.index = faiss.IndexFlatIP(dim)  # cosine if vectors normalized
        self.ids: list[str] = []

    def _normalize(self, v):
        n = np.linalg.norm(v, axis=1, keepdims=True) + 1e-10
        return v / n

    def add(self, ids: list[str], vectors: np.ndarray):
        vectors = self._normalize(vectors)
        self.index.add(vectors)
        self.ids.extend(ids)

    def search(self, query_vector: np.ndarray, k=10):
        q = self._normalize(query_vector)
        scores, idxs = self.index.search(q, k)
        results = []
        for row_scores, row_idxs in zip(scores, idxs):
            res = []
            for s, i in zip(row_scores, row_idxs):
                if i == -1: continue
                res.append((self.ids[i], float(s)))
            results.append(res)
        return results

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.path))
        with open(self.path.with_suffix(".ids.pkl"), "wb") as f:
            pickle.dump(self.ids, f)

    def load(self):
        if self.path.exists():
            self.index = faiss.read_index(str(self.path))
            with open(self.path.with_suffix(".ids.pkl"), "rb") as f:
                self.ids = pickle.load(f)
