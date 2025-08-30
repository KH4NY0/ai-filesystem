import re
from typing import Dict

def parse_intent(text: str) -> Dict:
    """
    Naive rule-based parser for demo.
    Returns a dict: {action, query, dest, tags}
    """

    text_l = text.lower()

    if text_l.startswith("search ") or text_l.startswith("find "):
        query = re.sub(r"^(search|find)\s+", "", text_l)
        return {"action": "search", "query": query}

    if text_l.startswith("move "):
        # Example: "move invoices to /Archive/Invoices"
        m = re.match(r"move (.+) to (.+)", text_l)
        if m:
            return {"action": "move", "query": m.group(1), "dest": m.group(2)}

    if text_l.startswith("tag "):
        # Example: "tag project notes with design,ux"
        m = re.match(r"tag (.+) with (.+)", text_l)
        if m:
            tags = [t.strip() for t in m.group(2).split(",")]
            return {"action": "tag", "query": m.group(1), "tags": tags}

    if text_l.startswith("summarize "):
        query = text_l.replace("summarize ", "", 1)
        return {"action": "summarize", "query": query}

    return {"action": "unknown", "query": text}
