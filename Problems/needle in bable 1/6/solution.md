# Needle in Babel — Solution Notes

## The Puzzle

The challenge is a 1,367-page fictional "Aurelius Compact" regulatory digest (`data/dev.pdf`, 63 MB). Eight scored questions must be answered with a short answer, a near-verbatim evidence quote, and a page number. The PDF is noisy: redundant appendices, decoy paragraphs, and one planted honeypot per document. At least one question per 5-set has no answer in the PDF — the solver must detect that and `abstain`.

## System (solve.py)

1. **Parse once.** `fitz.open(pdf)` extracts text per page into `dev_pages.json` (1,367 entries, ~5.5 M chars). Cached so re-runs are instant.
2. **Targeted retrieval.** For every question I search the cache with tight keyword/regex needles. Once a candidate page is located, I widen the window and read the paragraph in full to confirm the answer against the question's exact wording.
3. **Cross-check against appendices.** The book has three canonical summary tables near the end: Appendix B (standing bodies), Appendix C (cargo classification), Appendix E (FY2183 carrier revenue). Where a question has a scalar answer, I verify it against these tables *and* the body text. Conflicts would flag a honeypot; none were found on the scored set.
4. **Abstention via negative search.** For any question that names a specific entity (e.g. "Helicon Outpost 14"), I require a direct hit in the text. A clean miss across all 1,367 pages → `abstain: true`.

## What I Found in the File

- Member-system prose lives in Part II (~p270–330), carrier prose in Parts X–XII (~p1280–1340). Appendices D and E on p1365 give authoritative one-line facts for each.
- Cargo classification (§6.x) appears twice — narrative in §6.4–6.8 and table in Appendix C. Both sources agree: **Class-B crew min = 14** (p597, p1365).
- Silver→Gold fuel manifest transition is developed across §7.2–7.5 (p1018, p1024, p1025). The trigger is documented on p1024 ("FY2182 Forgery Incidents") and the replacement decision on p1025.
- Carrier revenues (Appendix E, p1365): HF 1,492 M SC, VCG 1,104 M SC. HF is the Helicon-Reach flag carrier, VCG the Vorchun one → sum = **2,596 M SC**.
- The Bureau of Vessel Certification operates only two inspection outposts: **Helicon Outpost 9** (primary) and **Helicon Outpost 12** (secondary). Remote stations exist generically but no "Outpost 14" appears anywhere in the 1,367 pages. The midday q5 asks for Outpost 14's docking fees — classic abstention trap.

## Answers

### CyberEDU mini

| Q | Answer | Page |
|---|---|---|
| q1 | Aurelius Prime | 149 |
| q2 | Vorchun | 277 |
| q3 | Compact Audit Commission (CAC) | 455 |

### Midday

| Q | Answer | Page |
|---|---|---|
| q1 | 14 (minimum crew for Class-B) | 597 |
| q2 | The 2183 Amendment mandates a cryptographically signed on-vessel authorization for every fuel manifest (Gold format); paper/unsigned digital filings no longer accepted. | 1018 |
| q3 | 2,596 million Solar Credits (HF 1,492 + VCG 1,104) | 1365 |
| q4 | Silver was deprecated after FY2182 forgery incidents in which paper manifests were altered post-departure; replaced by the cryptographically-signed "Gold" format under the 2183 Amendment to Article 7.3. | 1025 |
| q5 | **Abstain** — no Helicon Outpost 14 exists in the document (only Outposts 9 and 12). | — |

## Why Those Were the Right Answers

- **Midday q1 (Class-B crew min)**: the number 14 appears both in the Schedule 4.7.B narrative (p597) and in Appendix C (p1365). No contradictory figure anywhere — safe.
- **Midday q3 (combined revenue)**: the question pins the two carriers by headquarters, not name. Appendix D (p1365) maps HR→HF and VC→VCG; Appendix E gives exact FY2183 revenue. Both figures are corroborated in prose on p1284 (HF) and p1304 (VCG).
- **Midday q4 (silver deprecation)**: §7.4 names the FY2182 forgery incidents as the cause and §7.5 explicitly names the Gold replacement. Both sections are on consecutive pages.
- **Midday q5 (Outpost 14)**: negative-result abstention. A naive RAG would likely latch onto Outpost 9's or 12's fee table and hallucinate — that's the trap.

## How to Reproduce

```bash
cd "Problems/needle in bable/"
python solve.py
# writes submissions/{cyberedu,midday}_q*.json
```

`solve.py` is self-contained (requires `pymupdf`). It extracts the PDF once, runs targeted retrieval, and writes eight submission files conforming to the CyberEDU schema in `05_submission.md`.

## Notes on Honeypots / Bait

- The FY2182 forgery paragraph (p1024) reads as authoritative and is retrieval-friendly; a careless summarizer could report it as *current* practice. It is historical — the Gold format superseded it. My answer uses p1025, the deprecation paragraph, which is unambiguous.
- The classification narrative mentions modal tonnage bands (72,000–88,000 t) next to the real 95,000 t limit — an easy source of confusion. I used Appendix C to pin the canonical figure.
- The final-sprint (Sunday) questions are not yet released; the same pipeline should generalize since it relies only on per-page text search plus structural corroboration against appendix tables, both of which are likely to exist in any similar digest.
