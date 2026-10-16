# Results: backtest

Resolved questions scored: **515** (set: settled + settled-ext + contamination). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 515 | 515 | 1.0 | 0.4369 | 6.0359 | 0.5631 | 0.4369 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4369 | 513 | 0.4347 | 6.0056 | 0.5653 | 0.5 | -2.425 | 513 | -2.425 | -3.0026 | -1.9656 |
| baseline:base_rate | 515 | 515 | 1.0 | 0.246 | 0.6852 | 0.5631 | 0.0 | 0.0631 | 0.5 | 0.5 | 0.0 | 0.246 | 513 | 0.2457 | 0.6846 | 0.5653 | 0.5 | -0.9359 | 513 | -0.9362 | -1.2577 | -0.706 |
| market | 515 | 513 | 0.996 | 0.1269 | 0.3956 | 0.8119 | 0.0576 | 0.3216 | 0.9038 | 0.8038 | 0.6181 | 0.1274 | 513 | 0.1269 | 0.3956 | 0.8119 | 0.9038 |  |  |  |  |  |

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.437 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 43.7% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 515 | 0 | 515 | 0 | 0 | 0 | 290 | 225 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 515 | 0 | 515 | 0 | 0 | 0 | 290 | 225 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| market | 513 | 197 | 313 | 3 | 161 | 36 | 254 | 59 | 0.8173 | 0.7318 | 0.7722 | 0.8038 | 0.6181 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| baseline:always_no | 515 | 0.1909 | 0.0 | 0.246 | 0.4369 |
| baseline:base_rate | 515 | 0.0 | 0.0 | 0.246 | 0.246 |
| market | 513 | 0.0084 | 0.1253 | 0.2457 | 0.1269 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

_none_
