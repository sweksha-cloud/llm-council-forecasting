# Robustness: settled-all

Each cut splits the 1039 scored questions into groups and re-scores inside each. Paired rows: council minus reference on the questions both answered (negative = council better), 95% bootstrap interval; groups under 30 questions get no interval. Topics with fewer than 30 questions are grouped as Other.

## Council vs references, by group

_none_


## Every setup, by group

| cut | group | setup | n | brier | accuracy | skill_vs_market |
|---|---|---|---|---|---|---|
| source | kalshi | baseline:always_no | 200 | 0.45 | 0.55 | -2.3365 |
| source | kalshi | baseline:base_rate | 200 | 0.2477 | 0.55 | -0.8367 |
| source | kalshi | market | 200 | 0.1349 | 0.805 |  |
| source | polymarket | baseline:always_no | 839 | 0.4315 | 0.5685 | -1.4342 |
| source | polymarket | baseline:base_rate | 839 | 0.2453 | 0.5685 | -0.384 |
| source | polymarket | market | 839 | 0.1773 | 0.7223 |  |
| topic | Culture | baseline:always_no | 103 | 0.233 | 0.767 | -0.5605 |
| topic | Culture | baseline:base_rate | 103 | 0.2195 | 0.767 | -0.4702 |
| topic | Culture | market | 103 | 0.1493 | 0.8252 |  |
| topic | Elections | baseline:always_no | 83 | 0.3735 | 0.6265 | -2.0481 |
| topic | Elections | baseline:base_rate | 83 | 0.2378 | 0.6265 | -0.9406 |
| topic | Elections | market | 83 | 0.1225 | 0.8554 |  |
| topic | Geopolitics | baseline:always_no | 82 | 0.2561 | 0.7439 | -0.792 |
| topic | Geopolitics | baseline:base_rate | 82 | 0.2225 | 0.7439 | -0.5571 |
| topic | Geopolitics | market | 82 | 0.1429 | 0.8049 |  |
| topic | Other | baseline:always_no | 98 | 0.398 | 0.602 | -1.9276 |
| topic | Other | baseline:base_rate | 98 | 0.241 | 0.602 | -0.7726 |
| topic | Other | market | 98 | 0.1359 | 0.8061 |  |
| topic | Politics | baseline:always_no | 210 | 0.419 | 0.581 | -1.7435 |
| topic | Politics | baseline:base_rate | 210 | 0.2437 | 0.581 | -0.5955 |
| topic | Politics | market | 210 | 0.1527 | 0.7905 |  |
| topic | Sports | baseline:always_no | 420 | 0.5524 | 0.4476 | -1.7503 |
| topic | Sports | baseline:base_rate | 420 | 0.261 | 0.4476 | -0.2996 |
| topic | Sports | market | 420 | 0.2008 | 0.6405 |  |
| topic | World | baseline:always_no | 43 | 0.3953 | 0.6047 | -0.9617 |
| topic | World | baseline:base_rate | 43 | 0.2406 | 0.6047 | -0.1939 |
| topic | World | market | 43 | 0.2015 | 0.7209 |  |
| horizon | 8-30 days | baseline:always_no | 668 | 0.4132 | 0.5868 | -1.4007 |
| horizon | 8-30 days | baseline:base_rate | 668 | 0.2429 | 0.5868 | -0.4116 |
| horizon | 8-30 days | market | 668 | 0.1721 | 0.7201 |  |
| horizon | <=7 days | baseline:always_no | 351 | 0.4729 | 0.5271 | -1.9057 |
| horizon | <=7 days | baseline:base_rate | 351 | 0.2507 | 0.5271 | -0.5403 |
| horizon | <=7 days | market | 351 | 0.1628 | 0.7664 |  |
| horizon | >30 days | baseline:always_no | 20 | 0.5 | 0.5 |  |
| horizon | >30 days | baseline:base_rate | 20 | 0.2542 | 0.5 |  |
| horizon | >30 days | market | 20 | 0.1796 | 0.85 |  |
| extremity | leaning | baseline:always_no | 226 | 0.4646 | 0.5354 | -1.5448 |
| extremity | leaning | baseline:base_rate | 226 | 0.2496 | 0.5354 | -0.3673 |
| extremity | leaning | market | 226 | 0.1826 | 0.7788 |  |
| extremity | near-certain | baseline:always_no | 319 | 0.1724 | 0.8276 | -2.3901 |
| extremity | near-certain | baseline:base_rate | 319 | 0.2117 | 0.8276 | -3.1617 |
| extremity | near-certain | market | 319 | 0.0509 | 0.9467 |  |
| extremity | uncertain | baseline:always_no | 494 | 0.5911 | 0.4089 | -1.4703 |
| extremity | uncertain | baseline:base_rate | 494 | 0.2661 | 0.4089 | -0.1119 |
| extremity | uncertain | market | 494 | 0.2393 | 0.585 |  |
