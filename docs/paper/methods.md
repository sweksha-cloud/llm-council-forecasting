# Methods

*Draft paper section, written from `docs/decisions.md`, `docs/record_format.md`, `docs/reproduce.md` and the code they describe. Counts are as of 2026-10-16; numbers that change once the settled, contamination and live runs finish are marked ⟨TBD⟩.*

## Questions

All questions are binary (Yes/No) prediction-market questions from **Polymarket** and **Kalshi**, stored with the market's own resolution rules, which are given to the models as context. Each question is in one of three sets:

| Set | Questions | Sources | Closes / resolved | Role |
|---|---|---|---|---|
| Live | 545 (342 forecast so far) | 244 Polymarket, 301 Kalshi | 10 Oct – 15 Nov 2026 | Forecast before resolution; the cleanest test |
| Settled | 362 (360 with a price) | 162 Polymarket, 200 Kalshi | scheduled to close Jul – Oct 2026; 8 resolved early (from Nov 2025) | Retrospective test, larger and immediately scorable |
| Contamination | 153 | Polymarket | resolved Mar 2023 – Jan 2024 | Questions resolved before the models' training cutoffs |

**Selection.**
- **Filters:** a question is kept only if it is a true Yes/No market with enough trading (≥ $5,000 on Polymarket, ≥ 500 contracts on Kalshi). Crypto and price-threshold markets are excluded; they are mostly bets on a price crossing a line, not forecastable events.
- **Duplicates and topics:** at most one market per event (to avoid near-duplicates such as one market per candidate), and at most 40% of each source's questions from one topic.
- **Ranking:** within those limits, markets are taken in order of trading volume.
- **Live set:** questions closing before 15 November 2026. 58 of the first 400 closed before forecasting began, so 145 more were added; the 342 forecast so far were locked on 12–13 October 2026.

**Market price.**
- **Live:** the price recorded is the Yes price when the forecast was made. On Kalshi, the bid/ask midpoint if the spread is at most 10¢, otherwise the last trade.
- **Settled and contamination:** the last trade 7 days before the scheduled close, or before the resolution if that came first, taken from each market's price history. Anchoring on the earlier of the two matters: Polymarket can resolve days or weeks after its scheduled close. Anchoring on the resolution alone put 15 questions' price dates after the event had happened; these were repriced, or left unpriced where no trade existed.
- **Outcomes:** 1 if the event happened, 0 if not, read from the market's settlement.

**Leakage controls.**
- **The date the model is told:** for settled and contamination questions it is the price date, not today's date, so the model is never told a date after the question closed. A question without a price date before its close is skipped.
- **Model cutoffs:** every settled question, including the 8 that resolved early, resolved after every model's release (latest: May 2025). The contamination set is the deliberate exception, used to measure recall.
- **Residual risk:** Polymarket's description text may have been edited after a market opened, and we can't check this (see Limitations).

## Models and setups

Five open models, run locally with Ollama on a single GPU server:
- Llama 3.1 8B Instruct
- Mistral 7B Instruct v0.3
- Qwen3 8B
- Gemma 2 9B
- Phi-3 Medium 14B

DeepSeek-R1 8B (distill) is run as a single model only. Even with thinking disabled it reasons beyond 2,000 tokens without answering at temperature 0. It is therefore given a 1,024-token thinking budget, after which its reasoning is closed and it must answer. This works for every test question, at about 110 s each. Exact builds (Ollama digests) are logged with each run.

**Single models.** Each model gets the same system and user prompt. The user prompt gives:
- the date (see above), the question and the closing date;
- the resolution rules (truncated at 1,500 characters);
- a request for 2–4 sentences of reasoning followed by a probability, as JSON.

Asking for the reasoning first was a deliberate change. With the number first, Llama 3.1 answered 0.55 on 12 of 15 test questions.

**Council.**
- **Members:** the five models' independent single-model answers are the council's member answers, so a council and its members are compared on identical inputs.
- **Chair:** a chair model receives the question and all members' probabilities and reasoning, anonymised as Panelist A, B, C… It gives the panel's final probability in the same JSON format. A member whose answer had no usable probability is left out, and a council needs at least two members.
- **Two chairs:** Llama 3.1 and Qwen3, to show whether results depend on who chairs.
- **One round:** this is one round of deliberation; members don't see each other's answers or revise.

**Decoding.**
- **Settings:** temperature 0, seed 42, a 600 s timeout per call, and Ollama's structured-output mode with a JSON schema (reasoning, then probability). Reasoning modes are switched off (`think=false`) except for DeepSeek's budget.
- **Parsing:** a probability is taken from the JSON, or else from an explicit "probability: x" in the text. Values like `70` or `"70%"` are read as 0.70. Anything outside [0, 1], or no probability at all, is recorded as an **abstention**, never as an imputed number.
- **Failures:** failed calls (server errors, timeouts) are retried on a later run.
- **Records:** every raw response is kept. Live forecasts are marked `locked` with a timestamp and never edited.

## Baselines

Built from the same questions:
- **Market:** the market price defined above, used as a forecast.
- **Pools of the single models:**
  - mean;
  - median;
  - logit pool (mean in log-odds);
  - extremised logit pool, with log-odds scaled by *a* = 2.
- **Best single model:** chosen in-sample by Brier among models that answered at least half as many questions as the most-answering model. In-sample selection makes it slightly optimistic.
- **Always No:** 0% on every question. Most questions in some sets resolve No, so this is the accuracy any setup gets by saying No.
- **Base rate:** the share of the set that resolved Yes, on every question. It uses the outcomes, so it's slightly optimistic.

## Scoring

Only resolved questions are scored. For each setup we report:

- **Proper scores:**
  - Brier score, the mean of (p − y)²;
  - log score, −ln of the probability given to what happened, with p clipped to [10⁻⁶, 1 − 10⁻⁶].
- **Accuracy:** the share of forecasts on the right side of 0.5, where exactly 0.5 counts as half right.
- **Calibration and sharpness:**
  - expected calibration error over 10 equal-width bins (count-weighted |mean forecast − observed rate|);
  - reliability diagrams;
  - the Murphy decomposition of Brier into reliability, resolution and uncertainty;
  - sharpness, the mean |p − 0.5|. A model that always says about 50% can have low ECE while saying nothing, so ECE and sharpness are read together.
- **Discrimination:** AUROC (Mann–Whitney, ties count half).
- **Ground-truth calls:** each forecast is read as a Yes call (p > 0.5) or a No call (p < 0.5), and p = 0.5 is no call. We report precision, recall, F1, balanced accuracy and the Matthews correlation coefficient. Plain accuracy rewards always saying No; balanced accuracy and MCC don't.
- **Skill vs market:** 1 − Brier ÷ market Brier, on the questions both the setup and the market answered.

**Abstentions** are reported as coverage, the share of questions answered. Scores use answered questions only. As a sensitivity check, each abstention is counted as 0.5. Because setups answer different questions, head-to-head comparisons use the questions both answered (paired), or the common set every setup answered.

**Uncertainty.** Council-vs-reference comparisons are paired Brier differences on shared questions. References: market, best single model, mean pool, always No. Each comes with a 95% percentile bootstrap interval, 1,000 resamples of questions, fixed seed. Skill vs market uses the same paired bootstrap. Resampling questions treats them as independent; related markets (e.g. several deadlines for one event) make these intervals somewhat too narrow.

**Contamination.**
- **Cutoffs:** each model's cutoff is its stated training cutoff where published (Llama 3.1: Dec 2023; Phi-3: Oct 2023). Otherwise it is its release date, a safe upper bound. A council or pool takes its latest member's cutoff, since any member could know the answer.
- **The split:** questions are split by resolution date at that cutoff. We compare Brier before vs after, with a bootstrap interval, and subtract the market's own before−after gap on the same questions. This allows for the older questions being easier. Clearly lower error on pre-cutoff questions, beyond the market's, points to recall rather than forecasting.

**Member disagreement.** For each council we compute the Spearman correlation between the members' spread (standard deviation of their probabilities) and the council's Brier error. We also report Brier by low, middle and high thirds of spread.

**Power.** At n ≈ 360, the settled set detects a paired Brier difference of about 0.036 vs the market and about 0.030 vs a member, at 80% power with α = 0.05, for forecasters around Brier 0.21 (`docs/power.md`).

## Earlier results

We also re-score an earlier council study on the same platform (Polymarket, 2026). Its models answered in free text, without probabilities, and were scored by an LLM judge.
- **Grading:** an answer counts as Yes (1) or No (0) only if stated explicitly. Anything else abstains, and the original substring matching is not used.
- **Market price:** each question's Polymarket price on its collection date.
- **Scoring:** the same metrics as above. These rows are tagged with their origin and never pooled with probability forecasts.

## Reproducibility

- **Code and data:** questions, forecasts (with full raw responses), imported results and every results table are committed.
- **Rebuilding:** `make reproduce` runs the tests, re-imports the earlier results from a pinned commit, rebuilds every results table and the dashboard. It fails if any committed number changes.
- **Tests:** the scoring code is checked against hand-computed values. The dashboard, which recomputes every metric in the browser so filters work, is tested against the Python scores on the real data.
- **Re-running the models** requires Ollama and a GPU. Exact commands and model digests are in `logs/cmds_spark.log`.
- **Determinism:** even at temperature 0, hardware and Ollama versions can change a few tokens, so the committed forecasts, not a re-run, are the record.
- **Decisions log:** every choice that could change a result is logged with its date and reason in `docs/decisions.md`.

## Limitations

- **Small models only:** 7–14B models run locally, with no retrieval. Results don't speak to frontier models or tool-using forecasters.
- **One deliberation design:** one round, one chair, anonymised members. Debate or multiple rounds might behave differently.
- **Possible description edits:** retrospective (settled) questions rely on market descriptions as they are now. Polymarket keeps no edit history, so a description edited after a market opened can't be detected. We spot-checked dated text in all 69 settled descriptions that contain it, and found context from market creation rather than outcomes.
- **Question mix follows market supply:** sports and politics dominate. Per-topic results are reported where the counts allow.
- **Live set size:** the live set is limited to questions closing by mid-November ⟨TBD: resolved count at write-up⟩.
