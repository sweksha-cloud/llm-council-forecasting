# Results: contamination

Resolved questions scored: **146** (set: contamination). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 146 | 146 | 1.0 | 0.3356 | 4.6367 | 0.6644 | 0.3356 | 0.5 | 0.5 | 0.5 | 0.0 | 0.3356 | 146 | 0.3356 | 4.6367 | 0.6644 | 0.5 | -3.0324 | 146 | -3.0326 | -4.7705 | -2.0158 |
| baseline:base_rate | 146 | 146 | 1.0 | 0.223 | 0.6381 | 0.6644 | 0.0 | 0.1644 | 0.5 | 0.5 | 0.0 | 0.223 | 146 | 0.223 | 0.6381 | 0.6644 | 0.5 | -1.6795 | 146 | -1.6792 | -2.8266 | -1.0525 |
| market | 146 | 146 | 1.0 | 0.0832 | 0.2616 | 0.863 | 0.0824 | 0.3706 | 0.9572 | 0.8308 | 0.6999 | 0.0832 | 146 | 0.0832 | 0.2616 | 0.863 | 0.9572 |  |  |  |  |  |

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.336 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 33.6% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 146 | 0 | 146 | 0 | 0 | 0 | 97 | 49 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 146 | 0 | 146 | 0 | 0 | 0 | 97 | 49 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| market | 146 | 40 | 104 | 2 | 35 | 5 | 90 | 14 | 0.875 | 0.7143 | 0.7865 | 0.8308 | 0.6999 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| baseline:always_no | 146 | 0.1126 | 0.0 | 0.223 | 0.3356 |
| baseline:base_rate | 146 | 0.0 | 0.0 | 0.223 | 0.223 |
| market | 146 | 0.014 | 0.1528 | 0.223 | 0.0832 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

_none_
