# Results: aye-2026-new

Resolved questions scored: **1611** (set: all). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market.

| setup | questions | answered | coverage | brier | log_score | brier_abstain_0.5 |
|---|---|---|---|---|---|---|
| single:deepseek-r1:8b | 1611 | 138 | 0.086 | 0.6087 | 8.4094 | 0.2807 |
| single:gemma2:9b | 1611 | 41 | 0.025 | 0.6829 | 9.435 | 0.261 |
| single:llama3.1:8b-instruct-q4_K_M | 1611 | 76 | 0.047 | 0.5789 | 7.9985 | 0.2655 |
| single:mistral:latest | 1611 | 96 | 0.06 | 0.6875 | 9.4982 | 0.2761 |
| single:phi3:medium | 1611 | 887 | 0.551 | 0.646 | 8.9248 | 0.468 |
| single:qwen3:8b | 1611 | 60 | 0.037 | 0.6167 | 8.5196 | 0.2637 |
| baseline:best_single | 1611 | 887 | 0.551 | 0.646 | 8.9248 | 0.468 |
| baseline:extremized(a=2) | 1611 | 240 | 0.149 | 0.6489 | 8.2331 | 0.3094 |
| baseline:logit_pool | 1611 | 240 | 0.149 | 0.6474 | 7.9155 | 0.3092 |
| baseline:mean | 1611 | 240 | 0.149 | 0.6144 | 7.6781 | 0.3043 |
| baseline:median | 1611 | 240 | 0.149 | 0.649 | 8.5171 | 0.3094 |

- `baseline:best_single` = single:phi3:medium (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)


## Council vs baselines (paired Brier difference, negative = council better)

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
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

_none_
