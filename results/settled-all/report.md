# Results: settled-all

Resolved questions scored: **1039** (set: settled + settled-ext). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1039 | 1039 | 1.0 | 0.2532 | 0.7074 | 0.5611 | 0.0978 | 0.1617 | 0.5839 | 0.5525 | 0.1051 | 0.2532 | 359 | 0.2556 | 0.7147 | 0.571 | 0.5859 | -0.748 | 1039 | -0.4971 | -0.6327 | -0.3786 |
| council:chair=qwen3:8b | 1039 | 1039 | 1.0 | 0.2617 | 0.7929 | 0.5635 | 0.123 | 0.188 | 0.583 | 0.553 | 0.1073 | 0.2617 | 359 | 0.2639 | 0.8124 | 0.5724 | 0.587 | -0.8047 | 1039 | -0.5479 | -0.6866 | -0.4252 |
| single:deepseek-r1:8b | 1039 | 359 | 0.346 | 0.2906 | 0.897 | 0.5251 | 0.206 | 0.2277 | 0.5617 | 0.5115 | 0.0266 | 0.264 | 359 | 0.2906 | 0.897 | 0.5251 | 0.5617 | -0.9873 | 359 | -0.987 | -1.3635 | -0.7075 |
| single:gemma2:9b | 1039 | 1039 | 1.0 | 0.261 | 0.7424 | 0.5765 | 0.1242 | 0.1881 | 0.5924 | 0.5602 | 0.1273 | 0.261 | 359 | 0.2715 | 0.7692 | 0.5571 | 0.5771 | -0.8567 | 1039 | -0.5435 | -0.6834 | -0.4246 |
| single:llama3.1:8b | 1039 | 1039 | 1.0 | 0.257 | 0.7391 | 0.5452 | 0.1202 | 0.1649 | 0.5703 | 0.5238 | 0.0503 | 0.257 | 359 | 0.2711 | 0.7855 | 0.5042 | 0.5535 | -0.854 | 1039 | -0.52 | -0.6477 | -0.4033 |
| single:mistral:latest | 1039 | 1039 | 1.0 | 0.2774 | 0.8507 | 0.5563 | 0.1439 | 0.1964 | 0.5601 | 0.5593 | 0.1178 | 0.2774 | 359 | 0.2737 | 0.8058 | 0.5682 | 0.5707 | -0.8718 | 1039 | -0.6402 | -0.8029 | -0.5018 |
| single:phi3:medium | 1039 | 1039 | 1.0 | 0.2538 | 0.7273 | 0.5784 | 0.0979 | 0.1571 | 0.5969 | 0.5756 | 0.1555 | 0.2538 | 359 | 0.2595 | 0.7633 | 0.571 | 0.5897 | -0.7746 | 1039 | -0.5012 | -0.6332 | -0.3852 |
| single:qwen3:8b | 1039 | 1039 | 1.0 | 0.2948 | 1.0211 | 0.5539 | 0.2193 | 0.2601 | 0.5695 | 0.5205 | 0.0449 | 0.2948 | 359 | 0.29 | 0.9488 | 0.5529 | 0.5887 | -0.9832 | 1039 | -0.7436 | -0.9114 | -0.5994 |
| baseline:always_no | 1039 | 1039 | 1.0 | 0.435 | 6.0102 | 0.565 | 0.435 | 0.5 | 0.5 | 0.5 | 0.0 | 0.435 | 359 | 0.4735 | 6.5422 | 0.5265 | 0.5 | -2.2381 | 1039 | -1.5727 | -1.8177 | -1.3411 |
| baseline:base_rate | 1039 | 1039 | 1.0 | 0.2458 | 0.6847 | 0.565 | 0.0 | 0.065 | 0.5 | 0.5 | 0.0 | 0.2458 | 359 | 0.2508 | 0.6947 | 0.5265 | 0.5 | -0.7152 | 1039 | -0.4535 | -0.585 | -0.3396 |
| baseline:best_single | 1039 | 1039 | 1.0 | 0.2538 | 0.7273 | 0.5784 | 0.0979 | 0.1571 | 0.5969 | 0.5756 | 0.1555 | 0.2538 | 359 | 0.2595 | 0.7633 | 0.571 | 0.5897 | -0.7746 | 1039 | -0.5012 | -0.6332 | -0.3852 |
| baseline:extremized(a=2) | 1039 | 1039 | 1.0 | 0.2926 | 0.9803 | 0.5717 | 0.2052 | 0.2798 | 0.5898 | 0.5504 | 0.1059 | 0.2926 | 359 | 0.2939 | 0.9689 | 0.5738 | 0.5964 | -1.0099 | 1039 | -0.7302 | -0.8842 | -0.5928 |
| baseline:logit_pool | 1039 | 1039 | 1.0 | 0.2592 | 0.7454 | 0.5717 | 0.1156 | 0.1899 | 0.5898 | 0.5504 | 0.1059 | 0.2592 | 359 | 0.2611 | 0.7485 | 0.5738 | 0.5964 | -0.7856 | 1039 | -0.5326 | -0.6642 | -0.4172 |
| baseline:mean | 1039 | 1039 | 1.0 | 0.2503 | 0.702 | 0.5717 | 0.0856 | 0.162 | 0.5922 | 0.5514 | 0.1075 | 0.2503 | 359 | 0.2534 | 0.7086 | 0.5724 | 0.5959 | -0.7329 | 1039 | -0.4801 | -0.6067 | -0.3701 |
| baseline:median | 1039 | 1039 | 1.0 | 0.2568 | 0.7232 | 0.5722 | 0.11 | 0.1682 | 0.5825 | 0.5569 | 0.1188 | 0.2568 | 359 | 0.2632 | 0.7385 | 0.5529 | 0.5762 | -0.8 | 1039 | -0.5188 | -0.6529 | -0.3988 |
| market | 1039 | 1039 | 1.0 | 0.1691 | 0.5116 | 0.7382 | 0.0705 | 0.2952 | 0.8395 | 0.7282 | 0.4646 | 0.1691 | 359 | 0.1462 | 0.4585 | 0.7841 | 0.8745 |  |  |  |  |  |

- `baseline:mean` and the other pools use only council members: gemma2:9b, llama3.1:8b, mistral:latest, phi3:medium, qwen3:8b

- `baseline:best_single` = single:phi3:medium (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.435 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 43.5% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1039 | 441 | 592 | 6 | 217 | 224 | 363 | 229 | 0.4921 | 0.4865 | 0.4893 | 0.5525 | 0.1051 |
| council:chair=qwen3:8b | 1039 | 397 | 601 | 41 | 197 | 200 | 368 | 233 | 0.4962 | 0.4581 | 0.4764 | 0.553 | 0.1073 |
| single:deepseek-r1:8b | 359 | 83 | 257 | 19 | 41 | 42 | 138 | 119 | 0.494 | 0.2562 | 0.3374 | 0.5115 | 0.0266 |
| single:gemma2:9b | 1039 | 278 | 599 | 162 | 140 | 138 | 378 | 221 | 0.5036 | 0.3878 | 0.4382 | 0.5602 | 0.1273 |
| single:llama3.1:8b | 1039 | 334 | 686 | 19 | 157 | 177 | 400 | 286 | 0.4701 | 0.3544 | 0.4041 | 0.5238 | 0.0503 |
| single:mistral:latest | 1039 | 445 | 498 | 96 | 220 | 225 | 310 | 188 | 0.4944 | 0.5392 | 0.5158 | 0.5593 | 0.1178 |
| single:phi3:medium | 1039 | 289 | 528 | 222 | 148 | 141 | 342 | 186 | 0.5121 | 0.4431 | 0.4751 | 0.5756 | 0.1555 |
| single:qwen3:8b | 1039 | 257 | 667 | 115 | 114 | 143 | 404 | 263 | 0.4436 | 0.3024 | 0.3596 | 0.5205 | 0.0449 |
| baseline:always_no | 1039 | 0 | 1039 | 0 | 0 | 0 | 587 | 452 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 1039 | 0 | 1039 | 0 | 0 | 0 | 587 | 452 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:best_single | 1039 | 289 | 528 | 222 | 148 | 141 | 342 | 186 | 0.5121 | 0.4431 | 0.4751 | 0.5756 | 0.1555 |
| baseline:extremized(a=2) | 1039 | 342 | 687 | 10 | 173 | 169 | 416 | 271 | 0.5058 | 0.3896 | 0.4402 | 0.5504 | 0.1059 |
| baseline:logit_pool | 1039 | 342 | 687 | 10 | 173 | 169 | 416 | 271 | 0.5058 | 0.3896 | 0.4402 | 0.5504 | 0.1059 |
| baseline:mean | 1039 | 342 | 671 | 26 | 172 | 170 | 409 | 262 | 0.5029 | 0.3963 | 0.4433 | 0.5514 | 0.1075 |
| baseline:median | 1039 | 292 | 588 | 159 | 144 | 148 | 371 | 217 | 0.4932 | 0.3989 | 0.441 | 0.5569 | 0.1188 |
| market | 1039 | 400 | 635 | 4 | 290 | 110 | 475 | 160 | 0.725 | 0.6444 | 0.6824 | 0.7282 | 0.4646 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | market | 1039 | 0.0841 | 0.0688 | 0.099 | council worse |
| council:chair=llama3.1:8b | baseline:best_single | 1039 | -0.0007 | -0.0095 | 0.0079 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | 1039 | 0.0029 | -0.0006 | 0.0065 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | 1039 | -0.006 | -0.0123 | 0.0003 | no clear difference |
| council:chair=llama3.1:8b | baseline:always_no | 1039 | -0.1819 | -0.2102 | -0.1528 | council better |
| council:chair=qwen3:8b | market | 1039 | 0.0926 | 0.0766 | 0.1091 | council worse |
| council:chair=qwen3:8b | baseline:best_single | 1039 | 0.0079 | -0.0022 | 0.0184 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | 1039 | 0.0115 | 0.0068 | 0.0163 | council worse |
| council:chair=qwen3:8b | baseline:logit_pool | 1039 | 0.0026 | -0.0027 | 0.0079 | no clear difference |
| council:chair=qwen3:8b | baseline:always_no | 1039 | -0.1733 | -0.2004 | -0.1439 | council better |


## Council vs baselines, by source

| source | council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|---|
| kalshi | council:chair=llama3.1:8b | market | 200 | 0.1209 | 0.0871 | 0.1568 | council worse |
| kalshi | council:chair=llama3.1:8b | baseline:best_single | 200 | -0.0085 | -0.0308 | 0.0149 | no clear difference |
| kalshi | council:chair=llama3.1:8b | baseline:mean | 200 | 0.0 | -0.0084 | 0.0089 | no clear difference |
| kalshi | council:chair=llama3.1:8b | baseline:logit_pool | 200 | -0.0092 | -0.0235 | 0.0055 | no clear difference |
| kalshi | council:chair=llama3.1:8b | baseline:always_no | 200 | -0.1942 | -0.2589 | -0.1269 | council better |
| kalshi | council:chair=qwen3:8b | market | 200 | 0.1312 | 0.0936 | 0.1711 | council worse |
| kalshi | council:chair=qwen3:8b | baseline:best_single | 200 | 0.0017 | -0.0232 | 0.0274 | no clear difference |
| kalshi | council:chair=qwen3:8b | baseline:mean | 200 | 0.0103 | -0.0009 | 0.0225 | no clear difference |
| kalshi | council:chair=qwen3:8b | baseline:logit_pool | 200 | 0.001 | -0.0095 | 0.0121 | no clear difference |
| kalshi | council:chair=qwen3:8b | baseline:always_no | 200 | -0.1839 | -0.2469 | -0.1183 | council better |
| polymarket | council:chair=llama3.1:8b | market | 839 | 0.0753 | 0.0587 | 0.0907 | council worse |
| polymarket | council:chair=llama3.1:8b | baseline:best_single | 839 | 0.0028 | -0.0071 | 0.012 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:mean | 839 | 0.0036 | -0.0002 | 0.0075 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:logit_pool | 839 | -0.0052 | -0.0124 | 0.0021 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:always_no | 839 | -0.1789 | -0.2101 | -0.1492 | council better |
| polymarket | council:chair=qwen3:8b | market | 839 | 0.0835 | 0.0652 | 0.1007 | council worse |
| polymarket | council:chair=qwen3:8b | baseline:best_single | 839 | 0.011 | 0.0 | 0.0221 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:mean | 839 | 0.0117 | 0.0065 | 0.0176 | council worse |
| polymarket | council:chair=qwen3:8b | baseline:logit_pool | 839 | 0.0029 | -0.003 | 0.0091 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:always_no | 839 | -0.1708 | -0.2014 | -0.1428 | council better |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1039 | 0.0153 | 0.008 | 0.2458 | 0.2532 |
| council:chair=qwen3:8b | 1039 | 0.0239 | 0.0084 | 0.2458 | 0.2617 |
| single:deepseek-r1:8b | 359 | 0.0516 | 0.0108 | 0.2493 | 0.2906 |
| single:gemma2:9b | 1039 | 0.0259 | 0.0117 | 0.2458 | 0.261 |
| single:llama3.1:8b | 1039 | 0.02 | 0.0086 | 0.2458 | 0.257 |
| single:mistral:latest | 1039 | 0.0403 | 0.0075 | 0.2458 | 0.2774 |
| single:phi3:medium | 1039 | 0.0196 | 0.0113 | 0.2458 | 0.2538 |
| single:qwen3:8b | 1039 | 0.06 | 0.0119 | 0.2458 | 0.2948 |
| baseline:always_no | 1039 | 0.1893 | 0.0 | 0.2458 | 0.435 |
| baseline:base_rate | 1039 | 0.0 | 0.0 | 0.2458 | 0.2458 |
| baseline:best_single | 1039 | 0.0196 | 0.0113 | 0.2458 | 0.2538 |
| baseline:extremized(a=2) | 1039 | 0.0536 | 0.0078 | 0.2458 | 0.2926 |
| baseline:logit_pool | 1039 | 0.021 | 0.0085 | 0.2458 | 0.2592 |
| baseline:mean | 1039 | 0.0137 | 0.0083 | 0.2458 | 0.2503 |
| baseline:median | 1039 | 0.0204 | 0.0103 | 0.2458 | 0.2568 |
| market | 1039 | 0.0083 | 0.0826 | 0.2458 | 0.1691 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1039 | 0.0829 | 0.2462 | 0.2579 | 0.2553 |
| council:chair=qwen3:8b | 1039 | 0.0496 | 0.25 | 0.2656 | 0.2696 |
