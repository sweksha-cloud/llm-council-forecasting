"""analysis/inference.py: Holm adjustment and the equivalence (TOST) verdict, on hand-made numbers."""
from analysis.inference import MARGIN, holm, summarise


def test_holm_adjusts_in_rank_order_and_keeps_monotone():
    rows = [{"p": 0.01, "mean_diff": 0.02}, {"p": 0.04, "mean_diff": -0.01}, {"p": 0.03, "mean_diff": 0.01}]
    holm(rows)
    # sorted p: 0.01*3 = 0.03, 0.03*2 = 0.06, 0.04*1 -> max(0.06, 0.04) = 0.06
    assert [r["p_holm"] for r in rows] == [0.03, 0.06, 0.06]
    assert [r["verdict_holm"] for r in rows] == ["first worse", "no clear difference", "no clear difference"]


def test_equivalence_needs_the_90_interval_inside_the_margin():
    inside = summarise("a", "b", 100, 0.0, [MARGIN * (i / 100 - 0.5) for i in range(100)])
    assert inside["equivalent_within_margin"] == "yes" and inside["equivalence_bound"] < MARGIN
    wide = summarise("a", "b", 100, 0.0, [4 * MARGIN * (i / 100 - 0.5) for i in range(100)])
    assert wide["equivalent_within_margin"] == "no"


def test_two_sided_p_from_the_bootstrap():
    all_positive = summarise("a", "b", 10, 0.01, [0.01] * 100)
    assert all_positive["p"] == 0.0
    centred = summarise("a", "b", 10, 0.0, [x / 100 - 0.5 for x in range(101)])
    assert centred["p"] > 0.9
