# Chair ablations (settled + settled-ext)

Same members' answers on every question; only what the chair sees, or who chairs, changes. Paired Brier difference, first setup minus second (negative = first better), 95% bootstrap interval stratified by source.

## What the chair sees

| setup | versus | source | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|---|
| council:chair=gemma2:9b | baseline:mean | all | 1039 | 0.0124 | 0.0088 | 0.0162 | first worse |
| council:chair=gemma2:9b | baseline:mean | kalshi | 200 | 0.0123 | 0.0035 | 0.0224 | first worse |
| council:chair=gemma2:9b | baseline:mean | polymarket | 839 | 0.0124 | 0.0085 | 0.0165 | first worse |
| council:chair=gemma2:9b | baseline:logit_pool | all | 1039 | 0.0035 | -0.0016 | 0.0088 | no clear difference |
| council:chair=gemma2:9b | baseline:logit_pool | kalshi | 200 | 0.0031 | -0.008 | 0.0147 | no clear difference |
| council:chair=gemma2:9b | baseline:logit_pool | polymarket | 839 | 0.0036 | -0.0025 | 0.0094 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | all | 1039 | 0.0029 | -0.0006 | 0.0065 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | kalshi | 200 | 0.0 | -0.0084 | 0.0089 | no clear difference |
| council:chair=llama3.1:8b | baseline:mean | polymarket | 839 | 0.0036 | -0.0002 | 0.0075 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | all | 1039 | -0.006 | -0.0123 | 0.0003 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | kalshi | 200 | -0.0092 | -0.0235 | 0.0055 | no clear difference |
| council:chair=llama3.1:8b | baseline:logit_pool | polymarket | 839 | -0.0052 | -0.0124 | 0.0021 | no clear difference |
| council:chair=mistral:latest | baseline:mean | all | 1038 | 0.0121 | 0.005 | 0.0201 | first worse |
| council:chair=mistral:latest | baseline:mean | kalshi | 200 | -0.0017 | -0.0221 | 0.021 | no clear difference |
| council:chair=mistral:latest | baseline:mean | polymarket | 838 | 0.0153 | 0.0085 | 0.0233 | first worse |
| council:chair=mistral:latest | baseline:logit_pool | all | 1038 | 0.0032 | -0.0064 | 0.0133 | no clear difference |
| council:chair=mistral:latest | baseline:logit_pool | kalshi | 200 | -0.0109 | -0.0358 | 0.0151 | no clear difference |
| council:chair=mistral:latest | baseline:logit_pool | polymarket | 838 | 0.0065 | -0.0027 | 0.017 | no clear difference |
| council:chair=phi3:medium | baseline:mean | all | 1039 | 0.004 | 0.0004 | 0.0078 | first worse |
| council:chair=phi3:medium | baseline:mean | kalshi | 200 | 0.0003 | -0.0086 | 0.0093 | no clear difference |
| council:chair=phi3:medium | baseline:mean | polymarket | 839 | 0.0049 | 0.0011 | 0.0092 | first worse |
| council:chair=phi3:medium | baseline:logit_pool | all | 1039 | -0.0049 | -0.0114 | 0.0015 | no clear difference |
| council:chair=phi3:medium | baseline:logit_pool | kalshi | 200 | -0.009 | -0.0236 | 0.0055 | no clear difference |
| council:chair=phi3:medium | baseline:logit_pool | polymarket | 839 | -0.0039 | -0.0115 | 0.0034 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | all | 1039 | 0.0115 | 0.0068 | 0.0163 | first worse |
| council:chair=qwen3:8b | baseline:mean | kalshi | 200 | 0.0103 | -0.0009 | 0.0225 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | polymarket | 839 | 0.0117 | 0.0065 | 0.0176 | first worse |
| council:chair=qwen3:8b | baseline:logit_pool | all | 1039 | 0.0026 | -0.0027 | 0.0079 | no clear difference |
| council:chair=qwen3:8b | baseline:logit_pool | kalshi | 200 | 0.001 | -0.0095 | 0.0121 | no clear difference |
| council:chair=qwen3:8b | baseline:logit_pool | polymarket | 839 | 0.0029 | -0.003 | 0.0091 | no clear difference |
| council:numbers-only:chair=llama3.1:8b | council:chair=llama3.1:8b | all | 1039 | -0.0015 | -0.0054 | 0.0026 | no clear difference |
| council:numbers-only:chair=llama3.1:8b | council:chair=llama3.1:8b | kalshi | 200 | -0.0014 | -0.0105 | 0.0078 | no clear difference |
| council:numbers-only:chair=llama3.1:8b | council:chair=llama3.1:8b | polymarket | 839 | -0.0016 | -0.0061 | 0.0031 | no clear difference |
| council:numbers-only:chair=llama3.1:8b | baseline:mean | all | 1039 | 0.0013 | -0.0017 | 0.0045 | no clear difference |
| council:numbers-only:chair=llama3.1:8b | baseline:mean | kalshi | 200 | -0.0014 | -0.0086 | 0.0053 | no clear difference |
| council:numbers-only:chair=llama3.1:8b | baseline:mean | polymarket | 839 | 0.002 | -0.0012 | 0.0057 | no clear difference |
| council:numbers-only:chair=llama3.1:8b | baseline:logit_pool | all | 1039 | -0.0075 | -0.0137 | -0.0017 | first better |
| council:numbers-only:chair=llama3.1:8b | baseline:logit_pool | kalshi | 200 | -0.0106 | -0.0235 | 0.0013 | no clear difference |
| council:numbers-only:chair=llama3.1:8b | baseline:logit_pool | polymarket | 839 | -0.0068 | -0.0136 | 0.0001 | no clear difference |
| council:numbers-only:chair=qwen3:8b | council:chair=qwen3:8b | all | 1039 | -0.0004 | -0.0059 | 0.0053 | no clear difference |
| council:numbers-only:chair=qwen3:8b | council:chair=qwen3:8b | kalshi | 200 | 0.0013 | -0.0163 | 0.019 | no clear difference |
| council:numbers-only:chair=qwen3:8b | council:chair=qwen3:8b | polymarket | 839 | -0.0008 | -0.0067 | 0.0054 | no clear difference |
| council:numbers-only:chair=qwen3:8b | baseline:mean | all | 1039 | 0.011 | 0.0066 | 0.0158 | first worse |
| council:numbers-only:chair=qwen3:8b | baseline:mean | kalshi | 200 | 0.0116 | -0.0013 | 0.0274 | no clear difference |
| council:numbers-only:chair=qwen3:8b | baseline:mean | polymarket | 839 | 0.0109 | 0.0065 | 0.0158 | first worse |
| council:numbers-only:chair=qwen3:8b | baseline:logit_pool | all | 1039 | 0.0022 | -0.0046 | 0.0091 | no clear difference |
| council:numbers-only:chair=qwen3:8b | baseline:logit_pool | kalshi | 200 | 0.0023 | -0.014 | 0.0213 | no clear difference |
| council:numbers-only:chair=qwen3:8b | baseline:logit_pool | polymarket | 839 | 0.0021 | -0.0058 | 0.0096 | no clear difference |
| council:reasoning-only:chair=llama3.1:8b | council:chair=llama3.1:8b | all | 1039 | 0.0074 | 0.0011 | 0.014 | first worse |
| council:reasoning-only:chair=llama3.1:8b | council:chair=llama3.1:8b | kalshi | 200 | 0.0081 | -0.0086 | 0.0259 | no clear difference |
| council:reasoning-only:chair=llama3.1:8b | council:chair=llama3.1:8b | polymarket | 839 | 0.0072 | 0.0002 | 0.0142 | first worse |
| council:reasoning-only:chair=llama3.1:8b | baseline:mean | all | 1039 | 0.0103 | 0.003 | 0.0172 | first worse |
| council:reasoning-only:chair=llama3.1:8b | baseline:mean | kalshi | 200 | 0.0081 | -0.01 | 0.0265 | no clear difference |
| council:reasoning-only:chair=llama3.1:8b | baseline:mean | polymarket | 839 | 0.0108 | 0.0032 | 0.018 | first worse |
| council:reasoning-only:chair=llama3.1:8b | baseline:logit_pool | all | 1039 | 0.0014 | -0.0066 | 0.0095 | no clear difference |
| council:reasoning-only:chair=llama3.1:8b | baseline:logit_pool | kalshi | 200 | -0.0011 | -0.021 | 0.0197 | no clear difference |
| council:reasoning-only:chair=llama3.1:8b | baseline:logit_pool | polymarket | 839 | 0.002 | -0.0071 | 0.0105 | no clear difference |
| council:reasoning-only:chair=qwen3:8b | council:chair=qwen3:8b | all | 1039 | 0.0169 | 0.0088 | 0.0251 | first worse |
| council:reasoning-only:chair=qwen3:8b | council:chair=qwen3:8b | kalshi | 200 | 0.0103 | -0.0044 | 0.0247 | no clear difference |
| council:reasoning-only:chair=qwen3:8b | council:chair=qwen3:8b | polymarket | 839 | 0.0185 | 0.0089 | 0.0279 | first worse |
| council:reasoning-only:chair=qwen3:8b | baseline:mean | all | 1039 | 0.0284 | 0.0197 | 0.0368 | first worse |
| council:reasoning-only:chair=qwen3:8b | baseline:mean | kalshi | 200 | 0.0206 | 0.003 | 0.0389 | first worse |
| council:reasoning-only:chair=qwen3:8b | baseline:mean | polymarket | 839 | 0.0302 | 0.02 | 0.0399 | first worse |
| council:reasoning-only:chair=qwen3:8b | baseline:logit_pool | all | 1039 | 0.0195 | 0.0117 | 0.0272 | first worse |
| council:reasoning-only:chair=qwen3:8b | baseline:logit_pool | kalshi | 200 | 0.0114 | -0.0033 | 0.0272 | no clear difference |
| council:reasoning-only:chair=qwen3:8b | baseline:logit_pool | polymarket | 839 | 0.0214 | 0.0122 | 0.0305 | first worse |


## Who chairs (full view, questions every full-view council answered)

| council | chair | n_common | council_brier | chair_alone_brier | vs_mean_pool | vs_mean_pool_ci_low | vs_mean_pool_ci_high | vs_chair_alone | vs_chair_alone_ci_low | vs_chair_alone_ci_high | spearman_chair_vs_council |
|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=gemma2:9b | gemma2:9b | 1038 | 0.2628 | 0.2612 | 0.0124 | 0.0086 | 0.0159 | 0.0016 | -0.0058 | 0.0088 | 0.5 |
| council:chair=llama3.1:8b | llama3.1:8b | 1038 | 0.2533 | 0.2572 | 0.0029 | -0.0006 | 0.0065 | -0.0039 | -0.011 | 0.0028 | 0.5 |
| council:chair=mistral:latest | mistral:latest | 1038 | 0.2625 | 0.2775 | 0.0121 | 0.005 | 0.0201 | -0.015 | -0.024 | -0.0061 | 0.5 |
| council:chair=phi3:medium | phi3:medium | 1038 | 0.2544 | 0.2539 | 0.004 | 0.0005 | 0.0079 | 0.0005 | -0.0083 | 0.0094 | 0.5 |
| council:chair=qwen3:8b | qwen3:8b | 1038 | 0.2619 | 0.2951 | 0.0115 | 0.0065 | 0.0163 | -0.0332 | -0.0436 | -0.0221 | 0.5 |


## How far each council moves from the mean pool

| council | n | mean_abs_shift_from_mean_pool | share_within_0.05 |
|---|---|---|---|
| council:chair=gemma2:9b | 1039 | 0.0403 | 0.7469 |
| council:chair=llama3.1:8b | 1039 | 0.0415 | 0.7199 |
| council:chair=mistral:latest | 1038 | 0.0821 | 0.4942 |
| council:chair=phi3:medium | 1039 | 0.0382 | 0.7536 |
| council:chair=qwen3:8b | 1039 | 0.0468 | 0.718 |
| council:numbers-only:chair=llama3.1:8b | 1039 | 0.0256 | 0.8749 |
| council:numbers-only:chair=qwen3:8b | 1039 | 0.0348 | 0.8056 |
| council:reasoning-only:chair=llama3.1:8b | 1039 | 0.0863 | 0.3859 |
| council:reasoning-only:chair=qwen3:8b | 1039 | 0.101 | 0.334 |
