# How the chair combines its members (settled + settled-ext)

Weights (≥ 0, sum 1) that best reproduce the chair's forecast as a weighted average of the members' forecasts in log-odds; equal weights = the logit pool. 95% bootstrap intervals resample questions within source. Descriptive; uses no outcomes.

## Weights

| setup | member | n | weight | ci_low | ci_high | equal_weight |
|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | gemma2:9b | 1039 | 0.159 | 0.114 | 0.209 | 0.2 |
| council:chair=llama3.1:8b | llama3.1:8b | 1039 | 0.277 | 0.228 | 0.326 | 0.2 |
| council:chair=llama3.1:8b | mistral:latest | 1039 | 0.27 | 0.215 | 0.328 | 0.2 |
| council:chair=llama3.1:8b | phi3:medium | 1039 | 0.224 | 0.181 | 0.275 | 0.2 |
| council:chair=llama3.1:8b | qwen3:8b | 1039 | 0.07 | 0.047 | 0.092 | 0.2 |
| council:chair=qwen3:8b | gemma2:9b | 1039 | 0.171 | 0.099 | 0.241 | 0.2 |
| council:chair=qwen3:8b | llama3.1:8b | 1039 | 0.229 | 0.135 | 0.342 | 0.2 |
| council:chair=qwen3:8b | mistral:latest | 1039 | 0.224 | 0.165 | 0.283 | 0.2 |
| council:chair=qwen3:8b | phi3:medium | 1039 | 0.109 | 0.043 | 0.169 | 0.2 |
| council:chair=qwen3:8b | qwen3:8b | 1039 | 0.267 | 0.224 | 0.308 | 0.2 |


## Fit, and which member the chair lands closest to

| setup | n | rmse_fitted | rmse_equal_weights | nearest_gemma2:9b | nearest_llama3.1:8b | nearest_mistral:latest | nearest_phi3:medium | nearest_qwen3:8b |
|---|---|---|---|---|---|---|---|---|
| council:chair=llama3.1:8b | 1039 | 0.354 | 0.411 | 0.33 | 0.274 | 0.209 | 0.138 | 0.049 |
| council:chair=qwen3:8b | 1039 | 0.515 | 0.532 | 0.369 | 0.221 | 0.194 | 0.136 | 0.08 |


## Does a chair favour its own model?

| chair | versus_chairs | n | own_weight_minus_others | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| llama3.1:8b | qwen3:8b | 1039 | 0.047 | -0.121 | 0.175 | no clear difference |
| qwen3:8b | llama3.1:8b | 1039 | 0.197 | 0.151 | 0.243 | favours own model |
