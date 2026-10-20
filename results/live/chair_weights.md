# How the chair combines its members (live)

Weights (≥ 0, sum 1) that best reproduce the chair's forecast as a weighted average of the members' forecasts in log-odds; equal weights = the logit pool. 95% bootstrap intervals resample questions within source. Descriptive; uses no outcomes.

## Weights

| setup | member | n | weight | ci_low | ci_high | equal_weight |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | gemma2:9b | 342 | 0.123 | 0.064 | 0.175 | 0.2 |
| council:chair=llama3.1:8b | llama3.1:8b | 342 | 0.247 | 0.157 | 0.325 | 0.2 |
| council:chair=llama3.1:8b | mistral:latest | 342 | 0.325 | 0.253 | 0.396 | 0.2 |
| council:chair=llama3.1:8b | phi3:medium | 342 | 0.224 | 0.159 | 0.288 | 0.2 |
| council:chair=llama3.1:8b | qwen3:8b | 342 | 0.082 | 0.048 | 0.114 | 0.2 |
| council:chair=qwen3:8b | gemma2:9b | 342 | 0.179 | 0.094 | 0.243 | 0.2 |
| council:chair=qwen3:8b | llama3.1:8b | 342 | 0.161 | 0.088 | 0.238 | 0.2 |
| council:chair=qwen3:8b | mistral:latest | 342 | 0.267 | 0.195 | 0.335 | 0.2 |
| council:chair=qwen3:8b | phi3:medium | 342 | 0.208 | 0.15 | 0.292 | 0.2 |
| council:chair=qwen3:8b | qwen3:8b | 342 | 0.185 | 0.144 | 0.226 | 0.2 |


## Fit, and which member the chair lands closest to

| setup | n | rmse_fitted | rmse_equal_weights | nearest_gemma2:9b | nearest_llama3.1:8b | nearest_mistral:latest | nearest_phi3:medium | nearest_qwen3:8b |
|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 342 | 0.287 | 0.339 | 0.319 | 0.251 | 0.225 | 0.149 | 0.056 |
| council:chair=qwen3:8b | 342 | 0.312 | 0.318 | 0.327 | 0.219 | 0.24 | 0.155 | 0.058 |


## Does a chair favour its own model?

| chair | versus_chairs | n | own_weight_minus_others | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| llama3.1:8b | qwen3:8b | 342 | 0.085 | 0.008 | 0.157 | favours own model |
| qwen3:8b | llama3.1:8b | 342 | 0.103 | 0.06 | 0.146 | favours own model |
