# Robustness: settled

Each cut splits the 359 scored questions into groups and re-scores inside each. Paired rows: council minus reference on the questions both answered (negative = council better), 95% bootstrap interval; groups under 30 questions get no interval. Topics with fewer than 30 questions are grouped as Other.

## Council vs references, by group

_none_


## Every setup, by group

| cut | group | setup | n | brier | accuracy | skill_vs_market |
|---|---|---|---|---|---|---|
| source | kalshi | baseline:always_no | 200 | 0.45 | 0.55 | -2.3365 |
| source | kalshi | baseline:base_rate | 200 | 0.2481 | 0.55 | -0.8392 |
| source | kalshi | market | 200 | 0.1349 | 0.805 |  |
| source | polymarket | baseline:always_no | 159 | 0.5031 | 0.4969 | -2.1347 |
| source | polymarket | baseline:base_rate | 159 | 0.2509 | 0.4969 | -0.5629 |
| source | polymarket | market | 159 | 0.1605 | 0.7579 |  |
| topic | Elections | baseline:always_no | 72 | 0.375 | 0.625 | -1.9281 |
| topic | Elections | baseline:base_rate | 72 | 0.2441 | 0.625 | -0.9059 |
| topic | Elections | market | 72 | 0.1281 | 0.8472 |  |
| topic | Other | baseline:always_no | 73 | 0.3836 | 0.6164 | -1.3041 |
| topic | Other | baseline:base_rate | 73 | 0.2445 | 0.6164 | -0.4689 |
| topic | Other | market | 73 | 0.1665 | 0.7808 |  |
| topic | Politics | baseline:always_no | 66 | 0.3788 | 0.6212 | -2.947 |
| topic | Politics | baseline:base_rate | 66 | 0.2443 | 0.6212 | -1.5455 |
| topic | Politics | market | 66 | 0.096 | 0.8636 |  |
| topic | Sports | baseline:always_no | 148 | 0.6081 | 0.3919 | -2.6308 |
| topic | Sports | baseline:base_rate | 148 | 0.2564 | 0.3919 | -0.531 |
| topic | Sports | market | 148 | 0.1675 | 0.7196 |  |
| horizon | 8-30 days | baseline:always_no | 130 | 0.5154 | 0.4846 | -2.2907 |
| horizon | 8-30 days | baseline:base_rate | 130 | 0.2515 | 0.4846 | -0.6059 |
| horizon | 8-30 days | market | 130 | 0.1566 | 0.7577 |  |
| horizon | <=7 days | baseline:always_no | 228 | 0.4518 | 0.5482 | -2.2066 |
| horizon | <=7 days | baseline:base_rate | 228 | 0.2481 | 0.5482 | -0.7613 |
| horizon | <=7 days | market | 228 | 0.1409 | 0.7982 |  |
| horizon | >30 days | baseline:always_no | 1 | 0.0 | 1.0 |  |
| horizon | >30 days | baseline:base_rate | 1 | 0.2242 | 1.0 |  |
| horizon | >30 days | market | 1 | 0.0132 | 1.0 |  |
| extremity | leaning | baseline:always_no | 91 | 0.4725 | 0.5275 | -2.9552 |
| extremity | leaning | baseline:base_rate | 91 | 0.2492 | 0.5275 | -1.0863 |
| extremity | leaning | market | 91 | 0.1195 | 0.8681 |  |
| extremity | near-certain | baseline:always_no | 105 | 0.2571 | 0.7429 | -4.5606 |
| extremity | near-certain | baseline:base_rate | 105 | 0.2378 | 0.7429 | -4.1433 |
| extremity | near-certain | market | 105 | 0.0462 | 0.9524 |  |
| extremity | uncertain | baseline:always_no | 163 | 0.6135 | 0.3865 | -1.7198 |
| extremity | uncertain | baseline:base_rate | 163 | 0.2567 | 0.3865 | -0.138 |
| extremity | uncertain | market | 163 | 0.2256 | 0.6288 |  |
