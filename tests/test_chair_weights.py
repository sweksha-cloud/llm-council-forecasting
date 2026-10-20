"""analysis/chair_weights.py: recovers known weights, and detects a chair favouring its own model."""

import csv
import json
import math
import random
from pathlib import Path

import pytest

from analysis import chair_weights as cw

MEMBERS = ["a", "b", "c"]


def _sig(x):
    return 1 / (1 + math.exp(-x))


def _rows(weights, n=200, seed=1, noise=0.0):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        x = [rng.uniform(-3, 3) for _ in weights]
        rows.append((sum(w * v for w, v in zip(weights, x)) + rng.gauss(0, noise), x))
    return rows


def test_fit_recovers_known_weights():
    w = cw.fit(_rows([0.6, 0.3, 0.1]))
    assert w == pytest.approx([0.6, 0.3, 0.1], abs=1e-3)
    assert sum(w) == pytest.approx(1)


def test_fit_stays_on_the_simplex():
    # a chair that exaggerates one member would need a weight > 1; the fit caps it at the vertex
    w = cw.fit(_rows([1.5, -0.5, 0.0]))
    assert min(w) >= 0 and sum(w) == pytest.approx(1)
    assert w[0] == max(w)


def _write(tmp: Path, chair_weights):
    """Synthetic live set: chair -> weights over MEMBERS, members' answers random."""
    rng = random.Random(3)
    qs, fs = [], []
    for i in range(120):
        qid = f"q{i}"
        qs.append({"question_id": qid, "set": "live", "source": "polymarket" if i % 2 else "kalshi"})
        ps = {m: _sig(rng.uniform(-2.5, 2.5)) for m in MEMBERS}
        fs += [{"question_id": qid, "setup": f"single:{m}", "probability": p, "members": "", "raw_response": "{}"}
               for m, p in ps.items()]
        for chair, w in chair_weights.items():
            z = sum(wi * math.log(ps[m] / (1 - ps[m])) for wi, m in zip(w, MEMBERS)) + rng.gauss(0, 0.05)
            fs.append({"question_id": qid, "setup": f"council:chair={chair}", "probability": _sig(z),
                       "members": json.dumps(MEMBERS), "raw_response": "{}"})
    for name, rows in (("q.csv", qs), ("f.csv", fs)):
        with (tmp / name).open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    return str(tmp / "q.csv"), str(tmp / "f.csv")


def test_self_preference_detected(tmp_path):
    # each chair puts 0.6 on itself and 0.2 on the others
    q, f = _write(tmp_path, {"a": [0.6, 0.2, 0.2], "b": [0.2, 0.6, 0.2]})
    weights, fits, prefs = cw.tables(*cw.load_decisions([q], [f], ["live"]), n_boot=50)
    got = {(r["setup"], r["member"]): r["weight"] for r in weights}
    assert got[("council:chair=a", "a")] == pytest.approx(0.6, abs=0.03)
    assert got[("council:chair=b", "b")] == pytest.approx(0.6, abs=0.03)
    by_chair = {r["chair"]: r for r in prefs}
    assert by_chair["a"]["own_weight_minus_others"] == pytest.approx(0.4, abs=0.05)
    assert by_chair["a"]["verdict"] == by_chair["b"]["verdict"] == "favours own model"
    assert {r["setup"] for r in fits} == {"council:chair=a", "council:chair=b"}


def test_no_self_preference_when_chairs_weight_alike(tmp_path):
    q, f = _write(tmp_path, {"a": [1 / 3] * 3, "b": [1 / 3] * 3})
    _, _, prefs = cw.tables(*cw.load_decisions([q], [f], ["live"]), n_boot=50)
    assert all(r["verdict"] == "no clear difference" for r in prefs)
    assert all(abs(r["own_weight_minus_others"]) < 0.05 for r in prefs)


def test_variant_councils_are_fitted_but_not_in_self_preference(tmp_path):
    q, f = _write(tmp_path, {"a": [0.6, 0.2, 0.2], "b": [0.2, 0.6, 0.2]})
    rows = list(csv.DictReader(open(f)))
    for r in [r for r in rows if r["setup"] == "council:chair=a"]:
        rows.append({**r, "setup": "council:numbers-only:chair=a"})
    with open(f, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    weights, _, prefs = cw.tables(*cw.load_decisions([q], [f], ["live"]), n_boot=20)
    assert "council:numbers-only:chair=a" in {r["setup"] for r in weights}
    assert {r["chair"] for r in prefs} == {"a", "b"}
