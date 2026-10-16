# Results: aye-2026-old

Resolved questions scored: **890** (set: all). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| single:llama3.1:latest | 890 | 2 | 0.002 | 0.5 | 6.9078 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.0 | 0.2506 | 1 | 0.0 | 0.0 | 1.0 |  |  |  |  |  |
| single:mistral:latest | 890 | 7 | 0.008 | 0.4286 | 5.9209 | 0.5714 | 0.4286 | 0.5 | 0.75 | 0.75 | 0.3536 | 0.2514 | 1 | 0.0 | 0.0 | 1.0 |  |  |  |  |  |
| single:qwen3:8b | 890 | 9 | 0.01 | 0.8889 | 12.2805 | 0.1111 | 0.8889 | 0.5 | 0.5 | 0.5 | 0.0 | 0.2565 | 1 | 0.0 | 0.0 | 1.0 |  |  |  |  |  |
| baseline:always_no | 890 | 890 | 1.0 | 0.3798 | 5.2468 | 0.6202 | 0.3798 | 0.5 | 0.5 | 0.5 | 0.0 | 0.3798 | 1 | 1.0 | 13.8155 | 0.0 |  | 832 | -1.056 | -1.2132 | -0.8866 |
| baseline:base_rate | 890 | 890 | 1.0 | 0.2355 | 0.664 | 0.6202 | 0.0 | 0.1202 | 0.5 | 0.5 | 0.0 | 0.2355 | 1 | 0.3847 | 0.9682 | 0.0 |  | 832 | -0.2397 | -0.3 | -0.1805 |
| baseline:extremized(a=2) | 890 | 4 | 0.004 | 0.75 | 10.3616 | 0.25 | 0.75 | 0.5 | 0.5 | 0.5 | 0.0 | 0.2522 | 1 | 0.0 | 0.0 | 1.0 |  |  |  |  |  |
| baseline:logit_pool | 890 | 4 | 0.004 | 0.75 | 10.3616 | 0.25 | 0.75 | 0.5 | 0.5 | 0.5 | 0.0 | 0.2522 | 1 | 0.0 | 0.0 | 1.0 |  |  |  |  |  |
| baseline:mean | 890 | 4 | 0.004 | 0.75 | 10.3616 | 0.25 | 0.75 | 0.5 | 0.5 | 0.5 | 0.0 | 0.2522 | 1 | 0.0 | 0.0 | 1.0 |  |  |  |  |  |
| baseline:median | 890 | 4 | 0.004 | 0.75 | 10.3616 | 0.25 | 0.75 | 0.5 | 0.5 | 0.5 | 0.0 | 0.2522 | 1 | 0.0 | 0.0 | 1.0 |  |  |  |  |  |
| market | 890 | 832 | 0.935 | 0.1935 | 0.5534 | 0.6689 | 0.0232 | 0.1638 | 0.7384 | 0.6316 | 0.2892 | 0.1972 | 1 | 0.1722 | 0.5361 | 1.0 |  |  |  |  |  |

- `baseline:best_single` not reported: no single model answered 30 or more questions

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.380 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 38.0% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| single:llama3.1:latest | 2 | 2 | 0 | 0 | 1 | 1 | 0 | 0 | 0.5 | 1.0 | 0.6667 | 0.5 | 0.0 |
| single:mistral:latest | 7 | 4 | 3 | 0 | 1 | 3 | 3 | 0 | 0.25 | 1.0 | 0.4 | 0.75 | 0.3536 |
| single:qwen3:8b | 9 | 9 | 0 | 0 | 1 | 8 | 0 | 0 | 0.1111 | 1.0 | 0.2 | 0.5 | 0.0 |
| baseline:always_no | 890 | 0 | 890 | 0 | 0 | 0 | 552 | 338 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 890 | 0 | 890 | 0 | 0 | 0 | 552 | 338 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:extremized(a=2) | 4 | 4 | 0 | 0 | 1 | 3 | 0 | 0 | 0.25 | 1.0 | 0.4 | 0.5 | 0.0 |
| baseline:logit_pool | 4 | 4 | 0 | 0 | 1 | 3 | 0 | 0 | 0.25 | 1.0 | 0.4 | 0.5 | 0.0 |
| baseline:mean | 4 | 4 | 0 | 0 | 1 | 3 | 0 | 0 | 0.25 | 1.0 | 0.4 | 0.5 | 0.0 |
| baseline:median | 4 | 4 | 0 | 0 | 1 | 3 | 0 | 0 | 0.25 | 1.0 | 0.4 | 0.5 | 0.0 |
| market | 832 | 219 | 588 | 25 | 137 | 82 | 407 | 181 | 0.6256 | 0.4308 | 0.5102 | 0.6316 | 0.2892 |


## Does the LLM-judge score track the ground truth?

Mean judge score (1–5) for answers that turned out right vs wrong. `judge_auroc_for_right`: chance a right answer got a higher judge score than a wrong one; 0.5 = the judge can't tell.

| setup | n | right | wrong | judge_mean_right | judge_mean_wrong | judge_auroc_for_right |
|---|---|---|---|---|---|---|
| single:llama3.1:latest | 2 | 1 | 1 | 5.0 | 4.0 | 1.0 |
| single:mistral:latest | 6 | 3 | 3 | 4.667 | 4.333 | 0.6667 |
| single:qwen3:8b | 9 | 1 | 8 | 5.0 | 4.125 | 0.9375 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| single:llama3.1:latest | 2 | 0.25 | 0.0 | 0.25 | 0.5 |
| single:mistral:latest | 7 | 0.3214 | 0.0153 | 0.1224 | 0.4286 |
| single:qwen3:8b | 9 | 0.7901 | 0.0 | 0.0988 | 0.8889 |
| baseline:always_no | 890 | 0.1442 | 0.0 | 0.2355 | 0.3798 |
| baseline:base_rate | 890 | 0.0 | 0.0 | 0.2355 | 0.2355 |
| baseline:extremized(a=2) | 4 | 0.5625 | 0.0 | 0.1875 | 0.75 |
| baseline:logit_pool | 4 | 0.5625 | 0.0 | 0.1875 | 0.75 |
| baseline:mean | 4 | 0.5625 | 0.0 | 0.1875 | 0.75 |
| baseline:median | 4 | 0.5625 | 0.0 | 0.1875 | 0.75 |
| market | 832 | 0.001 | 0.0459 | 0.2396 | 0.1935 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

_none_
