# Week 9: previous council results, re-scored

Aye's "new" dataset (1,611 Yes/No Polymarket questions with outcomes, collected 2026-07-15), mapped into the shared record format and re-scored with strict Yes/No grading. Full tables: `report.md`. Import: `python3 -m importers.import_aye`.

## Main finding

Her councils beat every single model, but **not a model that always answers "No."** 67% of these questions resolved No, and the councils mostly answered No.

| Setup | Answered Yes/No | Accuracy when answering | "Always No" on the same questions |
|---|---|---|---|
| Council, Llama chair | 936 (58%) | 65.7% | 65.1% |
| Council, Mistral chair | 512 (32%) | 64.3% | 63.7% |
| Council, Qwen chair | 191 (12%) | 71.7% | 75.4% |
| Best single model (Phi-3) | 887 (55%) | 35.4% | 69.2% |
| Other single models | 41–138 (3–9%) | 31–42% | 62–89% |

The single models said "Yes" far more often than the outcomes justify (Gemma 2 answered Yes every time it committed). The council's apparent advantage is mostly a shift toward "No", not better forecasting.

## Which metrics transfer

| Metric | Transfers? | Why |
|---|---|---|
| Brier score | Partly | Answers are 0 or 1, so Brier = 1 − accuracy; it says nothing about confidence |
| Log score | No | A wrong 0/1 answer is infinitely bad; the clipped value only counts mistakes |
| Reliability diagram / Murphy decomposition | No | Only two forecast values (0 and 1), so there's no calibration curve; resolution is near 0 for everything |
| Aggregation baselines (mean, median, logit, extremized) | Weakly | Only 240 questions where 2+ members committed; averaging 0/1 votes is a vote count |
| Coverage / abstention | Yes, and it matters | Coverage ranges from 3% to 58%; how abstentions are scored changes the ranking |
| Council vs market | No | No market price was stored at answer time |
| Member disagreement | Weakly | Disagreement can only be measured on the few questions where several members committed |
| Contamination check | Yes | Resolution dates are known |
| Her LLM-judge scores | Not a forecast metric | The judge rated reasoning quality (4–5 for nearly everything), not correctness |

## Data notes

- 908 council rows were connection errors and are dropped.
- The council file isn't in her repo; it was copied from spark (`/data/swekshashaw/new_council_detailed.xlsx`, 2026-07-29) to `data/imported/aye-2026/source/` and is pinned by sha256 in the importer.
- Her "old" dataset (839 questions) has no per-question council file, so only single models are re-scored there.
- Earlier council runs by Aishwarya and aswitha aren't imported yet.
