# llm-council-forecasting

**Does an LLM council forecast better than its members?**

CS180 Individual Studies, San Jose State University, Fall 2026: Sweksha Shaw, advised by Prof. Bill Andreopoulos.

In an LLM council, several language models answer the same question and a chairman model combines their answers into one. This project tests whether the council actually beats the models it's built from. The test bed is prediction-market questions from **Polymarket** and **Kalshi**, which resolve to a real outcome and have a market price to compare against.

Every model, and the council, gives a **probability** that the event happens. Forecasts are scored with proper scoring rules (Brier and log score), calibration analysis, and a set of baselines that ends with the market price.

## Building on earlier work

This project continues the LLM-as-Council work by **Aye Nyein Kyaw** (Spring/Summer 2026):
https://github.com/JennicaANK/llm-council-judge

Her results are imported read-only from a pinned commit of that repo (see `importers/`); her repo isn't modified. Earlier council runs by Aishwarya and aswitha are documented in the team's shared Google Doc.

## Layout

| Folder | Purpose |
|---|---|
| `collect/` | Collect questions, market prices and resolution dates from Polymarket and Kalshi |
| `forecast/` | Run each model alone and as a council, with identical prompts, asking for a probability |
| `scoring/` | Brier score, log score, decomposition, aggregation baselines: plain functions |
| `tests/` | Scoring checked against hand-computed values |
| `importers/` | Convert earlier students' results into the shared record format |
| `data/` | Results in the shared record format. Locked forecasts are never edited. |
| `docs/` | Plan, record format, and notes |

See [`docs/record_format.md`](docs/record_format.md) for the shared record format and [`docs/plan.md`](docs/plan.md) for the timeline.

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
| Fill in outcomes as markets resolve | `python3 -m collect.update_outcomes` | anywhere |
| Results tables | `python3 -m scoring.report --set live --out results/live` | anywhere |
| Import and re-score Aye's results | `python3 -m importers.import_aye` | anywhere |
| Tests | `python3 -m pytest` | anywhere |

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Models run through [Ollama](https://ollama.com) on the SJSU GPU server (spark-833c-1), or locally with `scripts/run_local.sh`.
