# How the chair combines its members (settled + settled-ext)

Weights (≥ 0, sum 1) that best reproduce the chair's forecast as a weighted average of the members' forecasts in log-odds; equal weights = the logit pool. 95% bootstrap intervals resample questions within source. Descriptive; uses no outcomes.

## Weights

| setup | member | n | weight | ci_low | ci_high | equal_weight |
|---|---|---|---|---|---|---|
| council:chair=gemma2:9b | gemma2:9b | 1039 | 0.251 | 0.201 | 0.296 | 0.2 |
| council:chair=gemma2:9b | llama3.1:8b | 1039 | 0.171 | 0.128 | 0.217 | 0.2 |
| council:chair=gemma2:9b | mistral:latest | 1039 | 0.229 | 0.196 | 0.26 | 0.2 |
| council:chair=gemma2:9b | phi3:medium | 1039 | 0.149 | 0.118 | 0.179 | 0.2 |
| council:chair=gemma2:9b | qwen3:8b | 1039 | 0.199 | 0.176 | 0.225 | 0.2 |
| council:chair=llama3.1:8b | gemma2:9b | 1039 | 0.159 | 0.111 | 0.196 | 0.2 |
| council:chair=llama3.1:8b | llama3.1:8b | 1039 | 0.277 | 0.233 | 0.327 | 0.2 |
| council:chair=llama3.1:8b | mistral:latest | 1039 | 0.27 | 0.215 | 0.333 | 0.2 |
| council:chair=llama3.1:8b | phi3:medium | 1039 | 0.224 | 0.182 | 0.266 | 0.2 |
| council:chair=llama3.1:8b | qwen3:8b | 1039 | 0.07 | 0.046 | 0.095 | 0.2 |
| council:chair=mistral:latest | gemma2:9b | 1038 | 0.127 | 0.059 | 0.21 | 0.2 |
| council:chair=mistral:latest | llama3.1:8b | 1038 | 0.255 | 0.183 | 0.335 | 0.2 |
| council:chair=mistral:latest | mistral:latest | 1038 | 0.392 | 0.319 | 0.486 | 0.2 |
| council:chair=mistral:latest | phi3:medium | 1038 | 0.186 | 0.104 | 0.257 | 0.2 |
| council:chair=mistral:latest | qwen3:8b | 1038 | 0.04 | 0.006 | 0.076 | 0.2 |
| council:chair=phi3:medium | gemma2:9b | 1039 | 0.17 | 0.139 | 0.204 | 0.2 |
| council:chair=phi3:medium | llama3.1:8b | 1039 | 0.316 | 0.277 | 0.353 | 0.2 |
| council:chair=phi3:medium | mistral:latest | 1039 | 0.249 | 0.208 | 0.296 | 0.2 |
| council:chair=phi3:medium | phi3:medium | 1039 | 0.199 | 0.159 | 0.236 | 0.2 |
| council:chair=phi3:medium | qwen3:8b | 1039 | 0.066 | 0.047 | 0.089 | 0.2 |
| council:chair=qwen3:8b | gemma2:9b | 1039 | 0.171 | 0.095 | 0.248 | 0.2 |
| council:chair=qwen3:8b | llama3.1:8b | 1039 | 0.229 | 0.127 | 0.329 | 0.2 |
| council:chair=qwen3:8b | mistral:latest | 1039 | 0.224 | 0.164 | 0.283 | 0.2 |
| council:chair=qwen3:8b | phi3:medium | 1039 | 0.109 | 0.043 | 0.164 | 0.2 |
| council:chair=qwen3:8b | qwen3:8b | 1039 | 0.267 | 0.222 | 0.317 | 0.2 |
| council:numbers-only:chair=llama3.1:8b | gemma2:9b | 1039 | 0.168 | 0.127 | 0.199 | 0.2 |
| council:numbers-only:chair=llama3.1:8b | llama3.1:8b | 1039 | 0.338 | 0.26 | 0.44 | 0.2 |
| council:numbers-only:chair=llama3.1:8b | mistral:latest | 1039 | 0.19 | 0.162 | 0.227 | 0.2 |
| council:numbers-only:chair=llama3.1:8b | phi3:medium | 1039 | 0.239 | 0.182 | 0.294 | 0.2 |
| council:numbers-only:chair=llama3.1:8b | qwen3:8b | 1039 | 0.066 | 0.052 | 0.08 | 0.2 |
| council:numbers-only:chair=qwen3:8b | gemma2:9b | 1039 | 0.331 | 0.243 | 0.436 | 0.2 |
| council:numbers-only:chair=qwen3:8b | llama3.1:8b | 1039 | 0.193 | 0.111 | 0.262 | 0.2 |
| council:numbers-only:chair=qwen3:8b | mistral:latest | 1039 | 0.231 | 0.153 | 0.312 | 0.2 |
| council:numbers-only:chair=qwen3:8b | phi3:medium | 1039 | 0.176 | 0.112 | 0.249 | 0.2 |
| council:numbers-only:chair=qwen3:8b | qwen3:8b | 1039 | 0.069 | 0.043 | 0.1 | 0.2 |
| council:reasoning-only:chair=llama3.1:8b | gemma2:9b | 1039 | 0.072 | 0.012 | 0.133 | 0.2 |
| council:reasoning-only:chair=llama3.1:8b | llama3.1:8b | 1039 | 0.348 | 0.294 | 0.416 | 0.2 |
| council:reasoning-only:chair=llama3.1:8b | mistral:latest | 1039 | 0.234 | 0.186 | 0.29 | 0.2 |
| council:reasoning-only:chair=llama3.1:8b | phi3:medium | 1039 | 0.205 | 0.158 | 0.241 | 0.2 |
| council:reasoning-only:chair=llama3.1:8b | qwen3:8b | 1039 | 0.142 | 0.112 | 0.182 | 0.2 |
| council:reasoning-only:chair=qwen3:8b | gemma2:9b | 1039 | 0.107 | 0.029 | 0.166 | 0.2 |
| council:reasoning-only:chair=qwen3:8b | llama3.1:8b | 1039 | 0.083 | 0.004 | 0.168 | 0.2 |
| council:reasoning-only:chair=qwen3:8b | mistral:latest | 1039 | 0.191 | 0.109 | 0.293 | 0.2 |
| council:reasoning-only:chair=qwen3:8b | phi3:medium | 1039 | 0.13 | 0.047 | 0.204 | 0.2 |
| council:reasoning-only:chair=qwen3:8b | qwen3:8b | 1039 | 0.49 | 0.442 | 0.532 | 0.2 |


## Fit, and which member the chair lands closest to

| setup | n | rmse_fitted | rmse_equal_weights | nearest_gemma2:9b | nearest_llama3.1:8b | nearest_mistral:latest | nearest_phi3:medium | nearest_qwen3:8b |
|---|---|---|---|---|---|---|---|---|
| council:chair=gemma2:9b | 1039 | 0.34 | 0.346 | 0.388 | 0.214 | 0.192 | 0.132 | 0.075 |
| council:chair=llama3.1:8b | 1039 | 0.354 | 0.411 | 0.33 | 0.274 | 0.209 | 0.138 | 0.049 |
| council:chair=mistral:latest | 1038 | 0.632 | 0.699 | 0.314 | 0.249 | 0.213 | 0.155 | 0.069 |
| council:chair=phi3:medium | 1039 | 0.331 | 0.394 | 0.363 | 0.279 | 0.169 | 0.141 | 0.047 |
| council:chair=qwen3:8b | 1039 | 0.515 | 0.532 | 0.369 | 0.221 | 0.194 | 0.136 | 0.08 |
| council:numbers-only:chair=llama3.1:8b | 1039 | 0.303 | 0.374 | 0.361 | 0.261 | 0.183 | 0.153 | 0.042 |
| council:numbers-only:chair=qwen3:8b | 1039 | 0.415 | 0.459 | 0.398 | 0.244 | 0.169 | 0.141 | 0.047 |
| council:reasoning-only:chair=llama3.1:8b | 1039 | 0.61 | 0.632 | 0.261 | 0.311 | 0.203 | 0.135 | 0.09 |
| council:reasoning-only:chair=qwen3:8b | 1039 | 0.746 | 0.857 | 0.358 | 0.2 | 0.133 | 0.115 | 0.193 |


## Does a chair favour its own model?

| chair | versus_chairs | n | own_weight_minus_others | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|
| gemma2:9b | llama3.1:8b, mistral:latest, phi3:medium, qwen3:8b | 1038 | 0.095 | 0.063 | 0.132 | favours own model |
| llama3.1:8b | gemma2:9b, mistral:latest, phi3:medium, qwen3:8b | 1038 | 0.034 | -0.025 | 0.088 | no clear difference |
| mistral:latest | gemma2:9b, llama3.1:8b, phi3:medium, qwen3:8b | 1038 | 0.149 | 0.079 | 0.215 | favours own model |
| phi3:medium | gemma2:9b, llama3.1:8b, mistral:latest, qwen3:8b | 1038 | 0.032 | 0.001 | 0.058 | favours own model |
| qwen3:8b | gemma2:9b, llama3.1:8b, mistral:latest, phi3:medium | 1038 | 0.173 | 0.13 | 0.215 | favours own model |
