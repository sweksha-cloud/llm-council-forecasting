"""The dashboard scores in the browser (dashboard/metrics.js). These tests check that its
numbers match scoring/report.py on the real imported data, so the two can't drift apart."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from dashboard.build import DATASETS, build, build_dataset
from scoring.report import add_baselines, load, score_table

ROOT = Path(__file__).resolve().parent.parent
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node isn't installed")

HARNESS = """
const M = require(process.argv[2]);
const sets = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const out = {};
for (const [name, [ps, ys]] of Object.entries(sets)) out[name] = M.score(ps, ys);
console.log(JSON.stringify(out));
"""


def js_scores(tmp_path, sets):
    harness = tmp_path / "harness.js"
    harness.write_text(HARNESS)
    res = subprocess.run(["node", str(harness), str(ROOT / "dashboard" / "metrics.js")],
                         input=json.dumps(sets), capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def dashboard_pairs(ds_key):
    """(probabilities, outcomes) per setup, exactly as the page builds them, plus the mean/median pools."""
    ds = build_dataset(next(d for d in DATASETS if d["key"] == ds_key))
    singles = [i for i, s in enumerate(ds["setups"]) if s["kind"] == "single"]
    sets = {}
    for i, s in enumerate(ds["setups"]):
        pairs = [(q["f"][i]["p"], q["y"]) for q in ds["questions"]
                 if q["y"] is not None and q["f"][i] and q["f"][i]["p"] is not None]
        sets[s["id"]] = [[p for p, _ in pairs], [y for _, y in pairs]]
    mean_ps, mean_ys = [], []
    for q in ds["questions"]:
        ps = [q["f"][i]["p"] for i in singles if q["f"][i] and q["f"][i]["p"] is not None]
        if q["y"] is not None and len(ps) >= 2:
            mean_ps.append(sum(ps) / len(ps))
            mean_ys.append(q["y"])
    sets["baseline:mean"] = [mean_ps, mean_ys]
    return sets


@needs_node
@pytest.mark.parametrize("ds_key, prefix", [("aye-new", "aye-new:"), ("aye-old", "aye-old:")])
def test_dashboard_matches_report(tmp_path, ds_key, prefix):
    outcomes, probs, _, _ = load([str(ROOT / "data/imported/aye-2026/questions.csv")],
                                 [str(ROOT / "data/imported/aye-2026/forecasts.csv")], id_prefix=prefix)
    add_baselines(probs, outcomes)
    report = {r["setup"]: r for r in score_table(probs, outcomes)}
    js = js_scores(tmp_path, dashboard_pairs(ds_key))
    assert js, "no setups found"
    for setup, got in js.items():
        want = report[setup]
        assert got["n"] == want["answered"], setup
        for js_key, py_key in (("brier", "brier"), ("log", "log_score"), ("accuracy", "accuracy"),
                               ("ece", "ece"), ("sharpness", "sharpness"), ("auroc", "auroc"), ("balancedAccuracy", "balanced_accuracy"),
                               ("mcc", "mcc")):
            if want[py_key] == "":
                assert got[js_key] is None, (setup, js_key)
            else:
                assert got[js_key] == pytest.approx(want[py_key], abs=1e-4), (setup, js_key)


@needs_node
def test_metrics_js_hand_values(tmp_path):
    # same hand-computed cases as tests/test_scoring.py
    js = js_scores(tmp_path, {"a": [[0.1, 0.1, 0.8, 0.8], [0, 1, 1, 1]], "b": [[0.8, 0.4, 0.6, 0.4], [1, 1, 0, 0]],
                              "c": [[0.7, 0.2, 0.6, 0.5], [1, 0, 0, 1]],
                              "d": [[0.9, 0.6, 0.2, 0.4, 0.5, 0.7], [1, 0, 0, 1, 1, 1]]})
    assert js["a"]["ece"] == pytest.approx(0.3)
    assert js["b"]["auroc"] == pytest.approx(0.625)
    assert js["c"]["accuracy"] == pytest.approx(0.625)
    assert js["d"]["balancedAccuracy"] == pytest.approx(7 / 12)
    assert js["d"]["mcc"] == pytest.approx(1 / 6)
    assert js["d"]["sharpness"] == pytest.approx(1.1 / 6)   # (0.4 + 0.1 + 0.3 + 0.1 + 0 + 0.2) / 6


def test_build_writes_self_contained_page(tmp_path):
    out = build(tmp_path / "index.html")
    html = out.read_text()
    assert html.startswith("<!doctype html>")
    assert "/*DATA_JSON*/" not in html and "/*METRICS_JS*/" not in html
    assert '"key":"aye-new"' in html


# ── Analyses embedded in the page (computed by the results code) ─────────────

import csv as _csv
import random as _random

from dashboard.build import COMPARISON_ORDER, analyses


def test_dataset_tabs():
    tabs = {d["key"]: d for d in DATASETS}
    assert tabs["settled-all"]["set"] == ["settled", "settled-ext"]          # the pre-registered sample
    assert tabs["settled"]["set"] == ["settled"]                             # the original 360 on their own
    assert "resolved Jul–Oct" not in tabs["settled"]["who"]
    assert [d["key"] for d in DATASETS].index("settled-all") < [d["key"] for d in DATASETS].index("settled")


def _fake_backtest(tmp_path, n=80):
    """Settled (Kalshi + Polymarket), settled-ext and an older contamination set, with two members and a council."""
    rng = _random.Random(3)
    qs, fs = [], []
    for i in range(n):
        s = "settled" if i < n // 2 else "settled-ext" if i < n - 20 else "contamination"
        src = "kalshi" if (s == "settled" and i % 2) else "polymarket"
        when = "2023-06-01" if s == "contamination" else "2026-08-01"
        y = int(rng.random() < 0.45)
        market = 0.8 if y else 0.2
        qs.append({"question_id": f"q{i}", "source": src, "question_text": f"Q{i}?", "url": "", "topic": "Sports",
                   "set": s, "outcome": y, "market_price": market, "price_time": f"{when}T00:00:00Z",
                   "resolution_date": f"{when[:8]}08T00:00:00Z", "resolved_at": f"{when[:8]}08T00:00:00Z"})
        a, b = (0.7 if y else 0.35), (0.55 if y else 0.5)
        for setup, p in (("single:llama3.1:8b", a), ("single:qwen3:8b", b), ("council:chair=llama3.1:8b", (a + b) / 2 + 0.05 * (y - 0.5))):
            fs.append({"question_id": f"q{i}", "setup": setup, "probability": round(p, 3),
                       "raw_response": json.dumps({"probability": p}), "prompt_id": "v2", "origin": "this-project",
                       "members": json.dumps(["llama3.1:8b", "qwen3:8b"]) if setup.startswith("council") else "",
                       "market_price_at_forecast": market, "forecast_at": "2026-10-17T00:00:00Z", "judge_score": ""})
    for path, rows in ((tmp_path / "q.csv", qs), (tmp_path / "f.csv", fs)):
        with open(path, "w", newline="") as f:
            w = _csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return {"key": "settled-all", "set": ["settled", "settled-ext"], "prefix": None,
            "questions": str(tmp_path / "q.csv"), "forecasts": str(tmp_path / "f.csv")}


def test_analyses_on_fake_settled_rows(tmp_path):
    A = analyses(_fake_backtest(tmp_path), n_boot=100)
    # pre-registered comparisons, in the fixed order, pool of its own members first
    versus = [r["versus"] for r in A["comparisons"]]
    assert versus == [r for r in COMPARISON_ORDER if r in versus] and versus[0] == "baseline:mean"
    # per-source next to pooled
    assert {r["source"] for r in A["by_source"]} == {"kalshi", "polymarket"}
    # contamination split over all backtest sets, robustness cuts, recalibration
    assert any(r["n_before"] for r in A["contamination"])
    assert {r["cut"] for r in A["robustness"]} == {"source", "topic", "horizon", "extremity"}
    assert {r["setup"] for r in A["recalibration"]} >= {"council:chair=llama3.1:8b", "single:llama3.1:8b"}
    # the same numbers as scoring.report on the same data
    from scoring.report import add_baselines, comparison_table, load, load_sources
    outcomes, probs, members, _ = load([str(tmp_path / "q.csv")], [str(tmp_path / "f.csv")], ["settled", "settled-ext"])
    add_baselines(probs, outcomes, members=members)
    report = {(r["council"], r["versus"]): r for r in comparison_table(probs, outcomes, 100, load_sources([str(tmp_path / "q.csv")]))}
    for r in A["comparisons"]:
        if r["versus"] != "baseline:always_no":
            assert r == report[(r["council"], r["versus"])]


def test_variance_tables_across_seeds(tmp_path):
    from analysis.variance import score_run, tables
    spec = _fake_backtest(tmp_path)
    q = tmp_path / "q.csv"
    runs = {"T=0": score_run(q, [Path(spec["forecasts"])], 50)}
    for seed in (1, 2):   # seeds: the same forecasts nudged
        rows = list(_csv.DictReader(open(spec["forecasts"])))
        for r in rows:
            r["probability"] = round(min(0.99, float(r["probability"]) + 0.01 * seed), 3)
        path = tmp_path / f"seed{seed}.csv"
        with open(path, "w", newline="") as f:
            w = _csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
        runs[f"seed {seed}"] = score_run(q, [path], 50)
    setups, paired = tables(runs)
    first = paired[0]
    assert first["versus"] == "baseline:mean" and {"T=0", "seed 1", "seed 2", "seed_mean"} <= set(first)
    assert first["same_sign_as_T0"].endswith("of 2")
    assert any("seed_sd" in r for r in setups)
