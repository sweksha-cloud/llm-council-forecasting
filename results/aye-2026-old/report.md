# Results: aye-2026-old

Resolved questions scored: **890** (set: all). Lower Brier/log score is better.

## Scores

`brier`/`log_score`: answered questions only. `*_common`: the questions every setup answered, the fair comparison. `skill_vs_market` > 0 means better than the market.

| setup | questions | answered | coverage | brier | log_score | brier_abstain_0.5 | common_n | brier_common | log_common |
|---|---|---|---|---|---|---|---|---|---|
| single:llama3.1:latest | 890 | 2 | 0.002 | 0.5 | 6.9078 | 0.2506 | 1 | 0.0 | 0.0 |
| single:mistral:latest | 890 | 7 | 0.008 | 0.4286 | 5.9209 | 0.2514 | 1 | 0.0 | 0.0 |
| single:qwen3:8b | 890 | 9 | 0.01 | 0.8889 | 12.2805 | 0.2565 | 1 | 0.0 | 0.0 |
| baseline:best_single | 890 | 7 | 0.008 | 0.4286 | 5.9209 | 0.2514 | 1 | 0.0 | 0.0 |
| baseline:extremized(a=2) | 890 | 4 | 0.004 | 0.75 | 10.3616 | 0.2522 | 1 | 0.0 | 0.0 |
| baseline:logit_pool | 890 | 4 | 0.004 | 0.75 | 10.3616 | 0.2522 | 1 | 0.0 | 0.0 |
| baseline:mean | 890 | 4 | 0.004 | 0.75 | 10.3616 | 0.2522 | 1 | 0.0 | 0.0 |
| baseline:median | 890 | 4 | 0.004 | 0.75 | 10.3616 | 0.2522 | 1 | 0.0 | 0.0 |

- `baseline:best_single` = single:mistral:latest (lowest Brier on these same questions, so it's chosen in-sample and slightly optimistic)


## Council vs baselines (paired Brier difference, negative = council better)

_none_


## Murphy decomposition (Brier = reliability − resolution + uncertainty)

| setup | n | reliability | resolution | uncertainty | brier |
|---|---|---|---|---|---|
| single:llama3.1:latest | 2 | 0.25 | 0.0 | 0.25 | 0.5 |
| single:mistral:latest | 7 | 0.3214 | 0.0153 | 0.1224 | 0.4286 |
| single:qwen3:8b | 9 | 0.7901 | 0.0 | 0.0988 | 0.8889 |
| baseline:best_single | 7 | 0.3214 | 0.0153 | 0.1224 | 0.4286 |
| baseline:extremized(a=2) | 4 | 0.5625 | 0.0 | 0.1875 | 0.75 |
| baseline:logit_pool | 4 | 0.5625 | 0.0 | 0.1875 | 0.75 |
| baseline:mean | 4 | 0.5625 | 0.0 | 0.1875 | 0.75 |
| baseline:median | 4 | 0.5625 | 0.0 | 0.1875 | 0.75 |


## Does member disagreement predict council error?

Positive Spearman = the council does worse when members disagree more.

_none_
