from pathlib import Path
import shutil
from typing import List, Tuple

def move_files(paths: List[str], dest: str):
    Path(dest).mkdir(parents=True, exist_ok=True)
    for p in paths:
        shutil.move(p, str(Path(dest) / Path(p).name))