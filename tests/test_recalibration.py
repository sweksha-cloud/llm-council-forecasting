"""Post-hoc recalibration, checked on synthetic forecasts with known miscalibration."""

import random

import pytest

from analysis.recalibration import cross_fit, fit_extremize, fit_platt, half, logit, sigmoid, table


def underconfident(n=3000, factor=2.0, seed=0):
    """True probability q; the forecaster reports sigmoid(logit(q) / factor), i.e. too close to 50%."""
    rng = random.Random(seed)
    qs = [rng.uniform(0.02, 0.98) for _ in range(n)]
    return [sigmoid(logit(q) / factor) for q in qs], [int(rng.random() < q) for q in qs]


def test_fits_recover_known_miscalibration():
    ps, ys = underconfident()
    assert fit_extremize(ps, ys) == pytest.approx(2.0, abs=0.25)
    alpha, beta = fit_platt(ps, ys)
    assert alpha == pytest.approx(0.0, abs=0.15) and beta == pytest.approx(2.0, abs=0.25)


def test_platt_on_yes_no_answers_maps_each_call_to_its_hit_rate():
    # Yes calls: 3 of 10 happened; No calls: 1 of 10 happened
    ps = [1.0] * 10 + [0.0] * 10
    ys = [1] * 3 + [0] * 7 + [1] * 1 + [0] * 9
    alpha, beta = fit_platt(ps, ys)
    assert sigmoid(alpha + beta * logit(1.0)) == pytest.approx(0.3, abs=0.01)
    assert sigmoid(alpha + beta * logit(0.0)) == pytest.approx(0.1, abs=0.01)


def test_split_is_fixed_and_balanced():
    assert half("polymarket:123") == half("polymarket:123")
    share = sum(half(f"q{i}") for i in range(4000)) / 4000
    assert share == pytest.approx(0.5, abs=0.03)


def test_cross_fit_is_out_of_sample_and_helps():
    ps, ys = underconfident(n=2000, seed=1)
    probs = {f"q{i}": p for i, p in enumerate(ps)}
    outcomes = {f"q{i}": y for i, y in enumerate(ys)}
    ext, platt, params = cross_fit(probs, outcomes)
    assert set(ext) == set(probs) == set(platt)            # every question gets an out-of-sample forecast
    assert params[0] != params[1]                          # each half has its own fit
    rows = table({"single:m": probs}, outcomes, n_boot=200)
    row = rows[0]
    assert row["brier_platt"] < row["brier_raw"] and row["brier_extremized"] < row["brier_raw"]
    assert row["platt_ci_high"] < 0                        # clearly helps for a 2x-underconfident forecaster


def test_small_setups_are_left_out():
    probs = {"single:few": {f"q{i}": 0.6 for i in range(20)}}
    outcomes = {f"q{i}": i % 2 for i in range(20)}
    assert table(probs, outcomes) == []
