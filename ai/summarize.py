def summarize(text: str) -> str:
   
    if not text: return ""
    snip = text.strip().splitlines()[:3]
    return " ".join(snip)[:400]