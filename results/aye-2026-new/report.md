# Results: aye-2026-new

Resolved questions scored: **1611** (set: all). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | auroc | brier_abstain_0.5 |
|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | 1611 | 936 | 0.581 | 0.3429 | 4.738 | 0.6571 | 0.3429 | 0.6019 | 0.304 |
| council:chair=mistral:latest | 1611 | 512 | 0.318 | 0.3574 | 4.938 | 0.6426 | 0.3574 | 0.6454 | 0.2841 |
| council:chair=qwen3:8b | 1611 | 191 | 0.119 | 0.2827 | 3.906 | 0.7173 | 0.2827 | 0.5904 | 0.2539 |
| single:deepseek-r1:8b | 1611 | 138 | 0.086 | 0.6087 | 8.4094 | 0.3913 | 0.6087 | 0.3487 | 0.2807 |
| single:gemma2:9b | 1611 | 41 | 0.025 | 0.6829 | 9.435 | 0.3171 | 0.6829 | 0.5 | 0.261 |
| single:llama3.1:8b-instruct-q4_K_M | 1611 | 76 | 0.047 | 0.5789 | 7.9985 | 0.4211 | 0.5789 | 0.5417 | 0.2655 |
| single:mistral:latest | 1611 | 96 | 0.06 | 0.6875 | 9.4982 | 0.3125 | 0.6875 | 0.5722 | 0.2761 |
| single:phi3:medium | 1611 | 887 | 0.551 | 0.646 | 8.9248 | 0.354 | 0.646 | 0.5212 | 0.468 |
| single:qwen3:8b | 1611 | 60 | 0.037 | 0.6167 | 8.5196 | 0.3833 | 0.6167 | 0.4918 | 0.2637 |
| baseline:best_single | 1611 | 887 | 0.551 | 0.646 | 8.9248 | 0.354 | 0.646 | 0.5212 | 0.468 |
| baseline:extremized(a=2) | 1611 | 240 | 0.149 | 0.6489 | 8.2331 | 0.3625 | 0.6604 | 0.5334 | 0.3094 |
| baseline:logit_pool | 1611 | 240 | 0.149 | 0.6474 | 7.9155 | 0.3625 | 0.6595 | 0.5334 | 0.3092 |
| baseline:mean | 1611 | 240 | 0.149 | 0.6144 | 7.6781 | 0.3104 | 0.6342 | 0.5334 | 0.3043 |
| baseline:median | 1611 | 240 | 0.149 | 0.649 | 8.5171 | 0.3104 | 0.6604 | 0.5221 | 0.3094 |

- `baseline:best_single` = single:phi3:medium (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)


## Council vs baselines (paired Brier difference, negative = council better)

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | baseline:best_single | 479 | -0.1962 | -0.2568 | -0.1357 | council better |
| council:chair=llama3.1:8b-instruct-q4_K_M | baseline:mean | 151 | -0.1352 | -0.2494 | -0.0152 | council better |
| council:chair=mistral:latest | baseline:best_single | 268 | -0.1119 | -0.1903 | -0.0448 | council better |
| council:chair=mistral:latest | baseline:mean | 96 | -0.123 | -0.243 | 0.0051 | no clear difference |
| council:chair=qwen3:8b | baseline:best_single | 102 | -0.3137 | -0.4412 | -0.1961 | council better |
| council:chair=qwen3:8b | baseline:mean | 49 | -0.3112 | -0.4623 | -0.1453 | council better |


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
| baseline:best_single | 887 | 0.4341 | 0.0012 | 0.2131 | 0.646 |
| baseline:extremized(a=2) | 240 | 0.475 | 0.0004 | 0.1744 | 0.6489 |
| baseline:logit_pool | 240 | 0.4738 | 0.0004 | 0.1744 | 0.6474 |
| baseline:mean | 240 | 0.4463 | 0.0063 | 0.1744 | 0.6144 |
| baseline:median | 240 | 0.475 | 0.0004 | 0.1744 | 0.649 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b-instruct-q4_K_M | 151 | -0.0278 | 0.42 | 0.42 | 0.3922 |
| council:chair=mistral:latest | 96 | -0.105 | 0.3438 | 0.5312 | 0.375 |
| council:chair=qwen3:8b | 49 | -0.0019 | 0.25 | 0.1875 | 0.2941 |
