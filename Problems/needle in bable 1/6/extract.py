"""Extract dev.pdf text into a per-page JSON index."""
import fitz, json, os

PDF = "data/dev.pdf"
OUT = "dev_pages.json"

def main():
    doc = fitz.open(PDF)
    pages = []
    for i, page in enumerate(doc):
        pages.append(page.get_text())
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False)
    total = sum(len(p) for p in pages)
    print(f"extracted {len(pages)} pages, {total:,} chars -> {OUT}")

if __name__ == "__main__":
    main()
