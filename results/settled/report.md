# Results: settled

Resolved questions scored: **362** (set: settled). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 362 | 362 | 1.0 | 0.4779 | 6.6024 | 0.5221 | 0.4779 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4779 | 360 | 0.475 | 6.5624 | 0.525 | 0.5 | -2.2916 | 360 | -2.2916 | -2.9038 | -1.7961 |
| baseline:base_rate | 362 | 362 | 1.0 | 0.2495 | 0.6922 | 0.5221 | 0.0 | 0.0221 | 0.5 | 0.5 | 0.0 | 0.2495 | 360 | 0.2494 | 0.6919 | 0.525 | 0.5 | -0.7283 | 360 | -0.7281 | -1.034 | -0.4987 |
| market | 362 | 360 | 0.994 | 0.1443 | 0.4506 | 0.7875 | 0.0744 | 0.2992 | 0.878 | 0.7867 | 0.5784 | 0.1449 | 360 | 0.1443 | 0.4506 | 0.7875 | 0.878 |  |  |  |  |  |

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.478 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 47.8% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline:always_no | 362 | 0 | 362 | 0 | 0 | 0 | 189 | 173 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 362 | 0 | 362 | 0 | 0 | 0 | 189 | 173 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| market | 360 | 153 | 204 | 3 | 123 | 30 | 159 | 45 | 0.8039 | 0.7321 | 0.7664 | 0.7867 | 0.5784 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| baseline:always_no | 362 | 0.2284 | 0.0 | 0.2495 | 0.4779 |
| baseline:base_rate | 362 | 0.0 | 0.0 | 0.2495 | 0.2495 |
| market | 360 | 0.0105 | 0.1138 | 0.2494 | 0.1443 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

_none_
