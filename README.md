# llm-council-forecasting

**Does an LLM council forecast better than a simple average of its members?**

CS180 Individual Studies, San Jose State University, Fall 2026: Sweksha Shaw, advised by Prof. Bill Andreopoulos.

In an LLM council, several language models answer the same question and a chairman model combines their answers into one. This project tests whether the council actually beats the models it's built from. The test bed is prediction-market questions from **Polymarket** and **Kalshi**, which resolve to a real outcome and have a market price to compare against.

Every model, and the council, gives a **probability** that the event happens. Forecasts are scored with proper scoring rules (Brier and log score), accuracy, calibration and sharpness (ECE, reliability diagrams, mean distance from 50%), discrimination (AUROC), ground-truth Yes/No call metrics (balanced accuracy, MCC, precision/recall), and a set of baselines that ends with the market price.

## Research question

> **Does a deliberating council of small LLMs forecast better than a simple average of its members' probabilities, and what explains the difference?**

1. **Deliberation vs averaging (main):** each council against the mean and logit pools of exactly its own members, on 1,039 settled questions. Paired Brier differences with source-stratified bootstrap intervals; the power analysis gives the smallest difference we could detect (about 0.013 Brier vs the pool, [`docs/power.md`](docs/power.md)), so "no difference" is a result too.
2. **Why (chair ablation):** the chair is re-run seeing only the members' numbers, only their reasoning, or with each member as chair, so reasoning can be separated from averaging (`forecast/rechair.py`).
3. **How far from the market:** every setup against the market price 7 days before close, and on the live set, which can't leak.

Supporting checks: calibration, memorisation (contamination split by knowledge cutoff), robustness by source, topic, horizon and market certainty, and variance across seeds. Scope: open 8B models without retrieval; larger models and multi-round debate are next semester. The sample and every comparison were fixed before any results ([`docs/decisions.md`](docs/decisions.md), 2026-10-16 and 2026-10-20).

## At a glance

| | |
|---|---|
| Questions | 1,730 from Polymarket and Kalshi: 1,039 settled (pre-registered sample), 146 for the contamination check, 545 live |
| Forecasts | 5 open models (Llama 3.1 8B, Mistral 7B, Qwen 3 8B, Gemma 2 9B, Phi-3 Medium) alone and as councils with 2 chairs; 2,394 live forecasts locked before resolution |
| Earlier work | 2,501 questions from the previous council study re-scored after fixing its scoring bugs |
| Evaluation | Brier and log score, calibration, AUROC, ground-truth call metrics, paired source-stratified bootstrap, power analysis, pre-registration |
| Data quality | 5 kinds of leakage found and fixed before scoring ([`docs/leakage.md`](docs/leakage.md)) |
| Engineering | One-command reproduction (`make reproduce`), tests in CI, results dashboard and leaderboard |

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

See [`docs/record_format.md`](docs/record_format.md) for the shared record format, [`docs/plan.md`](docs/plan.md) for the timeline, and [`docs/reproduce.md`](docs/reproduce.md) for rebuilding the results.

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
