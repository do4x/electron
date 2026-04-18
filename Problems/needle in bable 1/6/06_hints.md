# 06 — Hints

Strategic advice. Every hint here is load-bearing. Do not skim.

## 1. Feed these rules to your LLM

All MD files in this repo are LLM-friendly. Paste [`01_overview.md`](01_overview.md), [`03_rules.md`](03_rules.md), [`04_scoring.md`](04_scoring.md), [`05_submission.md`](05_submission.md), and this file into a ChatGPT or Claude conversation. Ask it to summarize the scoring, compute break-even tables, remind you of edge cases. Then follow the paste-in recipe in [`07_advisor.md`](07_advisor.md) to build your own in-loop advisor.

## 2. Speed vs accuracy is a math problem, not a feeling

The formula is `score = accuracy × (0.5 + 0.5 × speed_factor)`. For the midday stage, `speed_factor = exp(-t/120)`.

The break-even logic: **is waiting N more minutes worth it, given you expect your accuracy to improve by Δa?**

```
wait if:  Δa × (0.5 + 0.5 × speed_factor(t + N))  >  a_now × 0.5 × (speed_factor(t) − speed_factor(t + N))
```

Compute this during the challenge for each question you're unsure about. Do not eyeball it.

## 3. Citations are mandatory

A correct answer **without** a valid evidence quote is capped at `0.5` accuracy. A correct answer **with** a valid evidence quote is capped at `1.0`. Always cite. Always copy the quote verbatim from the PDF.

## 4. Abstention detection is one of the highest-leverage tasks

One question per set has **no answer in the document**. A naive RAG system will happily hallucinate against a tempting distractor and score `0`. A system that can reliably say "this isn't in the doc" will pick up a free `1.0` on the trap. Build this.

## 5. Question difficulty is not uniform

The 5 midday questions cover five different difficulty levels:

- **L1** — direct lookup. `Ctrl+F` could find it.
- **L2** — paraphrase. Same fact stated in different words.
- **L3** — multi-hop. Requires combining 2+ sections.
- **L4** — synthesis. Requires reasoning on retrieved evidence.
- **L5** — abstention trap. Answer not in the document.

Do not spend equal time on each. L1 is cheap points. L4 needs your best retrieval + reasoning. L5 needs your abstention logic to fire.

## 6. Process the PDF once, well

Re-parsing the PDF for every question wastes time and tokens. Build an index — chunked, embedded, searchable — and query it. Your pipeline's cold-start matters on Sunday: the final PDF lands, and you have 15 minutes. That includes parsing.

## 7. The final PDF is different content, same scale

Everything you build must run end-to-end in 15 minutes against a PDF you've never seen. Do not overfit your chunking, your prompts, or your heuristics to the dev PDF. Test on something similar you generate or download, make sure your pipeline generalizes.

## 8. Cost is not scored, but it's asked about

There is no cost cap. You can burn whatever you want on API calls. But your write-up and presentation will be judged on `Strategic use of tools/technologies/AI`. "We called GPT-4 eight times per question" is a strategic choice you should be able to defend. Log your costs, report them, explain them.

## 9. Submit when confident, not when anxious

Only the first submission per `(team, question)` counts. There is no "resubmit with a better answer." Making a hasty wrong submission costs you everything. Making a slow correct submission costs you the speed bonus but keeps the floor of `0.5`. Prefer slow-correct to fast-wrong.

## 10. Honeypots exist

Each PDF contains **at least one honeypot**: an authoritative-looking paragraph that states something false with high confidence. Systems that pick the first high-retrieval-score paragraph and summarize it get burned. Cross-check retrieval results. Use multiple search queries. Reason over evidence, don't just quote it.

## Bonus: a sample build plan for 6–8 hours

This is not a required approach. It's one way to structure your time.

| Time | What |
|---|---|
| 0:00–0:30 | Read all rules + hints. Run your LLM advisor on them. Agree on architecture. |
| 0:30–1:30 | PDF parsing. Chunking. Indexing. |
| 1:30–3:00 | Retrieval + answer generation on calibration questions. Verify pipeline. |
| 3:00–4:00 | Add abstention detection. Add evidence-quote extraction. Add citation verification. |
| 4:00–5:00 | Optimize for speed. Cache. Parallelize. |
| 5:00–5:30 | Attack midday 5. Submit as you go. |
| 5:30–6:00 | CyberEDU mini 3 for live feedback. Debug anything your pipeline got wrong there. |
| 6:00+ | Harden against cold-start. Test on a different PDF. |
| Evening | Write-up draft. Presentation prep. |
