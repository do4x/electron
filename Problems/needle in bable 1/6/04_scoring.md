# 04 — Scoring

This is the binding reference for how every point is awarded. Read it carefully.

## Top-level breakdown

| Component | Weight |
|---|---|
| CTF (total) | **60%** |
| Write-up (automated AI evaluation) | **20%** |
| Jury presentation | **20%** |

## Needle in Babel internal breakdown

| Stage | Weight within Needle in Babel |
|---|---|
| CyberEDU mini — 3 simpler questions, AI-validated, live feedback on Saturday | **10%** |
| Midday — 5 questions on the dev PDF, scored by accuracy + speed | **40%** |
| Final sprint — 5 questions on a new PDF, 15 minutes, scored by accuracy + speed | **50%** |

## The scoring formula

For each question `q`:

```
score_q = accuracy_q × (α + (1 − α) × speed_factor_q)
```

Where:

- `accuracy_q ∈ {0, 0.25, 0.5, 0.75, 1.0}` — the AI judge's rubric-anchored grade of your answer.
- `α = 0.5` — the floor. A correct-but-slow answer still earns at least 50% of full credit.
- `speed_factor_q ∈ [0, 1]` — how fast you submitted, computed differently per stage (see below).

### Properties

- Fast + accurate → `≈ 1.0`
- Slow + accurate → `0.5`
- Fast + wrong → `0.0`
- Slow + wrong → `0.0`

**Accuracy is multiplicative.** If your answer is wrong, no speed bonus saves you.

### Speed factor — midday 5

Exponential decay with half-life `τ = 120 minutes`, starting from the challenge-open time:

```
speed_factor = exp( -t / 120 )
```

where `t` is minutes elapsed between challenge open and your submission.

Reference values:

| t (min) | speed_factor | score if accuracy = 1.0 |
|---|---|---|
| 0 | 1.00 | 1.00 |
| 30 | 0.78 | 0.89 |
| 60 | 0.61 | 0.80 |
| 120 | 0.37 | 0.68 |
| 240 | 0.14 | 0.57 |
| 360 | 0.05 | 0.52 |

### Speed factor — final 15-minute sprint

Linear decay:

```
speed_factor = max(0, 1 − t / 15)
```

where `t` is minutes elapsed since the final CyberEDU channel opened.

| t (min) | speed_factor | score if accuracy = 1.0 |
|---|---|---|
| 0 | 1.00 | 1.00 |
| 5 | 0.67 | 0.83 |
| 10 | 0.33 | 0.67 |
| 14 | 0.07 | 0.53 |
| 15 | 0.00 | 0.50 |

Note: the speed floor still applies via `α = 0.5`, so a last-second correct answer earns `0.5` in the worst case.

### Speed factor — CyberEDU mini 3

The CyberEDU mini stage gives live feedback, so speed matters less here. For simplicity:

```
speed_factor = 1.0
```

i.e., CyberEDU mini scoring is accuracy-only, provided you submit before the CyberEDU mini channel closes on Saturday.

## Accuracy rubric — 5 levels

The judge grades each answer against the key using this anchored rubric:

| Score | Anchor |
|---|---|
| **1.0** | Fully correct and specific. Matches the reference answer in substance. |
| **0.75** | Correct core claim with a minor omission or imprecision. |
| **0.5** | Partially correct. Right direction or right entity, but missing or wrong in a material detail. |
| **0.25** | Touches the topic but misses the actual answer. |
| **0.0** | Wrong, irrelevant, hallucinated, or matches a planted distractor. |

**Exception**: Level 1 (direct lookup) questions are graded on a binary `{0, 1}` — there is no partial credit for the wrong date, wrong name, or wrong number.

## Citation rule

Every answer must include:

- `evidence_quote` — a short verbatim or near-verbatim quote from the PDF that supports the answer.
- `page` — the page number where that quote appears.

The evaluator fuzzy-matches your quote against the PDF text (Levenshtein ratio ≥ 0.85) with page tolerance of ±2.

| Citation status | Effect on `accuracy_q` |
|---|---|
| Quote matches + page within ±2 | No penalty. Full rubric score applies. |
| Quote does not match, OR page off by more than 2 | `accuracy_q` is capped at **0.5**, regardless of rubric grade. |
| Abstention claimed (see below) | Citation not required. |

## Abstention

| Scenario | `accuracy_q` |
|---|---|
| Correct answer, valid citation | per rubric, up to 1.0 |
| Correct answer, citation fails | capped at 0.5 |
| Partial answer, valid citation | 0.25 – 0.75 per rubric |
| Wrong answer (including matching the honeypot) | 0.0 |
| `abstain = true` on a real question | 0.0 |
| `abstain = true` on the trap question | 1.0 |
| Answer text is "not in document" without the `abstain` flag | treated as implicit abstain |
| No submission at all | 0.0 |

## Stage aggregation

Within each stage:

```
stage_score = mean(score_q over all 5 questions)
```

(or `mean over 3` for CyberEDU mini.)

Stages then combine with the weights at the top of this file.

## Write-up — 20% of total

Evaluated by an AI judge against 5 criteria, each worth 20% of the write-up:

| Criterion | What it means |
|---|---|
| **Claim-to-evidence ratio** | Every claim in your write-up must be supported by a concrete artifact (code snippet, screenshot, metric, log excerpt, diagram referencing your real implementation). Unsupported marketing language is penalized. |
| **Technical accuracy** | What you describe must be technically correct. No hallucinated architectures. |
| **Solution design** | Is your system design coherent? Are trade-offs explained and justified? |
| **Innovation** | Did you do something non-obvious? Novel chunking, smart caching, clever retrieval, agent loops, adversarial self-evaluation, etc. |
| **AI slop** | Inverse criterion. Penalizes LLM-generated filler ("we prioritized quality and performance"), vague claims, purple prose, unmotivated structure. |

**Write-up length**: 1–2 pages. Longer is not better. Evidence-dense writing scores highest.

## Jury presentation — 20% of total

Judged live by 3 jurors (Teo, Ana, Lucian), each on 5 equally-weighted criteria:

| Criterion | What it means |
|---|---|
| Innovation | Non-obvious choices that impressed the jury. |
| Efficiency in handling difficult situations + technical strength | Problem-solving, engineering competence. |
| Delivery quality | Clear, paced, well-structured presentation. |
| Strategic use of tools/technologies/AI | Did you use your tools well? Did AI choices pay off? |
| Overall jury impression | The catch-all. |

Each juror scores each criterion; the mean across jurors × criteria is your presentation score.

## Tie-breakers

Used only to order the leaderboard. In order:

1. Final-sprint score (higher wins).
2. Midday accuracy score (higher wins).
3. Earliest correct midday submission timestamp (earlier wins).
4. Jury presentation score.

If still tied, the jury decides.

## Appeals

- **What can be appealed**: the AI judge's accuracy grade on any answer.
- **What cannot be appealed**: CyberEDU upload timestamps (authoritative to the second) or speed factors.
- **How**: submit `(team code, question id, your reasoning)` within **30 minutes** of the leaderboard release containing the disputed score.
- **Process**: we re-run the judge at `temp=0` against the logged submission. If the score changes, it's updated. Otherwise it stands.

## Judge determinism

- The judge runs at `temp=0` on a pinned model version.
- Every judge call is logged to a private JSONL audit trail (submission, prompt hash, judge response, score, timestamp).
- The judge prompt is structured to resist prompt injection in submissions.
- The write-up judge follows the same pattern with a rubric-anchored prompt per criterion.
