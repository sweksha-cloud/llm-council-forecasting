# Results: contamination

Resolved questions scored: **146** (set: contamination). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 146 | 146 | 1.0 | 0.1884 | 0.6218 | 0.6918 | 0.0873 | 0.2226 | 0.7428 | 0.6469 | 0.2986 | 0.1884 | 146 | 0.1884 | 0.6218 | 0.6918 | 0.7428 | -1.2637 | 146 | -1.2643 | -2.1708 | -0.7277 |
| council:chair=qwen3:8b | 146 | 146 | 1.0 | 0.1884 | 0.6992 | 0.7021 | 0.0957 | 0.261 | 0.7554 | 0.6398 | 0.3042 | 0.1884 | 146 | 0.1884 | 0.6992 | 0.7021 | 0.7554 | -1.2637 | 146 | -1.2636 | -2.1675 | -0.7231 |
| single:deepseek-r1:8b | 146 | 146 | 1.0 | 0.2122 | 0.6989 | 0.6747 | 0.1409 | 0.3101 | 0.707 | 0.5812 | 0.195 | 0.2122 | 146 | 0.2122 | 0.6989 | 0.6747 | 0.707 | -1.5497 | 146 | -1.55 | -2.5468 | -0.9407 |
| single:gemma2:9b | 146 | 146 | 1.0 | 0.1744 | 0.5106 | 0.7329 | 0.0881 | 0.2674 | 0.7933 | 0.6727 | 0.3718 | 0.1744 | 146 | 0.1744 | 0.5106 | 0.7329 | 0.7933 | -1.0955 | 146 | -1.0959 | -1.9524 | -0.5989 |
| single:llama3.1:8b | 146 | 146 | 1.0 | 0.2084 | 0.6289 | 0.6712 | 0.1103 | 0.2213 | 0.6876 | 0.6112 | 0.2337 | 0.2084 | 146 | 0.2084 | 0.6289 | 0.6712 | 0.6876 | -1.504 | 146 | -1.5044 | -2.6103 | -0.8353 |
| single:mistral:latest | 146 | 146 | 1.0 | 0.1994 | 0.5713 | 0.6747 | 0.1208 | 0.2655 | 0.7411 | 0.6464 | 0.2928 | 0.1994 | 146 | 0.1994 | 0.5713 | 0.6747 | 0.7411 | -1.3959 | 146 | -1.3953 | -2.274 | -0.8445 |
| single:phi3:medium | 146 | 146 | 1.0 | 0.2059 | 0.5923 | 0.6747 | 0.0866 | 0.2482 | 0.7023 | 0.5957 | 0.2206 | 0.2059 | 146 | 0.2059 | 0.5923 | 0.6747 | 0.7023 | -1.474 | 146 | -1.4744 | -2.45 | -0.9205 |
| single:qwen3:8b | 146 | 146 | 1.0 | 0.2052 | 0.7764 | 0.726 | 0.1412 | 0.3556 | 0.7352 | 0.6423 | 0.3369 | 0.2052 | 146 | 0.2052 | 0.7764 | 0.726 | 0.7352 | -1.4656 | 146 | -1.4655 | -2.3428 | -0.8444 |
| baseline:always_no | 146 | 146 | 1.0 | 0.3356 | 4.6367 | 0.6644 | 0.3356 | 0.5 | 0.5 | 0.5 | 0.0 | 0.3356 | 146 | 0.3356 | 4.6367 | 0.6644 | 0.5 | -3.0324 | 146 | -3.0326 | -4.7705 | -2.0158 |
| baseline:base_rate | 146 | 146 | 1.0 | 0.223 | 0.6381 | 0.6644 | 0.0 | 0.1644 | 0.5 | 0.5 | 0.0 | 0.223 | 146 | 0.223 | 0.6381 | 0.6644 | 0.5 | -1.6795 | 146 | -1.6792 | -2.8266 | -1.0525 |
| baseline:best_single | 146 | 146 | 1.0 | 0.1744 | 0.5106 | 0.7329 | 0.0881 | 0.2674 | 0.7933 | 0.6727 | 0.3718 | 0.1744 | 146 | 0.1744 | 0.5106 | 0.7329 | 0.7933 | -1.0955 | 146 | -1.0959 | -1.9524 | -0.5989 |
| baseline:extremized(a=2) | 146 | 146 | 1.0 | 0.208 | 0.6387 | 0.7089 | 0.172 | 0.3614 | 0.769 | 0.6364 | 0.3077 | 0.208 | 146 | 0.208 | 0.6387 | 0.7089 | 0.769 | -1.4992 | 146 | -1.4994 | -2.4084 | -0.9296 |
| baseline:logit_pool | 146 | 146 | 1.0 | 0.1812 | 0.5287 | 0.7089 | 0.0704 | 0.2599 | 0.769 | 0.6364 | 0.3077 | 0.1812 | 146 | 0.1812 | 0.5287 | 0.7089 | 0.769 | -1.1772 | 146 | -1.177 | -1.9877 | -0.6974 |
| baseline:mean | 146 | 146 | 1.0 | 0.1758 | 0.5158 | 0.7192 | 0.09 | 0.2344 | 0.7817 | 0.6496 | 0.337 | 0.1758 | 146 | 0.1758 | 0.5158 | 0.7192 | 0.7817 | -1.1123 | 146 | -1.1127 | -1.8965 | -0.6545 |
| baseline:median | 146 | 146 | 1.0 | 0.1758 | 0.5151 | 0.7158 | 0.0767 | 0.2616 | 0.7836 | 0.6416 | 0.323 | 0.1758 | 146 | 0.1758 | 0.5151 | 0.7158 | 0.7836 | -1.1123 | 146 | -1.1125 | -1.8621 | -0.6533 |
| market | 146 | 146 | 1.0 | 0.0832 | 0.2616 | 0.863 | 0.0824 | 0.3706 | 0.9572 | 0.8308 | 0.6999 | 0.0832 | 146 | 0.0832 | 0.2616 | 0.863 | 0.9572 |  |  |  |  |  |

- `baseline:mean` and the other pools use only council members: gemma2:9b, llama3.1:8b, mistral:latest, phi3:medium, qwen3:8b

- `baseline:best_single` = single:gemma2:9b (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.336 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 33.6% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 146 | 46 | 100 | 0 | 25 | 21 | 76 | 24 | 0.5435 | 0.5102 | 0.5263 | 0.6469 | 0.2986 |
| council:chair=qwen3:8b | 146 | 36 | 107 | 3 | 21 | 15 | 80 | 27 | 0.5833 | 0.4375 | 0.5 | 0.6398 | 0.3042 |
| single:deepseek-r1:8b | 146 | 27 | 116 | 3 | 14 | 13 | 83 | 33 | 0.5185 | 0.2979 | 0.3784 | 0.5812 | 0.195 |
| single:gemma2:9b | 146 | 38 | 108 | 0 | 24 | 14 | 83 | 25 | 0.6316 | 0.4898 | 0.5517 | 0.6727 | 0.3718 |
| single:llama3.1:8b | 146 | 41 | 105 | 0 | 21 | 20 | 77 | 28 | 0.5122 | 0.4286 | 0.4667 | 0.6112 | 0.2337 |
| single:mistral:latest | 146 | 47 | 92 | 7 | 25 | 22 | 70 | 22 | 0.5319 | 0.5319 | 0.5319 | 0.6464 | 0.2928 |
| single:phi3:medium | 146 | 30 | 111 | 5 | 16 | 14 | 80 | 31 | 0.5333 | 0.3404 | 0.4156 | 0.5957 | 0.2206 |
| single:qwen3:8b | 146 | 29 | 117 | 0 | 19 | 10 | 87 | 30 | 0.6552 | 0.3878 | 0.4872 | 0.6423 | 0.3369 |
| baseline:always_no | 146 | 0 | 146 | 0 | 0 | 0 | 97 | 49 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 146 | 0 | 146 | 0 | 0 | 0 | 97 | 49 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:best_single | 146 | 38 | 108 | 0 | 24 | 14 | 83 | 25 | 0.6316 | 0.4898 | 0.5517 | 0.6727 | 0.3718 |
| baseline:extremized(a=2) | 146 | 33 | 112 | 1 | 20 | 13 | 83 | 29 | 0.6061 | 0.4082 | 0.4878 | 0.6364 | 0.3077 |
| baseline:logit_pool | 146 | 33 | 112 | 1 | 20 | 13 | 83 | 29 | 0.6061 | 0.4082 | 0.4878 | 0.6364 | 0.3077 |
| baseline:mean | 146 | 32 | 110 | 4 | 20 | 12 | 83 | 27 | 0.625 | 0.4255 | 0.5063 | 0.6496 | 0.337 |
| baseline:median | 146 | 32 | 113 | 1 | 20 | 12 | 84 | 29 | 0.625 | 0.4082 | 0.4938 | 0.6416 | 0.323 |
| market | 146 | 40 | 104 | 2 | 35 | 5 | 90 | 14 | 0.875 | 0.7143 | 0.7865 | 0.8308 | 0.6999 |


## Contamination: resolved before vs after each model's training cutoff

`gap` = Brier before − Brier after (negative = better on questions the model might remember), with a 95% bootstrap interval. `excess_gap` subtracts the market's own before−after gap, so it allows for the older questions being easier; clearly negative points to recall. Cutoffs: `scoring/contamination.py` (stated cutoff, else release date; councils use their latest member).

| setup | cutoff | basis | n_before | brier_before | accuracy_before | market_brier_before | n_after | brier_after | accuracy_after | market_brier_after | gap | gap_ci_low | gap_ci_high | excess_gap | excess_ci_low | excess_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| single:llama3.1:8b | 2023-12-31 | stated cutoff | 102 | 0.2588 | 0.5784 | 0.1119 | 44 | 0.0917 | 0.8864 | 0.0167 | 0.1671 | 0.1094 | 0.2211 | 0.0719 | 0.0089 | 0.1314 |
| single:mistral:latest | 2024-05-22 | release date | 146 | 0.1994 | 0.6747 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| single:qwen3:8b | 2025-04-29 | release date | 146 | 0.2052 | 0.726 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| single:gemma2:9b | 2024-06-27 | release date | 146 | 0.1744 | 0.7329 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| single:phi3:medium | 2023-10-31 | stated cutoff | 61 | 0.243 | 0.6066 | 0.1115 | 85 | 0.1793 | 0.7235 | 0.0629 | 0.0637 | -0.0187 | 0.1394 | 0.0151 | -0.0553 | 0.0873 |
| council:chair=llama3.1:8b | 2025-04-29 | latest member (release date) | 146 | 0.1884 | 0.6918 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| council:chair=qwen3:8b | 2025-04-29 | latest member (release date) | 146 | 0.1884 | 0.7021 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| single:deepseek-r1:8b | 2025-05-28 | release date | 146 | 0.2122 | 0.6747 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| baseline:mean | 2025-05-28 | latest member (release date) | 146 | 0.1758 | 0.7192 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| baseline:median | 2025-05-28 | latest member (release date) | 146 | 0.1758 | 0.7158 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| baseline:logit_pool | 2025-05-28 | latest member (release date) | 146 | 0.1812 | 0.7089 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |
| baseline:extremized(a=2) | 2025-05-28 | latest member (release date) | 146 | 0.208 | 0.7089 | 0.0832 | 0 |  |  |  |  |  |  |  |  |  |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | market | 146 | 0.1052 | 0.0751 | 0.1357 | council worse |
| council:chair=llama3.1:8b | baseline:best_single | 146 | 0.014 | -0.0071 | 0.0373 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | 146 | 0.0126 | -0.0007 | 0.0297 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | 146 | 0.0073 | -0.0084 | 0.0218 | no clear difference |
| council:chair=llama3.1:8b | baseline:always_no | 146 | -0.1472 | -0.2176 | -0.0781 | council better |
| council:chair=qwen3:8b | market | 146 | 0.1052 | 0.0725 | 0.1396 | council worse |
| council:chair=qwen3:8b | baseline:best_single | 146 | 0.014 | -0.0142 | 0.0462 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | 146 | 0.0126 | -0.0035 | 0.0333 | no clear difference |
| council:chair=qwen3:8b | baseline:logit_pool | 146 | 0.0072 | -0.0074 | 0.0231 | no clear difference |
| council:chair=qwen3:8b | baseline:always_no | 146 | -0.1472 | -0.2199 | -0.0782 | council better |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 146 | 0.013 | 0.0492 | 0.223 | 0.1884 |
| council:chair=qwen3:8b | 146 | 0.0188 | 0.0553 | 0.223 | 0.1884 |
| single:deepseek-r1:8b | 146 | 0.0268 | 0.0349 | 0.223 | 0.2122 |
| single:gemma2:9b | 146 | 0.014 | 0.0657 | 0.223 | 0.1744 |
| single:llama3.1:8b | 146 | 0.0272 | 0.0398 | 0.223 | 0.2084 |
| single:mistral:latest | 146 | 0.0245 | 0.0477 | 0.223 | 0.1994 |
| single:phi3:medium | 146 | 0.0211 | 0.0362 | 0.223 | 0.2059 |
| single:qwen3:8b | 146 | 0.0279 | 0.0457 | 0.223 | 0.2052 |
| baseline:always_no | 146 | 0.1126 | 0.0 | 0.223 | 0.3356 |
| baseline:base_rate | 146 | 0.0 | 0.0 | 0.223 | 0.223 |
| baseline:best_single | 146 | 0.014 | 0.0657 | 0.223 | 0.1744 |
| baseline:extremized(a=2) | 146 | 0.0365 | 0.0455 | 0.223 | 0.208 |
| baseline:logit_pool | 146 | 0.0087 | 0.0463 | 0.223 | 0.1812 |
| baseline:mean | 146 | 0.0116 | 0.0579 | 0.223 | 0.1758 |
| baseline:median | 146 | 0.0089 | 0.054 | 0.223 | 0.1758 |
| market | 146 | 0.014 | 0.1528 | 0.223 | 0.0832 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 146 | 0.5212 | 0.088 | 0.2478 | 0.2276 |
| council:chair=qwen3:8b | 146 | 0.4779 | 0.0843 | 0.2572 | 0.2216 |
