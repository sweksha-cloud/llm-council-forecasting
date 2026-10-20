# Results: settled

Resolved questions scored: **359** (set: settled). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market. `accuracy`: share on the right side of 0.5 (exactly 0.5 counts half), so the `market` row is the market-baseline accuracy. `ece`: expected calibration error, 0 = perfectly calibrated. `sharpness`: mean |p − 0.5|, how far forecasts commit away from 50% (0 to 0.5, higher = sharper); read with `ece`, since a setup that always says about 50% can have low ECE and still be useless. `auroc`: how well the setup ranks Yes questions above No ones, 0.5 = chance, ignores calibration. `balanced_accuracy`/`mcc`: see Ground truth below. `skill_vs_market_paired`: 1 − Brier / market Brier on the `n_vs_market` questions both the setup and the market answered, with a 95% bootstrap interval (`skill_ci_low`..`skill_ci_high`); > 0 means better than the market. For 0/1 answers (imported free-text results) ECE and AUROC carry little information.

| setup | questions | answered | coverage | brier | log_score | accuracy | ece | sharpness | auroc | balanced_accuracy | mcc | brier_abstain_0.5 | common_n | brier_common | log_common | accuracy_common | auroc_common | skill_vs_market | n_vs_market | skill_vs_market_paired | skill_ci_low | skill_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 359 | 359 | 1.0 | 0.2556 | 0.7147 | 0.571 | 0.1049 | 0.1575 | 0.5859 | 0.5704 | 0.1407 | 0.2556 | 359 | 0.2556 | 0.7147 | 0.571 | 0.5859 | -0.748 | 359 | -0.7481 | -1.0521 | -0.5128 |
| council:chair=qwen3:8b | 359 | 359 | 1.0 | 0.2639 | 0.8124 | 0.5724 | 0.1347 | 0.1826 | 0.587 | 0.5719 | 0.1439 | 0.2639 | 359 | 0.2639 | 0.8124 | 0.5724 | 0.587 | -0.8047 | 359 | -0.8049 | -1.1238 | -0.5555 |
| single:deepseek-r1:8b | 359 | 359 | 1.0 | 0.2906 | 0.897 | 0.5251 | 0.206 | 0.2277 | 0.5617 | 0.5115 | 0.0266 | 0.2906 | 359 | 0.2906 | 0.897 | 0.5251 | 0.5617 | -0.9873 | 359 | -0.987 | -1.3635 | -0.7075 |
| single:gemma2:9b | 359 | 359 | 1.0 | 0.2715 | 0.7692 | 0.5571 | 0.1525 | 0.1849 | 0.5771 | 0.5532 | 0.1107 | 0.2715 | 359 | 0.2715 | 0.7692 | 0.5571 | 0.5771 | -0.8567 | 359 | -0.8566 | -1.1884 | -0.6071 |
| single:llama3.1:8b | 359 | 359 | 1.0 | 0.2711 | 0.7855 | 0.5042 | 0.1729 | 0.1737 | 0.5535 | 0.4982 | -0.0037 | 0.2711 | 359 | 0.2711 | 0.7855 | 0.5042 | 0.5535 | -0.854 | 359 | -0.8539 | -1.1718 | -0.61 |
| single:mistral:latest | 359 | 359 | 1.0 | 0.2737 | 0.8058 | 0.5682 | 0.1377 | 0.1891 | 0.5707 | 0.5762 | 0.152 | 0.2737 | 359 | 0.2737 | 0.8058 | 0.5682 | 0.5707 | -0.8718 | 359 | -0.8717 | -1.2244 | -0.5966 |
| single:phi3:medium | 359 | 359 | 1.0 | 0.2595 | 0.7633 | 0.571 | 0.1124 | 0.1439 | 0.5897 | 0.5813 | 0.1646 | 0.2595 | 359 | 0.2595 | 0.7633 | 0.571 | 0.5897 | -0.7746 | 359 | -0.775 | -1.0815 | -0.5295 |
| single:qwen3:8b | 359 | 359 | 1.0 | 0.29 | 0.9488 | 0.5529 | 0.2349 | 0.2471 | 0.5887 | 0.5355 | 0.0744 | 0.29 | 359 | 0.29 | 0.9488 | 0.5529 | 0.5887 | -0.9832 | 359 | -0.983 | -1.3544 | -0.6895 |
| baseline:always_no | 359 | 359 | 1.0 | 0.4735 | 6.5422 | 0.5265 | 0.4735 | 0.5 | 0.5 | 0.5 | 0.0 | 0.4735 | 359 | 0.4735 | 6.5422 | 0.5265 | 0.5 | -2.2381 | 359 | -2.2384 | -2.8204 | -1.7519 |
| baseline:base_rate | 359 | 359 | 1.0 | 0.2493 | 0.6917 | 0.5265 | 0.0 | 0.0265 | 0.5 | 0.5 | 0.0 | 0.2493 | 359 | 0.2493 | 0.6917 | 0.5265 | 0.5 | -0.7049 | 359 | -0.7049 | -1.0 | -0.4716 |
| baseline:best_single | 359 | 359 | 1.0 | 0.2595 | 0.7633 | 0.571 | 0.1124 | 0.1439 | 0.5897 | 0.5813 | 0.1646 | 0.2595 | 359 | 0.2595 | 0.7633 | 0.571 | 0.5897 | -0.7746 | 359 | -0.775 | -1.0815 | -0.5295 |
| baseline:extremized(a=2) | 359 | 359 | 1.0 | 0.2939 | 0.9689 | 0.5738 | 0.2041 | 0.2716 | 0.5964 | 0.568 | 0.1396 | 0.2939 | 359 | 0.2939 | 0.9689 | 0.5738 | 0.5964 | -1.0099 | 359 | -1.0099 | -1.364 | -0.7236 |
| baseline:logit_pool | 359 | 359 | 1.0 | 0.2611 | 0.7485 | 0.5738 | 0.1274 | 0.1793 | 0.5964 | 0.568 | 0.1396 | 0.2611 | 359 | 0.2611 | 0.7485 | 0.5738 | 0.5964 | -0.7856 | 359 | -0.7858 | -1.0883 | -0.545 |
| baseline:mean | 359 | 359 | 1.0 | 0.2534 | 0.7086 | 0.5724 | 0.1058 | 0.1547 | 0.5959 | 0.5677 | 0.1385 | 0.2534 | 359 | 0.2534 | 0.7086 | 0.5724 | 0.5959 | -0.7329 | 359 | -0.7332 | -1.0262 | -0.502 |
| baseline:median | 359 | 359 | 1.0 | 0.2632 | 0.7385 | 0.5529 | 0.1315 | 0.1654 | 0.5762 | 0.5466 | 0.0955 | 0.2632 | 359 | 0.2632 | 0.7385 | 0.5529 | 0.5762 | -0.8 | 359 | -0.7997 | -1.0964 | -0.5618 |
| market | 359 | 359 | 1.0 | 0.1462 | 0.4585 | 0.7841 | 0.0715 | 0.2994 | 0.8745 | 0.7813 | 0.5692 | 0.1462 | 359 | 0.1462 | 0.4585 | 0.7841 | 0.8745 |  |  |  |  |  |

- `baseline:mean` and the other pools use only council members: gemma2:9b, llama3.1:8b, mistral:latest, phi3:medium, qwen3:8b

- `baseline:best_single` = single:phi3:medium (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)

- `baseline:always_no` = 0% on every question; the accuracy any setup gets just by saying No

- `baseline:base_rate` = 0.474 (share resolved Yes) on every question; uses the outcomes, so it's slightly optimistic


## Ground truth (each forecast as a Yes/No call; 47.4% of questions resolved Yes)

Above 0.5 is a Yes call, below a No call, exactly 0.5 no call. `precision`: share of Yes calls that happened. `recall`: share of events that happened called Yes. `balanced_accuracy`: mean of Yes and No recall, 0.5 for always saying No. `mcc`: correlation between calls and outcomes, 0 = chance.

| setup | answered | yes_calls | no_calls | no_call_0.5 | tp | fp | tn | fn | precision | recall | f1 | balanced_accuracy | mcc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 359 | 168 | 187 | 4 | 91 | 77 | 112 | 75 | 0.5417 | 0.5482 | 0.5449 | 0.5704 | 0.1407 |
| council:chair=qwen3:8b | 359 | 159 | 189 | 11 | 86 | 73 | 114 | 75 | 0.5409 | 0.5342 | 0.5375 | 0.5719 | 0.1439 |
| single:deepseek-r1:8b | 359 | 83 | 257 | 19 | 41 | 42 | 138 | 119 | 0.494 | 0.2562 | 0.3374 | 0.5115 | 0.0266 |
| single:gemma2:9b | 359 | 107 | 196 | 56 | 56 | 51 | 116 | 80 | 0.5234 | 0.4118 | 0.4609 | 0.5532 | 0.1107 |
| single:llama3.1:8b | 359 | 133 | 222 | 4 | 63 | 70 | 116 | 106 | 0.4737 | 0.3728 | 0.4172 | 0.4982 | -0.0037 |
| single:mistral:latest | 359 | 155 | 164 | 40 | 84 | 71 | 100 | 64 | 0.5419 | 0.5676 | 0.5545 | 0.5762 | 0.152 |
| single:phi3:medium | 359 | 114 | 167 | 78 | 62 | 52 | 104 | 63 | 0.5439 | 0.496 | 0.5188 | 0.5813 | 0.1646 |
| single:qwen3:8b | 359 | 105 | 211 | 43 | 50 | 55 | 127 | 84 | 0.4762 | 0.3731 | 0.4184 | 0.5355 | 0.0744 |
| baseline:always_no | 359 | 0 | 359 | 0 | 0 | 0 | 189 | 170 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:base_rate | 359 | 0 | 359 | 0 | 0 | 0 | 189 | 170 |  | 0.0 | 0.0 | 0.5 | 0.0 |
| baseline:best_single | 359 | 114 | 167 | 78 | 62 | 52 | 104 | 63 | 0.5439 | 0.496 | 0.5188 | 0.5813 | 0.1646 |
| baseline:extremized(a=2) | 359 | 136 | 219 | 4 | 76 | 60 | 128 | 91 | 0.5588 | 0.4551 | 0.5017 | 0.568 | 0.1396 |
| baseline:logit_pool | 359 | 136 | 219 | 4 | 76 | 60 | 128 | 91 | 0.5588 | 0.4551 | 0.5017 | 0.568 | 0.1396 |
| baseline:mean | 359 | 137 | 213 | 9 | 76 | 61 | 125 | 88 | 0.5547 | 0.4634 | 0.505 | 0.5677 | 0.1385 |
| baseline:median | 359 | 116 | 194 | 49 | 58 | 58 | 116 | 78 | 0.5 | 0.4265 | 0.4603 | 0.5466 | 0.0955 |
| market | 359 | 150 | 208 | 1 | 121 | 29 | 160 | 48 | 0.8067 | 0.716 | 0.7586 | 0.7813 | 0.5692 |


## Council vs baselines (paired Brier difference, negative = council better)

Bootstrap resamples within each source, so the source mix is fixed. Per-source results follow.

| council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | market | 359 | 0.1094 | 0.0845 | 0.135 | council worse |
| council:chair=llama3.1:8b | baseline:best_single | 359 | -0.0039 | -0.0189 | 0.0105 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | 359 | 0.0022 | -0.004 | 0.008 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | 359 | -0.0055 | -0.0161 | 0.0037 | no clear difference |
| council:chair=llama3.1:8b | baseline:always_no | 359 | -0.2179 | -0.2699 | -0.167 | council better |
| council:chair=qwen3:8b | market | 359 | 0.1177 | 0.0899 | 0.1447 | council worse |
| council:chair=qwen3:8b | baseline:best_single | 359 | 0.0044 | -0.0119 | 0.0211 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | 359 | 0.0105 | 0.004 | 0.018 | council worse |
| council:chair=qwen3:8b | baseline:logit_pool | 359 | 0.0028 | -0.005 | 0.0105 | no clear difference |
| council:chair=qwen3:8b | baseline:always_no | 359 | -0.2096 | -0.2585 | -0.16 | council better |


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
| polymarket | council:chair=llama3.1:8b | market | 159 | 0.0949 | 0.0554 | 0.1328 | council worse |
| polymarket | council:chair=llama3.1:8b | baseline:best_single | 159 | 0.0107 | -0.0109 | 0.0325 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:mean | 159 | 0.0049 | -0.0027 | 0.0135 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:logit_pool | 159 | -0.0008 | -0.015 | 0.0129 | no clear difference |
| polymarket | council:chair=llama3.1:8b | baseline:always_no | 159 | -0.2478 | -0.3242 | -0.1692 | council better |
| polymarket | council:chair=qwen3:8b | market | 159 | 0.1007 | 0.0605 | 0.1428 | council worse |
| polymarket | council:chair=qwen3:8b | baseline:best_single | 159 | 0.0165 | -0.0069 | 0.0416 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:mean | 159 | 0.0107 | 0.003 | 0.0208 | council worse |
| polymarket | council:chair=qwen3:8b | baseline:logit_pool | 159 | 0.005 | -0.0065 | 0.0148 | no clear difference |
| polymarket | council:chair=qwen3:8b | baseline:always_no | 159 | -0.2419 | -0.318 | -0.1673 | council better |


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

Each row uses the questions that setup answered (see `n`), so rows with different `n` aren't directly comparable; compare them on `brier_common` above.

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 359 | 0.0157 | 0.0099 | 0.2493 | 0.2556 |
| council:chair=qwen3:8b | 359 | 0.0251 | 0.0118 | 0.2493 | 0.2639 |
| single:deepseek-r1:8b | 359 | 0.0516 | 0.0108 | 0.2493 | 0.2906 |
| single:gemma2:9b | 359 | 0.0337 | 0.0132 | 0.2493 | 0.2715 |
| single:llama3.1:8b | 359 | 0.0418 | 0.0189 | 0.2493 | 0.2711 |
| single:mistral:latest | 359 | 0.0341 | 0.0086 | 0.2493 | 0.2737 |
| single:phi3:medium | 359 | 0.0241 | 0.0134 | 0.2493 | 0.2595 |
| single:qwen3:8b | 359 | 0.0635 | 0.0242 | 0.2493 | 0.29 |
| baseline:always_no | 359 | 0.2242 | 0.0 | 0.2493 | 0.4735 |
| baseline:base_rate | 359 | 0.0 | 0.0 | 0.2493 | 0.2493 |
| baseline:best_single | 359 | 0.0241 | 0.0134 | 0.2493 | 0.2595 |
| baseline:extremized(a=2) | 359 | 0.0533 | 0.0103 | 0.2493 | 0.2939 |
| baseline:logit_pool | 359 | 0.0233 | 0.0108 | 0.2493 | 0.2611 |
| baseline:mean | 359 | 0.0185 | 0.0125 | 0.2493 | 0.2534 |
| baseline:median | 359 | 0.0251 | 0.0117 | 0.2493 | 0.2632 |
| market | 359 | 0.0086 | 0.1098 | 0.2493 | 0.1462 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

| council | n | spearman_spread_vs_brier | brier_low_spread | brier_mid_spread | brier_high_spread |
|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 359 | 0.0151 | 0.251 | 0.2672 | 0.2487 |
| council:chair=qwen3:8b | 359 | -0.0147 | 0.2519 | 0.2725 | 0.2672 |
