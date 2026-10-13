"""
chairman_table.py
-----------------
Builds the data table for the chairman question: one row per question × chairman,
with each member's forecast next to what the chairman decided. It only lines
the numbers up; it doesn't score or draw conclusions.

Columns:
  question_id, set, topic, question_text, outcome, market_price
  chair, chair_p               the council's final probability (empty = abstained)
  p_<model>                    each member's own forecast (same as its single:* row)
  n_members                    how many members gave a probability
  member_mean, member_median, member_min, member_max
  member_sd                    spread of the members (population SD)
  chair_minus_mean             chair_p − member_mean
  chair_outside_range          True if the chairman went below the lowest or above
                               the highest member

Only the first (locked) forecast per question and setup is used, as in scoring.

Usage (from the repo root):
  python3 -m analysis.chairman_table --set settled --out results/settled/chairman_table.csv
  python3 -m analysis.chairman_table --set all --resolved-only
"""

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent


def _float(x) -> Optional[float]:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def build(questions: List[Dict], forecasts: List[Dict], which_set="all", resolved_only=False,
          prompt_id=None) -> List[Dict]:
    qs = {q["question_id"]: q for q in questions
          if (which_set == "all" or q.get("set") == which_set)
          and (not resolved_only or q.get("outcome") in ("0", "1"))}

    first: Dict[tuple, Dict] = {}
    for f in forecasts:
        if f["question_id"] not in qs or (prompt_id and f.get("prompt_id") != prompt_id):
            continue
        first.setdefault((f["question_id"], f["setup"]), f)

    rows = []
    for (qid, setup), f in first.items():
        if not setup.startswith("council:chair="):
            continue
        q = qs[qid]
        members = json.loads(f["members"]) if f.get("members") else []
        member_p = {m: _float(first.get((qid, f"single:{m}"), {}).get("probability")) for m in members}
        given = [p for p in member_p.values() if p is not None]
        chair_p = _float(f.get("probability"))
        price = _float(f.get("market_price_at_forecast"))
        row = {"question_id": qid, "set": q.get("set"), "topic": q.get("topic"),
               "question_text": q.get("question_text"), "outcome": q.get("outcome", ""),
               "market_price": price if price is not None else _float(q.get("market_price")),
               "chair": setup.split("=", 1)[1], "chair_p": chair_p}
        row.update({f"p_{m}": p for m, p in member_p.items()})
        row["n_members"] = len(given)
        if given:
            mean = statistics.fmean(given)
            row.update({"member_mean": round(mean, 4), "member_median": statistics.median(given),
                        "member_min": min(given), "member_max": max(given),
                        "member_sd": round(statistics.pstdev(given), 4)})
            if chair_p is not None:
                row["chair_minus_mean"] = round(chair_p - mean, 4)
                row["chair_outside_range"] = chair_p < min(given) or chair_p > max(given)
        rows.append(row)
    rows.sort(key=lambda r: (r["set"] or "", r["question_id"], r["chair"]))
    return rows


def write(rows: List[Dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    cols: List[str] = []
    for r in rows:
        cols += [k for k in r if k not in cols]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", default=str(ROOT / "data" / "questions.csv"))
    ap.add_argument("--forecasts", nargs="+", default=[str(ROOT / "data" / "forecasts.csv")])
    ap.add_argument("--set", choices=["live", "settled", "contamination", "all"], default="all")
    ap.add_argument("--resolved-only", action="store_true", help="only questions with a known outcome")
    ap.add_argument("--prompt-id", default=None)
    ap.add_argument("--out", default=str(ROOT / "results" / "latest" / "chairman_table.csv"))
    args = ap.parse_args()

    with open(args.questions, newline="", encoding="utf-8") as f:
        questions = list(csv.DictReader(f))
    forecasts = []
    for p in args.forecasts:
        with open(p, newline="", encoding="utf-8") as f:
            forecasts += list(csv.DictReader(f))
    rows = build(questions, forecasts, args.set, args.resolved_only, args.prompt_id)
    write(rows, Path(args.out))
    print(f"{len(rows)} rows (question × chairman) → {args.out}")


if __name__ == "__main__":
    main()
