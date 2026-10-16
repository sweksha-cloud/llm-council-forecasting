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
