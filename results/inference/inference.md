# Strength of the evidence (added 2026-11-06)

Brier difference, first setup minus the mean pool of the same members (negative = first better). Bootstrap stratified by source, 2000 resamples. Holm-adjusted p-values control the family-wise error at 5%. Equivalent = the 90% interval lies inside +-0.013 (TOST at 5%), the difference docs/power.md says the study could detect.

## Every council variant vs the members' average

| setup | versus | n | mean_diff | ci95_low | ci95_high | ci90_low | ci90_high | p | equivalence_bound | equivalent_within_margin | p_holm | verdict_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| council:chair=gemma2:9b | baseline:mean | 1039 | 0.0124 | 0.0087 | 0.0162 | 0.0092 | 0.0155 | 0.0 | 0.0155 | no | 0.0 | first worse |
| council:chair=llama3.1:8b | baseline:mean | 1039 | 0.0029 | -0.0008 | 0.0066 | -0.0001 | 0.006 | 0.115 | 0.006 | yes | 0.23 | no clear difference |
| council:chair=mistral:latest | baseline:mean | 1038 | 0.0121 | 0.0049 | 0.0198 | 0.0061 | 0.0182 | 0.001 | 0.0182 | no | 0.007 | first worse |
| council:chair=phi3:medium | baseline:mean | 1039 | 0.004 | 0.0004 | 0.0078 | 0.0008 | 0.0072 | 0.036 | 0.0072 | yes | 0.108 | no clear difference |
| council:chair=qwen3:8b | baseline:mean | 1039 | 0.0115 | 0.0069 | 0.0164 | 0.0076 | 0.0156 | 0.0 | 0.0156 | no | 0.0 | first worse |
| council:numbers-only:chair=llama3.1:8b | baseline:mean | 1039 | 0.0013 | -0.0019 | 0.0045 | -0.0013 | 0.0042 | 0.417 | 0.0042 | yes | 0.417 | no clear difference |
| council:numbers-only:chair=qwen3:8b | baseline:mean | 1039 | 0.011 | 0.0066 | 0.0159 | 0.0072 | 0.0151 | 0.0 | 0.0151 | no | 0.0 | first worse |
| council:reasoning-only:chair=llama3.1:8b | baseline:mean | 1039 | 0.0103 | 0.0034 | 0.0172 | 0.0045 | 0.0161 | 0.002 | 0.0161 | no | 0.012 | first worse |
| council:reasoning-only:chair=qwen3:8b | baseline:mean | 1039 | 0.0284 | 0.0202 | 0.0369 | 0.0215 | 0.0356 | 0.0 | 0.0356 | no | 0.0 | first worse |
| debate:mean-r2 | baseline:mean | 359 | 0.0051 | 0.002 | 0.0083 | 0.0025 | 0.0078 | 0.003 | 0.0078 | yes | 0.015 | first worse |
| council:chair=llama3.3:70b | baseline:mean | 359 | 0.0074 | 0.002 | 0.014 | 0.0027 | 0.0128 | 0.009 | 0.0128 | yes | 0.036 | first worse |


## By how certain the market was (pre-registered robustness cut)

| market | setup | versus | n | mean_diff | ci95_low | ci95_high | ci90_low | ci90_high | p | equivalence_bound | equivalent_within_margin | p_holm | verdict_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| uncertain | council:chair=llama3.1:8b | baseline:mean | 494 | -0.0065 | -0.0108 | -0.0023 | -0.0102 | -0.003 | 0.001 | 0.0102 | yes | 0.004 | first better |
| leaning | council:chair=llama3.1:8b | baseline:mean | 226 | 0.0001 | -0.0085 | 0.0093 | -0.0073 | 0.0077 | 0.98 | 0.0077 | yes | 0.98 | no clear difference |
| near-certain | council:chair=llama3.1:8b | baseline:mean | 319 | 0.0194 | 0.0127 | 0.0264 | 0.0136 | 0.0254 | 0.0 | 0.0254 | no | 0.0 | first worse |
| uncertain | council:chair=qwen3:8b | baseline:mean | 494 | 0.0089 | 0.0025 | 0.0157 | 0.0036 | 0.0145 | 0.004 | 0.0145 | no | 0.008 | first worse |
| leaning | council:chair=qwen3:8b | baseline:mean | 226 | 0.0175 | 0.0068 | 0.0293 | 0.0084 | 0.0272 | 0.0 | 0.0272 | no | 0.0 | first worse |
| near-certain | council:chair=qwen3:8b | baseline:mean | 319 | 0.0112 | 0.0033 | 0.0208 | 0.0045 | 0.0189 | 0.001 | 0.0189 | no | 0.004 | first worse |


## Can the models forecast at all?

AUROC 0.5 = no better than chance at ranking which questions resolve Yes. `vs_base_rate` = Brier difference from always forecasting the share of Yes outcomes (negative = better than that constant).

| setup | n | auroc | auroc_ci_low | auroc_ci_high | vs_base_rate | vs_base_rate_ci_low | vs_base_rate_ci_high |
|---|---|---|---|---|---|---|---|
| single:gemma2:9b | 1039 | 0.5924 | 0.5572 | 0.6254 | 0.0152 | 0.0029 | 0.028 |
| single:llama3.1:8b | 1039 | 0.5703 | 0.5358 | 0.6031 | 0.0112 | 0.0009 | 0.0221 |
| single:mistral:latest | 1039 | 0.5601 | 0.5248 | 0.5932 | 0.0316 | 0.0182 | 0.046 |
| single:phi3:medium | 1039 | 0.5969 | 0.5635 | 0.6292 | 0.0081 | -0.0029 | 0.0196 |
| single:qwen3:8b | 1039 | 0.5695 | 0.5324 | 0.604 | 0.0491 | 0.0329 | 0.0667 |
| baseline:mean | 1039 | 0.5922 | 0.5571 | 0.6262 | 0.0045 | -0.0058 | 0.015 |
| council:chair=llama3.1:8b | 1039 | 0.5839 | 0.5495 | 0.6179 | 0.0074 | -0.0033 | 0.0182 |
| council:chair=qwen3:8b | 1039 | 0.583 | 0.5465 | 0.6158 | 0.016 | 0.0034 | 0.0291 |
| market | 1039 | 0.8395 | 0.8154 | 0.8629 | -0.0767 | -0.0906 | -0.0631 |
