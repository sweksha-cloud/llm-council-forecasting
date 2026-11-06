# Scale check: Llama 3.3 70B (settled)

Pre-registered in docs/decisions.md (2026-10-20). Paired Brier difference, 70B setup minus the other (negative = 70B better), 95% bootstrap interval stratified by source. The 70B council vs the mean and logit pools of its members is in [ablation.md](ablation.md).

## 70B council vs the 8B councils; 70B alone vs the best member, the mean pool and the market

| setup | versus | source | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|---|
| council:chair=llama3.3:70b | council:chair=gemma2:9b | all | 359 | -0.0017 | -0.0069 | 0.0038 | no clear difference |
| council:chair=llama3.3:70b | council:chair=gemma2:9b | kalshi | 200 | -0.0037 | -0.0122 | 0.0043 | no clear difference |
| council:chair=llama3.3:70b | council:chair=gemma2:9b | polymarket | 159 | 0.0007 | -0.0055 | 0.0073 | no clear difference |
| council:chair=llama3.3:70b | council:chair=llama3.1:8b | all | 359 | 0.0052 | -0.0028 | 0.0138 | no clear difference |
| council:chair=llama3.3:70b | council:chair=llama3.1:8b | kalshi | 200 | 0.0086 | -0.0027 | 0.0217 | no clear difference |
| council:chair=llama3.3:70b | council:chair=llama3.1:8b | polymarket | 159 | 0.0008 | -0.0107 | 0.0132 | no clear difference |
| council:chair=llama3.3:70b | council:chair=mistral:latest | all | 359 | 0.0009 | -0.0121 | 0.0142 | no clear difference |
| council:chair=llama3.3:70b | council:chair=mistral:latest | kalshi | 200 | 0.0103 | -0.0114 | 0.0316 | no clear difference |
| council:chair=llama3.3:70b | council:chair=mistral:latest | polymarket | 159 | -0.011 | -0.0234 | 0.0026 | no clear difference |
| council:chair=llama3.3:70b | council:chair=phi3:medium | all | 359 | 0.0067 | -0.0011 | 0.0152 | no clear difference |
| council:chair=llama3.3:70b | council:chair=phi3:medium | kalshi | 200 | 0.0084 | -0.0029 | 0.0212 | no clear difference |
| council:chair=llama3.3:70b | council:chair=phi3:medium | polymarket | 159 | 0.0047 | -0.0049 | 0.0159 | no clear difference |
| council:chair=llama3.3:70b | council:chair=qwen3:8b | all | 359 | -0.0031 | -0.0088 | 0.0022 | no clear difference |
| council:chair=llama3.3:70b | council:chair=qwen3:8b | kalshi | 200 | -0.0016 | -0.0101 | 0.0074 | no clear difference |
| council:chair=llama3.3:70b | council:chair=qwen3:8b | polymarket | 159 | -0.005 | -0.0113 | 0.0006 | no clear difference |
| single:llama3.3:70b | baseline:best_single | all | 359 | 0.0013 | -0.0201 | 0.0222 | no clear difference |
| single:llama3.3:70b | baseline:best_single | kalshi | 200 | 0.0038 | -0.0307 | 0.0357 | no clear difference |
| single:llama3.3:70b | baseline:best_single | polymarket | 159 | -0.0019 | -0.0303 | 0.0242 | no clear difference |
| single:llama3.3:70b | baseline:mean | all | 359 | 0.0074 | -0.009 | 0.0231 | no clear difference |
| single:llama3.3:70b | baseline:mean | kalshi | 200 | 0.0194 | -0.0046 | 0.0407 | no clear difference |
| single:llama3.3:70b | baseline:mean | polymarket | 159 | -0.0077 | -0.0304 | 0.0124 | no clear difference |
| single:llama3.3:70b | market | all | 359 | 0.1146 | 0.0884 | 0.1397 | 70B worse |
| single:llama3.3:70b | market | kalshi | 200 | 0.1403 | 0.1008 | 0.1818 | 70B worse |
| single:llama3.3:70b | market | polymarket | 159 | 0.0823 | 0.0452 | 0.1212 | 70B worse |
| council:chair=llama3.3:70b | market | all | 359 | 0.1146 | 0.0885 | 0.1403 | 70B worse |
| council:chair=llama3.3:70b | market | kalshi | 200 | 0.1296 | 0.092 | 0.1678 | 70B worse |
| council:chair=llama3.3:70b | market | polymarket | 159 | 0.0957 | 0.057 | 0.1368 | 70B worse |


## Does the 70B chair favour its own family's member?

| chair | own_family_member | versus_chairs | n | weight | own_weight_minus_others | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|---|---|
| llama3.3:70b | llama3.1:8b | gemma2:9b, llama3.1:8b, mistral:latest, phi3:medium, qwen3:8b | 359 | 0.264 | 0.049 | -0.032 | 0.138 | no clear difference |
