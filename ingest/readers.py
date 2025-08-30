from pathlib import Path
import pdfplumber
from PIL import Image
import pytesseract

TEXT_EXT = {".txt", ".md", ".py", ".json", ".csv"}
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}

def read_text(path: Path) -> str:
    return path.read_text(errors="ignore")

def read_pdf(path: Path) -> str:
    out = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            out.append(page.extract_text() or "")
    return "\n".join(out)

def read_image_ocr(path: Path) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def extract_content(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in TEXT_EXT:
        return read_text(path)
    if ext == ".pdf":
        return read_pdf(path)
    if ext in IMG_EXT:
        return read_image_ocr(path)
    return ""  # unsupported → still index basic metadata
