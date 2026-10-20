# Leakage found and fixed

Retrospective forecasting evaluations leak easily: if a model is asked about a question after it was decided, or scored against a price from after the event, the results look better (or stranger) than they are. These are the leaks this project found in its own data and in earlier results, how each was caught, and what was done. Every fix was made before the affected results were scored. Details and dates are in [`decisions.md`](decisions.md).

| # | Leak | Size | How it was caught | Fix |
|---|---|---|---|---|
| 1 | **Settled questions "asked" after they closed.** The price date given to the model was sometimes after the scheduled close (Polymarket can resolve weeks after it). Example: a ceasefire-by-July-31 question asked as of Aug 5, priced 83% vs 15% a week earlier | 15 settled questions | Audit of collection code | Price and "as of" date taken 7 days before the scheduled close or the resolution, whichever is first; 13 repriced, 2 left unpriced (no trades) |
| 2 | **Prices anchored on resolution, not the earlier of close and resolution.** Up to 7 days of the run-up to close leaked into the price and the date the model was told; 2 questions were asked under a day before close | 127 of 360 settled, 122 of 153 contamination | `forecast/postrun.py`, the post-run check, before any settled result was scored | 241 repriced (median change 0.005–0.007, 15 moved more than 0.10), 8 dropped; stale forecasts removed (`forecast/drop_stale.py`) and re-asked |
| 3 | **Markets outside the backtest window.** Polymarket's API filters by the event's end date, but a market inside an event can resolve months earlier or later; one resolved in Feb 2025, before two of the models were released | 25 questions in the 2025–26 extension | Checking each market's own dates | Markets must close and resolve inside the window themselves; the 25 dropped |
| 4 | **Live forecasts made after the market ended.** The stored close is the scheduled one; Kalshi games and "by date" markets end days early, so some live questions were already decided when asked, and their stored market price was the settled 0/1 | 49 of 342 live questions; all 5 live questions scored at the time | Independent audit against the APIs | Live forecasts made at or after `resolved_at` aren't scored and their price isn't used (`made_after_resolution`); the earlier live numbers were withdrawn |
| 5 | **Scoring bugs in the earlier council results.** Accuracy matched substrings, so any answer containing "no" (including "not" and "cannot", i.e. refusals) counted as a correct No; a judge reply that couldn't be parsed was scored 1 in single-model runs but dropped for councils | All 2,501 imported questions re-scored | Reading the earlier code | Answers graded strictly (Yes/No only if stated, otherwise abstain); removing the fake 1s raised single-model judge means from 3.46–3.71 to 4.30–4.75, close to the councils' 4.40–4.79 |

## Built-in protections

- Backtest questions are asked "as of" their price date, never today's date, which would reveal the outcome.
- The live set is the leak-free test: forecasts are locked with a timestamp before resolution and never changed (`tests/test_data_integrity.py` checks them against `main`).
- A contamination split compares questions resolved before and after each model's knowledge cutoff.
- The sample and every comparison were pre-registered before any settled results existed.

## Known, not fixed

- 71 live questions were collected while the event was underway (they closed within 24 hours of collection), so their stored price is an in-play snapshot. They are kept; the live comparison with the market should be read with this in mind.
