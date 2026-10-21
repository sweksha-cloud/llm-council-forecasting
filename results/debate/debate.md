# Debate, round 2 (settled)

Each member saw the others' first answers and could revise once. `debate:mean-r2` is the mean of the revised forecasts. Paired Brier difference, debate minus reference (negative = debate better), 95% bootstrap interval stratified by source.

## Debate vs references

| setup | versus | source | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|---|
| debate:mean-r2 | baseline:mean | all | 359 | 0.0051 | 0.0021 | 0.0083 | debate worse |
| debate:mean-r2 | baseline:mean | kalshi | 200 | 0.0042 | -0.0005 | 0.0091 | no clear difference |
| debate:mean-r2 | baseline:mean | polymarket | 159 | 0.0062 | 0.0026 | 0.0099 | debate worse |
| debate:mean-r2 | baseline:best_single | all | 359 | -0.001 | -0.0161 | 0.0134 | no clear difference |
| debate:mean-r2 | baseline:best_single | kalshi | 200 | -0.0114 | -0.0347 | 0.0087 | no clear difference |
| debate:mean-r2 | baseline:best_single | polymarket | 159 | 0.0119 | -0.0114 | 0.036 | no clear difference |
| debate:mean-r2 | market | all | 359 | 0.1123 | 0.0875 | 0.1376 | debate worse |
| debate:mean-r2 | market | kalshi | 200 | 0.1251 | 0.0885 | 0.1614 | debate worse |
| debate:mean-r2 | market | polymarket | 159 | 0.0962 | 0.0585 | 0.1341 | debate worse |
| debate:mean-r2 | council:chair=llama3.1:8b | all | 359 | 0.0029 | -0.0035 | 0.0095 | no clear difference |
| debate:mean-r2 | council:chair=llama3.1:8b | kalshi | 200 | 0.0042 | -0.0052 | 0.013 | no clear difference |
| debate:mean-r2 | council:chair=llama3.1:8b | polymarket | 159 | 0.0013 | -0.0078 | 0.0102 | no clear difference |
| debate:mean-r2 | council:chair=qwen3:8b | all | 359 | -0.0054 | -0.0122 | 0.0011 | no clear difference |
| debate:mean-r2 | council:chair=qwen3:8b | kalshi | 200 | -0.0061 | -0.0166 | 0.0046 | no clear difference |
| debate:mean-r2 | council:chair=qwen3:8b | polymarket | 159 | -0.0046 | -0.0141 | 0.0033 | no clear difference |


## How each member moved

| model | n | mean_abs_change | share_changed | share_moved_toward_outcome | brier_r1 | brier_r2 |
|---|---|---|---|---|---|---|
| gemma2:9b | 359 | 0.0566 | 0.8747 | 0.5223 | 0.2715 | 0.2663 |
| llama3.1:8b | 359 | 0.0087 | 0.2006 | 0.5417 | 0.2711 | 0.2707 |
| mistral:latest | 359 | 0.027 | 0.3844 | 0.413 | 0.2737 | 0.2758 |
| phi3:medium | 359 | 0.0426 | 0.571 | 0.5122 | 0.2595 | 0.2588 |
| qwen3:8b | 359 | 0.0346 | 0.3343 | 0.525 | 0.29 | 0.2909 |


## Spread between members, before and after

| n | member_sd_r1 | member_sd_r2 |
|---|---|---|
| 359 | 0.1216 | 0.1001 |
