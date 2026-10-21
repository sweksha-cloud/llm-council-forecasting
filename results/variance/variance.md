# Variance across seeds (temperature 0.7, fixed 200-question subset)

`T=0` is the main run on the same questions. Paired rows: council minus reference (negative = council better).

## Council comparisons per run

| council | versus | T=0 | seed 1 | seed 2 | seed 3 | seed_mean | same_sign_as_T0 |
|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | baseline:mean | 0.0028 | -0.0029 | 0.0029 | -0.0018 | -0.0006 | 1 of 3 |
| council:chair=llama3.1:8b | baseline:logit_pool | -0.0053 | -0.0094 | -0.0044 | -0.0086 | -0.0075 | 3 of 3 |
| council:chair=llama3.1:8b | baseline:best_single | -0.005 | -0.0098 | 0.0038 | -0.0086 | -0.0049 | 2 of 3 |
| council:chair=llama3.1:8b | market | 0.1101 | 0.1012 | 0.1111 | 0.1051 | 0.1058 | 3 of 3 |
| council:chair=llama3.1:8b | baseline:always_no | -0.2297 | -0.2386 | -0.2288 | -0.2347 | -0.234 | 3 of 3 |
| council:chair=qwen3:8b | baseline:mean | 0.0084 | 0.0059 | 0.0169 | 0.0046 | 0.0091 | 3 of 3 |
| council:chair=qwen3:8b | baseline:logit_pool | 0.0003 | -0.0006 | 0.0097 | -0.0022 | 0.0023 | 1 of 3 |
| council:chair=qwen3:8b | baseline:best_single | 0.0005 | -0.001 | 0.0178 | -0.0022 | 0.0049 | 1 of 3 |
| council:chair=qwen3:8b | market | 0.1157 | 0.11 | 0.1251 | 0.1115 | 0.1155 | 3 of 3 |
| council:chair=qwen3:8b | baseline:always_no | -0.2241 | -0.2298 | -0.2148 | -0.2283 | -0.2243 | 3 of 3 |


## Brier per setup and run

| setup | T=0 | seed 1 | seed 2 | seed 3 | seed_mean | seed_sd |
|---|---|---|---|---|---|---|
| baseline:always_no | 0.4874 | 0.4874 | 0.4874 | 0.4874 | 0.4874 | 0.0 |
| baseline:base_rate | 0.2498 | 0.2498 | 0.2498 | 0.2498 | 0.2498 | 0.0 |
| baseline:best_single | 0.2628 | 0.2586 | 0.2549 | 0.2613 | 0.2583 | 0.0032 |
| baseline:extremized(a=2) | 0.2955 | 0.2928 | 0.3017 | 0.2909 | 0.2951 | 0.0058 |
| baseline:logit_pool | 0.263 | 0.2582 | 0.263 | 0.2613 | 0.2608 | 0.0024 |
| baseline:mean | 0.2549 | 0.2517 | 0.2558 | 0.2545 | 0.254 | 0.0021 |
| baseline:median | 0.2675 | 0.2596 | 0.2639 | 0.2625 | 0.262 | 0.0022 |
| council:chair=llama3.1:8b | 0.2577 | 0.2488 | 0.2587 | 0.2527 | 0.2534 | 0.005 |
| council:chair=qwen3:8b | 0.2633 | 0.2576 | 0.2727 | 0.2591 | 0.2631 | 0.0083 |
| market | 0.1476 | 0.1476 | 0.1476 | 0.1476 | 0.1476 | 0.0 |
| single:deepseek-r1:8b | 0.2883 |  |  |  |  |  |
| single:gemma2:9b | 0.2711 | 0.2742 | 0.2716 | 0.2714 | 0.2724 | 0.0015 |
| single:llama3.1:8b | 0.2737 | 0.2599 | 0.2762 | 0.2763 | 0.2708 | 0.0095 |
| single:mistral:latest | 0.2669 | 0.2586 | 0.271 | 0.2666 | 0.2654 | 0.0063 |
| single:phi3:medium | 0.2628 | 0.2755 | 0.2549 | 0.2613 | 0.2639 | 0.0106 |
| single:qwen3:8b | 0.3015 | 0.2854 | 0.3153 | 0.3074 | 0.3027 | 0.0155 |
