"""
build.py
--------
Builds the results dashboard: one self-contained HTML file with the data inlined.

It reads only the shared-format files (questions + forecasts), so the dashboard
always shows exactly what's committed in data/. Metrics are computed in the page
(dashboard/metrics.js) so filters can re-score any subset; tests/test_dashboard.py
checks that those numbers match scoring/report.py.

Usage (from the repo root):
  python3 -m dashboard.build                 # writes dashboard/index.html (a full HTML page)
  python3 -m dashboard.build --fragment --out /tmp/dash.html   # body only, for hosts that add their own <head>
"""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional

from forecast.run_forecasts import parse_response

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

# Each dataset is a set of questions picked out of a questions file, plus the forecasts file for them.
DATASETS = [
    {"key": "live", "label": "Live set", "who": "This project, Oct 2026",
     "questions": "data/questions.csv", "forecasts": "data/forecasts.csv", "set": "live", "prefix": None,
     "note": "Probability forecasts (prompt v2), locked before the questions resolved. Scored as questions resolve."},
    {"key": "aye-new", "label": "Aye, new set", "who": "Aye Nyein Kyaw, Jul 2026",
     "questions": "data/imported/aye-2026/questions.csv", "forecasts": "data/imported/aye-2026/forecasts.csv",
     "set": None, "prefix": "aye-new:",
     "note": "Free-text answers graded strictly: an explicit Yes is 1, an explicit No is 0, anything else abstains."},
    {"key": "aye-old", "label": "Aye, old set", "who": "Aye Nyein Kyaw, Apr 2026",
     "questions": "data/imported/aye-2026/questions.csv", "forecasts": "data/imported/aye-2026/forecasts.csv",
     "set": None, "prefix": "aye-old:",
     "note": "Free-text answers graded strictly. No per-question council file exists for this set."},
]

MODEL_NAMES = {
    "llama3.1": "Llama 3.1 8B", "mistral": "Mistral 7B", "qwen3": "Qwen 3 8B", "gemma2": "Gemma 2 9B",
    "phi3": "Phi-3 Medium", "deepseek-r1": "DeepSeek R1 8B",
}
REASON_CHARS = 400


def model_name(tag: str) -> str:
    return MODEL_NAMES.get(tag.split(":")[0], tag)


def setup_label(setup: str) -> str:
    if setup.startswith("council:chair="):
        return f"Council, {model_name(setup.split('=', 1)[1])} chair"
    if setup.startswith("single:"):
        return model_name(setup.split(":", 1)[1])
    return setup


def _read(path: str) -> List[Dict[str, str]]:
    with open(REPO / path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _float(x) -> Optional[float]:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def reasoning(row: Dict[str, str]) -> str:
    raw = row.get("raw_response") or ""
    if row.get("origin") == "this-project":
        _, text = parse_response(raw)
    else:
        text = raw
    text = " ".join(text.split())
    return text if len(text) <= REASON_CHARS else text[:REASON_CHARS - 1] + "…"


def build_dataset(ds: Dict) -> Dict:
    questions = [q for q in _read(ds["questions"])
                 if (ds["set"] is None or q.get("set") == ds["set"])
                 and (ds["prefix"] is None or q["question_id"].startswith(ds["prefix"]))]
    by_id = {q["question_id"]: q for q in questions}

    setups: List[str] = []
    cells: Dict[str, Dict[str, Dict]] = {}
    members: Dict[str, List[str]] = {}
    forecast_price: Dict[str, float] = {}
    for f in _read(ds["forecasts"]):
        qid, setup = f["question_id"], f["setup"]
        if qid not in by_id:
            continue
        kept = cells.get(qid, {}).get(setup)
        if kept is not None and not kept.get("failed"):
            continue  # first (locked) forecast wins, as in scoring/report.py; a retry replaces a failed call
        if setup not in setups:
            setups.append(setup)
        cell = {"p": _float(f.get("probability")), "r": reasoning(f)}
        if (f.get("raw_response") or "").startswith("ERROR:"):
            cell["failed"] = True
        judge = _float(f.get("judge_score"))
        if judge is not None:
            cell["j"] = judge
        cells.setdefault(qid, {})[setup] = cell
        if f.get("members") and setup not in members:
            members[setup] = [f"single:{m}" for m in json.loads(f["members"])]
        price = _float(f.get("market_price_at_forecast"))
        if price is not None and qid not in forecast_price:
            forecast_price[qid] = price

    setups.sort(key=lambda s: (0 if s.startswith("council:") else 1, s))
    index = {s: i for i, s in enumerate(setups)}
    rows = []
    for qid, q in by_id.items():
        if qid not in cells:
            continue  # nothing was forecast for this question
        outcome = q.get("outcome")
        price = forecast_price.get(qid, _float(q.get("market_price")))
        rows.append({
            "id": qid, "text": q["question_text"], "url": q.get("url", ""), "source": q.get("source", ""),
            "topic": q.get("topic") or "Uncategorized", "close": (q.get("resolution_date") or "")[:10],
            "y": int(outcome) if outcome in ("0", "1") else None, "market": price,
            "f": [cells[qid].get(s) for s in setups],
        })
    rows.sort(key=lambda r: (r["close"], r["id"]))
    return {"key": ds["key"], "label": ds["label"], "who": ds["who"], "note": ds["note"],
            "setups": [{"id": s, "label": setup_label(s),
                        "kind": s.split(":", 1)[0], "members": [index[m] for m in members.get(s, []) if m in index]}
                       for s in setups],
            "questions": rows}


STANDALONE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>[hidden]{display:none!important} body{margin:0}</style>
</head>
<body>
%s
</body>
</html>
"""


def build(out: Path, fragment: bool = False) -> Path:
    data = {"datasets": [build_dataset(ds) for ds in DATASETS],
            "models": MODEL_NAMES}
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    metrics = (ROOT / "metrics.js").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = template.replace("/*METRICS_JS*/", metrics).replace("/*DATA_JSON*/", payload)
    if not fragment:
        html = STANDALONE % html
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "index.html"))
    ap.add_argument("--fragment", action="store_true", help="leave out <html>/<head>/<body>")
    args = ap.parse_args()
    out = build(Path(args.out), args.fragment)
    print(f"Wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
