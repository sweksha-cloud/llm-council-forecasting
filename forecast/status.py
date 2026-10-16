"""
status.py
---------
Read-only progress report for the spark queue (scripts/queue_spark.sh). Standard library only.

For each step of the queue (set x models), in order: how many of its eligible questions each
setup has answered, failed calls not yet retried, and an ETA for everything still to do. The
pace comes from the timestamps of the latest forecast rows: one pace for the 8B models and
councils, a separate one for deepseek-r1 (much slower; ~110 s/question until it has its own rows).
The variance runs (data/variance/seed*.csv) are reported the same way.

Nothing is written. Usage (from the repo root, on spark): bash scripts/status_spark.sh
"""

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from forecast import prompts
from forecast.postrun import CHAIRS, M5
from forecast.run_forecasts import as_of_date, is_error

ROOT = Path(__file__).resolve().parent.parent
# (set, setups) in the order scripts/queue_spark.sh runs them
STEPS: List[Tuple[str, List[str]]] = [
    ("settled", [f"single:{m}" for m in M5] + [f"council:chair={c}" for c in CHAIRS]),
    ("contamination", [f"single:{m}" for m in M5] + [f"council:chair={c}" for c in CHAIRS]),
    ("settled-ext", [f"single:{m}" for m in M5] + [f"council:chair={c}" for c in CHAIRS]),
    ("settled", ["single:deepseek-r1:8b"]),
    ("contamination", ["single:deepseek-r1:8b"]),
]
DEEPSEEK_DEFAULT = 110.0   # seconds per question with the thinking budget (decisions.md, 2026-10-12)


def _read(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _ts(s: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat((s or "").replace("Z", "+00:00"))
    except ValueError:
        return None


def pace(rows: List[Dict[str, str]], deepseek: bool, window: int = 200) -> Optional[float]:
    """Seconds per forecast row from the latest `window` rows of one kind (gaps over 1 h are ignored)."""
    times = sorted(t for r in rows if r["setup"].startswith("single:deepseek") == deepseek
                   for t in [_ts(r.get("forecast_at"))] if t)[-window:]
    gaps = [(b - a).total_seconds() for a, b in zip(times, times[1:]) if 0 < (b - a).total_seconds() < 3600]
    return sum(gaps) / len(gaps) if len(gaps) >= 5 else None


def progress(rows: List[Dict[str, str]], questions: List[Dict[str, str]], steps, today: str):
    """Per step: (set, [(setup, done, failed)], eligible, remaining calls, deepseek?)."""
    done = {(r["question_id"], r["setup"]) for r in rows
            if r["prompt_id"] == prompts.PROMPT_ID and not is_error(r.get("raw_response"))}
    failed = {(r["question_id"], r["setup"]) for r in rows
              if r["prompt_id"] == prompts.PROMPT_ID and is_error(r.get("raw_response"))} - done
    out = []
    for s, setups in steps:
        eligible = [q["question_id"] for q in questions if q.get("set") == s and as_of_date(q, today)]
        per = [(st, sum((q, st) in done for q in eligible), sum((q, st) in failed for q in eligible)) for st in setups]
        remaining = sum(len(eligible) - d for _, d, _ in per)
        out.append((s, per, len(eligible), remaining, setups[0].startswith("single:deepseek")))
    return out


def report(root: Path = ROOT, now: Optional[datetime] = None) -> str:
    now = now or datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    questions = _read(root / "data" / "questions.csv")
    rows = _read(root / "data" / "forecasts.csv")
    lines = [f"Spark queue status, {now:%Y-%m-%d %H:%M} UTC ({len(rows)} forecast rows)"]
    fast, slow = pace(rows, False), pace(rows, True)
    # without rows yet: the live run did 1.2 min per question for 7 calls (5 models + 2 chairs)
    sec_fast, sec_slow = fast or 1.2 * 60 / 7, slow or DEEPSEEK_DEFAULT
    total_eta = 0.0
    for i, (s, per, n, remaining, ds) in enumerate(progress(rows, questions, STEPS, today), 1):
        eta = remaining * (sec_slow if ds else sec_fast)
        total_eta += eta
        state = "done" if remaining == 0 else f"{remaining} calls left, ~{eta / 3600:.1f} h"
        lines.append(f"\n{i}. {s}{' (DeepSeek)' if ds else ''}: {n} eligible questions, {state}")
        for st, d, f in per:
            lines.append(f"     {st:30s} {d:4d}/{n:<4d} {d / n:6.1%}" + (f"   {f} failed, not yet retried" if f else "")
                         if n else f"     {st:30s} no eligible questions")
    lines.append(f"\nPace: {('%.0f s' % fast) if fast else 'n/a (estimate %.0f s)' % sec_fast} per call (8B models and chairs), "
                 f"{('%.0f s' % slow) if slow else 'n/a (estimate %.0f s)' % sec_slow} per DeepSeek question")
    lines.append(f"ETA for the whole queue: ~{total_eta / 3600:.1f} h"
                 + (f", around {(now + timedelta(seconds=total_eta)):%a %d %b %H:%M} UTC" if total_eta else " (finished)"))

    subset = _read(root / "data" / "variance" / "questions_200.csv")
    var_steps = [("settled", STEPS[0][1])]
    for seed in (1, 2, 3):
        vrows = _read(root / "data" / "variance" / f"seed{seed}.csv")
        (_, per, n, remaining, _), = progress(vrows, subset, var_steps, today)
        lines.append(f"Variance seed {seed}: " + ("not started" if not vrows else
                     f"{n * len(per) - remaining}/{n * len(per)} calls, ~{remaining * sec_fast / 3600:.1f} h left"))
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
