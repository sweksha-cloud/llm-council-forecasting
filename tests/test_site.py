"""The site (site/index.html) scores in the browser with site/site.js and dashboard/metrics.js.
These tests run that same code in node on the real data and check it against scoring/report.py."""

import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from scoring.report import add_baselines, add_reference_baselines, load, score_table

ROOT = Path(__file__).resolve().parent.parent
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node isn't installed")

# site/ isn't a package (it would shadow Python's site module), so load its builder by path.
_spec = importlib.util.spec_from_file_location("site_build", ROOT / "site" / "build.py")
site_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(site_build)

HARNESS = """
const Site = require(process.argv[2]);
const ds = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const m = Site.model(ds);
const out = {};
for (const b of Site.board(m, Site.filter(m.rows), 'answered')) {
  const { setup, bins, ...rest } = b;
  out[setup.id] = { ...rest, seconds: setup.seconds, params: setup.params };
}
console.log(JSON.stringify(out));
"""

METRICS = (("brier", "brier"), ("log", "log_score"), ("accuracy", "accuracy"), ("ece", "ece"),
           ("sharpness", "sharpness"), ("auroc", "auroc"), ("balancedAccuracy", "balanced_accuracy"),
           ("mcc", "mcc"), ("brierFill", "brier_abstain_0.5"), ("skill", "skill_vs_market_paired"))


def site_scores(tmp_path, ds):
    harness = tmp_path / "harness.js"
    harness.write_text(HARNESS)
    res = subprocess.run(["node", str(harness), str(ROOT / "site" / "site.js")],
                         input=json.dumps(ds), capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def report_scores(spec):
    outcomes, probs, members, _ = load([str(ROOT / spec["questions"])], [str(ROOT / spec["forecasts"])],
                                       spec["set"] or "all", None, spec["prefix"])
    add_baselines(probs, outcomes, members=members)
    add_reference_baselines(probs, outcomes)
    return {r["setup"]: r for r in score_table(probs, outcomes, n_boot=10)}


SCORED = [spec for spec in site_build.DATASETS]


@needs_node
@pytest.mark.parametrize("spec", SCORED, ids=[s["key"] for s in SCORED])
def test_site_matches_report(tmp_path, spec):
    ds = site_build.site_dataset(spec)
    if not any(q["y"] is not None for q in ds["questions"]):
        pytest.skip(f"no resolved questions with forecasts in {spec['key']} yet")
    got = site_scores(tmp_path, ds)
    want = report_scores(spec)
    assert {"baseline:always_no"} < set(got), "no setups scored"
    for setup, g in got.items():
        w = want[setup]
        assert (g["answered"], g["total"]) == (w["answered"], w["questions"]), setup   # so coverage matches
        for js_key, py_key in METRICS:
            if w.get(py_key, "") == "":
                assert g[js_key] is None, (setup, js_key)
            else:
                assert g[js_key] == pytest.approx(w[py_key], abs=1e-4), (setup, js_key)


def test_seconds_per_question(tmp_path):
    rows = [  # each question asked of two members and then the council, as forecast/run_forecasts.py does
        ("q0", "council:chair=a", '["a", "b"]', "2026-10-12T19:59:50Z"),   # not in the set: only a start time
        ("q1", "single:a", "", "2026-10-12T20:00:00Z"),
        ("q1", "single:b", "", "2026-10-12T20:00:10Z"),
        ("q1", "council:chair=a", '["a", "b"]', "2026-10-12T20:00:14Z"),
        ("q2", "single:a", "", "2026-10-12T20:00:20Z"),
        ("q2", "single:b", "", "2026-10-12T21:00:00Z"),   # a pause, not time spent on q2
        ("q2", "council:chair=a", '["a", "b"]', "2026-10-12T21:00:03Z"),   # so q2's council has no time
        ("q1", "single:a", "", "2026-10-12T21:00:05Z"),   # a retry: the first forecast counts
        ("q3", "single:a", "", "2026-04-07"),             # a date only (Aye's files): no time
    ]
    path = tmp_path / "f.csv"
    path.write_text("question_id,setup,members,forecast_at\n"
                    + "".join(f"{q},{s},\"{m.replace(chr(34), chr(34) * 2)}\",{t}\n" for q, s, m, t in rows))
    got = site_build.seconds_per_question(str(path), {"q1", "q2", "q3"})
    # the council's time on q1 is its own 4 s plus its members' 10 s and 10 s
    assert got == {"single:a": 8.0, "single:b": 10.0, "council:chair=a": 24.0}


def test_model_size():
    assert site_build.params_b("single:phi3:medium") == 14
    assert site_build.params_b("single:llama3.1:8b-instruct-q4_K_M") == 8
    assert site_build.params_b("council:chair=qwen3:8b") is None
    live = site_build.site_dataset(next(d for d in site_build.DATASETS if d["key"] == "live"))
    council = next(s for s in live["setups"] if s["kind"] == "council")
    assert council["params"] == sum(live["setups"][i]["params"] for i in council["members"])


def test_build_writes_static_page(tmp_path):
    html = site_build.build(tmp_path / "index.html").read_text()
    assert html.startswith("<!doctype html>")
    for marker in ("/*METRICS_JS*/", "/*SITE_JS*/", "/*DATA_JSON*/"):
        assert marker not in html
    assert '"key":"aye-new"' in html and "const Metrics" in html
    assert 'src="http' not in html  # no scripts from elsewhere: it runs from a file or GitHub Pages
