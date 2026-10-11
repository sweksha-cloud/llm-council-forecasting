# Shared record format

Every result in this project uses the same format: **one row per (question × setup)**, where a setup is one model alone, one council configuration, a baseline, or the market. Collection, forecasting, scoring and (later) the dashboard all read and write only this format. New runs and imported older results can then be compared directly.

This is a first draft. Fields will be finalised when the first collector and forecast run are written.

## Questions table (`data/questions.csv`)

| Field | Type | Meaning |
|---|---|---|
| `question_id` | str | Stable ID, e.g. `polymarket:<market_id>` or `kalshi:<ticker>` |
| `source` | str | `polymarket` or `kalshi` |
| `question_text` | str | The question exactly as asked |
| `resolution_criteria` | str | The market's own rules for how it resolves (given to models as context) |
| `answer_type` | str | `binary` or `multi` |
| `choices` | str | JSON list of answer options (for binary: `["Yes","No"]`) |
| `set` | str | `live`, `settled`, or `contamination` (older questions for the Week 8 check) |
| `topic` | str | Category label, if available |
| `url` | str | Market page |
| `collected_at` | datetime (UTC) | When the question was collected |
| `resolution_date` | datetime (UTC) | When the market closes (Polymarket `endDate`, Kalshi `close_time`) |
| `market_price` | float | Market probability of "Yes" at `price_time` (Polymarket Yes price; Kalshi bid/ask midpoint, or last trade) |
| `price_time` | datetime (UTC) | When `market_price` was taken: collection time for live questions, N days before close (default 7) for settled ones |
| `volume` | float | Traded volume at collection (Polymarket: USD; Kalshi: contracts) |
| `outcome` | int / null | 1 if the event happened, 0 if not; empty until resolved |
| `resolved_at` | datetime / null | When the outcome was recorded |

## Forecasts table (`data/forecasts.csv`)

| Field | Type | Meaning |
|---|---|---|
| `question_id` | str | Links to the questions table |
| `setup` | str | e.g. `single:qwen3:8b`, `council:chair=llama3.1`, `baseline:mean`, `market` |
| `model` | str | Model tag, or `council` / `baseline` / `market` |
| `members` | str | For a council or baseline, a JSON list of member models |
| `probability` | float / null | Forecast probability that the event happens (0 to 1); empty if it abstained |
| `abstained` | bool | True if the model refused or gave no usable probability |
| `raw_response` | str | Full model output, kept for auditing |
| `prompt_id` | str | Which prompt version was used (identical across setups) |
| `forecast_at` | datetime (UTC) | When the forecast was made |
| `market_price_at_forecast` | float / null | Market probability at `forecast_at` |
| `locked` | bool | True for live-set forecasts once locked. These rows are never edited. |
| `origin` | str | `this-project`, or the source of imported results (e.g. `aye-2026@<commit>`) |

## Notes

- `outcome` and `probability` are always "probability the event happens / did happen", so Brier and log scores can be computed with no extra logic.
- Older results (Aye's) have no probabilities. When imported, a clear Yes becomes 1.0, a clear No 0.0, and anything else `abstained = true`. These rows are tagged by `origin` and are never mixed silently with real probability forecasts.
