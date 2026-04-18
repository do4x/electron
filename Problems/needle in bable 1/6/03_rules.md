# 03 — Rules

## Team identity

- Teams are **pre-registered** with codes from CyberEDU.

## Tools and models — what's allowed

- **Any model**, any provider (OpenAI, Anthropic, Google, Meta, local, self-hosted, etc.).
- **Any tool**: LangChain, LlamaIndex, raw SDK, your own stack, whatever.
- **Paid APIs are fine.** There is no cost cap.
- Bring your own API keys. We do not provide any.
- Internet access is allowed.

## What counts as "building your own system"

- Wrapping ChatGPT's built-in file-upload RAG and calling it yours is technically allowed for answer correctness, but the **write-up** and **jury** will see through that. Criteria like "claim-to-evidence ratio", "solution design", and "innovation" will score very low.
- Your presentation has to show what **you** built. "We uploaded the PDF to ChatGPT" is not a system.
- Using Claude Code / Codex / Cursor to write your code is encouraged. The strategic use of AI tools is itself a scoring criterion.

## Submission rules

- Submissions are uploaded as **JSON files to 4 separate CyberEDU channels** (calibration / midday / CyberEDU mini / final). See [`05_submission.md`](05_submission.md).
- **Only the first submission per `(team, question)` counts.** Re-uploads are ignored.
- **Do not attempt to game the resubmission mechanism.** Attempts to bypass or abuse CyberEDU submission (e.g., submitting under another team's account, DDOS-ing the platform, etc.) = disqualification.
- Every answer must include **answer text + evidence quote + page number**, or the `abstain` flag set if you believe the answer is not in the document.
- A correct answer without valid citation is **capped at 0.5** accuracy. Always cite.

## Abstention

- Every set of 5 questions contains **at least one trap**: a question whose answer is **not in the PDF**.
- If you believe a question cannot be answered from the document, set `"abstain": true` in your JSON submission or write "not in document" in the `answer` field.
- Correct abstention on a trap: full credit.
- Abstention on a real question: zero.
- Wrong answer on a trap (including matching the planted distractor): zero.

## Honeypot disclosure

- **Each PDF contains at least one honeypot**: an authoritative-sounding paragraph that makes a confident but incorrect claim.
- Honeypots are placed to catch systems that retrieve-and-summarize without reasoning.
- Trust retrieval + reasoning + cross-checking. Do not trust the first high-confidence hit.

## Anti-cheat

- **No inter-team collaboration.** Your team works alone.
- **No sharing of answers** across teams, on any channel, at any time during the hackathon.
- **No leaking of the dev PDF** outside your team.
- **The final PDF is released only at the final-sprint hour.** Attempting to obtain it early = disqualification.
- We reserve the right to review your write-up, code (if linked voluntarily), and presentation for signs of cheating.

## Forbidden

- Submitting as another team.
- Sharing answers with other teams.
- Trying to access the answer keys, organizer-only files, or the final PDF before its release time.
- Abusing the CyberEDU resubmission mechanism.
- Inserting prompt-injection payloads into your submission text to manipulate the judge. (Our judge is injection-resistant, and any attempt will be logged and counted as a DQ-eligible offense.)

## Questions?

- **Technical / logistical**: ask the organizing team.
- **Rule interpretation**: check [`08_faq.md`](08_faq.md), which grows during the hackathon. Raise new questions to the organizers; answered questions are added back to FAQ for everyone.
- **Strategic**: use your own advisor LLM (see [`07_advisor.md`](07_advisor.md)). We do not answer strategy questions during the challenge.
