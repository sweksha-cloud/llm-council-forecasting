"""
import_aye.py
-------------
Imports Aye Nyein Kyaw's single-model results (github.com/JennicaANK/llm-council-judge)
into the shared record format, and re-scores them with corrected grading.

Her models answered in free text, without a probability. Grading here is strict:
  - an answer counts as "Yes" or "No" only if it starts with Yes/No, or labels it
    explicitly ("Answer: No", "Prediction: Yes")
  - everything else (refusals, hedging, "I don't know") is an abstention
  - a judge reply that couldn't be parsed is left empty, not scored as 1

This fixes the two bugs in her compare_predictions*.py / single_llm_judge.py:
substring matching ("not" counted as "No") and failed judge reads scored as 1.

Her files are read from a pinned commit, so the import is reproducible; her
repo is never modified. Her per-question council file (new_council_detailed.xlsx)
isn't in her repo; it was copied from spark (/data/swekshashaw/, dated 2026-07-29)
into data/imported/aye-2026/source/ and is checked against COUNCIL_SHA256.
Council rows that failed with a connection error are dropped.

Usage (run from the repo root; needs openpyxl):
  python3 -m importers.import_aye
"""

import csv
import json
import re
import statistics
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

from scoring.proper import drop_abstentions, fill_abstentions, mean_brier

AYE_REPO = "JennicaANK/llm-council-judge"
AYE_COMMIT = "b77bdd934a7b4349b5971849fd6ceeabed3f2c5c"
RAW_URL = f"https://raw.githubusercontent.com/{AYE_REPO}/{AYE_COMMIT}/{{name}}"
ORIGIN = f"aye-2026@{AYE_COMMIT[:7]}"

ROOT = Path(__file__).resolve().parent.parent
COUNCIL_FILE = ROOT / "data" / "imported" / "aye-2026" / "source" / "new_council_detailed.xlsx"
COUNCIL_SHA256 = "9fb4ae9ab2e72b3583f61827ccf84d5ff31d0b4dbc306b9b9396c7828f8a04ea"
CACHE = ROOT / "data" / "raw" / "aye"          # git-ignored download cache
OUT = ROOT / "data" / "imported" / "aye-2026"

DATASETS = {
    # name: (questions file, answers file, collected, question id prefix)
    "old": ("CS180_DataCollection_resolved.xlsx", "single_llm_results.csv", "2026-04-07", "aye-old"),
    "new": ("new_questions_resolved.xlsx", "new_single_llm_results.csv", "2026-07-15", "aye-new"),
}

QUESTION_COLUMNS = [
    "question_id", "source", "question_text", "resolution_criteria", "answer_type", "choices",
    "set", "topic", "url", "collected_at", "resolution_date", "market_price", "price_time",
    "volume", "outcome", "resolved_at",
]
FORECAST_COLUMNS = [
    "question_id", "setup", "model", "members", "probability", "abstained", "raw_response",
    "prompt_id", "forecast_at", "market_price_at_forecast", "locked", "origin",
    "judge_score",  # imported results only: her LLM-judge score, empty where the judge reply was unreadable
]

STARTS_WITH = re.compile(r"^\W*(yes|no)\b", re.IGNORECASE)
LABELLED = re.compile(r"\b(?:answer|prediction|predicted answer|final answer|verdict)\s*[:\-]\s*\**\s*(yes|no)\b",
                      re.IGNORECASE)


# ── Grading ───────────────────────────────────────────────────────────────────

def strict_yes_no(answer: str) -> Optional[float]:
    """1.0 for an explicit Yes, 0.0 for an explicit No, None (abstain) otherwise."""
    m = STARTS_WITH.search(answer or "") or LABELLED.search(answer or "")
    if not m:
        return None
    return 1.0 if m.group(1).lower() == "yes" else 0.0


def corrected_judge_score(row: Dict[str, str]) -> Optional[int]:
    """Her judge score, or None where the 1 was really a failed read of the judge's reply."""
    reason = (row.get("reason") or "").lower()
    if reason.startswith("failed to parse") or reason.startswith("error"):
        return None
    try:
        return int(row["score"])
    except (KeyError, ValueError):
        return None


def norm(text: str) -> str:
    return " ".join(str(text or "").lower().split())


# ── Loading ───────────────────────────────────────────────────────────────────

def fetch(name: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{AYE_COMMIT[:7]}_{name}"
    if not path.exists():
        print(f"  downloading {name}")
        urllib.request.urlretrieve(RAW_URL.format(name=name), path)
    return path


def read_xlsx(path: Path) -> List[Dict]:
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True).active
    rows = ws.iter_rows(values_only=True)
    header = [str(h) for h in next(rows)]
    return [dict(zip(header, r)) for r in rows]


def date_str(v) -> str:
    return v.strftime("%Y-%m-%d") if hasattr(v, "strftime") else str(v or "")[:10]


# ── Import ────────────────────────────────────────────────────────────────────

def import_dataset(name: str):
    q_file, a_file, collected, prefix = DATASETS[name]
    questions, by_text = [], {}
    for r in read_xlsx(fetch(q_file)):
        answer = str(r.get("correct_answer") or "").strip().lower()
        # Only true Yes/No markets with a Yes/No outcome. (In her old dataset, multi-choice
        # questions were wrongly resolved to Yes/No, so their answer_type is checked too.)
        if str(r.get("answer_type") or "").replace(" ", "").lower() != "(yes,no)" or answer not in ("yes", "no"):
            continue
        q = {
            "question_id": f"{prefix}:{r['id']}", "source": "polymarket",
            "question_text": str(r["question_text"]).strip(), "resolution_criteria": "",
            "answer_type": "binary", "choices": json.dumps(["Yes", "No"]), "set": "settled",
            "topic": r.get("category") or "", "url": r.get("question_link") or "",
            "collected_at": date_str(r.get("date_collected")) or collected,
            "resolution_date": date_str(r.get("resolution_date")),
            "outcome": 1 if answer == "yes" else 0,
        }
        questions.append(q)
        by_text.setdefault(norm(q["question_text"]), q)

    forecasts = []
    with fetch(a_file).open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            q = by_text.get(norm(r["question"]))
            if not q:
                continue
            p = strict_yes_no(r["answer"])
            model = r.get("model_id") or r["model"]
            forecasts.append({
                "question_id": q["question_id"], "setup": f"single:{model}", "model": model,
                "probability": "" if p is None else p, "abstained": p is None,
                "raw_response": r["answer"], "prompt_id": "aye-free-text",
                "forecast_at": q["collected_at"], "locked": False, "origin": ORIGIN,
                "judge_score": corrected_judge_score(r),
                "_label": r["model"], "_reported_score": int(r["score"]) if r["score"].isdigit() else None,
                "_outcome": q["outcome"],
            })
    if name == "new" and COUNCIL_FILE.exists():
        forecasts += import_council(by_text)
    return questions, forecasts


def import_council(by_text: Dict[str, Dict]) -> List[Dict]:
    """Her council answers (new dataset only), one row per question and chairman."""
    import hashlib
    digest = hashlib.sha256(COUNCIL_FILE.read_bytes()).hexdigest()
    if digest != COUNCIL_SHA256:
        raise SystemExit(f"{COUNCIL_FILE} has changed (sha256 {digest})")
    forecasts = []
    for r in read_xlsx(COUNCIL_FILE):
        chair = r.get("chairman_model")
        q = by_text.get(norm(r.get("question_text")))
        if not chair or not q:  # connection-error rows, or not a Yes/No question
            continue
        answer = str(r.get("council_answer") or "")
        p = strict_yes_no(answer)
        try:
            judge = int(r.get("judge_overall"))
        except (TypeError, ValueError):
            judge = None
        forecasts.append({
            "question_id": q["question_id"], "setup": f"council:chair={chair}", "model": "council",
            "members": json.dumps([m.strip() for m in str(r.get("answer_models") or "").split(",") if m.strip()]),
            "probability": "" if p is None else p, "abstained": p is None,
            "raw_response": answer, "prompt_id": "aye-free-text",
            "forecast_at": q["collected_at"], "locked": False, "origin": ORIGIN,
            "judge_score": judge, "_label": f"council ({chair})", "_reported_score": judge,
            "_outcome": q["outcome"],
        })
    return forecasts


def summarise(name: str, forecasts: List[Dict]) -> List[Dict]:
    rows = []
    for label in sorted({f["_label"] for f in forecasts}):
        fs = [f for f in forecasts if f["_label"] == label]
        ps = [None if f["probability"] == "" else f["probability"] for f in fs]
        ys = [f["_outcome"] for f in fs]
        answered_ps, answered_ys, coverage = drop_abstentions(ps, ys)
        judged = [f["judge_score"] for f in fs if f["judge_score"] is not None]
        reported = [f["_reported_score"] for f in fs if f["_reported_score"] is not None]
        rows.append({
            "dataset": name, "model": label, "n_questions": len(fs),
            "answered": len(answered_ps), "coverage": round(coverage, 3),
            "accuracy_answered": round(sum(p == y for p, y in zip(answered_ps, answered_ys)) / len(answered_ps), 3)
            if answered_ps else "",
            "brier_answered": round(mean_brier(answered_ps, answered_ys), 3) if answered_ps else "",
            "brier_abstain_as_0.5": round(mean_brier(fill_abstentions(ps), ys), 3),
            "judge_mean_reported": round(statistics.fmean(reported), 2) if reported else "",
            "judge_mean_corrected": round(statistics.fmean(judged), 2) if judged else "",
            "judge_unreadable": len(fs) - len(judged),
        })
    return rows


def write_csv(path: Path, rows: List[Dict], columns: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in columns})


def main() -> None:
    all_q, all_f, summary = [], [], []
    for name in DATASETS:
        print(f"{name} dataset…")
        qs, fs = import_dataset(name)
        print(f"  {len(qs)} Yes/No questions with outcomes, {len(fs)} model answers")
        all_q += qs
        all_f += fs
        summary += summarise(name, fs)
    write_csv(OUT / "questions.csv", all_q, QUESTION_COLUMNS)
    write_csv(OUT / "forecasts.csv", all_f, FORECAST_COLUMNS)
    cols = list(summary[0].keys())
    write_csv(OUT / "summary.csv", summary, cols)
    print(f"\nSaved to {OUT}\n")
    widths = {c: max(len(c), *(len(str(r[c])) for r in summary)) for c in cols}
    print("  ".join(c.ljust(widths[c]) for c in cols))
    for r in summary:
        print("  ".join(str(r[c]).ljust(widths[c]) for c in cols))


if __name__ == "__main__":
    main()
