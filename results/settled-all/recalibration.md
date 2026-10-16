# Post-hoc recalibration: settled-all

Each method is fitted on one half of the questions and tested on the other (2-fold, fixed split), so every Brier here is out of sample. `*_minus_raw` < 0 means recalibration helps, with a 95% bootstrap interval. `a` > 1 means the setup was underconfident. Setups with fewer than 60 answered questions are left out.

| setup | n | brier_raw | brier_extremized | brier_platt | extremized_minus_raw | extremized_ci_low | extremized_ci_high | platt_minus_raw | platt_ci_low | platt_ci_high | a_half0 | a_half1 | platt_alpha_beta_half0 | platt_alpha_beta_half1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| market | 1039 | 0.1691 | 0.1666 | 0.1626 | -0.0025 | -0.0056 | 0.0006 | -0.0065 | -0.0111 | -0.0018 | 0.55 | 0.752 | 0.408, 0.666 | 0.283, 0.758 |
