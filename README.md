# llm-council-forecasting

**Does an LLM council forecast better than a simple average of its members?**

CS180 Individual Studies, San Jose State University, Fall 2026: Sweksha Shaw, advised by Prof. Bill Andreopoulos.

In an LLM council, several language models answer the same question and a chairman model combines their answers into one. This project tests whether the council actually beats the models it's built from. The test bed is prediction-market questions from **Polymarket** and **Kalshi**, which resolve to a real outcome and have a market price to compare against.

Every model, and the council, gives a **probability** that the event happens. Forecasts are scored with proper scoring rules (Brier and log score), accuracy, calibration and sharpness (ECE, reliability diagrams, mean distance from 50%), discrimination (AUROC), ground-truth Yes/No call metrics (balanced accuracy, MCC, precision/recall), and a set of baselines that ends with the market price.

## Research question

> **Does a deliberating council of small LLMs forecast better than a simple average of its members' probabilities, and what explains the difference?**

**Answer so far (pre-registered sample, 1,039 settled questions):** no. Neither council beats a simple average of its own members' probabilities. With the Llama chair the difference is +0.003 Brier (95% CI −0.001 to +0.007); with the Qwen chair the council is *worse* than the average (+0.012, CI +0.007 to +0.016). Both trail the market by 0.08–0.09 Brier (market 0.169, councils 0.253–0.262). The Qwen chair also gives its own model's forecasts about 0.20 more weight than the other chair does (CI 0.15–0.24). Kalshi and Polymarket agree, and no model shows signs of having memorised the older questions. Tables: [`results/settled-all/report.md`](results/settled-all/report.md). One round of debate, in which every member revises after seeing the others, doesn't help either: the average of the revised forecasts is slightly worse than before debate (+0.005 Brier, CI 0.002 to 0.008, 359 questions), even though the members' disagreement shrinks by 18% ([`results/debate/`](results/debate/debate.md)). Across all five models tried as chair, none beats the average and four are significantly worse (+0.004 to +0.012 Brier). A chair shown only the members' numbers matches the full council, while one shown only their arguments is significantly worse, so the chair adds nothing beyond averaging and following arguments hurts. Four of five chairs over-weight their own model's forecasts (+0.03 to +0.17 weight). Across three resampled runs at temperature 0.7, the market gap and the Qwen chair's deficit hold in every seed, and the Llama chair's difference from the average stays near zero ([`results/ablation/`](results/ablation/ablation.md), [`results/variance/`](results/variance/variance.md)).

1. **Deliberation vs averaging (main):** each council against the mean and logit pools of exactly its own members, on 1,039 settled questions. Paired Brier differences with source-stratified bootstrap intervals; the power analysis gives the smallest difference we could detect (about 0.013 Brier vs the pool, [`docs/power.md`](docs/power.md)), so "no difference" is a result too.
2. **Why (chair ablation):** the chair is re-run seeing only the members' numbers, only their reasoning, or with each member as chair, so reasoning can be separated from averaging (`forecast/rechair.py`), and each chair's effective weight on every member is fitted, including whether it favours its own model (`analysis/chair_weights.py`). A second form of deliberation, one round of debate in which every member revises after seeing the others, is tested the same way (`forecast/debate.py`).
3. **How far from the market:** every setup against the market price 7 days before close, and on the live set, which can't leak.

Supporting checks: calibration, memorisation (contamination split by knowledge cutoff), robustness by source, topic, horizon and market certainty, and variance across seeds. Scope: open 8B models without retrieval; larger models and multi-round debate are next semester. The sample and every comparison were fixed before any results ([`docs/decisions.md`](docs/decisions.md), 2026-10-16 and 2026-10-20).

## At a glance

| | |
|---|---|
| Questions | 1,730 from Polymarket and Kalshi: 1,039 settled (pre-registered sample), 146 for the contamination check, 545 live |
| Forecasts | 5 open models (Llama 3.1 8B, Mistral 7B, Qwen 3 8B, Gemma 2 9B, Phi-3 Medium) alone and as councils with 2 chairs; 2,394 live forecasts locked before resolution |
| Earlier work | 2,501 questions from the previous council study re-scored after fixing its scoring bugs |
| Evaluation | Brier and log score, calibration, AUROC, ground-truth call metrics, paired source-stratified bootstrap, power analysis, pre-registration |
| Result | No council beats a simple average of its members (4 of 5 chairs are worse); chairs act as averagers and favour their own model; every model trails the market by ≈ 0.08 Brier |
| Data quality | 5 kinds of leakage found and fixed before scoring ([`docs/leakage.md`](docs/leakage.md)) |
| Benchmark | 1,185 leak-checked resolved questions released for reuse ([`benchmark/`](benchmark/README.md)) |
| Engineering | One-command reproduction (`make reproduce`), tests in CI, results dashboard and leaderboard |

**Live results:** https://sweksha-cloud.github.io/llm-council-forecasting/ · **Reproduce in your browser:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sweksha-cloud/llm-council-forecasting/blob/main/notebooks/reproduce.ipynb)

**Results dashboard:** `make dashboard` builds `dashboard/index.html` from the committed data. **Reproducing everything:** `make setup && make reproduce`; see [`docs/reproduce.md`](docs/reproduce.md).

## Building on earlier work

This project continues the LLM-as-Council work by **Aye Nyein Kyaw** (Spring/Summer 2026):
https://github.com/JennicaANK/llm-council-judge

Her results are imported read-only from a pinned commit of that repo (see `importers/`); her repo isn't modified. Earlier council runs by Aishwarya and aswitha are documented in the team's shared Google Doc.

## Layout

| Folder | Purpose |
|---|---|
| `collect/` | Collect questions, market prices and resolution dates from Polymarket and Kalshi |
| `forecast/` | Run each model alone and as a council, with identical prompts, asking for a probability |
| `scoring/` | Brier, log score, accuracy, ECE, AUROC, balanced accuracy, MCC, decomposition, aggregation baselines: plain functions |
| `dashboard/` | Builds the results dashboard (one self-contained HTML page) from the data files |
| `tests/` | Scoring checked against hand-computed values |
| `importers/` | Convert earlier students' results into the shared record format |
| `data/` | Results in the shared record format. Locked forecasts are never edited. |
| `docs/` | Plan, record format, and notes |

**New to the project?** Start with [`docs/handoff.md`](docs/handoff.md). See [`docs/record_format.md`](docs/record_format.md) for the shared record format, [`docs/plan.md`](docs/plan.md) for the timeline, and [`docs/reproduce.md`](docs/reproduce.md) for rebuilding the results.

## Working rules

- Never commit to `main`. Every change goes through a branch and a pull request.
- Live-set forecasts are locked with a timestamp and never changed afterward.
- Every run's commands are saved (e.g. `history > cmds.log`) so it can be reproduced.

## Running each step

All commands run from the repo root.

| Step | Command | Where |
|---|---|---|
| Collect live questions (open, resolving soon) | `python3 collect/collect_live.py` | anywhere |
| Collect settled questions (resolved, price 7 days before close) | `python3 -m collect.collect_settled` | anywhere |
| Collect the older subset for the contamination check | `python3 -m collect.collect_settled --from 2023-01-01 --to 2023-12-31 --skip-kalshi --set-name contamination` | anywhere |
| Forecast: single models + council | `python3 -m forecast.run_forecasts --set live --lock --models ... --chairmen ...` | GPU server ([docs/spark.md](docs/spark.md)) |
| Forecast on a laptop (one model at a time, low disk) | `caffeinate -i bash scripts/run_local.sh` | Mac with Ollama |
| Chair ablations: re-run only the chair (numbers only, reasoning only, each member as chair) | `python3 -m forecast.rechair --set settled settled-ext --no-think ...` (queue: `scripts/queue_ablation.sh`) | GPU server |
| Fill in outcomes as markets resolve | `python3 -m collect.update_outcomes` | anywhere |
| Results tables | `python3 -m scoring.report --set live --out results/live` | anywhere |
| Import and re-score Aye's results | `python3 -m importers.import_aye` | anywhere |
| Dashboard | `make dashboard` (or `python3 -m dashboard.build`) | anywhere |
| Rebuild every result and check it matches | `make reproduce` | anywhere |
| Tests | `python3 -m pytest` | anywhere |

## Setup

```bash
make setup        # or: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Models run through [Ollama](https://ollama.com) on the SJSU GPU server (spark-833c-1), or locally with `scripts/run_local.sh`.
