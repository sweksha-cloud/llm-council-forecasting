# Forecasting benchmark v1: resolved prediction-market questions with leak-checked prices

1,185 resolved yes/no questions from **Polymarket** and **Kalshi**, each with its outcome, the market price, and the date that price was taken. A forecaster is asked each question "as of" that date and scored against the outcome and the price. Built for [llm-council-forecasting](../README.md) by Sweksha Shaw (San José State University, advised by Prof. William Andreopoulos).

| Split | Questions | Sources | Resolved | Share Yes | Use |
|---|---|---|---|---|---|
| `settled` | 1,039 | 839 Polymarket, 200 Kalshi | Jul 2025 – Oct 2026 | 43.5% | Main evaluation (after the open models' training cutoffs) |
| `contamination` | 146 | Polymarket | Mar 2023 – Jan 2024 | 33.6% | Memorisation check: same scoring on older questions models may have seen |

`subset` keeps the original sets: `settled` (359, closing Jul–Oct 2026) and `settled-ext` (680, Jul 2025 – Jun 2026).

## Columns

| Column | Meaning |
|---|---|
| `question_id` | `polymarket:<market id>` or `kalshi:<ticker>` |
| `split`, `subset` | see above |
| `source`, `topic`, `url` | market, the market's own category, link |
| `question_text`, `resolution_criteria` | as published by the market |
| `as_of` | when the price was taken: 7 days before the earlier of the scheduled close and the resolution. Give the forecaster this date, never today's |
| `market_price` | Yes price at `as_of` (0–1) |
| `scheduled_close`, `resolved_at` | the market's scheduled close and when it actually ended |
| `outcome` | 1 = Yes, 0 = No |

## How it was checked

Every price is taken 7 days before the earlier of close and resolution and comes before resolution. Markets must close and resolve inside their window. Outcomes and prices were re-fetched from both APIs by independent code (0 mismatches). The leaks found and fixed while building it are in [`docs/leakage.md`](../docs/leakage.md); questions without a trade at the 7-day mark were dropped rather than priced at another time.

## Using it

Score probability forecasts with the Brier score against `outcome`, and compare with `market_price` on the same questions (`scoring/` in this repo has Brier, log score, calibration, AUROC and paired bootstrap tests). Rebuild the file with `python3 benchmark/build.py`; `SHA256SUMS` verifies a copy.

Question text and prices come from the public Polymarket and Kalshi APIs; check their terms before commercial use.

## Citation

See [`CITATION.cff`](../CITATION.cff), or: Shaw, S. (2026). *Forecasting benchmark v1: resolved prediction-market questions with leak-checked prices.* https://github.com/sweksha-cloud/llm-council-forecasting
