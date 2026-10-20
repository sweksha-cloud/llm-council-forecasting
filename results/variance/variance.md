# Variance across seeds (temperature 0.7, fixed 200-question subset)

`T=0` is the main run on the same questions. Paired rows: council minus reference (negative = council better).

## Council comparisons per run

| council | versus | T=0 |
|---|---|---|
| council:chair=llama3.1:8b | baseline:mean | 0.0028 |
| council:chair=llama3.1:8b | baseline:logit_pool | -0.0053 |
| council:chair=llama3.1:8b | baseline:best_single | -0.005 |
| council:chair=llama3.1:8b | market | 0.1101 |
| council:chair=llama3.1:8b | baseline:always_no | -0.2297 |
| council:chair=qwen3:8b | baseline:mean | 0.0084 |
| council:chair=qwen3:8b | baseline:logit_pool | 0.0003 |
| council:chair=qwen3:8b | baseline:best_single | 0.0005 |
| council:chair=qwen3:8b | market | 0.1157 |
| council:chair=qwen3:8b | baseline:always_no | -0.2241 |


## Brier per setup and run

| setup | T=0 |
|---|---|
| baseline:always_no | 0.4874 |
| baseline:base_rate | 0.2498 |
| baseline:best_single | 0.2628 |
| baseline:extremized(a=2) | 0.2955 |
| baseline:logit_pool | 0.263 |
| baseline:mean | 0.2549 |
| baseline:median | 0.2675 |
| council:chair=llama3.1:8b | 0.2577 |
| council:chair=qwen3:8b | 0.2633 |
| market | 0.1476 |
| single:deepseek-r1:8b | 0.2883 |
| single:gemma2:9b | 0.2711 |
| single:llama3.1:8b | 0.2737 |
| single:mistral:latest | 0.2669 |
| single:phi3:medium | 0.2628 |
| single:qwen3:8b | 0.3015 |
