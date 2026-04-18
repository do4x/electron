"""Simple keyword + regex search over the extracted PDF pages."""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

with open("dev_pages.json", "r", encoding="utf-8") as f:
    PAGES = json.load(f)

def search(pattern, flags=re.IGNORECASE, window=240, max_hits=30):
    rx = re.compile(pattern, flags)
    hits = []
    for i, text in enumerate(PAGES):
        for m in rx.finditer(text):
            lo = max(0, m.start() - window)
            hi = min(len(text), m.end() + window)
            snippet = text[lo:hi].replace("\n", " ")
            hits.append((i + 1, snippet))
            if len(hits) >= max_hits:
                return hits
    return hits

def show(hits):
    for p, s in hits:
        print(f"[p{p}] {s}")
        print("---")

if __name__ == "__main__":
    pattern = sys.argv[1] if len(sys.argv) > 1 else "BVC-certified tonnage"
    show(search(pattern))
