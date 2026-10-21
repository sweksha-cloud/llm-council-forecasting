# Results: backtest

Resolved questions scored: **1185** (set: settled + settled-ext + contamination). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1185 | 1185 | 1.0 | 0.2452 | 0.6968 | 0.5772 | 0.0898 | 0.1692 | 0.6068 | 0.5654 | 0.131 | 0.2452 | 505 | 0.2362 | 0.6878 | 0.6059 | 0.6416 | -0.8451 | 1185 | -0.5468 | -0.6717 | -0.4295 |
| council:chair=qwen3:8b | 1185 | 1185 | 1.0 | 0.2527 | 0.7814 | 0.5806 | 0.1156 | 0.197 | 0.6075 | 0.5659 | 0.134 | 0.2527 | 505 | 0.2421 | 0.7797 | 0.6099 | 0.6456 | -0.8912 | 1185 | -0.5942 | -0.7303 | -0.4701 |
| single:deepseek-r1:8b | 1185 | 505 | 0.426 | 0.2679 | 0.8397 | 0.5683 | 0.1866 | 0.2515 | 0.6131 | 0.5332 | 0.0784 | 0.2576 | 505 | 0.2679 | 0.8397 | 0.5683 | 0.6131 | -1.0928 | 505 | -1.0928 | -1.4361 | -0.8221 |
| single:gemma2:9b | 1185 | 1185 | 1.0 | 0.2503 | 0.7139 | 0.5958 | 0.1121 | 0.1979 | 0.6195 | 0.576 | 0.1613 | 0.2503 | 505 | 0.2434 | 0.6944 | 0.6079 | 0.6473 | -0.9014 | 1185 | -0.5792 | -0.7068 | -0.4561 |
| single:llama3.1:8b | 1185 | 1185 | 1.0 | 0.251 | 0.7256 | 0.5608 | 0.1115 | 0.1719 | 0.5872 | 0.5348 | 0.0735 | 0.251 | 505 | 0.253 | 0.7403 | 0.5525 | 0.5995 | -0.9764 | 1185 | -0.5837 | -0.7262 | -0.4585 |
| single:mistral:latest | 1185 | 1185 | 1.0 | 0.2677 | 0.8163 | 0.5709 | 0.1391 | 0.2049 | 0.5841 | 0.5723 | 0.1433 | 0.2677 | 505 | 0.2522 | 0.738 | 0.599 | 0.6256 | -0.9701 | 1185 | -0.6891 | -0.8366 | -0.5437 |
| single:phi3:medium | 1185 | 1185 | 1.0 | 0.2479 | 0.7107 | 0.5903 | 0.0948 | 0.1683 | 0.6124 | 0.5809 | 0.168 | 0.2479 | 505 | 0.244 | 0.7138 | 0.601 | 0.6313 | -0.9061 | 1185 | -0.5642 | -0.6999 | -0.4513 |
| single:qwen3:8b | 1185 | 1185 | 1.0 | 0.2838 | 0.991 | 0.5751 | 0.2071 | 0.2719 | 0.594 | 0.5373 | 0.0825 | 0.2838 | 505 | 0.2655 | 0.899 | 0.603 | 0.6431 | -1.074 | 1185 | -0.7903 | -0.9405 | -0.6401 |
| baseline:always_no | 1185 | 1185 | 1.0 | 0.4228 | 5.841 | 0.5772 | 0.4228 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4228 | 505 | 0.4337 | 5.9913 | 0.5663 | 0.5 | -2.388 | 1185 | -1.6672 | -1.8983 | -1.441 |
| baseline:base_rate | 1185 | 1185 | 1.0 | 0.244 | 0.6812 | 0.5772 | 0.0 | 0.0772 | 0.5 | 0.5 | 0.0 | 0.244 | 505 | 0.2457 | 0.6846 | 0.5663 | 0.5 | -0.9193 | 1185 | -0.5395 | -0.6703 | -0.4241 |
| baseline:best_single | 1185 | 1185 | 1.0 | 0.2479 | 0.7107 | 0.5903 | 0.0948 | 0.1683 | 0.6124 | 0.5809 | 0.168 | 0.2479 | 505 | 0.244 | 0.7138 | 0.601 | 0.6313 | -0.9061 | 1185 | -0.5642 | -0.6999 | -0.4513 |
| baseline:extremized(a=2) | 1185 | 1185 | 1.0 | 0.2821 | 0.9382 | 0.5886 | 0.1991 | 0.2898 | 0.6131 | 0.5621 | 0.1315 | 0.2821 | 505 | 0.2691 | 0.8734 | 0.6129 | 0.6527 | -1.1021 | 1185 | -0.7799 | -0.9283 | -0.6289 |
| baseline:logit_pool | 1185 | 1185 | 1.0 | 0.2495 | 0.7187 | 0.5886 | 0.1084 | 0.1986 | 0.6131 | 0.5621 | 0.1315 | 0.2495 | 505 | 0.238 | 0.685 | 0.6129 | 0.6527 | -0.8592 | 1185 | -0.5743 | -0.7 | -0.4503 |
| baseline:mean | 1185 | 1185 | 1.0 | 0.2411 | 0.6791 | 0.5899 | 0.0772 | 0.1709 | 0.6182 | 0.5646 | 0.136 | 0.2411 | 505 | 0.231 | 0.6529 | 0.6149 | 0.658 | -0.8045 | 1185 | -0.521 | -0.6384 | -0.4086 |
| baseline:median | 1185 | 1185 | 1.0 | 0.2468 | 0.6976 | 0.5899 | 0.1028 | 0.1797 | 0.61 | 0.5699 | 0.1473 | 0.2468 | 505 | 0.2379 | 0.6739 | 0.6 | 0.6456 | -0.8584 | 1185 | -0.5572 | -0.6838 | -0.4395 |
| market | 1185 | 1185 | 1.0 | 0.1585 | 0.4808 | 0.7536 | 0.063 | 0.3045 | 0.8561 | 0.7411 | 0.4926 | 0.1585 | 505 | 0.128 | 0.4016 | 0.8069 | 0.9012 |  |  |  |  |  |

- `baseline:mean` and the other pools use only council members: gemma2:9b, llama3.1:8b, mistral:latest, phi3:medium, qwen3:8b

- `baseline:best_single` = single:phi3:medium (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.423 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 42.3% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1185 | 487 | 692 | 6 | 242 | 245 | 439 | 253 | 0.4969 | 0.4889 | 0.4929 | 0.5654 | 0.131 |
| council:chair=qwen3:8b | 1185 | 433 | 708 | 44 | 218 | 215 | 448 | 260 | 0.5035 | 0.4561 | 0.4786 | 0.5659 | 0.134 |
| single:deepseek-r1:8b | 505 | 110 | 373 | 22 | 55 | 55 | 221 | 152 | 0.5 | 0.2657 | 0.347 | 0.5332 | 0.0784 |
| single:gemma2:9b | 1185 | 316 | 707 | 162 | 164 | 152 | 461 | 246 | 0.519 | 0.4 | 0.4518 | 0.576 | 0.1613 |
| single:llama3.1:8b | 1185 | 375 | 791 | 19 | 178 | 197 | 477 | 314 | 0.4747 | 0.3618 | 0.4106 | 0.5348 | 0.0735 |
| single:mistral:latest | 1185 | 492 | 590 | 103 | 245 | 247 | 380 | 210 | 0.498 | 0.5385 | 0.5174 | 0.5723 | 0.1433 |
| single:phi3:medium | 1185 | 319 | 639 | 227 | 164 | 155 | 422 | 217 | 0.5141 | 0.4304 | 0.4686 | 0.5809 | 0.168 |
| single:qwen3:8b | 1185 | 286 | 784 | 115 | 133 | 153 | 491 | 293 | 0.465 | 0.3122 | 0.3736 | 0.5373 | 0.0825 |
| baseline:always_no | 1185 | 0 | 1185 | 0 | 0 | 0 | 684 | 501 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 1185 | 0 | 1185 | 0 | 0 | 0 | 684 | 501 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:best_single | 1185 | 319 | 639 | 227 | 164 | 155 | 422 | 217 | 0.5141 | 0.4304 | 0.4686 | 0.5809 | 0.168 |
| baseline:extremized(a=2) | 1185 | 375 | 799 | 11 | 193 | 182 | 499 | 300 | 0.5147 | 0.3915 | 0.4447 | 0.5621 | 0.1315 |
| baseline:logit_pool | 1185 | 375 | 799 | 11 | 193 | 182 | 499 | 300 | 0.5147 | 0.3915 | 0.4447 | 0.5621 | 0.1315 |
| baseline:mean | 1185 | 374 | 781 | 30 | 192 | 182 | 492 | 289 | 0.5134 | 0.3992 | 0.4491 | 0.5646 | 0.136 |
| baseline:median | 1185 | 324 | 701 | 160 | 164 | 160 | 455 | 246 | 0.5062 | 0.4 | 0.4469 | 0.5699 | 0.1473 |
| market | 1185 | 440 | 739 | 6 | 325 | 115 | 565 | 174 | 0.7386 | 0.6513 | 0.6922 | 0.7411 | 0.4926 |


## Contamination: resolved before vs after each model's training cutoff

`gap` = Brier before − Brier after (negative = better on questions the model might remember), with a 95% bootstrap interval. `excess_gap` subtracts the market's own before−after gap, so it allows for the older questions being easier; clearly negative points to recall. Cutoffs: `scoring/contamination.py` (stated cutoff, else release date; councils use their latest member).

| setup | cutoff | basis | n_before | brier_before | accuracy_before | market_brier_before | n_after | brier_after | accuracy_after | market_brier_after | gap | gap_ci_low | gap_ci_high | excess_gap | excess_ci_low | excess_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| single:llama3.1:8b | 2023-12-31 | stated cutoff | 102 | 0.2588 | 0.5784 | 0.1119 | 1083 | 0.2503 | 0.5591 | 0.1629 | 0.0085 | -0.0336 | 0.0551 | 0.0595 | 0.0105 | 0.1101 |
| single:mistral:latest | 2024-05-22 | release date | 146 | 0.1994 | 0.6747 | 0.0832 | 1039 | 0.2774 | 0.5563 | 0.1691 | -0.078 | -0.1139 | -0.0403 | 0.0079 | -0.0278 | 0.0427 |
| single:qwen3:8b | 2025-04-29 | release date | 146 | 0.2052 | 0.726 | 0.0832 | 1039 | 0.2948 | 0.5539 | 0.1691 | -0.0896 | -0.1406 | -0.0414 | -0.0038 | -0.0496 | 0.0418 |
| single:gemma2:9b | 2024-06-27 | release date | 146 | 0.1744 | 0.7329 | 0.0832 | 1039 | 0.261 | 0.5765 | 0.1691 | -0.0866 | -0.1216 | -0.0519 | -0.0007 | -0.0349 | 0.0314 |
| single:phi3:medium | 2023-10-31 | stated cutoff | 61 | 0.243 | 0.6066 | 0.1115 | 1124 | 0.2482 | 0.5894 | 0.1611 | -0.0052 | -0.0645 | 0.0572 | 0.0444 | -0.015 | 0.1008 |
| council:chair=llama3.1:8b | 2025-04-29 | latest member (release date) | 146 | 0.1884 | 0.6918 | 0.0832 | 1039 | 0.2532 | 0.5611 | 0.1691 | -0.0647 | -0.0963 | -0.0338 | 0.0212 | -0.0125 | 0.0537 |
| council:chair=qwen3:8b | 2025-04-29 | latest member (release date) | 146 | 0.1884 | 0.7021 | 0.0832 | 1039 | 0.2617 | 0.5635 | 0.1691 | -0.0733 | -0.1101 | -0.0366 | 0.0125 | -0.0248 | 0.0482 |
| single:deepseek-r1:8b | 2025-05-28 | release date | 146 | 0.2122 | 0.6747 | 0.0832 | 359 | 0.2906 | 0.5251 | 0.1462 | -0.0783 | -0.1305 | -0.0275 | -0.0153 | -0.0671 | 0.0326 |
| baseline:mean | 2025-04-29 | latest member (release date) | 146 | 0.1758 | 0.7192 | 0.0832 | 1039 | 0.2503 | 0.5717 | 0.1691 | -0.0744 | -0.1054 | -0.0433 | 0.0114 | -0.0174 | 0.0389 |
| baseline:median | 2025-04-29 | latest member (release date) | 146 | 0.1758 | 0.7158 | 0.0832 | 1039 | 0.2568 | 0.5722 | 0.1691 | -0.081 | -0.117 | -0.0453 | 0.0049 | -0.0273 | 0.0352 |
| baseline:logit_pool | 2025-04-29 | latest member (release date) | 146 | 0.1812 | 0.7089 | 0.0832 | 1039 | 0.2592 | 0.5717 | 0.1691 | -0.078 | -0.1112 | -0.0431 | 0.0079 | -0.0246 | 0.0406 |
| baseline:extremized(a=2) | 2025-04-29 | latest member (release date) | 146 | 0.208 | 0.7089 | 0.0832 | 1039 | 0.2926 | 0.5717 | 0.1691 | -0.0845 | -0.1333 | -0.0339 | 0.0013 | -0.0438 | 0.0451 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | market | 1185 | 0.0867 | 0.0725 | 0.1001 | council worse |
| council:chair=llama3.1:8b | baseline:best_single | 1185 | -0.0028 | -0.0107 | 0.0049 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | 1185 | 0.0041 | 0.0003 | 0.0077 | council worse |
| council:chair=llama3.1:8b | baseline:logit_pool | 1185 | -0.0044 | -0.0104 | 0.0019 | no clear difference |
| council:chair=llama3.1:8b | baseline:always_no | 1185 | -0.1776 | -0.2021 | -0.1502 | council better |
| council:chair=qwen3:8b | market | 1185 | 0.0942 | 0.0787 | 0.1087 | council worse |
| council:chair=qwen3:8b | baseline:best_single | 1185 | 0.0048 | -0.0049 | 0.0139 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | 1185 | 0.0116 | 0.007 | 0.0166 | council worse |
| council:chair=qwen3:8b | baseline:logit_pool | 1185 | 0.0032 | -0.0018 | 0.008 | no clear difference |
| council:chair=qwen3:8b | baseline:always_no | 1185 | -0.1701 | -0.1944 | -0.1444 | council better |


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
| polymarket | council:chair=llama3.1:8b | market | 985 | 0.0797 | 0.0657 | 0.0938 | council worse |
| polymarket | council:chair=llama3.1:8b | baseline:best_single | 985 | -0.0002 | -0.0089 | 0.0084 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:mean | 985 | 0.0049 | 0.0008 | 0.0089 | council worse |
| polymarket | council:chair=llama3.1:8b | baseline:logit_pool | 985 | -0.0034 | -0.0097 | 0.0032 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:always_no | 985 | -0.1742 | -0.2028 | -0.1447 | council better |
| polymarket | council:chair=qwen3:8b | market | 985 | 0.0867 | 0.0712 | 0.102 | council worse |
| polymarket | council:chair=qwen3:8b | baseline:best_single | 985 | 0.0068 | -0.0032 | 0.0167 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:mean | 985 | 0.0119 | 0.0071 | 0.017 | council worse |
| polymarket | council:chair=qwen3:8b | baseline:logit_pool | 985 | 0.0036 | -0.002 | 0.0089 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:always_no | 985 | -0.1673 | -0.1963 | -0.1382 | council better |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1185 | 0.0122 | 0.0112 | 0.244 | 0.2452 |
| council:chair=qwen3:8b | 1185 | 0.0195 | 0.0114 | 0.244 | 0.2527 |
| single:deepseek-r1:8b | 505 | 0.0389 | 0.0162 | 0.2456 | 0.2679 |
| single:gemma2:9b | 1185 | 0.0194 | 0.0143 | 0.244 | 0.2503 |
| single:llama3.1:8b | 1185 | 0.0172 | 0.0098 | 0.244 | 0.251 |
| single:mistral:latest | 1185 | 0.0331 | 0.0081 | 0.244 | 0.2677 |
| single:phi3:medium | 1185 | 0.0165 | 0.0122 | 0.244 | 0.2479 |
| single:qwen3:8b | 1185 | 0.0531 | 0.0142 | 0.244 | 0.2838 |
| baseline:always_no | 1185 | 0.1787 | 0.0 | 0.244 | 0.4228 |
| baseline:base_rate | 1185 | 0.0 | 0.0 | 0.244 | 0.244 |
| baseline:best_single | 1185 | 0.0165 | 0.0122 | 0.244 | 0.2479 |
| baseline:extremized(a=2) | 1185 | 0.0485 | 0.0104 | 0.244 | 0.2821 |
| baseline:logit_pool | 1185 | 0.0168 | 0.0115 | 0.244 | 0.2495 |
| baseline:mean | 1185 | 0.0103 | 0.0122 | 0.244 | 0.2411 |
| baseline:median | 1185 | 0.0165 | 0.0142 | 0.244 | 0.2468 |
| market | 1185 | 0.0075 | 0.0909 | 0.244 | 0.1585 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1185 | 0.1305 | 0.2265 | 0.2593 | 0.2497 |
| council:chair=qwen3:8b | 1185 | 0.0936 | 0.23 | 0.2668 | 0.2613 |
