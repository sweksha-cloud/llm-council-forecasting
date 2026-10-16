# Results: settled-all

Resolved questions scored: **1039** (set: settled + settled-ext). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 1039 | 1039 | 1.0 | 0.435 | 6.0102 | 0.565 | 0.435 | 0.5 | 0.5 | 0.5 | 0.0 | 0.435 | 1039 | 0.435 | 6.0102 | 0.565 | 0.5 | -1.5725 | 1039 | -1.5727 | -1.8177 | -1.3411 |
| baseline:base_rate | 1039 | 1039 | 1.0 | 0.2458 | 0.6847 | 0.565 | 0.0 | 0.065 | 0.5 | 0.5 | 0.0 | 0.2458 | 1039 | 0.2458 | 0.6847 | 0.565 | 0.5 | -0.4536 | 1039 | -0.4535 | -0.585 | -0.3396 |
| market | 1039 | 1039 | 1.0 | 0.1691 | 0.5116 | 0.7382 | 0.0705 | 0.2952 | 0.8395 | 0.7282 | 0.4646 | 0.1691 | 1039 | 0.1691 | 0.5116 | 0.7382 | 0.8395 |  |  |  |  |  |

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.435 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 43.5% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 1039 | 0 | 1039 | 0 | 0 | 0 | 587 | 452 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 1039 | 0 | 1039 | 0 | 0 | 0 | 587 | 452 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| market | 1039 | 400 | 635 | 4 | 290 | 110 | 475 | 160 | 0.725 | 0.6444 | 0.6824 | 0.7282 | 0.4646 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| baseline:always_no | 1039 | 0.1893 | 0.0 | 0.2458 | 0.435 |
| baseline:base_rate | 1039 | 0.0 | 0.0 | 0.2458 | 0.2458 |
| market | 1039 | 0.0083 | 0.0826 | 0.2458 | 0.1691 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

_none_
