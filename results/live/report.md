# Results: live

Resolved questions scored: **496** (set: live). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 496 | 260 | 0.524 | 0.2254 | 0.6395 | 0.6135 | 0.15 | 0.1434 | 0.7008 | 0.6496 | 0.2879 | 0.2371 | 260 | 0.2254 | 0.6395 | 0.6135 | 0.7008 | -2.2113 | 260 | -2.2115 | -3.216 | -1.5315 |
| council:chair=qwen3:8b | 496 | 260 | 0.524 | 0.2188 | 0.6245 | 0.6423 | 0.1338 | 0.1601 | 0.7112 | 0.6729 | 0.331 | 0.2337 | 260 | 0.2188 | 0.6245 | 0.6423 | 0.7112 | -2.1173 | 260 | -2.1179 | -3.1327 | -1.4785 |
| single:gemma2:9b | 496 | 260 | 0.524 | 0.2195 | 0.624 | 0.6308 | 0.1014 | 0.1823 | 0.6783 | 0.6324 | 0.2545 | 0.234 | 260 | 0.2195 | 0.624 | 0.6308 | 0.6783 | -2.1273 | 260 | -2.1267 | -3.1627 | -1.4527 |
| single:llama3.1:8b | 496 | 260 | 0.524 | 0.233 | 0.679 | 0.6212 | 0.1282 | 0.146 | 0.6476 | 0.6508 | 0.2877 | 0.2411 | 260 | 0.233 | 0.679 | 0.6212 | 0.6476 | -2.3196 | 260 | -2.3198 | -3.3708 | -1.6197 |
| single:mistral:latest | 496 | 260 | 0.524 | 0.2449 | 0.6864 | 0.5808 | 0.1548 | 0.1729 | 0.6344 | 0.6398 | 0.274 | 0.2473 | 260 | 0.2449 | 0.6864 | 0.5808 | 0.6344 | -2.4892 | 260 | -2.4898 | -3.6514 | -1.7533 |
| single:phi3:medium | 496 | 260 | 0.524 | 0.2223 | 0.6396 | 0.6596 | 0.1401 | 0.1502 | 0.7111 | 0.7166 | 0.4047 | 0.2355 | 260 | 0.2223 | 0.6396 | 0.6596 | 0.7111 | -2.1672 | 260 | -2.1666 | -3.2268 | -1.4683 |
| single:qwen3:8b | 496 | 260 | 0.524 | 0.2336 | 0.7259 | 0.6308 | 0.12 | 0.2469 | 0.6568 | 0.6024 | 0.2023 | 0.2414 | 260 | 0.2336 | 0.7259 | 0.6308 | 0.6568 | -2.3282 | 260 | -2.3275 | -3.3604 | -1.6263 |
| baseline:always_no | 496 | 496 | 1.0 | 0.4133 | 5.71 | 0.5867 | 0.4133 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4133 | 260 | 0.3462 | 4.7823 | 0.6538 | 0.5 | -3.9324 | 496 | -2.5124 | -3.1083 | -2.0395 |
| baseline:base_rate | 496 | 496 | 1.0 | 0.2425 | 0.678 | 0.5867 | 0.0 | 0.0867 | 0.5 | 0.5 | 0.0 | 0.2425 | 260 | 0.2308 | 0.6545 | 0.6538 | 0.5 | -2.2883 | 496 | -1.0607 | -1.3873 | -0.8188 |
| baseline:best_single | 496 | 260 | 0.524 | 0.2195 | 0.624 | 0.6308 | 0.1014 | 0.1823 | 0.6783 | 0.6324 | 0.2545 | 0.234 | 260 | 0.2195 | 0.624 | 0.6308 | 0.6783 | -2.1273 | 260 | -2.1267 | -3.1627 | -1.4527 |
| baseline:extremized(a=2) | 496 | 260 | 0.524 | 0.2171 | 0.6647 | 0.675 | 0.1246 | 0.2423 | 0.7212 | 0.6807 | 0.3443 | 0.2328 | 260 | 0.2171 | 0.6647 | 0.675 | 0.7212 | -2.0931 | 260 | -2.093 | -3.0654 | -1.4293 |
| baseline:logit_pool | 496 | 260 | 0.524 | 0.2114 | 0.6138 | 0.675 | 0.1038 | 0.1539 | 0.7212 | 0.6807 | 0.3443 | 0.2298 | 260 | 0.2114 | 0.6138 | 0.675 | 0.7212 | -2.0119 | 260 | -2.0126 | -2.9742 | -1.3985 |
| baseline:mean | 496 | 260 | 0.524 | 0.2105 | 0.6064 | 0.6731 | 0.114 | 0.1377 | 0.7212 | 0.6847 | 0.3507 | 0.2293 | 260 | 0.2105 | 0.6064 | 0.6731 | 0.7212 | -1.9991 | 260 | -1.9991 | -2.9582 | -1.3972 |
| baseline:median | 496 | 260 | 0.524 | 0.2143 | 0.6177 | 0.6596 | 0.1112 | 0.155 | 0.7054 | 0.6891 | 0.3574 | 0.2313 | 260 | 0.2143 | 0.6177 | 0.6596 | 0.7054 | -2.0532 | 260 | -2.0533 | -3.0314 | -1.4184 |
| market | 496 | 496 | 1.0 | 0.1177 | 0.3514 | 0.8165 | 0.0502 | 0.3263 | 0.9175 | 0.807 | 0.6215 | 0.1177 | 260 | 0.0702 | 0.2308 | 0.9038 | 0.9687 |  |  |  |  |  |

- `baseline:best_single` = single:gemma2:9b (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.413 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 41.3% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 260 | 148 | 111 | 1 | 69 | 79 | 90 | 21 | 0.4662 | 0.7667 | 0.5798 | 0.6496 | 0.2879 |
| council:chair=qwen3:8b | 260 | 137 | 117 | 6 | 68 | 69 | 96 | 21 | 0.4964 | 0.764 | 0.6018 | 0.6729 | 0.331 |
| single:gemma2:9b | 260 | 103 | 137 | 20 | 50 | 53 | 104 | 33 | 0.4854 | 0.6024 | 0.5376 | 0.6324 | 0.2545 |
| single:llama3.1:8b | 260 | 138 | 117 | 5 | 65 | 73 | 94 | 23 | 0.471 | 0.7386 | 0.5752 | 0.6508 | 0.2877 |
| single:mistral:latest | 260 | 145 | 89 | 26 | 65 | 80 | 73 | 16 | 0.4483 | 0.8025 | 0.5752 | 0.6398 | 0.274 |
| single:phi3:medium | 260 | 105 | 110 | 45 | 54 | 51 | 95 | 15 | 0.5143 | 0.7826 | 0.6207 | 0.7166 | 0.4047 |
| single:qwen3:8b | 260 | 93 | 161 | 6 | 44 | 49 | 117 | 44 | 0.4731 | 0.5 | 0.4862 | 0.6024 | 0.2023 |
| baseline:always_no | 496 | 0 | 496 | 0 | 0 | 0 | 291 | 205 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 496 | 0 | 496 | 0 | 0 | 0 | 291 | 205 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:best_single | 260 | 103 | 137 | 20 | 50 | 53 | 104 | 33 | 0.4854 | 0.6024 | 0.5376 | 0.6324 | 0.2545 |
| baseline:extremized(a=2) | 260 | 119 | 140 | 1 | 62 | 57 | 113 | 27 | 0.521 | 0.6966 | 0.5962 | 0.6807 | 0.3443 |
| baseline:logit_pool | 260 | 119 | 140 | 1 | 62 | 57 | 113 | 27 | 0.521 | 0.6966 | 0.5962 | 0.6807 | 0.3443 |
| baseline:mean | 260 | 120 | 136 | 4 | 62 | 58 | 111 | 25 | 0.5167 | 0.7126 | 0.599 | 0.6847 | 0.3507 |
| baseline:median | 260 | 118 | 123 | 19 | 60 | 58 | 102 | 21 | 0.5085 | 0.7407 | 0.603 | 0.6891 | 0.3574 |
| market | 496 | 190 | 304 | 2 | 152 | 38 | 252 | 52 | 0.8 | 0.7451 | 0.7716 | 0.807 | 0.6215 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | market | 260 | 0.1552 | 0.1327 | 0.1776 | council worse |
| council:chair=llama3.1:8b | baseline:best_single | 260 | 0.006 | -0.012 | 0.0241 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | 260 | 0.0149 | 0.0075 | 0.0224 | council worse |
| council:chair=llama3.1:8b | baseline:logit_pool | 260 | 0.014 | 0.0053 | 0.0227 | council worse |
| council:chair=llama3.1:8b | baseline:always_no | 260 | -0.1207 | -0.1791 | -0.0598 | council better |
| council:chair=qwen3:8b | market | 260 | 0.1487 | 0.124 | 0.1739 | council worse |
| council:chair=qwen3:8b | baseline:best_single | 260 | -0.0006 | -0.0185 | 0.0173 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | 260 | 0.0083 | 0.0007 | 0.0158 | council worse |
| council:chair=qwen3:8b | baseline:logit_pool | 260 | 0.0074 | -0.001 | 0.015 | no clear difference |
| council:chair=qwen3:8b | baseline:always_no | 260 | -0.1273 | -0.1874 | -0.0664 | council better |


## Council vs baselines, by source

| source | council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|---|
| kalshi | council:chair=llama3.1:8b | market | 101 | 0.151 | 0.1119 | 0.1908 | council worse |
| kalshi | council:chair=llama3.1:8b | baseline:best_single | 101 | 0.0391 | 0.004 | 0.0725 | council worse |
| kalshi | council:chair=llama3.1:8b | baseline:mean | 101 | 0.0229 | 0.0095 | 0.0375 | council worse |
| kalshi | council:chair=llama3.1:8b | baseline:logit_pool | 101 | 0.0197 | 0.0035 | 0.0357 | council worse |
| kalshi | council:chair=llama3.1:8b | baseline:always_no | 101 | -0.0566 | -0.1512 | 0.034 | no clear difference |
| kalshi | council:chair=qwen3:8b | market | 101 | 0.1429 | 0.101 | 0.1852 | council worse |
| kalshi | council:chair=qwen3:8b | baseline:best_single | 101 | 0.031 | -0.0025 | 0.0682 | no clear difference |
| kalshi | council:chair=qwen3:8b | baseline:mean | 101 | 0.0148 | 0.0004 | 0.031 | council worse |
| kalshi | council:chair=qwen3:8b | baseline:logit_pool | 101 | 0.0116 | -0.0022 | 0.0246 | no clear difference |
| kalshi | council:chair=qwen3:8b | baseline:always_no | 101 | -0.0647 | -0.1578 | 0.0266 | no clear difference |
| polymarket | council:chair=llama3.1:8b | market | 159 | 0.1579 | 0.1304 | 0.1822 | council worse |
| polymarket | council:chair=llama3.1:8b | baseline:best_single | 159 | 0.0028 | -0.016 | 0.0216 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:mean | 159 | 0.0099 | 0.0026 | 0.0177 | council worse |
| polymarket | council:chair=llama3.1:8b | baseline:logit_pool | 159 | 0.0103 | 0.0002 | 0.0201 | council worse |
| polymarket | council:chair=llama3.1:8b | baseline:always_no | 159 | -0.1615 | -0.2444 | -0.0849 | council better |
| polymarket | council:chair=qwen3:8b | market | 159 | 0.1523 | 0.1244 | 0.1781 | council worse |
| polymarket | council:chair=qwen3:8b | baseline:best_single | 159 | -0.0028 | -0.0222 | 0.015 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:mean | 159 | 0.0042 | -0.0039 | 0.0122 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:logit_pool | 159 | 0.0047 | -0.0059 | 0.0137 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:always_no | 159 | -0.1671 | -0.2506 | -0.0899 | council better |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 260 | 0.0256 | 0.0237 | 0.2263 | 0.2254 |
| council:chair=qwen3:8b | 260 | 0.022 | 0.0301 | 0.2263 | 0.2188 |
| single:gemma2:9b | 260 | 0.0216 | 0.0272 | 0.2263 | 0.2195 |
| single:llama3.1:8b | 260 | 0.0277 | 0.0215 | 0.2263 | 0.233 |
| single:mistral:latest | 260 | 0.0399 | 0.0173 | 0.2263 | 0.2449 |
| single:phi3:medium | 260 | 0.0314 | 0.0356 | 0.2263 | 0.2223 |
| single:qwen3:8b | 260 | 0.028 | 0.0204 | 0.2263 | 0.2336 |
| baseline:always_no | 496 | 0.1708 | 0.0 | 0.2425 | 0.4133 |
| baseline:base_rate | 496 | 0.0 | 0.0 | 0.2425 | 0.2425 |
| baseline:best_single | 260 | 0.0216 | 0.0272 | 0.2263 | 0.2195 |
| baseline:extremized(a=2) | 260 | 0.0252 | 0.0337 | 0.2263 | 0.2171 |
| baseline:logit_pool | 260 | 0.018 | 0.0317 | 0.2263 | 0.2114 |
| baseline:mean | 260 | 0.0183 | 0.0328 | 0.2263 | 0.2105 |
| baseline:median | 260 | 0.0206 | 0.0324 | 0.2263 | 0.2143 |
| market | 496 | 0.0038 | 0.1283 | 0.2425 | 0.1177 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 260 | 0.1548 | 0.1894 | 0.2384 | 0.248 |
| council:chair=qwen3:8b | 260 | 0.1179 | 0.1858 | 0.2307 | 0.2396 |
