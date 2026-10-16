# Results: aye-2026-new

Resolved questions scored: **1611** (set: all). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | 1611 | 936 | 0.581 | 0.3429 | 4.738 | 0.6571 | 0.3429 | 0.5 | 0.6019 | 0.6019 | 0.215 | 0.304 | 901 | -0.8531 | -1.0279 | -0.6872 |
| council:chair=mistral:latest | 1611 | 512 | 0.318 | 0.3574 | 4.938 | 0.6426 | 0.3574 | 0.5 | 0.6454 | 0.6454 | 0.2803 | 0.2841 | 484 | -1.1594 | -1.441 | -0.8969 |
| council:chair=qwen3:8b | 1611 | 191 | 0.119 | 0.2827 | 3.906 | 0.7173 | 0.2827 | 0.5 | 0.5904 | 0.5904 | 0.1931 | 0.2539 | 172 | -1.3604 | -1.9397 | -0.8384 |
| single:deepseek-r1:8b | 1611 | 138 | 0.086 | 0.6087 | 8.4094 | 0.3913 | 0.6087 | 0.5 | 0.3487 | 0.3487 | -0.2608 | 0.2807 | 129 | -3.8034 | -4.8827 | -3.0012 |
| single:gemma2:9b | 1611 | 41 | 0.025 | 0.6829 | 9.435 | 0.3171 | 0.6829 | 0.5 | 0.5 | 0.5 | 0.0 | 0.261 | 38 | -3.1907 | -5.7578 | -1.6942 |
| single:llama3.1:8b-instruct-q4_K_M | 1611 | 76 | 0.047 | 0.5789 | 7.9985 | 0.4211 | 0.5789 | 0.5 | 0.5417 | 0.5417 | 0.18 | 0.2655 | 76 | -1.4396 | -2.0097 | -0.873 |
| single:mistral:latest | 1611 | 96 | 0.06 | 0.6875 | 9.4982 | 0.3125 | 0.6875 | 0.5 | 0.5722 | 0.5722 | 0.1112 | 0.2761 | 95 | -3.3795 | -4.633 | -2.4549 |
| single:phi3:medium | 1611 | 887 | 0.551 | 0.646 | 8.9248 | 0.354 | 0.646 | 0.5 | 0.5212 | 0.5212 | 0.075 | 0.468 | 872 | -2.1399 | -2.3455 | -1.9164 |
| single:qwen3:8b | 1611 | 60 | 0.037 | 0.6167 | 8.5196 | 0.3833 | 0.6167 | 0.5 | 0.4918 | 0.4918 | -0.0446 | 0.2637 | 55 | -2.0265 | -2.8936 | -1.2854 |
| baseline:always_no | 1611 | 1611 | 1.0 | 0.3302 | 4.5623 | 0.6698 | 0.3302 | 0.5 | 0.5 | 0.5 | 0.0 | 0.3302 | 1572 | -0.7159 | -0.8309 | -0.5973 |
| baseline:base_rate | 1611 | 1611 | 1.0 | 0.2212 | 0.6343 | 0.6698 | 0.0 | 0.1698 | 0.5 | 0.5 | 0.0 | 0.2212 | 1572 | -0.145 | -0.1942 | -0.0987 |
| baseline:best_single | 1611 | 887 | 0.551 | 0.646 | 8.9248 | 0.354 | 0.646 | 0.5 | 0.5212 | 0.5212 | 0.075 | 0.468 | 872 | -2.1399 | -2.3455 | -1.9164 |
| baseline:extremized(a=2) | 1611 | 240 | 0.149 | 0.6489 | 8.2331 | 0.3625 | 0.6604 | 0.4187 | 0.5334 | 0.523 | 0.0463 | 0.3094 | 229 | -2.9285 | -3.5567 | -2.385 |
| baseline:logit_pool | 1611 | 240 | 0.149 | 0.6474 | 7.9155 | 0.3625 | 0.6595 | 0.4178 | 0.5334 | 0.523 | 0.0463 | 0.3092 | 229 | -2.9195 | -3.5437 | -2.3803 |
| baseline:mean | 1611 | 240 | 0.149 | 0.6144 | 7.6781 | 0.3104 | 0.6342 | 0.3909 | 0.5334 | 0.5038 | 0.0126 | 0.3043 | 229 | -2.7269 | -3.3324 | -2.2039 |
| baseline:median | 1611 | 240 | 0.149 | 0.649 | 8.5171 | 0.3104 | 0.6604 | 0.4188 | 0.5221 | 0.5038 | 0.0126 | 0.3094 | 229 | -2.9287 | -3.557 | -2.3852 |
| market | 1611 | 1572 | 0.976 | 0.1939 | 0.5582 | 0.7223 | 0.0929 | 0.1317 | 0.7385 | 0.6382 | 0.3695 | 0.1953 |  |  |  |  |

- `baseline:best_single` = single:phi3:medium (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.330 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 33.0% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | 936 | 268 | 668 | 0 | 137 | 131 | 478 | 190 | 0.5112 | 0.419 | 0.4605 | 0.6019 | 0.215 |
| council:chair=mistral:latest | 512 | 241 | 271 | 0 | 122 | 119 | 207 | 64 | 0.5062 | 0.6559 | 0.5714 | 0.6454 | 0.2803 |
| council:chair=qwen3:8b | 191 | 39 | 152 | 0 | 16 | 23 | 121 | 31 | 0.4103 | 0.3404 | 0.3721 | 0.5904 | 0.1931 |
| single:deepseek-r1:8b | 138 | 68 | 70 | 0 | 9 | 59 | 45 | 25 | 0.1324 | 0.2647 | 0.1765 | 0.3487 | -0.2608 |
| single:gemma2:9b | 41 | 41 | 0 | 0 | 13 | 28 | 0 | 0 | 0.3171 | 1.0 | 0.4815 | 0.5 | 0.0 |
| single:llama3.1:8b-instruct-q4_K_M | 76 | 72 | 4 | 0 | 28 | 44 | 4 | 0 | 0.3889 | 1.0 | 0.56 | 0.5417 | 0.18 |
| single:mistral:latest | 96 | 75 | 21 | 0 | 10 | 65 | 20 | 1 | 0.1333 | 0.9091 | 0.2326 | 0.5722 | 0.1112 |
| single:phi3:medium | 887 | 822 | 65 | 0 | 261 | 561 | 53 | 12 | 0.3175 | 0.956 | 0.4767 | 0.5212 | 0.075 |
| single:qwen3:8b | 60 | 58 | 2 | 0 | 22 | 36 | 1 | 1 | 0.3793 | 0.9565 | 0.5432 | 0.4918 | -0.0446 |
| baseline:always_no | 1611 | 0 | 1611 | 0 | 0 | 0 | 1079 | 532 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 1611 | 0 | 1611 | 0 | 0 | 0 | 1079 | 532 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:best_single | 887 | 822 | 65 | 0 | 261 | 561 | 53 | 12 | 0.3175 | 0.956 | 0.4767 | 0.5212 | 0.075 |
| baseline:extremized(a=2) | 240 | 187 | 53 | 0 | 44 | 143 | 43 | 10 | 0.2353 | 0.8148 | 0.3651 | 0.523 | 0.0463 |
| baseline:logit_pool | 240 | 187 | 53 | 0 | 44 | 143 | 43 | 10 | 0.2353 | 0.8148 | 0.3651 | 0.523 | 0.0463 |
| baseline:mean | 240 | 187 | 14 | 39 | 44 | 143 | 11 | 3 | 0.2353 | 0.9362 | 0.3761 | 0.5038 | 0.0126 |
| baseline:median | 240 | 187 | 14 | 39 | 44 | 143 | 11 | 3 | 0.2353 | 0.9362 | 0.3761 | 0.5038 | 0.0126 |
| market | 1572 | 201 | 1210 | 161 | 150 | 51 | 905 | 305 | 0.7463 | 0.3297 | 0.4573 | 0.6382 | 0.3695 |


## Does the LLM-judge score track the ground truth?

Mean judge score (1–5) for answers that turned out right vs wrong. `judge_auroc_for_right`: chance a right answer got a higher judge score than a wrong one; 0.5 = the judge can't tell.

| setup | n | right | wrong | judge_mean_right | judge_mean_wrong | judge_auroc_for_right |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | 936 | 615 | 321 | 4.777 | 4.81 | 0.4836 |
| council:chair=mistral:latest | 512 | 329 | 183 | 4.261 | 4.372 | 0.4449 |
| council:chair=qwen3:8b | 191 | 137 | 54 | 4.752 | 4.667 | 0.5426 |
| single:deepseek-r1:8b | 106 | 38 | 68 | 4.605 | 4.412 | 0.6043 |
| single:gemma2:9b | 36 | 13 | 23 | 4.385 | 4.304 | 0.5401 |
| single:llama3.1:8b-instruct-q4_K_M | 43 | 18 | 25 | 3.722 | 4.12 | 0.3944 |
| single:mistral:latest | 54 | 18 | 36 | 4.556 | 4.333 | 0.6111 |
| single:phi3:medium | 597 | 205 | 392 | 4.234 | 4.319 | 0.4631 |
| single:qwen3:8b | 45 | 21 | 24 | 4.952 | 4.5 | 0.6647 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | market | 901 | 0.1584 | 0.1293 | 0.1883 | council worse |
| council:chair=llama3.1:8b-instruct-q4_K_M | baseline:best_single | 479 | -0.1962 | -0.2568 | -0.1357 | council better |
| council:chair=llama3.1:8b-instruct-q4_K_M | baseline:mean | 151 | -0.1352 | -0.2494 | -0.0152 | council better |
| council:chair=llama3.1:8b-instruct-q4_K_M | baseline:logit_pool | 151 | -0.1672 | -0.2867 | -0.044 | council better |
| council:chair=llama3.1:8b-instruct-q4_K_M | baseline:always_no | 936 | -0.0064 | -0.0374 | 0.0288 | no clear difference |
| council:chair=mistral:latest | market | 484 | 0.193 | 0.1519 | 0.2305 | council worse |
| council:chair=mistral:latest | baseline:best_single | 268 | -0.1119 | -0.1903 | -0.0448 | council better |
| council:chair=mistral:latest | baseline:mean | 96 | -0.123 | -0.243 | 0.0051 | no clear difference |
| council:chair=mistral:latest | baseline:logit_pool | 96 | -0.1678 | -0.2891 | -0.035 | council better |
| council:chair=mistral:latest | baseline:always_no | 512 | -0.0059 | -0.0664 | 0.0547 | no clear difference |
| council:chair=qwen3:8b | market | 172 | 0.1675 | 0.1074 | 0.236 | council worse |
| council:chair=qwen3:8b | baseline:best_single | 102 | -0.3137 | -0.4412 | -0.1961 | council better |
| council:chair=qwen3:8b | baseline:mean | 49 | -0.3112 | -0.4623 | -0.1453 | council better |
| council:chair=qwen3:8b | baseline:logit_pool | 49 | -0.39 | -0.547 | -0.2173 | council better |
| council:chair=qwen3:8b | baseline:always_no | 191 | 0.0366 | -0.0262 | 0.1047 | no clear difference |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | 936 | 0.1261 | 0.0105 | 0.2273 | 0.3429 |
| council:chair=mistral:latest | 512 | 0.1443 | 0.0182 | 0.2313 | 0.3574 |
| council:chair=qwen3:8b | 191 | 0.1041 | 0.0069 | 0.1855 | 0.2827 |
| single:deepseek-r1:8b | 138 | 0.4357 | 0.0126 | 0.1857 | 0.6087 |
| single:gemma2:9b | 41 | 0.4664 | 0.0 | 0.2165 | 0.6829 |
| single:llama3.1:8b-instruct-q4_K_M | 76 | 0.3538 | 0.0075 | 0.2327 | 0.5789 |
| single:mistral:latest | 96 | 0.5873 | 0.0013 | 0.1015 | 0.6875 |
| single:phi3:medium | 887 | 0.4341 | 0.0012 | 0.2131 | 0.646 |
| single:qwen3:8b | 60 | 0.3807 | 0.0005 | 0.2364 | 0.6167 |
| baseline:always_no | 1611 | 0.1091 | 0.0 | 0.2212 | 0.3302 |
| baseline:base_rate | 1611 | 0.0 | 0.0 | 0.2212 | 0.2212 |
| baseline:best_single | 887 | 0.4341 | 0.0012 | 0.2131 | 0.646 |
| baseline:extremized(a=2) | 240 | 0.475 | 0.0004 | 0.1744 | 0.6489 |
| baseline:logit_pool | 240 | 0.4738 | 0.0004 | 0.1744 | 0.6474 |
| baseline:mean | 240 | 0.4463 | 0.0063 | 0.1744 | 0.6144 |
| baseline:median | 240 | 0.475 | 0.0004 | 0.1744 | 0.649 |
| market | 1572 | 0.0131 | 0.0391 | 0.222 | 0.1939 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | 151 | -0.0278 | 0.42 | 0.42 | 0.3922 |
| council:chair=mistral:latest | 96 | -0.105 | 0.3438 | 0.5312 | 0.375 |
| council:chair=qwen3:8b | 49 | -0.0019 | 0.25 | 0.1875 | 0.2941 |
