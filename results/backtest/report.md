# Results: backtest

Resolved questions scored: **1185** (set: settled + settled-ext + contamination). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 1185 | 1185 | 1.0 | 0.4228 | 5.841 | 0.5772 | 0.4228 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4228 | 1185 | 0.4228 | 5.841 | 0.5772 | 0.5 | -1.6673 | 1185 | -1.6672 | -1.8983 | -1.441 |
| baseline:base_rate | 1185 | 1185 | 1.0 | 0.244 | 0.6812 | 0.5772 | 0.0 | 0.0772 | 0.5 | 0.5 | 0.0 | 0.244 | 1185 | 0.244 | 0.6812 | 0.5772 | 0.5 | -0.5393 | 1185 | -0.5395 | -0.6703 | -0.4241 |
| market | 1185 | 1185 | 1.0 | 0.1585 | 0.4808 | 0.7536 | 0.063 | 0.3045 | 0.8561 | 0.7411 | 0.4926 | 0.1585 | 1185 | 0.1585 | 0.4808 | 0.7536 | 0.8561 |  |  |  |  |  |

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.423 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 42.3% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 1185 | 0 | 1185 | 0 | 0 | 0 | 684 | 501 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 1185 | 0 | 1185 | 0 | 0 | 0 | 684 | 501 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| market | 1185 | 440 | 739 | 6 | 325 | 115 | 565 | 174 | 0.7386 | 0.6513 | 0.6922 | 0.7411 | 0.4926 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| baseline:always_no | 1185 | 0.1787 | 0.0 | 0.244 | 0.4228 |
| baseline:base_rate | 1185 | 0.0 | 0.0 | 0.244 | 0.244 |
| market | 1185 | 0.0075 | 0.0909 | 0.244 | 0.1585 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

_none_
