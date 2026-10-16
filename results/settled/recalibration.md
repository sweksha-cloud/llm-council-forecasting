# Post-hoc recalibration: settled

Each method is fitted on one half of the questions and tested on the other (2-fold, fixed split), so every Brier here is out of sample. `*_minus_raw` < 0 means recalibration helps, with a 95% bootstrap interval. `a` > 1 means the setup was underconfident. Setups with fewer than 60 answered questions are left out.

| setup | n | brier_raw | brier_extremized | brier_platt | extremized_minus_raw | extremized_ci_low | extremized_ci_high | platt_minus_raw | platt_ci_low | platt_ci_high | a_half0 | a_half1 | platt_alpha_beta_half0 | platt_alpha_beta_half1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| market | 360 | 0.1443 | 0.1455 | 0.1403 | 0.0012 | -0.0007 | 0.0029 | -0.004 | -0.0105 | 0.0029 | 0.821 | 1.117 | 0.493, 0.852 | 0.306, 0.883 |
