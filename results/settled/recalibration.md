# Post-hoc recalibration: settled

Each method is fitted on one half of the questions and tested on the other (2-fold, fixed split), so every Brier here is out of sample. `*_minus_raw` < 0 means recalibration helps, with a 95% bootstrap interval. `a` > 1 means the setup was underconfident. Setups with fewer than 60 answered questions are left out.

| setup | n | brier_raw | brier_extremized | brier_platt | extremized_minus_raw | extremized_ci_low | extremized_ci_high | platt_minus_raw | platt_ci_low | platt_ci_high | a_half0 | a_half1 | platt_alpha_beta_half0 | platt_alpha_beta_half1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| market | 359 | 0.1462 | 0.1475 | 0.1425 | 0.0013 | -0.0005 | 0.0029 | -0.0037 | -0.0097 | 0.0028 | 0.814 | 1.12 | 0.431, 0.834 | 0.293, 0.856 |
