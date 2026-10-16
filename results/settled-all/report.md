# Results: settled-all

Resolved questions scored: **1042** (set: settled + settled-ext). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 1042 | 1042 | 1.0 | 0.4367 | 6.0327 | 0.5633 | 0.4367 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4367 | 1040 | 0.4356 | 6.0177 | 0.5644 | 0.5 | -1.5866 | 1040 | -1.5865 | -1.8272 | -1.3553 |
| baseline:base_rate | 1042 | 1042 | 1.0 | 0.246 | 0.6851 | 0.5633 | 0.0 | 0.0633 | 0.5 | 0.5 | 0.0 | 0.246 | 1040 | 0.2459 | 0.6848 | 0.5644 | 0.5 | -0.4602 | 1040 | -0.4599 | -0.5839 | -0.346 |
| market | 1042 | 1040 | 0.998 | 0.1684 | 0.5088 | 0.7394 | 0.0707 | 0.2952 | 0.8408 | 0.7303 | 0.4681 | 0.1686 | 1040 | 0.1684 | 0.5088 | 0.7394 | 0.8408 |  |  |  |  |  |

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.437 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 43.7% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 1042 | 0 | 1042 | 0 | 0 | 0 | 587 | 455 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 1042 | 0 | 1042 | 0 | 0 | 0 | 587 | 455 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| market | 1040 | 403 | 631 | 6 | 292 | 111 | 474 | 157 | 0.7246 | 0.6503 | 0.6854 | 0.7303 | 0.4681 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| baseline:always_no | 1042 | 0.1907 | 0.0 | 0.246 | 0.4367 |
| baseline:base_rate | 1042 | 0.0 | 0.0 | 0.246 | 0.246 |
| market | 1040 | 0.0084 | 0.0836 | 0.2458 | 0.1684 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

_none_
