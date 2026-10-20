# Taking over this project

For the next student working on LLM councils and forecasting. Read this first, then [`decisions.md`](decisions.md) (every choice and why) and [`leakage.md`](leakage.md) (the mistakes not to repeat).

## Your first hour

1. `make setup && make test`, then `make reproduce`. If it ends with "every committed result matches", your copy is right. No GPU is needed for this: every forecast is stored in `data/forecasts.csv`. Or open the Colab notebook (`notebooks/reproduce.ipynb`).
2. Open the dashboard (`make dashboard`, then `dashboard/index.html`) and the leaderboard (`make site`), or the live copies linked in the README.
3. Read the research question at the top of the README, and the pre-registration in `decisions.md` (2026-10-16 and 2026-10-20).

## How the pieces fit

```
collect/  →  data/questions.csv  →  forecast/ (on spark)  →  data/forecasts.csv  →  scoring/ + analysis/  →  results/, dashboard/, site/
```

- **Questions** (`collect/`): Polymarket and Kalshi public APIs, no keys. Settled questions are priced 7 days before the earlier of close and resolution.
- **Forecasts** (`forecast/run_forecasts.py`): every model answers alone with the same prompt; then a chair combines the anonymised answers. Rows are only ever appended; live rows are locked.
- **Scoring** (`scoring/report.py`): plain functions, checked against hand-computed values in `tests/`. Everything in `results/` and on the dashboard comes from this code.
- **Analyses** (`analysis/`): robustness, recalibration, variance, the chair ablation, chair weighting.
- **Benchmark** (`benchmark/`): the leak-checked questions as one file, for anyone's forecaster.

## Running models on spark

Follow [`spark.md`](spark.md). The short version:
- You need an SJSU Tailscale login and a spark account from the professor.
- Code goes up with rsync and results come back with scp. Spark has no GitHub credentials.
- Run long jobs in tmux; every run resumes where it stopped.
- `bash scripts/status_spark.sh` shows progress and an ETA.
- When a run finishes, copy `data/forecasts.csv` back and run `make postrun SPARK=…`. It checks the file before merging anything.
- Models on spark are shared with other users: never `ollama rm`, and never run `scripts/run_local.sh` there.

## Pitfalls we hit (so you don't)

- **Never tell a model today's date on a past question.** Ask it "as of" the price date (`as_of_date`).
- **A market's stored close is the scheduled one.** Kalshi games end early; `made_after_resolution` stops those forecasts being scored.
- **Polymarket's API filters by the event's dates, not the market's.** Check each market's own close and resolution.
- **Don't grade free text by substring.** "not" contains "no". Grade only explicit answers and count the rest as abstentions.
- **LLM-judge scores don't track correctness** (AUROC ≈ 0.5 on the earlier data). Use ground-truth metrics.
- **Accuracy rewards saying No** when most questions resolve No. Report balanced accuracy, MCC and the always-No baseline.
- **deepseek-r1 ignores `think=false`** and can reason forever at temperature 0. It runs separately with a thinking budget.
- **Fix the sample and the comparisons before looking at results,** and write them in `decisions.md` with the date.

## Where to go next

Ideas ranked in [`plan.md`](plan.md) and the README's scope line:
- **Multi-round debate:** members revise after seeing each other.
- **A stronger model** (70B) as member and chair.
- **Retrieval with time-stamped news.**
- **Kalshi's `/historical` API** (`collect/kalshi_historical.py` is ready) to add 2025–26 Kalshi questions.

## Working rules

Branch and pull request for every change; CI runs the tests on each PR. Never edit locked forecasts. Log any choice that could change a result in `decisions.md`.
