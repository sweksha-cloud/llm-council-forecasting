# Reproducing the results

Anyone with this repo should be able to get every number in `results/` and on the dashboard without asking us. There are two levels:

| Level | What it redoes | Needs | Time |
|---|---|---|---|
| **1. Re-score** | Every table and the dashboard, from the committed questions and forecasts | Python 3.12, internet once | about a minute |
| **2. Re-forecast** | The model answers themselves | Ollama on a GPU server | hours per set |

Level 1 should match exactly. Level 2 regenerates the forecasts, which can differ slightly between machines (see the end of this page), so the committed forecast files are the record and level 1 always starts from them.

## Level 1: re-score from the committed data

```bash
git clone https://github.com/sweksha-cloud/llm-council-forecasting.git
cd llm-council-forecasting
make setup        # .venv with the pinned packages in requirements.txt
make reproduce    # tests, re-import, every results table, the dashboard
```

`make reproduce` ends with `git diff --exit-code` over `data/imported/` and `results/`. If it prints **"Reproduced: every committed result matches."**, every committed number was rebuilt from scratch and came out identical. If anything differs, it shows the diff and exits with an error.

Without `make`, the same steps are:

```bash
python3 -m pytest -q                       # scoring checked against hand-computed values
python3 -m importers.import_aye            # Aye's results, from her pinned commit
python3 -m scoring.report --questions data/imported/aye-2026/questions.csv \
    --forecasts data/imported/aye-2026/forecasts.csv --id-prefix aye-new: --out results/aye-2026-new
python3 -m scoring.report --questions data/imported/aye-2026/questions.csv \
    --forecasts data/imported/aye-2026/forecasts.csv --id-prefix aye-old: --out results/aye-2026-old
python3 -m dashboard.build                 # dashboard/index.html; open it in a browser
```

Live-set tables, once enough questions have resolved: `python3 -m scoring.report --set live --out results/live`.

### Where each input comes from

| File | What it is | How it's fixed in place |
|---|---|---|
| `data/questions.csv` | Our questions, market prices at collection, outcomes | Committed. Outcomes are added by `collect.update_outcomes` and committed. |
| `data/forecasts.csv` | Our model and council forecasts, with full raw responses | Committed. Live rows are `locked` and never edited. |
| `data/imported/aye-2026/` | Aye's results in our format, re-graded | Rebuilt by `import_aye` from her repo at commit `b77bdd9` (pinned in the code) |
| `data/imported/aye-2026/market_prices.csv` | Polymarket Yes price for each of her questions at 00:00 UTC on her collection date (her files have none) | Fetched once by `python3 -m importers.aye_market_prices` (`make aye-prices`, needs internet, about 10 minutes) and committed; `import_aye` merges it offline |
| `data/imported/aye-2026/source/new_council_detailed.xlsx` | Her council answers, which aren't in her repo | Copied from spark; the importer checks its sha256 |

### What each script computes

| Output | Code | Metrics |
|---|---|---|
| `results/*/scores.csv` | `scoring/report.py` | Brier, log score, accuracy, ECE, sharpness, AUROC, balanced accuracy, MCC, coverage, Brier skill vs market (common set, and paired per setup with a 95% bootstrap, seed 0) |
| `results/*/ground_truth.csv` | `scoring/classification.py` | Forecasts as Yes/No calls vs outcomes: confusion matrix, precision, recall, F1, balanced accuracy, MCC |
| `results/*/judge_vs_truth.csv` | `scoring/report.py` | Imported results: mean LLM-judge score for right vs wrong answers, judge AUROC for being right |
| `results/*/comparisons.csv` | `scoring/report.py` | Council minus market / best single / mean / always No, paired, 95% bootstrap (seed 0) |
| `results/*/decomposition.csv`, `reliability.csv` | `scoring/calibration.py` | Murphy decomposition, reliability bins (10 equal bins) |
| `results/*/disagreement.csv` | `scoring/report.py` | Spearman of member spread vs council error |
| `dashboard/index.html` | `dashboard/build.py`, `dashboard/metrics.js` | The same metrics, recomputed in the page so filters work. `tests/test_dashboard.py` checks they match `scoring/report.py`. |

Metric definitions are in the docstrings of `scoring/` and on the dashboard under "How it's scored". Choices that affect the numbers (grading rules, abstentions, baselines) are logged with their reasons in [`decisions.md`](decisions.md).

## Level 2: re-run the models

Forecasts come from Ollama on the SJSU GPU server. Setup, long runs and copying results back are in [`spark.md`](spark.md); a laptop alternative is `scripts/run_local.sh`.

The exact command for each run and the model builds (Ollama digests) are appended to [`../logs/cmds_spark.log`](../logs/cmds_spark.log). The live set was produced by:

```bash
python3 -u -m forecast.run_forecasts --set live --lock --no-think \
    --models llama3.1:8b mistral:latest qwen3:8b gemma2:9b deepseek-r1:8b phi3:medium \
    --chairmen llama3.1:8b qwen3:8b
```

Fixed for every run: the prompts in `forecast/prompts.py` (the version is stored in each row's `prompt_id`), temperature 0, a fixed seed, and the same prompt for single models and council members.

What can still differ on a re-run, and why the committed forecasts are the record:

- **Model builds.** An Ollama tag can point to a new build later. Pull by the digest in `cmds_spark.log` to get the same weights.
- **Hardware and Ollama version.** Even at temperature 0, GPU arithmetic and Ollama versions can change a few tokens, and sometimes a probability.
- **Time.** Live forecasts depend on when they were made. They're locked with a timestamp, and the market price at that moment is stored next to them.
- **Market data.** Prices and resolutions are read from Polymarket and Kalshi at collection time and stored; re-collecting later gives different prices.
