# Results: live-no-in-play

Resolved questions scored: **136** (set: live). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 136 | 37 | 0.272 | 0.2947 | 0.7922 | 0.4324 | 0.2507 | 0.1647 | 0.4631 | 0.4744 | -0.0513 | 0.2622 | 37 | 0.2947 | 0.7922 | 0.4324 | 0.4631 | -2.6569 | 37 | -2.6567 | -5.3938 | -1.3256 |
| council:chair=qwen3:8b | 136 | 37 | 0.272 | 0.2956 | 0.7936 | 0.5 | 0.2589 | 0.187 | 0.4776 | 0.5251 | 0.0489 | 0.2624 | 37 | 0.2956 | 0.7936 | 0.5 | 0.4776 | -2.6681 | 37 | -2.6678 | -5.6182 | -1.295 |
| single:gemma2:9b | 136 | 37 | 0.272 | 0.3001 | 0.8167 | 0.4595 | 0.2727 | 0.1646 | 0.4054 | 0.3965 | -0.2172 | 0.2636 | 37 | 0.3001 | 0.8167 | 0.4595 | 0.4054 | -2.7239 | 37 | -2.7234 | -5.2195 | -1.4806 |
| single:llama3.1:8b | 136 | 37 | 0.272 | 0.2976 | 0.9215 | 0.473 | 0.24 | 0.1535 | 0.484 | 0.4835 | -0.0323 | 0.2629 | 37 | 0.2976 | 0.9215 | 0.473 | 0.484 | -2.6929 | 37 | -2.6925 | -5.3479 | -1.3724 |
| single:mistral:latest | 136 | 37 | 0.272 | 0.3411 | 0.9153 | 0.4459 | 0.3181 | 0.2235 | 0.3942 | 0.4816 | -0.0368 | 0.2748 | 37 | 0.3411 | 0.9153 | 0.4459 | 0.3942 | -3.2327 | 37 | -3.2324 | -6.4492 | -1.6354 |
| single:phi3:medium | 136 | 37 | 0.272 | 0.2637 | 0.751 | 0.6081 | 0.25 | 0.1743 | 0.5978 | 0.6746 | 0.3208 | 0.2537 | 37 | 0.2637 | 0.751 | 0.6081 | 0.5978 | -2.2722 | 37 | -2.2724 | -5.0486 | -0.9055 |
| single:qwen3:8b | 136 | 37 | 0.272 | 0.3216 | 0.9703 | 0.5811 | 0.2884 | 0.2749 | 0.5513 | 0.5871 | 0.1668 | 0.2695 | 37 | 0.3216 | 0.9703 | 0.5811 | 0.5513 | -2.9907 | 37 | -2.9911 | -6.012 | -1.295 |
| baseline:always_no | 136 | 136 | 1.0 | 0.4559 | 6.2982 | 0.5441 | 0.4559 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4559 | 37 | 0.3514 | 4.8541 | 0.6486 | 0.5 | -3.3605 | 136 | -1.9059 | -2.6287 | -1.3254 |
| baseline:base_rate | 136 | 136 | 1.0 | 0.2481 | 0.6892 | 0.5441 | 0.0 | 0.0441 | 0.5 | 0.5 | 0.0 | 0.2481 | 37 | 0.2388 | 0.6708 | 0.6486 | 0.5 | -1.9632 | 136 | -0.5812 | -0.8935 | -0.3233 |
| baseline:best_single | 136 | 37 | 0.272 | 0.2637 | 0.751 | 0.6081 | 0.25 | 0.1743 | 0.5978 | 0.6746 | 0.3208 | 0.2537 | 37 | 0.2637 | 0.751 | 0.6081 | 0.5978 | -2.2722 | 37 | -2.2724 | -5.0486 | -0.9055 |
| baseline:extremized(a=2) | 136 | 37 | 0.272 | 0.3557 | 1.0787 | 0.5135 | 0.3771 | 0.2785 | 0.4872 | 0.5192 | 0.0367 | 0.2788 | 37 | 0.3557 | 1.0787 | 0.5135 | 0.4872 | -3.4138 | 37 | -3.4139 | -6.9636 | -1.6516 |
| baseline:logit_pool | 136 | 37 | 0.272 | 0.2958 | 0.7995 | 0.5135 | 0.2833 | 0.186 | 0.4872 | 0.5192 | 0.0367 | 0.2625 | 37 | 0.2958 | 0.7995 | 0.5135 | 0.4872 | -2.6705 | 37 | -2.6706 | -5.4004 | -1.3218 |
| baseline:mean | 136 | 37 | 0.272 | 0.282 | 0.7612 | 0.4865 | 0.2175 | 0.1604 | 0.4728 | 0.4984 | -0.0031 | 0.2587 | 37 | 0.282 | 0.7612 | 0.4865 | 0.4728 | -2.4993 | 37 | -2.4992 | -5.0565 | -1.2365 |
| baseline:median | 136 | 37 | 0.272 | 0.2836 | 0.7742 | 0.5135 | 0.2343 | 0.1803 | 0.4872 | 0.5192 | 0.0372 | 0.2591 | 37 | 0.2836 | 0.7742 | 0.5135 | 0.4872 | -2.5191 | 37 | -2.5187 | -5.1335 | -1.2137 |
| market | 136 | 136 | 1.0 | 0.1569 | 0.4481 | 0.7353 | 0.0921 | 0.2632 | 0.8467 | 0.728 | 0.4641 | 0.1569 | 37 | 0.0806 | 0.2578 | 0.9189 | 0.9728 |  |  |  |  |  |

- `baseline:best_single` = single:phi3:medium (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.456 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 45.6% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 37 | 24 | 13 | 0 | 8 | 16 | 8 | 5 | 0.3333 | 0.6154 | 0.4324 | 0.4744 | -0.0513 |
| council:chair=qwen3:8b | 37 | 21 | 15 | 1 | 8 | 13 | 10 | 5 | 0.381 | 0.6154 | 0.4706 | 0.5251 | 0.0489 |
| single:gemma2:9b | 37 | 9 | 20 | 8 | 2 | 7 | 11 | 9 | 0.2222 | 0.1818 | 0.2 | 0.3965 | -0.2172 |
| single:llama3.1:8b | 37 | 19 | 15 | 3 | 7 | 12 | 9 | 6 | 0.3684 | 0.5385 | 0.4375 | 0.4835 | -0.0323 |
| single:mistral:latest | 37 | 23 | 13 | 1 | 8 | 15 | 8 | 5 | 0.3478 | 0.6154 | 0.4444 | 0.4816 | -0.0368 |
| single:phi3:medium | 37 | 16 | 14 | 7 | 7 | 9 | 12 | 2 | 0.4375 | 0.7778 | 0.56 | 0.6746 | 0.3208 |
| single:qwen3:8b | 37 | 16 | 18 | 3 | 7 | 9 | 13 | 5 | 0.4375 | 0.5833 | 0.5 | 0.5871 | 0.1668 |
| baseline:always_no | 136 | 0 | 136 | 0 | 0 | 0 | 74 | 62 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 136 | 0 | 136 | 0 | 0 | 0 | 74 | 62 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:best_single | 37 | 16 | 14 | 7 | 7 | 9 | 12 | 2 | 0.4375 | 0.7778 | 0.56 | 0.6746 | 0.3208 |
| baseline:extremized(a=2) | 37 | 19 | 18 | 0 | 7 | 12 | 12 | 6 | 0.3684 | 0.5385 | 0.4375 | 0.5192 | 0.0367 |
| baseline:logit_pool | 37 | 19 | 18 | 0 | 7 | 12 | 12 | 6 | 0.3684 | 0.5385 | 0.4375 | 0.5192 | 0.0367 |
| baseline:mean | 37 | 20 | 17 | 0 | 7 | 13 | 11 | 6 | 0.35 | 0.5385 | 0.4242 | 0.4984 | -0.0031 |
| baseline:median | 37 | 18 | 17 | 2 | 7 | 11 | 11 | 6 | 0.3889 | 0.5385 | 0.4516 | 0.5192 | 0.0372 |
| market | 136 | 54 | 82 | 0 | 40 | 14 | 60 | 22 | 0.7407 | 0.6452 | 0.6897 | 0.728 | 0.4641 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | market | 37 | 0.2141 | 0.1395 | 0.2881 | council worse |
| council:chair=llama3.1:8b | baseline:best_single | 37 | 0.031 | -0.0105 | 0.0817 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | 37 | 0.0127 | -0.0123 | 0.0391 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | 37 | -0.0011 | -0.0377 | 0.0353 | no clear difference |
| council:chair=llama3.1:8b | baseline:always_no | 37 | -0.0567 | -0.2404 | 0.1073 | no clear difference |
| council:chair=qwen3:8b | market | 37 | 0.215 | 0.1374 | 0.2931 | council worse |
| council:chair=qwen3:8b | baseline:best_single | 37 | 0.0319 | -0.0115 | 0.0812 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | 37 | 0.0136 | -0.0093 | 0.0382 | no clear difference |
| council:chair=qwen3:8b | baseline:logit_pool | 37 | -0.0002 | -0.033 | 0.0316 | no clear difference |
| council:chair=qwen3:8b | baseline:always_no | 37 | -0.0558 | -0.2365 | 0.1134 | no clear difference |


## Council vs baselines, by source

| source | council | versus | n | mean_diff | verdict |
|---|---|---|---|---|---|
| kalshi | council:chair=llama3.1:8b | market | 25 | 0.1965 | too few (< 30) |
| kalshi | council:chair=llama3.1:8b | baseline:mean | 25 | 0.0126 | too few (< 30) |
| kalshi | council:chair=llama3.1:8b | baseline:logit_pool | 25 | -0.0019 | too few (< 30) |
| kalshi | council:chair=llama3.1:8b | baseline:always_no | 25 | -0.1441 | too few (< 30) |
| kalshi | council:chair=qwen3:8b | market | 25 | 0.2025 | too few (< 30) |
| kalshi | council:chair=qwen3:8b | baseline:mean | 25 | 0.0186 | too few (< 30) |
| kalshi | council:chair=qwen3:8b | baseline:logit_pool | 25 | 0.0041 | too few (< 30) |
| kalshi | council:chair=qwen3:8b | baseline:always_no | 25 | -0.1381 | too few (< 30) |
| polymarket | council:chair=llama3.1:8b | market | 12 | 0.2507 | too few (< 30) |
| polymarket | council:chair=llama3.1:8b | baseline:mean | 12 | 0.0129 | too few (< 30) |
| polymarket | council:chair=llama3.1:8b | baseline:logit_pool | 12 | 0.0004 | too few (< 30) |
| polymarket | council:chair=llama3.1:8b | baseline:always_no | 12 | 0.1254 | too few (< 30) |
| polymarket | council:chair=qwen3:8b | market | 12 | 0.241 | too few (< 30) |
| polymarket | council:chair=qwen3:8b | baseline:mean | 12 | 0.0032 | too few (< 30) |
| polymarket | council:chair=qwen3:8b | baseline:logit_pool | 12 | -0.0092 | too few (< 30) |
| polymarket | council:chair=qwen3:8b | baseline:always_no | 12 | 0.1158 | too few (< 30) |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 37 | 0.1077 | 0.0371 | 0.2279 | 0.2947 |
| council:chair=qwen3:8b | 37 | 0.112 | 0.0408 | 0.2279 | 0.2956 |
| single:gemma2:9b | 37 | 0.1245 | 0.048 | 0.2279 | 0.3001 |
| single:llama3.1:8b | 37 | 0.1017 | 0.0284 | 0.2279 | 0.2976 |
| single:mistral:latest | 37 | 0.1742 | 0.0619 | 0.2279 | 0.3411 |
| single:phi3:medium | 37 | 0.1171 | 0.0809 | 0.2279 | 0.2637 |
| single:qwen3:8b | 37 | 0.1446 | 0.0482 | 0.2279 | 0.3216 |
| baseline:always_no | 136 | 0.2078 | 0.0 | 0.2481 | 0.4559 |
| baseline:base_rate | 136 | 0.0 | 0.0 | 0.2481 | 0.2481 |
| baseline:best_single | 37 | 0.1171 | 0.0809 | 0.2279 | 0.2637 |
| baseline:extremized(a=2) | 37 | 0.1898 | 0.0578 | 0.2279 | 0.3557 |
| baseline:logit_pool | 37 | 0.1459 | 0.0768 | 0.2279 | 0.2958 |
| baseline:mean | 37 | 0.0829 | 0.0252 | 0.2279 | 0.282 |
| baseline:median | 37 | 0.0952 | 0.042 | 0.2279 | 0.2836 |
| market | 136 | 0.0166 | 0.1093 | 0.2481 | 0.1569 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 37 | 0.2675 | 0.254 | 0.2805 | 0.3453 |
| council:chair=qwen3:8b | 37 | 0.1945 | 0.261 | 0.3014 | 0.3221 |
