"""
site/build.py
-------------
Builds site/index.html, the leaderboard-style results page: ranked bars of a metric, trade-off
scatter plots, and a detail view per setup. It is one static file, so it works on GitHub Pages.

Same data and the same metric code as the dashboard: questions and forecasts come from
dashboard/build.py (build_dataset), and every score is computed in the page by dashboard/metrics.js.
This file only adds what the charts need on top: seconds per question and model size.
tests/test_site.py checks the page's numbers against scoring/report.py.

Run it as a script, not with -m: a package named `site` would shadow Python's own site module.
  python3 site/build.py                  # writes site/index.html (or: make site)
"""

import argparse
import csv
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(REPO))

from dashboard.build import DATASETS, MODEL_NAMES, build_dataset  # noqa: E402

# Parameters, in billions, of the models behind each tag (the 8B/7B/9B in MODEL_NAMES; Phi-3 Medium is 14B).
PARAMS_B = {"llama3.1": 8, "mistral": 7, "qwen3": 8, "gemma2": 9, "phi3": 14, "deepseek-r1": 8}
PAUSE_SECONDS = 600  # a longer gap between two forecasts is a pause in the run, not time spent on a question


def params_b(setup_id: str) -> Optional[float]:
    if not setup_id.startswith("single:"):
        return None
    return PARAMS_B.get(setup_id.split(":")[1])


def _when(stamp: str) -> Optional[datetime]:
    if "T" not in (stamp or ""):
        return None  # a date without a time of day (Aye's files) says nothing about speed
    try:
        return datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def seconds_per_question(forecasts: str, question_ids) -> Dict[str, float]:
    """Median seconds each setup spends on one question, from the forecast timestamps.

    forecast/run_forecasts.py asks every setup in turn, one question at a time, so a forecast took
    the gap since the forecast before it. A council reuses its members' answers, so its time is its
    members' time plus the chairman's own call. Questions missing a member's time are left out."""
    rows = []
    with open(REPO / forecasts, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = _when(r.get("forecast_at", ""))
            if t is not None:
                rows.append((t, r))
    rows.sort(key=lambda x: x[0])
    own: Dict[tuple, float] = {}
    members: Dict[tuple, List[str]] = {}
    seen, prev = set(), None
    for t, r in rows:
        key = (r["setup"], r["question_id"])
        gap, prev = (None if prev is None else (t - prev).total_seconds()), t
        if key in seen:
            continue  # first forecast per setup and question, as in scoring
        seen.add(key)
        if gap is None or gap > PAUSE_SECONDS:
            continue
        own[key] = gap
        if r.get("members"):
            members[key] = [f"single:{m}" for m in json.loads(r["members"])]
    per_setup: Dict[str, List[float]] = {}
    for (setup, qid), gap in own.items():
        if qid not in question_ids:
            continue
        parts = [own.get((m, qid)) for m in members.get((setup, qid), [])]
        if any(p is None for p in parts):
            continue
        per_setup.setdefault(setup, []).append(gap + sum(parts))
    return {s: round(statistics.median(v), 1) for s, v in per_setup.items()}


def has_forecasts(ds: Dict) -> bool:
    return any(c for q in ds["questions"] for c in q["f"])


def site_dataset(spec: Dict) -> Dict:
    ds = build_dataset(spec)
    ds["seconds"] = seconds_per_question(spec["forecasts"], {q["id"] for q in ds["questions"]})
    for s in ds["setups"]:
        s["params"] = params_b(s["id"])
    for s in ds["setups"]:  # a council runs all its members: its size is theirs added up
        sizes = [ds["setups"][i]["params"] for i in s["members"]]
        if s["kind"] == "council" and sizes and None not in sizes:
            s["params"] = sum(sizes)
    return ds


def datasets() -> List[Dict]:
    # A set appears once it has forecasts, as on the dashboard.
    return [d for d in (site_dataset(spec) for spec in DATASETS) if has_forecasts(d)]


def build(out: Path) -> Path:
    data = {"datasets": datasets(), "models": MODEL_NAMES}
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (ROOT / "template.html").read_text(encoding="utf-8")
    html = (html.replace("/*METRICS_JS*/", (REPO / "dashboard" / "metrics.js").read_text(encoding="utf-8"))
                .replace("/*SITE_JS*/", (ROOT / "site.js").read_text(encoding="utf-8"))
                .replace("/*DATA_JSON*/", payload))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "index.html"))
    out = build(Path(ap.parse_args().out))
    print(f"Wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
