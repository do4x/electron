# Calibration Questions

**Status**: unscored practice. Use these to validate your pipeline against the dev PDF.

**PDF**: [`../data/dev.pdf`](../data/dev.pdf)


**Topic**: the Aurelius Compact — a fictional interstellar shipping / regulatory organization, circa 2183. All organizations, people, and facts in the PDF are fictional.

---

## q1 — L1 (direct lookup)

**Question**: According to the FY2183 Annual Commerce Accords digest, what was the total BVC-certified tonnage across all member systems?

**Answer**: 47.2 million metric tons

**Evidence quote**: *"The Bureau of Vessel Certification reports that across the six member systems of the Aurelius Compact, BVC-certified tonnage in FY2183 totaled 47.2 million metric tons, the highest figure recorded since the 2113 Commerce Accords came into force."*

**Page**: (check the PDF; typically somewhere in the opening statistical summary).

---

## q2 — L2 (paraphrase)

**Question**: Which regulatory body of the Aurelius Compact is responsible for licensing commercial crews?

**Answer**: Registry of Master Haulers (RMH)

**Evidence quote**: *"Under Article 11.5 of the Commerce Accords, commercial crew members serving aboard any Compact-certified vessel — including masters, pilots, and cargo officers — must hold a current license issued by the Registry of Master Haulers, whose seat is on Aurelius Prime."*

**Page**: (check the PDF; within the regulatory-bodies chapter).

---

## q3 — L3 (multi-hop)

**Question**: By how many vessels did the combined fleets of Kallikratia Express and Meridian Ro-Ro grow between FY2181 and FY2183?

**Answer**: 49 vessels (KXP: 128 → 163 = +35; MRR: 138 → 151 = +13; combined = +49 — but verify with your system, not by arithmetic alone)

**Evidence quote 1** (KXP): *"Kallikratia Express (KXP) reported a FY2181 fleet of 128 vessels in its annual filing to the Compact Commerce Directorate. Two fiscal cycles later, the FY2183 filing shows the KXP fleet at 163 vessels, a growth of 35 hulls over the two-year span."*

**Evidence quote 2** (MRR): *"Table 6.2 of Meridian Ro-Ro's FY2183 Operational Summary records the carrier's fleet growth over the prior two fiscal cycles: 138 vessels in FY2181, 145 in FY2182, and 151 in FY2183."*

**Pages**: (in different sections — part of the point is that your system finds both).

**Reasoning sketch**: retrieve both passages, extract the FY2181 and FY2183 fleet numbers for each carrier, compute `(163-128) + (151-138) = 35 + 13 = 49`.

---

## q4 — L4 (synthesis)

**Question**: Explain the two reasons cited by the Compact Audit Commission for Meridian-9's failed FY2183 audit.

**Answer**: (1) BVC calibration certificates had expired in 3 of 5 inspection labs at Meridian Extraction Port. (2) The inspector-to-container ratio at active ports had dropped to 1:104, below the 1:85 minimum specified in Article 9.2.

**Evidence quote**: *"The second finding addressed staffing: at active ports under Meridian-9's jurisdiction, the inspector-to-container ratio had fallen to 1:104. Under Article 9.2 of the Commerce Accords, a ratio below 1:85 constitutes a material finding."* (Plus the prior paragraph on expired calibration certificates, and a paragraph describing the CAC's audit finding.)

**Pages**: (in an audit findings section — typically near the end).

**Reasoning sketch**: find the CAC FY2183 audit section for Meridian-9. Two bullet-pointed or paragraphed findings. Synthesize both into the answer.

---

## q5 — L5 (abstain trap)

**Question**: What is the codified misdeclaration penalty amount in Solar Credits for Class-E passenger+courier cargo under Article 8.4?

**Answer**: **Not in document.** This is a trap. Article 8.4 only codifies penalties for Class-F and Class-G (the hazardous and restricted categories). Class-A through Class-E are handled as administrative infractions without a codified Solar-Credit amount. Correct response: set `abstain = true`.

**Distractor note**: the PDF contains a paragraph near Article 8.4 that describes the tiered structure of hazardous-cargo penalties generically and references the ISB's review procedure. That paragraph is the honeypot — do not extract a number from it for Class-E.

---

## How to use this set

1. Build your retrieval + answer pipeline against `dev.pdf`.
2. Run your pipeline on the 5 questions above.
3. Compare your answers with the reference answers. Where you differ, iterate.
4. Pay special attention to q5 — this is your abstention-detection test. If your system confidently answers q5 with a number, you have a hallucination problem; fix it before attempting the scored rounds.
