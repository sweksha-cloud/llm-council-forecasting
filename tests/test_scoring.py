"""Scoring checked against values worked out by hand (shown in each comment)."""

import math

import pytest

from scoring.aggregation import (best_single, extremize, extremized_pool, logit_pool,
                                 mean_pool, median_pool)
from scoring.calibration import expected_calibration_error, murphy_decomposition, reliability_bins
from scoring.discrimination import auroc
from scoring.proper import (accuracy, brier, brier_skill_score, drop_abstentions, fill_abstentions,
                            log_score, mean_brier, mean_log_score)

approx = lambda x: pytest.approx(x, abs=1e-6)


# ── Brier ─────────────────────────────────────────────────────────────────────

def test_brier_single():
    assert brier(0.7, 1) == approx(0.09)   # (0.7 - 1)^2
    assert brier(0.7, 0) == approx(0.49)   # (0.7 - 0)^2
    assert brier(0.5, 1) == approx(0.25)   # always-0.5 forecaster
    assert brier(1.0, 1) == approx(0.0)


def test_mean_brier():
    # (0.09 + 0.04) / 2
    assert mean_brier([0.7, 0.2], [1, 0]) == approx(0.065)


def test_brier_skill_vs_reference():
    # model: (0.09 + 0.04)/2 = 0.065 ; reference always 0.5: 0.25 ; skill = 1 - 0.065/0.25 = 0.74
    assert brier_skill_score([0.7, 0.2], [1, 0], [0.5, 0.5]) == approx(0.74)


# ── Log score ─────────────────────────────────────────────────────────────────

def test_log_score_single():
    assert log_score(0.5, 1) == approx(math.log(2))   # 0.693147
    assert log_score(0.8, 1) == approx(0.223144)      # -ln(0.8)
    assert log_score(0.8, 0) == approx(1.609438)      # -ln(0.2)


def test_log_score_is_finite_at_extremes():
    assert math.isfinite(log_score(0.0, 1))
    assert log_score(0.0, 1) > log_score(0.01, 1)


def test_mean_log_score():
    # (0.223144 + 1.609438) / 2
    assert mean_log_score([0.8, 0.8], [1, 0]) == approx(0.916291)


def test_log_score_punishes_confident_miss_more_than_brier():
    # both forecasters are wrong on the same question; the confident one is punished far more by log score
    assert log_score(0.99, 0) / log_score(0.6, 0) > brier(0.99, 0) / brier(0.6, 0)


# ── Input checks and abstentions ──────────────────────────────────────────────

def test_rejects_bad_inputs():
    with pytest.raises(ValueError):
        brier(1.2, 1)
    with pytest.raises(ValueError):
        brier(0.5, 2)
    with pytest.raises(ValueError):
        mean_brier([0.5], [1, 0])


def test_drop_abstentions_reports_coverage():
    ps, ys, cov = drop_abstentions([0.7, None, 0.2, None], [1, 1, 0, 0])
    assert ps == [0.7, 0.2] and ys == [1, 0]
    assert cov == approx(0.5)


def test_fill_abstentions():
    assert fill_abstentions([0.7, None]) == [0.7, 0.5]


# ── Aggregation baselines ─────────────────────────────────────────────────────

def test_mean_and_median():
    assert mean_pool([0.2, 0.4, 0.9]) == approx(0.5)
    assert median_pool([0.2, 0.4, 0.9]) == approx(0.4)


def test_logit_pool():
    # logits: -1.386294, -0.405465, 2.197225 ; mean 0.135155 ; sigmoid -> 0.533737
    assert logit_pool([0.2, 0.4, 0.9]) == approx(0.533737)


def test_extremize():
    # odds 0.6/0.4 = 1.5 ; squared 2.25 ; back to probability 2.25/3.25
    assert extremize(0.6, 2) == approx(0.692308)
    assert extremize(0.5, 3) == approx(0.5)          # 0.5 stays put
    assert extremize(0.6, 1) == approx(0.6)          # a = 1 changes nothing


def test_extremized_pool_of_identical_forecasts():
    assert extremized_pool([0.6, 0.6], a=2) == approx(0.692308)


def test_best_single():
    assert best_single({"llama": 0.24, "qwen": 0.19, "gemma": 0.21}) == "qwen"


# ── Calibration and Murphy decomposition ──────────────────────────────────────

def test_murphy_decomposition_exact_case():
    # forecasts 0.2, 0.2, 0.8, 0.8 ; outcomes 0, 1, 1, 1 ; base rate 0.75
    # bin 0.2: n=2, observed 0.5 ; bin 0.8: n=2, observed 1.0
    # reliability = (2*(0.2-0.5)^2 + 2*(0.8-1.0)^2)/4 = (0.18 + 0.08)/4 = 0.065
    # resolution  = (2*(0.5-0.75)^2 + 2*(1.0-0.75)^2)/4 = 0.0625
    # uncertainty = 0.75 * 0.25 = 0.1875
    # Brier = 0.065 - 0.0625 + 0.1875 = 0.19 = (0.04 + 0.64 + 0.04 + 0.04)/4
    d = murphy_decomposition([0.2, 0.2, 0.8, 0.8], [0, 1, 1, 1])
    assert d.reliability == approx(0.065)
    assert d.resolution == approx(0.0625)
    assert d.uncertainty == approx(0.1875)
    assert d.brier == approx(0.19)
    assert d.reliability - d.resolution + d.uncertainty == approx(d.brier)


def test_reliability_bins():
    bins = reliability_bins([0.05, 0.15, 0.12, 1.0], [0, 1, 0, 1], n_bins=10)
    assert [(b.lower, b.count) for b in bins] == [(0.0, 1), (0.1, 2), (0.9, 1)]
    assert bins[1].mean_forecast == approx(0.135)
    assert bins[1].observed_rate == approx(0.5)


# ── Accuracy ──────────────────────────────────────────────────────────────────

def test_accuracy_threshold_at_half():
    # 0.7 on a Yes: right ; 0.2 on a No: right ; 0.6 on a No: wrong ; 0.5: half -> 2.5 / 4
    assert accuracy([0.7, 0.2, 0.6, 0.5], [1, 0, 0, 1]) == approx(0.625)


def test_accuracy_of_hard_answers():
    assert accuracy([1.0, 0.0, 0.0], [1, 1, 0]) == approx(2 / 3)


# ── Expected calibration error ────────────────────────────────────────────────

def test_ece_hand_computed():
    # bin 0.1-0.2: forecasts 0.1, 0.1, outcomes 0, 1 -> |0.1 - 0.5| = 0.4, weight 2
    # bin 0.8-0.9: forecasts 0.8, 0.8, outcomes 1, 1 -> |0.8 - 1.0| = 0.2, weight 2
    # ECE = (2 * 0.4 + 2 * 0.2) / 4 = 0.3
    assert expected_calibration_error([0.1, 0.1, 0.8, 0.8], [0, 1, 1, 1]) == approx(0.3)


def test_ece_perfectly_calibrated():
    # 0.25 four times with one Yes, 0.75 four times with three Yes
    ps = [0.25] * 4 + [0.75] * 4
    ys = [1, 0, 0, 0, 1, 1, 1, 0]
    assert expected_calibration_error(ps, ys) == approx(0.0)


# ── AUROC ─────────────────────────────────────────────────────────────────────

def test_auroc_perfect_and_reversed():
    assert auroc([0.9, 0.8, 0.3, 0.1], [1, 1, 0, 0]) == approx(1.0)
    assert auroc([0.1, 0.3, 0.8, 0.9], [1, 1, 0, 0]) == approx(0.0)


def test_auroc_ignores_calibration():
    # every Yes gets 0.55 and every No 0.52: badly calibrated, but ranked perfectly
    assert auroc([0.55, 0.55, 0.52, 0.52], [1, 1, 0, 0]) == approx(1.0)


def test_auroc_hand_computed_with_tie():
    # Yes forecasts 0.8, 0.4 ; No forecasts 0.6, 0.4
    # pairs (Yes, No): (0.8, 0.6) win, (0.8, 0.4) win, (0.4, 0.6) loss, (0.4, 0.4) tie = 0.5 -> 2.5 / 4
    assert auroc([0.8, 0.4, 0.6, 0.4], [1, 1, 0, 0]) == approx(0.625)


def test_auroc_undefined_with_one_outcome():
    assert auroc([0.2, 0.7], [1, 1]) is None


# ── Ground truth (Yes/No calls) ───────────────────────────────────────────────

from scoring.classification import balanced_accuracy, confusion, f1, mcc, precision, recall


def test_confusion_and_rates():
    # calls: Yes, Yes, No, No, none, Yes ; outcomes 1, 0, 0, 1, 1, 1
    c = confusion([0.9, 0.6, 0.2, 0.4, 0.5, 0.7], [1, 0, 0, 1, 1, 1])
    assert (c.tp, c.fp, c.tn, c.fn, c.no_call) == (2, 1, 1, 1, 1)
    assert precision(c) == approx(2 / 3)            # 2 / (2 + 1)
    assert recall(c) == approx(2 / 3)               # 2 / (2 + 1)
    assert f1(c) == approx(2 / 3)                   # 4 / (4 + 1 + 1)
    assert balanced_accuracy(c) == approx(7 / 12)   # (2/3 + 1/2) / 2
    # (2*1 - 1*1) / sqrt(3 * 3 * 2 * 2) = 1/6
    assert mcc(c) == approx(1 / 6)


def test_always_no_gets_no_credit_from_balanced_accuracy_or_mcc():
    c = confusion([0.0] * 4, [0, 0, 0, 1])   # 75% accurate by always saying No
    assert balanced_accuracy(c) == approx(0.5)
    assert mcc(c) == 0.0
    assert precision(c) is None and recall(c) == approx(0.0)


def test_sharpness():
    from scoring.calibration import sharpness
    assert sharpness([0.5, 0.5]) == approx(0.0)            # never commits
    assert sharpness([0.0, 1.0]) == approx(0.5)            # always certain
    assert sharpness([0.55, 0.45, 0.9]) == approx(0.5 / 3)   # (0.05 + 0.05 + 0.4) / 3
