# 01 — Overview

## What you are building

A system that answers questions over a large, noisy, hidden PDF document, **fast** and **accurately**, with valid citations.

The PDF is big — large enough that you cannot dump it into any current LLM context window in one shot. You must build something smarter than "paste and pray."

## The shape of the challenge

- You get a **dev PDF** (hundreds to a few thousand pages) on Saturday morning. You spend the day building your system against it.
- You answer **5 midday questions** on the dev PDF over the course of Saturday. Scored on accuracy + speed.
- You also answer **3 simpler questions** in the CyberEDU mini stage (gives you live feedback). Scored lightly.
- On Sunday, a **different PDF of the same scale** lands. You have **15 minutes** to answer 5 new questions on it.
- You then present your work to a jury and submit a write-up.

Every question requires an answer **plus** a short evidence quote from the PDF **plus** a page number. No unsupported answers.

## What makes this hard

- **Scale**: the PDF exceeds any current model's context window. No brute force by dumping.
- **Noise**: the document is full of on-topic filler, near-duplicate paragraphs with wrong numbers, tables that rephrase the same facts, and distractors.
- **Honeypots**: at least one paragraph per PDF is an authoritative-looking trap. Do not trust the first plausible hit.
- **Question difficulty varies**: from `Ctrl+F` easy to multi-hop synthesis across distant sections.
- **Abstention traps**: at least one question per set of 5 has **no answer in the document**. You must detect this and abstain. Wrong answers are scored 0; correct abstention is scored 1.
- **Speed matters**: scoring rewards fast correct answers more than slow correct answers, but never rewards fast wrong ones.
- **You also have to build a cold-start system**. The Sunday PDF is new. Your pipeline must generalize from the dev PDF, not overfit to it.

## What you deliver

1. Answers as JSON files uploaded to CyberEDU (schema in [`05_submission.md`](05_submission.md)).
2. A 1–2 page write-up (criteria in [`04_scoring.md`](04_scoring.md)).
3. A 7-minute presentation to the jury on Sunday.

## What you do NOT deliver

- No code is submitted for evaluation. Nobody will run your repo. Build whatever you want.
- No Docker image, no HTTP service, no live demo required.

## The general shape of a good solution

We do not tell you how to build this. Part of the challenge is figuring it out. Your architecture, retrieval strategy, chunking choices, model selection, and speed/accuracy trade-off are all yours.

Read [`06_hints.md`](06_hints.md) for strategic hints.
