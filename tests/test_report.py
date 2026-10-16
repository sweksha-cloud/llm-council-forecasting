import csv
import json

import pytest

from scoring.report import (add_baselines, common_questions, disagreement_table, load,
                            paired_brier_diff, score_table, spearman)

approx = lambda x: pytest.approx(x, abs=1e-4)


def _write(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


@pytest.fixture
def data(tmp_path):
    # 3 resolved questions (outcomes 1, 0, 1) and one unresolved that must be ignored
    q = [{"question_id": f"q{i}", "set": "live", "outcome": o, "market_price": mp}
         for i, (o, mp) in enumerate([("1", "0.6"), ("0", "0.3"), ("1", "0.7"), ("", "0.5")])]
    f = []
    a = {"q0": 0.8, "q1": 0.2, "q2": 0.6, "q3": 0.5}
    b = {"q0": 0.6, "q1": 0.4, "q2": None, "q3": 0.5}   # b abstains on q2
    for setup, ps in (("single:a", a), ("single:b", b)):
        for qid, p in ps.items():
            f.append({"question_id": qid, "setup": setup, "probability": "" if p is None else p,
                      "members": "", "prompt_id": "v1", "market_price_at_forecast": ""})
    for qid, p in {"q0": 0.9, "q1": 0.1, "q2": 0.7}.items():
        f.append({"question_id": qid, "setup": "council:chair=a", "probability": p,
                  "members": json.dumps(["a", "b"]), "prompt_id": "v1", "market_price_at_forecast": ""})
    _write(tmp_path / "q.csv", q)
    _write(tmp_path / "f.csv", f)
    return load([str(tmp_path / "q.csv")], [str(tmp_path / "f.csv")])


def test_load_skips_unresolved_and_adds_market(data):
    outcomes, probs, members, market = data
    assert outcomes == {"q0": 1, "q1": 0, "q2": 1}
    assert probs["market"] == {"q0": 0.6, "q1": 0.3, "q2": 0.7}
    assert probs["single:b"]["q2"] is None
    assert members[("council:chair=a", "q0")] == ["a", "b"]


def test_baselines(data):
    outcomes, probs, _, _ = data
    notes = add_baselines(probs, outcomes)
    assert probs["baseline:mean"]["q0"] == approx(0.7)       # (0.8 + 0.6) / 2
    assert probs["baseline:median"]["q1"] == approx(0.3)     # median of 0.2, 0.4
    assert probs["baseline:mean"]["q2"] is None               # only one member answered
    # a: (0.04 + 0.04 + 0.16)/3 = 0.08 ; b on answered: (0.16 + 0.16)/2 = 0.16 -> a is best
    assert "single:a" in notes["baseline:best_single"]


def test_scores_and_common_set(data):
    outcomes, probs, _, _ = data
    assert common_questions(probs, outcomes) == ["q0", "q1"]  # b abstained on q2
    rows = {r["setup"]: r for r in score_table(probs, outcomes)}
    # council answered: (0.01 + 0.01 + 0.09)/3 = 0.036667
    assert rows["council:chair=a"]["brier"] == approx(0.0367)
    # council on common q0, q1: (0.01 + 0.01)/2 = 0.01 ; market on common: (0.16 + 0.09)/2 = 0.125
    assert rows["council:chair=a"]["brier_common"] == approx(0.01)
    assert rows["council:chair=a"]["skill_vs_market"] == approx(1 - 0.01 / 0.125)
    # b: coverage 2/3 ; abstention filled with 0.5 on q2: (0.16 + 0.16 + 0.25)/3 = 0.19
    assert rows["single:b"]["coverage"] == approx(0.667)
    assert rows["single:b"]["brier_abstain_0.5"] == approx(0.19)


def test_new_metrics_in_score_table(data):
    outcomes, probs, _, _ = data
    rows = {r["setup"]: r for r in score_table(probs, outcomes)}
    # market 0.6, 0.3, 0.7 vs outcomes 1, 0, 1: all on the right side of 0.5
    assert rows["market"]["accuracy"] == approx(1.0)
    # market Yes forecasts 0.6, 0.7 both above the No forecast 0.3
    assert rows["market"]["auroc"] == approx(1.0)
    # market bins: 0.3 (No) -> 0.3 ; 0.6 (Yes) -> 0.4 ; 0.7 (Yes) -> 0.3 ; ECE = 1.0 / 3
    assert rows["market"]["ece"] == approx(0.3333)
    # single:b answered q0 (0.6, Yes) and q1 (0.4, No) -> both right
    assert rows["single:b"]["accuracy"] == approx(1.0)
    # common set is q0, q1 (one Yes, one No)
    assert rows["council:chair=a"]["accuracy_common"] == approx(1.0)
    assert rows["council:chair=a"]["auroc_common"] == approx(1.0)


def test_paired_difference(data):
    outcomes, probs, _, _ = data
    res = paired_brier_diff(probs["council:chair=a"], probs["market"], outcomes, n_boot=200)
    # per question: q0 0.01-0.16, q1 0.01-0.09, q2 0.09-0.09 -> mean (-0.15 - 0.08 + 0)/3
    assert res["mean_diff"] == approx(-0.0767)
    assert res["ci_low"] <= res["mean_diff"] <= res["ci_high"]


def test_spearman():
    assert spearman([1, 2, 3, 4], [10, 20, 30, 40]) == approx(1.0)
    assert spearman([1, 2, 3, 4], [4, 3, 2, 1]) == approx(-1.0)
    assert spearman([1, 2], [1, 2]) is None


def test_disagreement_needs_enough_questions(data):
    outcomes, probs, members, _ = data
    # only q0 and q1 have two member answers -> fewer than 3 points, so no row
    assert disagreement_table(probs, members, outcomes) == []


def test_best_single_ignores_models_that_barely_answered():
    outcomes = {f"q{i}": i % 2 for i in range(10)}
    probs = {
        "single:many": {q: (0.7 if y else 0.3) for q, y in outcomes.items()},          # Brier 0.09 on 10
        "single:few": {q: (float(y) if q in ("q0", "q1") else None) for q, y in outcomes.items()},  # perfect on 2
    }
    notes = add_baselines(probs, outcomes)
    assert "single:many" in notes["baseline:best_single"]


def test_reference_baselines_and_ground_truth(data):
    from scoring.report import add_reference_baselines, ground_truth_table
    outcomes, probs, _, _ = data
    add_reference_baselines(probs, outcomes)
    assert probs["baseline:always_no"] == {"q0": 0.0, "q1": 0.0, "q2": 0.0}
    assert probs["baseline:base_rate"]["q0"] == approx(2 / 3)
    rows = {r["setup"]: r for r in ground_truth_table(probs, outcomes)}
    # single:a calls Yes, No, Yes on outcomes 1, 0, 1: all right
    assert (rows["single:a"]["tp"], rows["single:a"]["tn"], rows["single:a"]["mcc"]) == (2, 1, 1.0)
    assert rows["baseline:always_no"]["balanced_accuracy"] == 0.5


def test_market_skill_paired(data):
    from scoring.report import market_skill
    outcomes, probs, _, _ = data
    # single:b answered q0, q1. Brier b: 0.16, 0.16 ; market (0.6, 0.3): 0.16, 0.09
    # skill = 1 - 0.32 / 0.25 = -0.28
    res = market_skill(probs["single:b"], probs["market"], outcomes, n_boot=200)
    assert res["n_vs_market"] == 2
    assert res["skill_vs_market_paired"] == approx(-0.28)
    assert res["skill_ci_low"] <= res["skill_vs_market_paired"] <= res["skill_ci_high"]


def test_judge_table():
    from scoring.report import judge_table
    outcomes = {"q0": 1, "q1": 0, "q2": 1}
    probs = {"single:a": {"q0": 1.0, "q1": 1.0, "q2": 0.0}}   # right, wrong, wrong
    judges = {("single:a", "q0"): 5, ("single:a", "q1"): 4, ("single:a", "q2"): 5}
    row = judge_table(probs, judges, outcomes)[0]
    assert (row["right"], row["wrong"]) == (1, 2)
    assert row["judge_mean_right"] == 5 and row["judge_mean_wrong"] == 4.5
    assert row["judge_auroc_for_right"] == approx(0.75)   # 5 vs 4 wins, 5 vs 5 ties: (1 + 0.5) / 2


def test_retry_replaces_failed_call(tmp_path):
    _write(tmp_path / "q.csv", [{"question_id": "q0", "set": "settled", "outcome": "1", "market_price": ""}])
    _write(tmp_path / "f.csv", [
        {"question_id": "q0", "setup": "single:a", "probability": "", "raw_response": "ERROR: timed out",
         "members": "", "prompt_id": "v2", "market_price_at_forecast": ""},
        {"question_id": "q0", "setup": "single:a", "probability": "0.8", "raw_response": "{}",
         "members": "", "prompt_id": "v2", "market_price_at_forecast": ""},
        {"question_id": "q0", "setup": "single:a", "probability": "0.1", "raw_response": "{}",
         "members": "", "prompt_id": "v2", "market_price_at_forecast": ""},
    ])
    _, probs, _, _ = load([str(tmp_path / "q.csv")], [str(tmp_path / "f.csv")])
    assert probs["single:a"]["q0"] == 0.8   # the retry, and after that the first real answer still wins
