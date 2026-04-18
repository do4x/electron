"""
solve.py — Needle in Babel (dev.pdf)

Reproduces the scored-stage answers end-to-end from data/dev.pdf.

Pipeline:
  1. Extract per-page text from the PDF with PyMuPDF (once, cached to dev_pages.json).
  2. Use targeted regex/keyword search against the page cache to locate evidence.
  3. For each question, emit a CyberEDU-schema JSON submission to submissions/.

Run from the task folder:
    python solve.py
"""
from __future__ import annotations
import json, os, re, sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = Path(__file__).parent
PDF = HERE / "data" / "dev.pdf"
CACHE = HERE / "dev_pages.json"
OUT = HERE / "submissions"


def load_pages() -> list[str]:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    import fitz
    doc = fitz.open(PDF)
    pages = [p.get_text() for p in doc]
    CACHE.write_text(json.dumps(pages, ensure_ascii=False), encoding="utf-8")
    return pages


def find_page(pages: list[str], needle: str, flags=re.IGNORECASE) -> int | None:
    rx = re.compile(re.escape(needle), flags)
    for i, text in enumerate(pages):
        if rx.search(text):
            return i + 1
    return None


def assert_in(pages: list[str], page_1idx: int, quote_start: str):
    text = pages[page_1idx - 1]
    assert quote_start.lower() in text.lower(), (
        f"quote not found on page {page_1idx}: {quote_start[:80]!r}"
    )


def build_submissions(pages: list[str]) -> dict:
    submissions = {}

    # ── CyberEDU mini (3 questions) ───────────────────────────────────
    submissions["cyberedu"] = {}

    # q1 — capital / administrative seat
    q_quote = (
        "The capital and administrative seat of the Compact is Aurelius Prime, "
        "from which the Compact Commerce Directorate and the Registry of Master "
        "Haulers conduct regulatory operations."
    )
    p = find_page(pages, "capital and administrative seat of the Compact is Aurelius Prime")
    assert p is not None
    submissions["cyberedu"]["q1"] = {
        "question_id": "q1",
        "answer": "Aurelius Prime",
        "evidence_quote": q_quote,
        "page": p,
        "abstain": False,
        "confidence": "high",
    }

    # q2 — agricultural exporter
    q_quote = (
        "Vorchun remains the Compact's principal agricultural exporter, its "
        "cold-chain bonded ports handling over a billion metric tons of bio-freight "
        "annually as of FY2183."
    )
    p = find_page(pages, "Vorchun remains the Compact")
    assert p is not None
    submissions["cyberedu"]["q2"] = {
        "question_id": "q2",
        "answer": "Vorchun",
        "evidence_quote": q_quote,
        "page": p,
        "abstain": False,
        "confidence": "high",
    }

    # q3 — body that audits member-system regulatory implementations
    q_quote = (
        "The Commission's remit is the audit of member-system regulatory "
        "implementations, and its findings — published following each annual audit "
        "cycle — are the principal mechanism by which the Directorate tracks the "
        "operational performance of the member systems at the port level."
    )
    p = find_page(pages, "remit is the audit of member-system regulatory implementations")
    assert p is not None
    submissions["cyberedu"]["q3"] = {
        "question_id": "q3",
        "answer": "Compact Audit Commission (CAC)",
        "evidence_quote": q_quote,
        "page": p,
        "abstain": False,
        "confidence": "high",
    }

    # ── Midday (5 questions) ──────────────────────────────────────────
    submissions["midday"] = {}

    # q1 — Class-B crew minimum.  Corroborated on p597 (§4.4.2) and Appendix C.
    q_quote = (
        "Schedule 4.7.B of the Commerce Accords specifies the operational "
        "requirements for Class-B bulk non-perishable carriers. The tonnage limit "
        "per vessel is set at 95,000 metric tons, and the minimum crew complement "
        "is 14, including at least one officer qualified in bulk-manifest "
        "verification."
    )
    p = find_page(pages, "Class-B bulk non-perishable carriers")
    assert p is not None
    submissions["midday"]["q1"] = {
        "question_id": "q1",
        "answer": "14",
        "evidence_quote": q_quote,
        "page": p,
        "abstain": False,
        "confidence": "high",
    }

    # q2 — 2183 Amendment to Article 7.3
    q_quote = (
        "The 2183 Amendment to Article 7.3 of the Commerce Accords mandates that "
        "all fuel manifests filed with the Compact Commerce Directorate must carry "
        "a cryptographically signed authorization generated on-vessel at time of "
        "departure."
    )
    p = find_page(pages, "must carry a cryptographically signed authorization generated on-vessel")
    assert p is not None
    submissions["midday"]["q2"] = {
        "question_id": "q2",
        "answer": (
            "It mandates that every fuel manifest filed with the Compact Commerce "
            "Directorate carry a cryptographically signed authorization generated "
            "on-vessel at the time of departure (the 'Gold' format); paper and "
            "unsigned digital submissions are no longer accepted."
        ),
        "evidence_quote": q_quote,
        "page": p,
        "abstain": False,
        "confidence": "high",
    }

    # q3 — combined FY2183 revenue of Helicon-Reach-HQ (HF) and Vorchun-HQ (VCG) carriers
    # HF = 1,492 mSC (p1284); VCG = 1,104 mSC (p1304); both confirmed by Appendix E (p1365).
    # 1,492 + 1,104 = 2,596 million Solar Credits.
    q_quote = (
        "Carrier FY2183 revenue (SC millions) Fleet (FY2183) AUSC 2,817 412 HF "
        "1,492 238 VCG 1,104 196 KXP 1,058 163 MRR 874 151 PSF 812 128 Total "
        "8,157 1,288"
    )
    p = find_page(pages, "HF\n1,492")  # Appendix E layout
    if p is None:
        p = find_page(pages, "1,492")
    submissions["midday"]["q3"] = {
        "question_id": "q3",
        "answer": "2,596 million Solar Credits (HF 1,492 M + VCG 1,104 M)",
        "evidence_quote": q_quote,
        "page": p,
        "abstain": False,
        "confidence": "high",
    }

    # q4 — why silver was deprecated, what replaced it
    q_quote = (
        "In response to the FY2182 incidents, the Compact Commerce Directorate "
        "formally deprecated the silver manifest format at the start of FY2183 and "
        "replaced it with the \u2018Gold\u2019 manifest format defined in the 2183 "
        "Amendment to Article 7.3, which requires cryptographic signing at time of "
        "departure."
    )
    p = find_page(pages, "formally deprecated the silver manifest format")
    assert p is not None
    submissions["midday"]["q4"] = {
        "question_id": "q4",
        "answer": (
            "The silver (paper-plus-unsigned-digital) format was deprecated after "
            "FY2182 forgery incidents in which paper manifests were altered after "
            "departure and the tampering was only detected post-voyage; the ISB "
            "identified the post-hoc verification lag as the common enabler. It "
            "was replaced by the 'Gold' manifest format defined in the 2183 "
            "Amendment to Article 7.3, which binds the manifest cryptographically "
            "to the vessel at the moment of departure."
        ),
        "evidence_quote": q_quote,
        "page": p,
        "abstain": False,
        "confidence": "high",
    }

    # q5 — docking fee schedule at Helicon Outpost 14.  The document only
    # describes Helicon Outpost 9 (primary) and Helicon Outpost 12 (secondary);
    # no Outpost 14 exists.  Abstain.
    has_14 = any("Helicon Outpost 14" in t or "Outpost 14" in t for t in pages)
    assert not has_14, "unexpected: Outpost 14 appears in the PDF"
    submissions["midday"]["q5"] = {
        "question_id": "q5",
        "answer": "",
        "evidence_quote": "",
        "page": 0,
        "abstain": True,
        "confidence": "high",
    }

    return submissions


def main():
    pages = load_pages()
    print(f"loaded {len(pages)} pages")
    subs = build_submissions(pages)
    OUT.mkdir(exist_ok=True)
    for stage, qs in subs.items():
        for qid, payload in qs.items():
            path = OUT / f"{stage}_{qid}.json"
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                            encoding="utf-8")
            flag = "ABSTAIN" if payload["abstain"] else f"p{payload['page']}"
            print(f"  {stage}/{qid}  [{flag}]  -> {path.name}")
    print(f"\nwrote {sum(len(v) for v in subs.values())} submissions to {OUT}")


if __name__ == "__main__":
    main()
