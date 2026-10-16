# Robustness: settled-all

Each cut splits the 1042 scored questions into groups and re-scores inside each. Paired rows: council minus reference on the questions both answered (negative = council better), 95% bootstrap interval; groups under 30 questions get no interval. Topics with fewer than 30 questions are grouped as Other.

## Council vs references, by group

_none_


## Every setup, by group

| cut | group | setup | n | brier | accuracy | skill_vs_market |
|---|---|---|---|---|---|---|
| source | kalshi | baseline:always_no | 200 | 0.45 | 0.55 | -2.3365 |
| source | kalshi | baseline:base_rate | 200 | 0.2477 | 0.55 | -0.8364 |
| source | kalshi | market | 200 | 0.1349 | 0.805 |  |
| source | polymarket | baseline:always_no | 842 | 0.4335 | 0.5665 | -1.4499 |
| source | polymarket | baseline:base_rate | 842 | 0.2456 | 0.5665 | -0.3913 |
| source | polymarket | market | 840 | 0.1764 | 0.7238 |  |
| topic | Culture | baseline:always_no | 103 | 0.233 | 0.767 | -0.5682 |
| topic | Culture | baseline:base_rate | 103 | 0.2202 | 0.767 | -0.4819 |
| topic | Culture | market | 103 | 0.1486 | 0.8252 |  |
| topic | Elections | baseline:always_no | 83 | 0.3735 | 0.6265 | -2.0767 |
| topic | Elections | baseline:base_rate | 83 | 0.238 | 0.6265 | -0.9604 |
| topic | Elections | market | 83 | 0.1214 | 0.8554 |  |
| topic | Geopolitics | baseline:always_no | 83 | 0.2651 | 0.7349 | -0.7931 |
| topic | Geopolitics | baseline:base_rate | 83 | 0.2242 | 0.7349 | -0.5622 |
| topic | Geopolitics | market | 82 | 0.1428 | 0.8049 |  |
| topic | Other | baseline:always_no | 98 | 0.398 | 0.602 | -2.0407 |
| topic | Other | baseline:base_rate | 98 | 0.2411 | 0.602 | -0.8421 |
| topic | Other | market | 98 | 0.1309 | 0.8163 |  |
| topic | Politics | baseline:always_no | 211 | 0.4218 | 0.5782 | -1.7558 |
| topic | Politics | baseline:base_rate | 211 | 0.2441 | 0.5782 | -0.603 |
| topic | Politics | market | 210 | 0.1521 | 0.7857 |  |
| topic | Sports | baseline:always_no | 421 | 0.5534 | 0.4466 | -1.7536 |
| topic | Sports | baseline:base_rate | 421 | 0.2608 | 0.4466 | -0.2975 |
| topic | Sports | market | 421 | 0.201 | 0.6437 |  |
| topic | World | baseline:always_no | 43 | 0.3953 | 0.6047 | -0.959 |
| topic | World | baseline:base_rate | 43 | 0.2408 | 0.6047 | -0.193 |
| topic | World | market | 43 | 0.2018 | 0.7209 |  |
| horizon | 8-30 days | baseline:always_no | 542 | 0.3875 | 0.6125 | -1.2031 |
| horizon | 8-30 days | baseline:base_rate | 542 | 0.2398 | 0.6125 | -0.3633 |
| horizon | 8-30 days | market | 542 | 0.1759 | 0.7113 |  |
| horizon | <=7 days | baseline:always_no | 478 | 0.4874 | 0.5126 | -2.0566 |
| horizon | <=7 days | baseline:base_rate | 478 | 0.2524 | 0.5126 | -0.5828 |
| horizon | <=7 days | market | 478 | 0.1595 | 0.7667 |  |
| horizon | >30 days | baseline:always_no | 20 | 0.5 | 0.5 |  |
| horizon | >30 days | baseline:base_rate | 20 | 0.254 | 0.5 |  |
| horizon | >30 days | market | 20 | 0.1796 | 0.85 |  |
| extremity | leaning | baseline:always_no | 224 | 0.4554 | 0.5446 | -1.4671 |
| extremity | leaning | baseline:base_rate | 224 | 0.2484 | 0.5446 | -0.3456 |
| extremity | leaning | market | 224 | 0.1846 | 0.7768 |  |
| extremity | near-certain | baseline:always_no | 321 | 0.1713 | 0.8287 | -2.5981 |
| extremity | near-certain | baseline:base_rate | 321 | 0.2124 | 0.8287 | -3.4599 |
| extremity | near-certain | market | 321 | 0.0476 | 0.9502 |  |
| extremity | uncertain | baseline:always_no | 495 | 0.598 | 0.402 | -1.4976 |
| extremity | uncertain | baseline:base_rate | 495 | 0.2664 | 0.402 | -0.1128 |
| extremity | uncertain | market | 495 | 0.2394 | 0.5859 |  |
