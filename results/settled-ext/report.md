# Results: settled-ext

Resolved questions scored: **680** (set: settled-ext). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 680 | 680 | 1.0 | 0.2519 | 0.7036 | 0.5559 | 0.1065 | 0.1638 | 0.5791 | 0.5403 | 0.081 | 0.2519 | 680 | 0.2519 | 0.7036 | 0.5559 | 0.5791 | -0.3904 | 680 | -0.3902 | -0.5199 | -0.2757 |
| council:chair=qwen3:8b | 680 | 680 | 1.0 | 0.2606 | 0.7826 | 0.5588 | 0.135 | 0.1909 | 0.577 | 0.5397 | 0.0811 | 0.2606 | 680 | 0.2606 | 0.7826 | 0.5588 | 0.577 | -0.4385 | 680 | -0.4384 | -0.5812 | -0.3105 |
| single:gemma2:9b | 680 | 680 | 1.0 | 0.2555 | 0.7283 | 0.5868 | 0.1107 | 0.1898 | 0.5981 | 0.562 | 0.1324 | 0.2555 | 680 | 0.2555 | 0.7283 | 0.5868 | 0.5981 | -0.4103 | 680 | -0.4101 | -0.5371 | -0.2952 |
| single:llama3.1:8b | 680 | 680 | 1.0 | 0.2496 | 0.7147 | 0.5669 | 0.0926 | 0.1603 | 0.5786 | 0.5347 | 0.0744 | 0.2496 | 680 | 0.2496 | 0.7147 | 0.5669 | 0.5786 | -0.3777 | 680 | -0.3777 | -0.5133 | -0.2627 |
| single:mistral:latest | 680 | 680 | 1.0 | 0.2793 | 0.8745 | 0.55 | 0.159 | 0.2002 | 0.5536 | 0.55 | 0.0988 | 0.2793 | 680 | 0.2793 | 0.8745 | 0.55 | 0.5536 | -0.5417 | 680 | -0.5416 | -0.708 | -0.3968 |
| single:phi3:medium | 680 | 680 | 1.0 | 0.2508 | 0.7084 | 0.5824 | 0.099 | 0.1641 | 0.5979 | 0.5697 | 0.1449 | 0.2508 | 680 | 0.2508 | 0.7084 | 0.5824 | 0.5979 | -0.3844 | 680 | -0.3846 | -0.5036 | -0.2701 |
| single:qwen3:8b | 680 | 680 | 1.0 | 0.2974 | 1.0593 | 0.5544 | 0.2181 | 0.267 | 0.5555 | 0.5111 | 0.0252 | 0.2974 | 680 | 0.2974 | 1.0593 | 0.5544 | 0.5555 | -0.6416 | 680 | -0.6416 | -0.8174 | -0.4901 |
| baseline:always_no | 680 | 680 | 1.0 | 0.4147 | 5.7294 | 0.5853 | 0.4147 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4147 | 680 | 0.4147 | 5.7294 | 0.5853 | 0.5 | -1.2891 | 680 | -1.2891 | -1.5352 | -1.0635 |
| baseline:base_rate | 680 | 680 | 1.0 | 0.2427 | 0.6785 | 0.5853 | 0.0 | 0.0853 | 0.5 | 0.5 | 0.0 | 0.2427 | 680 | 0.2427 | 0.6785 | 0.5853 | 0.5 | -0.3397 | 680 | -0.3398 | -0.476 | -0.2264 |
| baseline:best_single | 680 | 680 | 1.0 | 0.2496 | 0.7147 | 0.5669 | 0.0926 | 0.1603 | 0.5786 | 0.5347 | 0.0744 | 0.2496 | 680 | 0.2496 | 0.7147 | 0.5669 | 0.5786 | -0.3777 | 680 | -0.3777 | -0.5133 | -0.2627 |
| baseline:extremized(a=2) | 680 | 680 | 1.0 | 0.2919 | 0.9863 | 0.5706 | 0.2105 | 0.2841 | 0.5822 | 0.5378 | 0.0808 | 0.2919 | 680 | 0.2919 | 0.9863 | 0.5706 | 0.5822 | -0.6112 | 680 | -0.611 | -0.7698 | -0.46 |
| baseline:logit_pool | 680 | 680 | 1.0 | 0.2581 | 0.7438 | 0.5706 | 0.1222 | 0.1956 | 0.5822 | 0.5378 | 0.0808 | 0.2581 | 680 | 0.2581 | 0.7438 | 0.5706 | 0.5822 | -0.4247 | 680 | -0.4247 | -0.5563 | -0.2995 |
| baseline:mean | 680 | 680 | 1.0 | 0.2486 | 0.6985 | 0.5713 | 0.0893 | 0.1658 | 0.5867 | 0.5391 | 0.0831 | 0.2486 | 680 | 0.2486 | 0.6985 | 0.5713 | 0.5867 | -0.3722 | 680 | -0.3723 | -0.4951 | -0.2639 |
| baseline:median | 680 | 680 | 1.0 | 0.2535 | 0.7152 | 0.5824 | 0.099 | 0.1697 | 0.5836 | 0.5607 | 0.1284 | 0.2535 | 680 | 0.2535 | 0.7152 | 0.5824 | 0.5836 | -0.3993 | 680 | -0.3991 | -0.5325 | -0.284 |
| market | 680 | 680 | 1.0 | 0.1812 | 0.5396 | 0.714 | 0.0818 | 0.293 | 0.8189 | 0.6984 | 0.4052 | 0.1812 | 680 | 0.1812 | 0.5396 | 0.714 | 0.8189 |  |  |  |  |  |

- `baseline:best_single` = single:llama3.1:8b (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.415 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 41.5% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 680 | 273 | 405 | 2 | 126 | 147 | 251 | 154 | 0.4615 | 0.45 | 0.4557 | 0.5403 | 0.081 |
| council:chair=qwen3:8b | 680 | 238 | 412 | 30 | 111 | 127 | 254 | 158 | 0.4664 | 0.4126 | 0.4379 | 0.5397 | 0.0811 |
| single:gemma2:9b | 680 | 171 | 403 | 106 | 84 | 87 | 262 | 141 | 0.4912 | 0.3733 | 0.4242 | 0.562 | 0.1324 |
| single:llama3.1:8b | 680 | 201 | 464 | 15 | 94 | 107 | 284 | 180 | 0.4677 | 0.3431 | 0.3958 | 0.5347 | 0.0744 |
| single:mistral:latest | 680 | 290 | 334 | 56 | 136 | 154 | 210 | 124 | 0.469 | 0.5231 | 0.4945 | 0.55 | 0.0988 |
| single:phi3:medium | 680 | 175 | 361 | 144 | 86 | 89 | 238 | 123 | 0.4914 | 0.4115 | 0.4479 | 0.5697 | 0.1449 |
| single:qwen3:8b | 680 | 152 | 456 | 72 | 64 | 88 | 277 | 179 | 0.4211 | 0.2634 | 0.3241 | 0.5111 | 0.0252 |
| baseline:always_no | 680 | 0 | 680 | 0 | 0 | 0 | 398 | 282 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 680 | 0 | 680 | 0 | 0 | 0 | 398 | 282 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:best_single | 680 | 201 | 464 | 15 | 94 | 107 | 284 | 180 | 0.4677 | 0.3431 | 0.3958 | 0.5347 | 0.0744 |
| baseline:extremized(a=2) | 680 | 206 | 468 | 6 | 97 | 109 | 288 | 180 | 0.4709 | 0.3502 | 0.4017 | 0.5378 | 0.0808 |
| baseline:logit_pool | 680 | 206 | 468 | 6 | 97 | 109 | 288 | 180 | 0.4709 | 0.3502 | 0.4017 | 0.5378 | 0.0808 |
| baseline:mean | 680 | 205 | 458 | 17 | 96 | 109 | 284 | 174 | 0.4683 | 0.3556 | 0.4042 | 0.5391 | 0.0831 |
| baseline:median | 680 | 176 | 394 | 110 | 86 | 90 | 255 | 139 | 0.4886 | 0.3822 | 0.4289 | 0.5607 | 0.1284 |
| market | 680 | 250 | 427 | 3 | 169 | 81 | 315 | 112 | 0.676 | 0.6014 | 0.6365 | 0.6984 | 0.4052 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | market | 680 | 0.0707 | 0.0535 | 0.0876 | council worse |
| council:chair=llama3.1:8b | baseline:best_single | 680 | 0.0023 | -0.006 | 0.0107 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | 680 | 0.0032 | -0.0012 | 0.0078 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | 680 | -0.0063 | -0.015 | 0.0025 | no clear difference |
| council:chair=llama3.1:8b | baseline:always_no | 680 | -0.1629 | -0.196 | -0.1295 | council better |
| council:chair=qwen3:8b | market | 680 | 0.0794 | 0.0607 | 0.0979 | council worse |
| council:chair=qwen3:8b | baseline:best_single | 680 | 0.011 | 0.0011 | 0.0221 | council worse |
| council:chair=qwen3:8b | baseline:mean | 680 | 0.012 | 0.0063 | 0.0185 | council worse |
| council:chair=qwen3:8b | baseline:logit_pool | 680 | 0.0025 | -0.0048 | 0.0096 | no clear difference |
| council:chair=qwen3:8b | baseline:always_no | 680 | -0.1541 | -0.1877 | -0.1231 | council better |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 680 | 0.0172 | 0.008 | 0.2427 | 0.2519 |
| council:chair=qwen3:8b | 680 | 0.026 | 0.0082 | 0.2427 | 0.2606 |
| single:gemma2:9b | 680 | 0.0239 | 0.0117 | 0.2427 | 0.2555 |
| single:llama3.1:8b | 680 | 0.0152 | 0.0084 | 0.2427 | 0.2496 |
| single:mistral:latest | 680 | 0.0475 | 0.0096 | 0.2427 | 0.2793 |
| single:phi3:medium | 680 | 0.0211 | 0.0128 | 0.2427 | 0.2508 |
| single:qwen3:8b | 680 | 0.0625 | 0.0083 | 0.2427 | 0.2974 |
| baseline:always_no | 680 | 0.172 | 0.0 | 0.2427 | 0.4147 |
| baseline:base_rate | 680 | 0.0 | 0.0 | 0.2427 | 0.2427 |
| baseline:best_single | 680 | 0.0152 | 0.0084 | 0.2427 | 0.2496 |
| baseline:extremized(a=2) | 680 | 0.0553 | 0.0069 | 0.2427 | 0.2919 |
| baseline:logit_pool | 680 | 0.0218 | 0.0082 | 0.2427 | 0.2581 |
| baseline:mean | 680 | 0.013 | 0.0068 | 0.2427 | 0.2486 |
| baseline:median | 680 | 0.0195 | 0.0098 | 0.2427 | 0.2535 |
| market | 680 | 0.0149 | 0.074 | 0.2427 | 0.1812 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 680 | 0.1173 | 0.2406 | 0.2551 | 0.2598 |
| council:chair=qwen3:8b | 680 | 0.08 | 0.2462 | 0.2639 | 0.2716 |
