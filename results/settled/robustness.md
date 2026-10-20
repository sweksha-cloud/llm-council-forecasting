# Robustness: settled

Each cut splits the 359 scored questions into groups and re-scores inside each. Paired rows: council minus reference on the questions both answered (negative = council better), 95% bootstrap interval; groups under 30 questions get no interval. Topics with fewer than 30 questions are grouped as Other.

## Council vs references, by group

| cut | group | council | versus | n | mean_diff | ci_low | ci_high | verdict |
|---|---|---|---|---|---|---|---|---|
| source | kalshi | council:chair=llama3.1:8b | baseline:mean | 200 | 0.0 | -0.0084 | 0.0089 | no clear difference |
| source | kalshi | council:chair=llama3.1:8b | baseline:logit_pool | 200 | -0.0092 | -0.0235 | 0.0055 | no clear difference |
| source | kalshi | council:chair=llama3.1:8b | baseline:best_single | 200 | -0.0155 | -0.0376 | 0.0043 | no clear difference |
| source | kalshi | council:chair=llama3.1:8b | market | 200 | 0.1209 | 0.0871 | 0.1568 | council worse |
| source | kalshi | council:chair=llama3.1:8b | baseline:always_no | 200 | -0.1942 | -0.2589 | -0.1269 | council better |
| source | kalshi | council:chair=qwen3:8b | baseline:mean | 200 | 0.0103 | -0.0009 | 0.0225 | no clear difference |
| source | kalshi | council:chair=qwen3:8b | baseline:logit_pool | 200 | 0.001 | -0.0095 | 0.0121 | no clear difference |
| source | kalshi | council:chair=qwen3:8b | baseline:best_single | 200 | -0.0053 | -0.0316 | 0.0192 | no clear difference |
| source | kalshi | council:chair=qwen3:8b | market | 200 | 0.1312 | 0.0936 | 0.1711 | council worse |
| source | kalshi | council:chair=qwen3:8b | baseline:always_no | 200 | -0.1839 | -0.2469 | -0.1183 | council better |
| source | polymarket | council:chair=llama3.1:8b | baseline:mean | 159 | 0.0049 | -0.0027 | 0.0135 | no clear difference |
| source | polymarket | council:chair=llama3.1:8b | baseline:logit_pool | 159 | -0.0008 | -0.015 | 0.0129 | no clear difference |
| source | polymarket | council:chair=llama3.1:8b | baseline:best_single | 159 | 0.0107 | -0.0109 | 0.0325 | no clear difference |
| source | polymarket | council:chair=llama3.1:8b | market | 159 | 0.0949 | 0.0554 | 0.1328 | council worse |
| source | polymarket | council:chair=llama3.1:8b | baseline:always_no | 159 | -0.2478 | -0.3242 | -0.1692 | council better |
| source | polymarket | council:chair=qwen3:8b | baseline:mean | 159 | 0.0107 | 0.003 | 0.0208 | council worse |
| source | polymarket | council:chair=qwen3:8b | baseline:logit_pool | 159 | 0.005 | -0.0065 | 0.0148 | no clear difference |
| source | polymarket | council:chair=qwen3:8b | baseline:best_single | 159 | 0.0165 | -0.0069 | 0.0416 | no clear difference |
| source | polymarket | council:chair=qwen3:8b | market | 159 | 0.1007 | 0.0605 | 0.1428 | council worse |
| source | polymarket | council:chair=qwen3:8b | baseline:always_no | 159 | -0.2419 | -0.318 | -0.1673 | council better |
| topic | Elections | council:chair=llama3.1:8b | baseline:mean | 72 | 0.0063 | -0.0051 | 0.0183 | no clear difference |
| topic | Elections | council:chair=llama3.1:8b | baseline:logit_pool | 72 | -0.0014 | -0.0243 | 0.0199 | no clear difference |
| topic | Elections | council:chair=llama3.1:8b | baseline:best_single | 72 | -0.0225 | -0.0578 | 0.0103 | no clear difference |
| topic | Elections | council:chair=llama3.1:8b | market | 72 | 0.1318 | 0.0538 | 0.1964 | council worse |
| topic | Elections | council:chair=llama3.1:8b | baseline:always_no | 72 | -0.1151 | -0.2167 | -0.0163 | council better |
| topic | Elections | council:chair=qwen3:8b | baseline:mean | 72 | 0.017 | 0.0012 | 0.0341 | council worse |
| topic | Elections | council:chair=qwen3:8b | baseline:logit_pool | 72 | 0.0092 | -0.0072 | 0.0271 | no clear difference |
| topic | Elections | council:chair=qwen3:8b | baseline:best_single | 72 | -0.0119 | -0.056 | 0.0287 | no clear difference |
| topic | Elections | council:chair=qwen3:8b | market | 72 | 0.1424 | 0.0665 | 0.2093 | council worse |
| topic | Elections | council:chair=qwen3:8b | baseline:always_no | 72 | -0.1045 | -0.2029 | -0.0088 | council better |
| topic | Other | council:chair=llama3.1:8b | baseline:mean | 73 | 0.012 | -0.003 | 0.0275 | no clear difference |
| topic | Other | council:chair=llama3.1:8b | baseline:logit_pool | 73 | 0.0048 | -0.0174 | 0.0269 | no clear difference |
| topic | Other | council:chair=llama3.1:8b | baseline:best_single | 73 | 0.0253 | -0.0134 | 0.0604 | no clear difference |
| topic | Other | council:chair=llama3.1:8b | market | 73 | 0.1202 | 0.0503 | 0.1909 | council worse |
| topic | Other | council:chair=llama3.1:8b | baseline:always_no | 73 | -0.0969 | -0.2054 | 0.0184 | no clear difference |
| topic | Other | council:chair=qwen3:8b | baseline:mean | 73 | 0.0157 | -0.0028 | 0.0341 | no clear difference |
| topic | Other | council:chair=qwen3:8b | baseline:logit_pool | 73 | 0.0085 | -0.0167 | 0.0305 | no clear difference |
| topic | Other | council:chair=qwen3:8b | baseline:best_single | 73 | 0.029 | -0.0166 | 0.0713 | no clear difference |
| topic | Other | council:chair=qwen3:8b | market | 73 | 0.1239 | 0.0488 | 0.2012 | council worse |
| topic | Other | council:chair=qwen3:8b | baseline:always_no | 73 | -0.0932 | -0.2043 | 0.0156 | no clear difference |
| topic | Politics | council:chair=llama3.1:8b | baseline:mean | 66 | 0.0016 | -0.0167 | 0.0208 | no clear difference |
| topic | Politics | council:chair=llama3.1:8b | baseline:logit_pool | 66 | -0.0078 | -0.04 | 0.0195 | no clear difference |
| topic | Politics | council:chair=llama3.1:8b | baseline:best_single | 66 | -0.0065 | -0.0494 | 0.0311 | no clear difference |
| topic | Politics | council:chair=llama3.1:8b | market | 66 | 0.1621 | 0.0918 | 0.2281 | council worse |
| topic | Politics | council:chair=llama3.1:8b | baseline:always_no | 66 | -0.1207 | -0.221 | -0.02 | council better |
| topic | Politics | council:chair=qwen3:8b | baseline:mean | 66 | 0.0134 | -0.0035 | 0.0343 | no clear difference |
| topic | Politics | council:chair=qwen3:8b | baseline:logit_pool | 66 | 0.004 | -0.0088 | 0.0174 | no clear difference |
| topic | Politics | council:chair=qwen3:8b | baseline:best_single | 66 | 0.0053 | -0.0415 | 0.0489 | no clear difference |
| topic | Politics | council:chair=qwen3:8b | market | 66 | 0.1739 | 0.0971 | 0.2488 | council worse |
| topic | Politics | council:chair=qwen3:8b | baseline:always_no | 66 | -0.1089 | -0.2048 | -0.0135 | council better |
| topic | Sports | council:chair=llama3.1:8b | baseline:mean | 148 | -0.0044 | -0.0119 | 0.0029 | no clear difference |
| topic | Sports | council:chair=llama3.1:8b | baseline:logit_pool | 148 | -0.0116 | -0.0271 | 0.0014 | no clear difference |
| topic | Sports | council:chair=llama3.1:8b | baseline:best_single | 148 | -0.0082 | -0.0258 | 0.0085 | no clear difference |
| topic | Sports | council:chair=llama3.1:8b | market | 148 | 0.0696 | 0.0443 | 0.0973 | council worse |
| topic | Sports | council:chair=llama3.1:8b | baseline:always_no | 148 | -0.371 | -0.4465 | -0.2921 | council better |
| topic | Sports | council:chair=qwen3:8b | baseline:mean | 148 | 0.0035 | -0.0048 | 0.0138 | no clear difference |
| topic | Sports | council:chair=qwen3:8b | baseline:logit_pool | 148 | -0.0037 | -0.0158 | 0.0055 | no clear difference |
| topic | Sports | council:chair=qwen3:8b | baseline:best_single | 148 | -0.0003 | -0.0204 | 0.0195 | no clear difference |
| topic | Sports | council:chair=qwen3:8b | market | 148 | 0.0775 | 0.0477 | 0.1091 | council worse |
| topic | Sports | council:chair=qwen3:8b | baseline:always_no | 148 | -0.3631 | -0.4391 | -0.2873 | council better |
| horizon | 8-30 days | council:chair=llama3.1:8b | baseline:mean | 130 | 0.0067 | -0.0029 | 0.0175 | no clear difference |
| horizon | 8-30 days | council:chair=llama3.1:8b | baseline:logit_pool | 130 | -0.0 | -0.019 | 0.0158 | no clear difference |
| horizon | 8-30 days | council:chair=llama3.1:8b | baseline:best_single | 130 | 0.0114 | -0.0152 | 0.0366 | no clear difference |
| horizon | 8-30 days | council:chair=llama3.1:8b | market | 130 | 0.1027 | 0.0578 | 0.1478 | council worse |
| horizon | 8-30 days | council:chair=llama3.1:8b | baseline:always_no | 130 | -0.256 | -0.3441 | -0.1695 | council better |
| horizon | 8-30 days | council:chair=qwen3:8b | baseline:mean | 130 | 0.0116 | 0.0023 | 0.0226 | council worse |
| horizon | 8-30 days | council:chair=qwen3:8b | baseline:logit_pool | 130 | 0.0048 | -0.0086 | 0.0159 | no clear difference |
| horizon | 8-30 days | council:chair=qwen3:8b | baseline:best_single | 130 | 0.0162 | -0.0119 | 0.0443 | no clear difference |
| horizon | 8-30 days | council:chair=qwen3:8b | market | 130 | 0.1076 | 0.0624 | 0.1548 | council worse |
| horizon | 8-30 days | council:chair=qwen3:8b | baseline:always_no | 130 | -0.2512 | -0.3381 | -0.1677 | council better |
| horizon | <=7 days | council:chair=llama3.1:8b | baseline:mean | 228 | -0.0006 | -0.0091 | 0.0073 | no clear difference |
| horizon | <=7 days | council:chair=llama3.1:8b | baseline:logit_pool | 228 | -0.0089 | -0.0229 | 0.0041 | no clear difference |
| horizon | <=7 days | council:chair=llama3.1:8b | baseline:best_single | 228 | -0.0133 | -0.0335 | 0.0042 | no clear difference |
| horizon | <=7 days | council:chair=llama3.1:8b | market | 228 | 0.1128 | 0.0809 | 0.1476 | council worse |
| horizon | <=7 days | council:chair=llama3.1:8b | baseline:always_no | 228 | -0.198 | -0.2603 | -0.1365 | council better |
| horizon | <=7 days | council:chair=qwen3:8b | baseline:mean | 228 | 0.0099 | 0.0007 | 0.0207 | council worse |
| horizon | <=7 days | council:chair=qwen3:8b | baseline:logit_pool | 228 | 0.0016 | -0.0081 | 0.0119 | no clear difference |
| horizon | <=7 days | council:chair=qwen3:8b | baseline:best_single | 228 | -0.0028 | -0.0263 | 0.0191 | no clear difference |
| horizon | <=7 days | council:chair=qwen3:8b | market | 228 | 0.1233 | 0.0879 | 0.1616 | council worse |
| horizon | <=7 days | council:chair=qwen3:8b | baseline:always_no | 228 | -0.1875 | -0.2482 | -0.1296 | council better |
| horizon | >30 days | council:chair=llama3.1:8b | baseline:mean | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=llama3.1:8b | baseline:logit_pool | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=llama3.1:8b | baseline:best_single | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=llama3.1:8b | market | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=llama3.1:8b | baseline:always_no | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=qwen3:8b | baseline:mean | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=qwen3:8b | baseline:logit_pool | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=qwen3:8b | baseline:best_single | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=qwen3:8b | market | 1 |  |  |  | too few (< 30) |
| horizon | >30 days | council:chair=qwen3:8b | baseline:always_no | 1 |  |  |  | too few (< 30) |
| extremity | leaning | council:chair=llama3.1:8b | baseline:mean | 91 | -0.0004 | -0.0168 | 0.015 | no clear difference |
| extremity | leaning | council:chair=llama3.1:8b | baseline:logit_pool | 91 | -0.0109 | -0.0397 | 0.0133 | no clear difference |
| extremity | leaning | council:chair=llama3.1:8b | baseline:best_single | 91 | -0.0086 | -0.0461 | 0.0235 | no clear difference |
| extremity | leaning | council:chair=llama3.1:8b | market | 91 | 0.1429 | 0.083 | 0.2045 | council worse |
| extremity | leaning | council:chair=llama3.1:8b | baseline:always_no | 91 | -0.2102 | -0.3127 | -0.1123 | council better |
| extremity | leaning | council:chair=qwen3:8b | baseline:mean | 91 | 0.0166 | 0.0002 | 0.0343 | council worse |
| extremity | leaning | council:chair=qwen3:8b | baseline:logit_pool | 91 | 0.0061 | -0.0067 | 0.0179 | no clear difference |
| extremity | leaning | council:chair=qwen3:8b | baseline:best_single | 91 | 0.0083 | -0.0287 | 0.0445 | no clear difference |
| extremity | leaning | council:chair=qwen3:8b | market | 91 | 0.1598 | 0.0932 | 0.2309 | council worse |
| extremity | leaning | council:chair=qwen3:8b | baseline:always_no | 91 | -0.1933 | -0.2916 | -0.0998 | council better |
| extremity | near-certain | council:chair=llama3.1:8b | baseline:mean | 105 | 0.0119 | 0.002 | 0.0221 | council worse |
| extremity | near-certain | council:chair=llama3.1:8b | baseline:logit_pool | 105 | 0.007 | -0.0123 | 0.024 | no clear difference |
| extremity | near-certain | council:chair=llama3.1:8b | baseline:best_single | 105 | -0.0115 | -0.0447 | 0.0193 | no clear difference |
| extremity | near-certain | council:chair=llama3.1:8b | market | 105 | 0.1796 | 0.1285 | 0.2296 | council worse |
| extremity | near-certain | council:chair=llama3.1:8b | baseline:always_no | 105 | -0.0313 | -0.1098 | 0.0442 | no clear difference |
| extremity | near-certain | council:chair=qwen3:8b | baseline:mean | 105 | 0.0109 | -0.0016 | 0.0252 | no clear difference |
| extremity | near-certain | council:chair=qwen3:8b | baseline:logit_pool | 105 | 0.006 | -0.0103 | 0.0205 | no clear difference |
| extremity | near-certain | council:chair=qwen3:8b | baseline:best_single | 105 | -0.0125 | -0.051 | 0.0227 | no clear difference |
| extremity | near-certain | council:chair=qwen3:8b | market | 105 | 0.1786 | 0.127 | 0.2297 | council worse |
| extremity | near-certain | council:chair=qwen3:8b | baseline:always_no | 105 | -0.0323 | -0.1086 | 0.0454 | no clear difference |
| extremity | uncertain | council:chair=llama3.1:8b | baseline:mean | 163 | -0.0026 | -0.0104 | 0.0054 | no clear difference |
| extremity | uncertain | council:chair=llama3.1:8b | baseline:logit_pool | 163 | -0.0106 | -0.0239 | 0.002 | no clear difference |
| extremity | uncertain | council:chair=llama3.1:8b | baseline:best_single | 163 | 0.0036 | -0.0151 | 0.0225 | no clear difference |
| extremity | uncertain | council:chair=llama3.1:8b | market | 163 | 0.0455 | 0.0146 | 0.0785 | council worse |
| extremity | uncertain | council:chair=llama3.1:8b | baseline:always_no | 163 | -0.3424 | -0.4256 | -0.2588 | council better |
| extremity | uncertain | council:chair=qwen3:8b | baseline:mean | 163 | 0.0068 | -0.0026 | 0.0169 | no clear difference |
| extremity | uncertain | council:chair=qwen3:8b | baseline:logit_pool | 163 | -0.0011 | -0.0145 | 0.0111 | no clear difference |
| extremity | uncertain | council:chair=qwen3:8b | baseline:best_single | 163 | 0.013 | -0.0081 | 0.0357 | no clear difference |
| extremity | uncertain | council:chair=qwen3:8b | market | 163 | 0.0549 | 0.0207 | 0.0917 | council worse |
| extremity | uncertain | council:chair=qwen3:8b | baseline:always_no | 163 | -0.333 | -0.412 | -0.2525 | council better |


## Every setup, by group

| cut | group | setup | n | brier | accuracy | skill_vs_market |
|---|---|---|---|---|---|---|
| source | kalshi | baseline:always_no | 200 | 0.45 | 0.55 | -2.3365 |
| source | kalshi | baseline:base_rate | 200 | 0.2481 | 0.55 | -0.8392 |
| source | kalshi | baseline:best_single | 200 | 0.2713 | 0.56 | -1.0118 |
| source | kalshi | baseline:extremized(a=2) | 200 | 0.3029 | 0.5775 | -1.2458 |
| source | kalshi | baseline:logit_pool | 200 | 0.265 | 0.5775 | -0.965 |
| source | kalshi | baseline:mean | 200 | 0.2558 | 0.5825 | -0.8966 |
| source | kalshi | baseline:median | 200 | 0.2703 | 0.56 | -1.0044 |
| source | kalshi | council:chair=llama3.1:8b | 200 | 0.2558 | 0.5725 | -0.8967 |
| source | kalshi | council:chair=qwen3:8b | 200 | 0.2661 | 0.5775 | -0.9727 |
| source | kalshi | market | 200 | 0.1349 | 0.805 |  |
| source | kalshi | single:deepseek-r1:8b | 200 | 0.3039 | 0.55 | -1.2536 |
| source | kalshi | single:gemma2:9b | 200 | 0.2827 | 0.5525 | -1.0963 |
| source | kalshi | single:llama3.1:8b | 200 | 0.2742 | 0.5325 | -1.0328 |
| source | kalshi | single:mistral:latest | 200 | 0.2643 | 0.5725 | -0.9599 |
| source | kalshi | single:phi3:medium | 200 | 0.2713 | 0.56 | -1.0118 |
| source | kalshi | single:qwen3:8b | 200 | 0.3039 | 0.5575 | -1.2536 |
| source | polymarket | baseline:always_no | 159 | 0.5031 | 0.4969 | -2.1347 |
| source | polymarket | baseline:base_rate | 159 | 0.2509 | 0.4969 | -0.5629 |
| source | polymarket | baseline:best_single | 159 | 0.2447 | 0.5849 | -0.5247 |
| source | polymarket | baseline:extremized(a=2) | 159 | 0.2826 | 0.5692 | -0.7606 |
| source | polymarket | baseline:logit_pool | 159 | 0.2562 | 0.5692 | -0.5964 |
| source | polymarket | baseline:mean | 159 | 0.2505 | 0.5597 | -0.5605 |
| source | polymarket | baseline:median | 159 | 0.2541 | 0.544 | -0.5834 |
| source | polymarket | council:chair=llama3.1:8b | 159 | 0.2554 | 0.5692 | -0.5911 |
| source | polymarket | council:chair=qwen3:8b | 159 | 0.2612 | 0.566 | -0.6274 |
| source | polymarket | market | 159 | 0.1605 | 0.7579 |  |
| source | polymarket | single:deepseek-r1:8b | 159 | 0.2737 | 0.4937 | -0.7052 |
| source | polymarket | single:gemma2:9b | 159 | 0.2573 | 0.5629 | -0.6032 |
| source | polymarket | single:llama3.1:8b | 159 | 0.2672 | 0.4686 | -0.6649 |
| source | polymarket | single:mistral:latest | 159 | 0.2854 | 0.5629 | -0.7784 |
| source | polymarket | single:phi3:medium | 159 | 0.2447 | 0.5849 | -0.5247 |
| source | polymarket | single:qwen3:8b | 159 | 0.2724 | 0.5472 | -0.6971 |
| topic | Elections | baseline:always_no | 72 | 0.375 | 0.625 | -1.9281 |
| topic | Elections | baseline:base_rate | 72 | 0.2441 | 0.625 | -0.9059 |
| topic | Elections | baseline:best_single | 72 | 0.2824 | 0.5764 | -1.2047 |
| topic | Elections | baseline:extremized(a=2) | 72 | 0.3074 | 0.5833 | -1.4006 |
| topic | Elections | baseline:logit_pool | 72 | 0.2613 | 0.5833 | -1.0403 |
| topic | Elections | baseline:mean | 72 | 0.2535 | 0.5833 | -0.9798 |
| topic | Elections | baseline:median | 72 | 0.2664 | 0.5556 | -1.0798 |
| topic | Elections | council:chair=llama3.1:8b | 72 | 0.2599 | 0.5833 | -1.0293 |
| topic | Elections | council:chair=qwen3:8b | 72 | 0.2705 | 0.5764 | -1.1122 |
| topic | Elections | market | 72 | 0.1281 | 0.8472 |  |
| topic | Elections | single:deepseek-r1:8b | 72 | 0.3143 | 0.5278 | -1.4542 |
| topic | Elections | single:gemma2:9b | 72 | 0.2761 | 0.5417 | -1.1557 |
| topic | Elections | single:llama3.1:8b | 72 | 0.2636 | 0.5764 | -1.0586 |
| topic | Elections | single:mistral:latest | 72 | 0.2489 | 0.5764 | -0.9431 |
| topic | Elections | single:phi3:medium | 72 | 0.2824 | 0.5764 | -1.2047 |
| topic | Elections | single:qwen3:8b | 72 | 0.3061 | 0.5694 | -1.3902 |
| topic | Other | baseline:always_no | 73 | 0.3836 | 0.6164 | -1.3041 |
| topic | Other | baseline:base_rate | 73 | 0.2445 | 0.6164 | -0.4689 |
| topic | Other | baseline:best_single | 73 | 0.2614 | 0.5342 | -0.5701 |
| topic | Other | baseline:extremized(a=2) | 73 | 0.3351 | 0.5205 | -1.0131 |
| topic | Other | baseline:logit_pool | 73 | 0.2818 | 0.5205 | -0.693 |
| topic | Other | baseline:mean | 73 | 0.2746 | 0.5205 | -0.6497 |
| topic | Other | baseline:median | 73 | 0.2918 | 0.5 | -0.7527 |
| topic | Other | council:chair=llama3.1:8b | 73 | 0.2867 | 0.4795 | -0.7221 |
| topic | Other | council:chair=qwen3:8b | 73 | 0.2904 | 0.5137 | -0.7443 |
| topic | Other | market | 73 | 0.1665 | 0.7808 |  |
| topic | Other | single:deepseek-r1:8b | 73 | 0.3107 | 0.5 | -0.8661 |
| topic | Other | single:gemma2:9b | 73 | 0.2977 | 0.5137 | -0.7881 |
| topic | Other | single:llama3.1:8b | 73 | 0.3149 | 0.3973 | -0.8917 |
| topic | Other | single:mistral:latest | 73 | 0.3179 | 0.4658 | -0.9097 |
| topic | Other | single:phi3:medium | 73 | 0.2614 | 0.5342 | -0.5701 |
| topic | Other | single:qwen3:8b | 73 | 0.3226 | 0.5068 | -0.9381 |
| topic | Politics | baseline:always_no | 66 | 0.3788 | 0.6212 | -2.947 |
| topic | Politics | baseline:base_rate | 66 | 0.2443 | 0.6212 | -1.5455 |
| topic | Politics | baseline:best_single | 66 | 0.2646 | 0.5606 | -1.757 |
| topic | Politics | baseline:extremized(a=2) | 66 | 0.3135 | 0.6061 | -2.2662 |
| topic | Politics | baseline:logit_pool | 66 | 0.2659 | 0.6061 | -1.7706 |
| topic | Politics | baseline:mean | 66 | 0.2565 | 0.5758 | -1.6731 |
| topic | Politics | baseline:median | 66 | 0.2694 | 0.5758 | -1.8067 |
| topic | Politics | council:chair=llama3.1:8b | 66 | 0.2581 | 0.5303 | -1.6893 |
| topic | Politics | council:chair=qwen3:8b | 66 | 0.2699 | 0.553 | -1.8124 |
| topic | Politics | market | 66 | 0.096 | 0.8636 |  |
| topic | Politics | single:deepseek-r1:8b | 66 | 0.2835 | 0.6288 | -1.9545 |
| topic | Politics | single:gemma2:9b | 66 | 0.283 | 0.5758 | -1.9492 |
| topic | Politics | single:llama3.1:8b | 66 | 0.2614 | 0.5455 | -1.7241 |
| topic | Politics | single:mistral:latest | 66 | 0.3185 | 0.5379 | -2.319 |
| topic | Politics | single:phi3:medium | 66 | 0.2646 | 0.5606 | -1.757 |
| topic | Politics | single:qwen3:8b | 66 | 0.2759 | 0.6212 | -1.8744 |
| topic | Sports | baseline:always_no | 148 | 0.6081 | 0.3919 | -2.6308 |
| topic | Sports | baseline:base_rate | 148 | 0.2564 | 0.3919 | -0.531 |
| topic | Sports | baseline:best_single | 148 | 0.2453 | 0.5912 | -0.4646 |
| topic | Sports | baseline:extremized(a=2) | 148 | 0.2583 | 0.5811 | -0.542 |
| topic | Sports | baseline:logit_pool | 148 | 0.2487 | 0.5811 | -0.4849 |
| topic | Sports | baseline:mean | 148 | 0.2415 | 0.5912 | -0.4422 |
| topic | Sports | baseline:median | 148 | 0.2447 | 0.5676 | -0.4613 |
| topic | Sports | council:chair=llama3.1:8b | 148 | 0.2371 | 0.6284 | -0.4158 |
| topic | Sports | council:chair=qwen3:8b | 148 | 0.245 | 0.6081 | -0.4628 |
| topic | Sports | market | 148 | 0.1675 | 0.7196 |  |
| topic | Sports | single:deepseek-r1:8b | 148 | 0.2722 | 0.4899 | -0.6253 |
| topic | Sports | single:gemma2:9b | 148 | 0.2512 | 0.5777 | -0.4997 |
| topic | Sports | single:llama3.1:8b | 148 | 0.2574 | 0.5034 | -0.5369 |
| topic | Sports | single:mistral:latest | 148 | 0.244 | 0.6284 | -0.4566 |
| topic | Sports | single:phi3:medium | 148 | 0.2453 | 0.5912 | -0.4646 |
| topic | Sports | single:qwen3:8b | 148 | 0.2723 | 0.5372 | -0.6258 |
| horizon | 8-30 days | baseline:always_no | 130 | 0.5154 | 0.4846 | -2.2907 |
| horizon | 8-30 days | baseline:base_rate | 130 | 0.2515 | 0.4846 | -0.6059 |
| horizon | 8-30 days | baseline:best_single | 130 | 0.248 | 0.5654 | -0.5832 |
| horizon | 8-30 days | baseline:extremized(a=2) | 130 | 0.2855 | 0.5577 | -0.8232 |
| horizon | 8-30 days | baseline:logit_pool | 130 | 0.2594 | 0.5577 | -0.6562 |
| horizon | 8-30 days | baseline:mean | 130 | 0.2526 | 0.5538 | -0.6129 |
| horizon | 8-30 days | baseline:median | 130 | 0.255 | 0.5346 | -0.628 |
| horizon | 8-30 days | council:chair=llama3.1:8b | 130 | 0.2594 | 0.5577 | -0.656 |
| horizon | 8-30 days | council:chair=qwen3:8b | 130 | 0.2642 | 0.5538 | -0.6868 |
| horizon | 8-30 days | market | 130 | 0.1566 | 0.7577 |  |
| horizon | 8-30 days | single:deepseek-r1:8b | 130 | 0.2642 | 0.4885 | -0.6869 |
| horizon | 8-30 days | single:gemma2:9b | 130 | 0.2572 | 0.5577 | -0.642 |
| horizon | 8-30 days | single:llama3.1:8b | 130 | 0.2703 | 0.4423 | -0.7261 |
| horizon | 8-30 days | single:mistral:latest | 130 | 0.2868 | 0.55 | -0.8311 |
| horizon | 8-30 days | single:phi3:medium | 130 | 0.248 | 0.5654 | -0.5832 |
| horizon | 8-30 days | single:qwen3:8b | 130 | 0.2723 | 0.5385 | -0.7389 |
| horizon | <=7 days | baseline:always_no | 228 | 0.4518 | 0.5482 | -2.2066 |
| horizon | <=7 days | baseline:base_rate | 228 | 0.2481 | 0.5482 | -0.7613 |
| horizon | <=7 days | baseline:best_single | 228 | 0.267 | 0.5724 | -0.8953 |
| horizon | <=7 days | baseline:extremized(a=2) | 228 | 0.2996 | 0.5811 | -1.1267 |
| horizon | <=7 days | baseline:logit_pool | 228 | 0.2626 | 0.5811 | -0.8641 |
| horizon | <=7 days | baseline:mean | 228 | 0.2543 | 0.5811 | -0.8054 |
| horizon | <=7 days | baseline:median | 228 | 0.2685 | 0.5614 | -0.9055 |
| horizon | <=7 days | council:chair=llama3.1:8b | 228 | 0.2537 | 0.5768 | -0.8009 |
| horizon | <=7 days | council:chair=qwen3:8b | 228 | 0.2642 | 0.5811 | -0.8754 |
| horizon | <=7 days | market | 228 | 0.1409 | 0.7982 |  |
| horizon | <=7 days | single:deepseek-r1:8b | 228 | 0.3062 | 0.5439 | -1.1731 |
| horizon | <=7 days | single:gemma2:9b | 228 | 0.279 | 0.5592 | -0.9802 |
| horizon | <=7 days | single:llama3.1:8b | 228 | 0.2724 | 0.5373 | -0.9338 |
| horizon | <=7 days | single:mistral:latest | 228 | 0.2669 | 0.5768 | -0.8943 |
| horizon | <=7 days | single:phi3:medium | 228 | 0.267 | 0.5724 | -0.8953 |
| horizon | <=7 days | single:qwen3:8b | 228 | 0.3004 | 0.5592 | -1.1323 |
| horizon | >30 days | baseline:always_no | 1 | 0.0 | 1.0 |  |
| horizon | >30 days | baseline:base_rate | 1 | 0.2242 | 1.0 |  |
| horizon | >30 days | baseline:best_single | 1 | 0.0625 | 1.0 |  |
| horizon | >30 days | baseline:extremized(a=2) | 1 | 0.0768 | 1.0 |  |
| horizon | >30 days | baseline:logit_pool | 1 | 0.1462 | 1.0 |  |
| horizon | >30 days | baseline:mean | 1 | 0.1521 | 1.0 |  |
| horizon | >30 days | baseline:median | 1 | 0.1225 | 1.0 |  |
| horizon | >30 days | council:chair=llama3.1:8b | 1 | 0.2025 | 1.0 |  |
| horizon | >30 days | council:chair=qwen3:8b | 1 | 0.16 | 1.0 |  |
| horizon | >30 days | market | 1 | 0.0132 | 1.0 |  |
| horizon | >30 days | single:deepseek-r1:8b | 1 | 0.16 | 1.0 |  |
| horizon | >30 days | single:gemma2:9b | 1 | 0.4225 | 0.0 |  |
| horizon | >30 days | single:llama3.1:8b | 1 | 0.0625 | 1.0 |  |
| horizon | >30 days | single:mistral:latest | 1 | 0.1225 | 1.0 |  |
| horizon | >30 days | single:phi3:medium | 1 | 0.0625 | 1.0 |  |
| horizon | >30 days | single:qwen3:8b | 1 | 0.2025 | 1.0 |  |
| extremity | leaning | baseline:always_no | 91 | 0.4725 | 0.5275 | -2.9552 |
| extremity | leaning | baseline:base_rate | 91 | 0.2492 | 0.5275 | -1.0863 |
| extremity | leaning | baseline:best_single | 91 | 0.2709 | 0.5549 | -1.2678 |
| extremity | leaning | baseline:extremized(a=2) | 91 | 0.3102 | 0.5934 | -1.5967 |
| extremity | leaning | baseline:logit_pool | 91 | 0.2732 | 0.5934 | -1.2867 |
| extremity | leaning | baseline:mean | 91 | 0.2627 | 0.5769 | -1.199 |
| extremity | leaning | baseline:median | 91 | 0.2743 | 0.533 | -1.2961 |
| extremity | leaning | council:chair=llama3.1:8b | 91 | 0.2623 | 0.544 | -1.1958 |
| extremity | leaning | council:chair=qwen3:8b | 91 | 0.2793 | 0.5659 | -1.3376 |
| extremity | leaning | market | 91 | 0.1195 | 0.8681 |  |
| extremity | leaning | single:deepseek-r1:8b | 91 | 0.305 | 0.5165 | -1.5533 |
| extremity | leaning | single:gemma2:9b | 91 | 0.2741 | 0.5549 | -1.2942 |
| extremity | leaning | single:llama3.1:8b | 91 | 0.2826 | 0.511 | -1.3653 |
| extremity | leaning | single:mistral:latest | 91 | 0.2704 | 0.544 | -1.263 |
| extremity | leaning | single:phi3:medium | 91 | 0.2709 | 0.5549 | -1.2678 |
| extremity | leaning | single:qwen3:8b | 91 | 0.326 | 0.522 | -1.7289 |
| extremity | near-certain | baseline:always_no | 105 | 0.2571 | 0.7429 | -4.5606 |
| extremity | near-certain | baseline:base_rate | 105 | 0.2378 | 0.7429 | -4.1433 |
| extremity | near-certain | baseline:best_single | 105 | 0.2373 | 0.6381 | -4.1323 |
| extremity | near-certain | baseline:extremized(a=2) | 105 | 0.2453 | 0.6667 | -4.3041 |
| extremity | near-certain | baseline:logit_pool | 105 | 0.2189 | 0.6667 | -3.7325 |
| extremity | near-certain | baseline:mean | 105 | 0.214 | 0.6714 | -3.6268 |
| extremity | near-certain | baseline:median | 105 | 0.2191 | 0.681 | -3.7384 |
| extremity | near-certain | council:chair=llama3.1:8b | 105 | 0.2259 | 0.6286 | -3.884 |
| extremity | near-certain | council:chair=qwen3:8b | 105 | 0.2248 | 0.6429 | -3.8622 |
| extremity | near-certain | market | 105 | 0.0462 | 0.9524 |  |
| extremity | near-certain | single:deepseek-r1:8b | 105 | 0.2415 | 0.6429 | -4.2234 |
| extremity | near-certain | single:gemma2:9b | 105 | 0.2363 | 0.6714 | -4.1089 |
| extremity | near-certain | single:llama3.1:8b | 105 | 0.2274 | 0.6286 | -3.918 |
| extremity | near-certain | single:mistral:latest | 105 | 0.2492 | 0.6333 | -4.3888 |
| extremity | near-certain | single:phi3:medium | 105 | 0.2373 | 0.6381 | -4.1323 |
| extremity | near-certain | single:qwen3:8b | 105 | 0.2435 | 0.6095 | -4.2662 |
| extremity | uncertain | baseline:always_no | 163 | 0.6135 | 0.3865 | -1.7198 |
| extremity | uncertain | baseline:base_rate | 163 | 0.2567 | 0.3865 | -0.138 |
| extremity | uncertain | baseline:best_single | 163 | 0.2675 | 0.5368 | -0.1859 |
| extremity | uncertain | baseline:extremized(a=2) | 163 | 0.3161 | 0.5031 | -0.4014 |
| extremity | uncertain | baseline:logit_pool | 163 | 0.2816 | 0.5031 | -0.2485 |
| extremity | uncertain | baseline:mean | 163 | 0.2737 | 0.5061 | -0.2133 |
| extremity | uncertain | baseline:median | 163 | 0.2853 | 0.4816 | -0.2649 |
| extremity | uncertain | council:chair=llama3.1:8b | 163 | 0.2711 | 0.5491 | -0.2016 |
| extremity | uncertain | council:chair=qwen3:8b | 163 | 0.2805 | 0.5307 | -0.2436 |
| extremity | uncertain | market | 163 | 0.2256 | 0.6288 |  |
| extremity | uncertain | single:deepseek-r1:8b | 163 | 0.314 | 0.454 | -0.3922 |
| extremity | uncertain | single:gemma2:9b | 163 | 0.2927 | 0.4847 | -0.2977 |
| extremity | uncertain | single:llama3.1:8b | 163 | 0.2928 | 0.4202 | -0.2981 |
| extremity | uncertain | single:mistral:latest | 163 | 0.2913 | 0.5399 | -0.2915 |
| extremity | uncertain | single:phi3:medium | 163 | 0.2675 | 0.5368 | -0.1859 |
| extremity | uncertain | single:qwen3:8b | 163 | 0.2998 | 0.5337 | -0.3289 |
