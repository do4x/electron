# 05 — Submission

## Submission platform

All submissions go through **CyberEDU**, the hackathon platform. Four separate channels, one per stage:

| Stage | When it's open | CyberEDU channel |
|---|---|---|
| Calibration (unscored practice) | From challenge open to end of Saturday | `TBA` |
| Midday (5 questions, scored) | From challenge open until Sunday `01:00` | `TBA` |
| CyberEDU mini (3 questions, scored) | From challenge open until Sunday `01:00` | `TBA` |
| Final sprint (5 questions, scored) | Sunday `10:00` for exactly 15 minutes | `TBA` |

Your team is identified by your CyberEDU account (pre-registered with your team code). You do not include a team code in the submission itself.

## One submission = one JSON file

Each submission is **one answer to one question** from **one team**, uploaded as a JSON file to the stage's CyberEDU channel. To answer all 5 midday questions, you upload 5 JSON files.

## Submission schema

```json
{
  "question_id": "q3",
  "answer": "214.7 million solar credits",
  "evidence_quote": "Aurelius Shipping reported total revenue of 214.7 million solar credits for FY2183, a 12.4% increase over FY2182.",
  "page": 1847,
  "abstain": false,
  "confidence": "high"
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `question_id` | string (`q1`..`q5` for the active stage, `q1`..`q3` for CyberEDU mini) | yes | Must match the stage's question ID. |
| `answer` | string | yes (unless `abstain`) | Short answer text. |
| `evidence_quote` | string | yes (unless `abstain`) | Short verbatim or near-verbatim quote from the PDF. |
| `page` | integer | yes (unless `abstain`) | Page number where the quote appears. |
| `abstain` | boolean | default `false` | Set to `true` if the answer is not in the document. |
| `confidence` | string (`low` / `medium` / `high`) | optional | Self-reported confidence. |

The submission timestamp is recorded automatically by CyberEDU when you upload the file.

## First submission wins

**Only the first submission per `(team, question)` is scored.** Re-uploads are ignored by the evaluator. Gaming this (coordinated re-uploads, submitting under another team's account, etc.) is grounds for disqualification.

## Working example

Assume the question is:

> `q3` — What was the total revenue reported by Aurelius Shipping in fiscal year 2183?

A good submission looks like:

```json
{
  "question_id": "q3",
  "answer": "214.7 million solar credits",
  "evidence_quote": "Aurelius Shipping reported total revenue of 214.7 million solar credits for FY2183, a 12.4% increase over FY2182.",
  "page": 1847,
  "abstain": false,
  "confidence": "high"
}
```

The evaluator will:

1. Fuzzy-match your quote against the PDF text → finds it on page 1847. ✓ citation valid.
2. Run the AI judge at `temp=0` with the rubric + correct answer + your answer → `1.0`.
3. Compute `speed_factor` from your upload timestamp.
4. Compute `score_q = 1.0 × (0.5 + 0.5 × speed_factor)`.

## Abstention example

For a trap question like `q5 — What was the company's Q4 2184 guidance?` where Q4 2184 guidance is NOT in the document:

```json
{
  "question_id": "q5",
  "answer": "",
  "evidence_quote": "",
  "page": 0,
  "abstain": true,
  "confidence": "high"
}
```

If the question is indeed a trap, you get `accuracy = 1.0`. If it was a real question you missed, you get `0.0`.

## Common mistakes to avoid

- **Wrong question ID.** Scored against the wrong answer key. Double-check.
- **Invalid JSON.** If the file does not parse, the submission is rejected. Validate before uploading.
- **Quote is a paraphrase.** Fuzzy matching needs real text from the PDF. Paraphrases fail, your accuracy is capped at 0.5.
- **Page number is guessed.** The evaluator tolerates ±2, but ±50 fails.
- **Re-uploading because you changed your mind.** The first submission is the one that counts. Make it your best.
- **Leaving the evidence blank** on a real answer. Capped at 0.5.

## What the evaluator does not see

- Any code you wrote.
- Any context or reasoning beyond what you put in the JSON file.
- Any links you embed. The evaluator grades the answer text + the evidence quote. That's it.
