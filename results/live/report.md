# Results: live

Resolved questions scored: **62** (set: live). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 62 | 5 | 0.081 | 0.3911 | 1.0172 | 0.4 | 0.596 | 0.2 | 0.0 | 0.3333 | -0.4082 | 0.2614 | 5 | 0.3911 | 1.0172 | 0.4 | 0.0 |  |  |  |  |
| council:chair=qwen3:8b | 62 | 5 | 0.081 | 0.3904 | 1.0204 | 0.4 | 0.596 | 0.196 | 0.0 | 0.3333 | -0.4082 | 0.2613 | 5 | 0.3904 | 1.0204 | 0.4 | 0.0 |  |  |  |  |
| single:gemma2:9b | 62 | 5 | 0.081 | 0.404 | 1.0628 | 0.3 | 0.5 | 0.2 | 0.25 | 0.25 | -0.5774 | 0.2624 | 5 | 0.404 | 1.0628 | 0.3 | 0.25 |  |  |  |  |
| single:llama3.1:8b | 62 | 5 | 0.081 | 0.3545 | 0.9548 | 0.4 | 0.25 | 0.15 | 0.3333 | 0.3333 | -0.4082 | 0.2584 | 5 | 0.3545 | 0.9548 | 0.4 | 0.3333 |  |  |  |  |
| single:mistral:latest | 62 | 5 | 0.081 | 0.332 | 0.8692 | 0.4 | 0.32 | 0.14 | 0.1667 | 0.3333 | -0.4082 | 0.2566 | 5 | 0.332 | 0.8692 | 0.4 | 0.1667 |  |  |  |  |
| single:phi3:medium | 62 | 5 | 0.081 | 0.386 | 1.0211 | 0.4 | 0.44 | 0.16 | 0.0 | 0.3333 | -0.4082 | 0.261 | 5 | 0.386 | 1.0211 | 0.4 | 0.0 |  |  |  |  |
| single:qwen3:8b | 62 | 5 | 0.081 | 0.4745 | 1.3943 | 0.4 | 0.51 | 0.23 | 0.0833 | 0.3333 | -0.4082 | 0.2681 | 5 | 0.4745 | 1.3943 | 0.4 | 0.0833 |  |  |  |  |
| baseline:always_no | 62 | 62 | 1.0 | 0.4677 | 6.4621 | 0.5323 | 0.4677 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4677 | 5 | 0.6 | 8.2893 | 0.4 | 0.5 | 62 | -2.1728 | -3.98 | -1.0622 |
| baseline:base_rate | 62 | 62 | 1.0 | 0.249 | 0.6911 | 0.5323 | 0.0 | 0.0323 | 0.5 | 0.5 | 0.0 | 0.249 | 5 | 0.2575 | 0.7082 | 0.4 | 0.5 | 62 | -0.6887 | -1.5434 | -0.2473 |
| baseline:extremized(a=2) | 62 | 5 | 0.081 | 0.4932 | 1.5455 | 0.4 | 0.6427 | 0.2978 | 0.0 | 0.3333 | -0.4082 | 0.2696 | 5 | 0.4932 | 1.5455 | 0.4 | 0.0 |  |  |  |  |
| baseline:logit_pool | 62 | 5 | 0.081 | 0.3941 | 1.0456 | 0.4 | 0.4547 | 0.183 | 0.0 | 0.3333 | -0.4082 | 0.2616 | 5 | 0.3941 | 1.0456 | 0.4 | 0.0 |  |  |  |  |
| baseline:mean | 62 | 5 | 0.081 | 0.3851 | 1.015 | 0.4 | 0.448 | 0.176 | 0.0 | 0.3333 | -0.4082 | 0.2609 | 5 | 0.3851 | 1.015 | 0.4 | 0.0 |  |  |  |  |
| baseline:median | 62 | 5 | 0.081 | 0.386 | 1.0211 | 0.4 | 0.44 | 0.16 | 0.0 | 0.3333 | -0.4082 | 0.261 | 5 | 0.386 | 1.0211 | 0.4 | 0.0 |  |  |  |  |
| market | 62 | 62 | 1.0 | 0.1474 | 0.419 | 0.7581 | 0.0908 | 0.3121 | 0.8683 | 0.756 | 0.5134 | 0.1474 | 5 | 0.0001 | 0.008 | 1.0 | 1.0 |  |  |  |  |

- `baseline:best_single` not reported: no single model answered 30 or more questions

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.468 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 46.8% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| council:chair=qwen3:8b | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| single:gemma2:9b | 5 | 3 | 1 | 1 | 1 | 2 | 0 | 1 | 0.3333 | 0.5 | 0.4 | 0.25 | -0.5774 |
| single:llama3.1:8b | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| single:mistral:latest | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| single:phi3:medium | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| single:qwen3:8b | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| baseline:always_no | 62 | 0 | 62 | 0 | 0 | 0 | 33 | 29 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 62 | 0 | 62 | 0 | 0 | 0 | 33 | 29 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:extremized(a=2) | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| baseline:logit_pool | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| baseline:mean | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| baseline:median | 5 | 4 | 1 | 0 | 2 | 2 | 0 | 1 | 0.5 | 0.6667 | 0.5714 | 0.3333 | -0.4082 |
| market | 62 | 28 | 34 | 0 | 21 | 7 | 26 | 8 | 0.75 | 0.7241 | 0.7368 | 0.756 | 0.5134 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | market | 5 | 0.391 | 0.2394 | 0.5426 | council worse |
| council:chair=llama3.1:8b | baseline:mean | 5 | 0.006 | -0.0303 | 0.0424 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | 5 | -0.003 | -0.0352 | 0.0292 | no clear difference |
| council:chair=llama3.1:8b | baseline:always_no | 5 | -0.2089 | -0.7605 | 0.3427 | no clear difference |
| council:chair=qwen3:8b | market | 5 | 0.3903 | 0.2485 | 0.532 | council worse |
| council:chair=qwen3:8b | baseline:mean | 5 | 0.0053 | -0.0212 | 0.0318 | no clear difference |
| council:chair=qwen3:8b | baseline:logit_pool | 5 | -0.0038 | -0.0262 | 0.0186 | no clear difference |
| council:chair=qwen3:8b | baseline:always_no | 5 | -0.2096 | -0.7514 | 0.3321 | no clear difference |


## Council vs baselines, by source

| source | council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|---|
| kalshi | council:chair=llama3.1:8b | market | 4 | 0.3288 | 0.1208 | 0.5183 | council worse |
| kalshi | council:chair=llama3.1:8b | baseline:mean | 4 | 0.024 | -0.028 | 0.0761 | no clear difference |
| kalshi | council:chair=llama3.1:8b | baseline:logit_pool | 4 | 0.0203 | -0.0261 | 0.0639 | no clear difference |
| kalshi | council:chair=llama3.1:8b | baseline:always_no | 4 | -0.1711 | -0.8791 | 0.5184 | no clear difference |
| kalshi | council:chair=qwen3:8b | market | 4 | 0.3197 | 0.1257 | 0.497 | council worse |
| kalshi | council:chair=qwen3:8b | baseline:mean | 4 | 0.0149 | -0.0231 | 0.0512 | no clear difference |
| kalshi | council:chair=qwen3:8b | baseline:logit_pool | 4 | 0.0113 | -0.0212 | 0.0393 | no clear difference |
| kalshi | council:chair=qwen3:8b | baseline:always_no | 4 | -0.1802 | -0.8742 | 0.497 | no clear difference |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 5 | 0.3911 | 0.24 | 0.24 | 0.3911 |
| council:chair=qwen3:8b | 5 | 0.3904 | 0.24 | 0.24 | 0.3904 |
| single:gemma2:9b | 5 | 0.304 | 0.14 | 0.24 | 0.404 |
| single:llama3.1:8b | 5 | 0.1545 | 0.04 | 0.24 | 0.3545 |
| single:mistral:latest | 5 | 0.1987 | 0.1067 | 0.24 | 0.332 |
| single:phi3:medium | 5 | 0.239 | 0.1067 | 0.24 | 0.386 |
| single:qwen3:8b | 5 | 0.3745 | 0.14 | 0.24 | 0.4745 |
| baseline:always_no | 62 | 0.2188 | 0.0 | 0.249 | 0.4677 |
| baseline:base_rate | 62 | 0.0 | 0.0 | 0.249 | 0.249 |
| baseline:extremized(a=2) | 5 | 0.4932 | 0.24 | 0.24 | 0.4932 |
| baseline:logit_pool | 5 | 0.2489 | 0.1067 | 0.24 | 0.3941 |
| baseline:mean | 5 | 0.2408 | 0.1067 | 0.24 | 0.3851 |
| baseline:median | 5 | 0.239 | 0.1067 | 0.24 | 0.386 |
| market | 62 | 0.0248 | 0.1304 | 0.249 | 0.1474 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 5 | 0.3078 | 0.5184 | 0.1394 | 0.5792 |
| council:chair=qwen3:8b | 5 | 0.1 | 0.5041 | 0.1426 | 0.5812 |
