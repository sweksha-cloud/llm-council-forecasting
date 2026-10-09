# Plan

Expectations come from the course timeline below.

## Timeline

| Week | Action | Deliverable |
|---|---|---|
| 1 | Read on LLM forecasting and ensembles. Review previous students' code and results. Get Polymarket and Kalshi API access and a server account. | 1-page summary of the research question and what is already known |
| 2 | Build the question set from both markets: settled questions, and live questions resolving before mid-November. Record market price and resolution date. | Dataset of ≥150 questions, split settled/live, with market prices |
| 3 | Read on proper scoring rules and forecast evaluation. Fix the metric suite and name the baselines. | 1-page summary of metrics and baselines |
| 4 | Run the council and every single model on the live set with identical prompts. Lock forecasts with timestamps. | Locked forecast file with timestamps, and the prompts used |
| 5 | Run the council and single models on the settled set. Score with Brier and log score. | First results table: council vs each model |
| 6 | Aggregation baselines (mean, median, logit pool, extremized pool, best single model) on the settled set. | Comparison table across aggregation methods |
| 7 | Reliability diagrams and Murphy decomposition for the council and each model. | Calibration plots and decomposition table |
| 8 | Contamination check: split the settled set by resolution date vs each model's knowledge cutoff. | 1-page contamination summary |
| 9 | Map previous students' council results into the same format and re-score them; note which metrics don't transfer. | Merged dataset and combined results table |
| 10 | Does member disagreement predict council errors? Council vs market price at forecast time. | Results table and plots |
| 11 | Score the live set as questions resolve, vs single models and vs market price at lock time. | Live-set results table |
| 12 | Dashboard: leaderboard (Brier, log), per-question view, calibration curves, council vs market. | Working dashboard |
| 13 | Dashboard filters (market, topic, resolution date) and export. Test cases for the scoring code. | Dashboard with filters/export; test case summary |
| 14 | Publish code and data; deploy dashboard; code review. | gSheet, GitHub, gDrive, Colab; deployed dashboard; recorded presentation |
| 15 | Write-up, with the goal of an arXiv submission next semester. | Report on GitHub |

## Known issues in the earlier results

Aye's repo has scoring bugs that affect the reported numbers. They were noted in the team doc (07/24) and confirmed in the code (10/09):

1. Accuracy uses substring matching: any answer containing "no" (e.g. "not", "cannot") counts as a correct "No".
2. As a result, refusals are often counted as correct.
3. In single-model runs, a judge response that can't be parsed is scored 1, while the council script drops it. Removing these fake 1s raises single-model judge means from 3.46–3.71 to 4.30–4.75, close to the councils' 4.40–4.79.

Imported results must be re-scored, not reused as reported.
