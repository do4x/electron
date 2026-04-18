# 08 — FAQ

This file starts small and grows as real questions come in during the hackathon. Check back regularly.

## General

**Q: Can I use my own API key? OpenAI, Anthropic, Google, whatever?**
A: Yes. Any model, any provider. See [`03_rules.md`](03_rules.md).

**Q: Is internet access allowed during the challenge?**
A: Yes.

**Q: How large is the PDF?**
A: Hundreds to a few thousand pages. Large enough that you cannot dump it into a single model context.

**Q: Is the PDF real-world content or synthetic?**
A: The content is synthetic. Do not try to look up answers online — the organization, people, and facts in the document are fictional.

## Submission

**Q: What if I submit twice by accident?**
A: Only the first submission per `(team, question)` counts. The duplicate is ignored. This is not a DQ unless it's a pattern or looks intentional.

**Q: What if I upload the JSON file to CyberEDU before I'm ready?**
A: You cannot undo. That submission is now your answer. Be careful — validate your JSON and double-check the answer before uploading.

**Q: My evidence quote is slightly paraphrased because I had to clean up OCR artifacts. Is that okay?**
A: The evaluator uses fuzzy matching (Levenshtein ratio ≥ 0.85). Minor cleanup is tolerated. Paraphrasing the content is not.

**Q: Can I submit an abstain flag AND an answer?**
A: The `abstain = true` flag is authoritative. If you check it, your answer text is ignored. Don't hedge by filling in both.

## Scoring

**Q: What happens if my team doesn't submit a particular question?**
A: Score for that question = 0.

**Q: Does the calibration stage count toward my score?**
A: No. Calibration is unscored practice. See [`questions/calibration.md`](questions/calibration.md).

**Q: How is the AI judge kept fair across teams?**
A: Single deterministic call per answer at `temp=0`, pinned model version, rubric-anchored prompt. Every call is logged for audit.

## Tools

**Q: Can I use ChatGPT's "Ask about this PDF" feature?**
A: Technically yes — for correctness of your answers. But your write-up and presentation have to show what you built. "I uploaded the PDF to ChatGPT" is not a system. See `Claim-to-evidence ratio`, `Solution design`, and `Innovation` in [`04_scoring.md`](04_scoring.md).

**Q: Can I use Claude Code / Codex / Cursor to write my code?**
A: Yes, encouraged. Strategic use of AI tooling is itself a scoring criterion.

## Cheating / DQ

**Q: Is it OK to share the dev PDF with another team for discussion?**
A: No. No inter-team sharing of anything.

**Q: Can I contact organizers during the challenge?**
A: Yes, for technical / logistical issues. Not for strategy or content questions.

## Appeals

**Q: I think the AI judge graded me wrong.**
A: Submit an appeal within 30 minutes of the leaderboard release. See the Appeals section of [`04_scoring.md`](04_scoring.md).

---

> **Organizers**: add new answers here as questions come in from teams. Keep each entry to a few lines.
