"""
postrun.py
----------
One command for after a spark run: check spark's forecasts file, merge it, rebuild everything.

  1. Validate the spark file BEFORE touching data/forecasts.csv, for each backtest set:
       - every expected setup (the queue in scripts/queue_spark.sh, see QUEUE) answered every
         eligible question (questions without a price date before close are skipped by design)
       - failed calls ("ERROR: ...") with no later successful retry
       - abstention rate (no usable probability) and malformed replies (no parseable JSON) per setup
       - one prompt version, the current one (forecast/prompts.py)
       - councils list at least 2 members, all of them models run as singles in that set
       - the market price stored with each forecast equals the price in data/questions.csv
         (catches a stale questions file on spark)
       - no --seed / --temperature overrides in spark's command log for these runs (seeds aren't
         stored per row, so the log is the record; the variance runs write their own files)
  2. If anything is wrong: print the report and stop (exit 1); nothing is merged.
  3. Otherwise merge (forecast.merge_forecasts: only new rows are appended) and run
     `make results dashboard`.

Usage (from the repo root, after copying spark's files back as in docs/spark.md):
  python3 -m forecast.postrun data/tmp/spark_forecasts.csv --log logs/cmds_spark.log
  python3 -m forecast.postrun data/tmp/spark_forecasts.csv --dry-run     # check only
  make postrun SPARK=data/tmp/spark_forecasts.csv
"""

import argparse
import csv
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set

from forecast import prompts
from forecast.merge_forecasts import merge
from forecast.run_forecasts import as_of_date, is_error, parse_response

ROOT = Path(__file__).resolve().parent.parent

M5 = ["llama3.1:8b", "mistral:latest", "qwen3:8b", "gemma2:9b", "phi3:medium"]
CHAIRS = ["llama3.1:8b", "qwen3:8b"]
# What scripts/queue_spark.sh runs, per set. tests/test_postrun.py checks the two agree.
QUEUE: Dict[str, List[str]] = {
    "settled": [f"single:{m}" for m in M5] + [f"council:chair={c}" for c in CHAIRS] + ["single:deepseek-r1:8b"],
    "contamination": [f"single:{m}" for m in M5] + [f"council:chair={c}" for c in CHAIRS] + ["single:deepseek-r1:8b"],
    "settled-ext": [f"single:{m}" for m in M5] + [f"council:chair={c}" for c in CHAIRS],
}
MAX_ABSTAIN = 0.20     # per setup; above this the run is flagged
MAX_MALFORMED = 0.05   # replies with no parseable JSON, per setup


def _read(path: Path) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _float(x) -> Optional[float]:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def malformed(raw: str) -> bool:
    """A reply (not a failed call) with no JSON object we can read."""
    if not raw or is_error(raw):
        return False
    p, _ = parse_response(raw)
    return p is None and "{" not in raw.split("</think>")[-1]


def log_overrides(log_path: Optional[Path], sets: List[str]) -> List[str]:
    """Queue commands for these sets that changed the seed or temperature."""
    if not log_path or not log_path.exists():
        return []
    bad = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if "run_forecasts" not in line and "queue:" not in line:
            continue
        m = re.search(r"--set (\S+)", line)
        if m and m.group(1) in sets and ("--questions data/variance" not in line) and \
                ("--seed" in line or "--temperature" in line):
            bad.append(line.strip())
    return bad


def validate(spark_rows: List[Dict[str, str]], questions: List[Dict[str, str]], sets: List[str],
             log_path: Optional[Path] = None, today: str = "2026-10-16",
             max_abstain: float = MAX_ABSTAIN, max_malformed: float = MAX_MALFORMED):
    """Returns (problems, report_lines). problems is empty when the run looks complete and clean."""
    problems: List[str] = []
    report: List[str] = []
    by_id = {q["question_id"]: q for q in questions}

    # last row per (question, setup, prompt) wins for the success check: a retry replaces a failure
    rows_by_key: Dict[tuple, List[Dict[str, str]]] = defaultdict(list)
    for r in spark_rows:
        rows_by_key[(r["question_id"], r["setup"], r["prompt_id"])].append(r)

    prompt_ids = Counter(r["prompt_id"] for r in spark_rows if by_id.get(r["question_id"], {}).get("set") in sets)
    if set(prompt_ids) - {prompts.PROMPT_ID}:
        problems.append(f"prompt_id other than {prompts.PROMPT_ID}: {dict(prompt_ids)}")

    for s in sets:
        qs = [q for q in questions if q.get("set") == s]
        eligible = [q for q in qs if as_of_date(q, today) is not None]
        report.append(f"\n## {s}: {len(qs)} questions, {len(eligible)} eligible "
                      f"({len(qs) - len(eligible)} skipped by design: no price date before close)")
        expected = QUEUE.get(s, [])
        rows = [r for r in spark_rows if by_id.get(r["question_id"], {}).get("set") == s]
        setups = sorted({r["setup"] for r in rows} | set(expected))
        singles_here = {st.split(":", 1)[1] for st in setups if st.startswith("single:")}
        report.append(f"{'setup':34s} {'answered':>9s} {'missing':>8s} {'failed':>7s} {'abstain':>8s} {'malformed':>9s}")
        for st in setups:
            done, failed, abstained, bad_json = set(), 0, 0, 0
            for q in eligible:
                versions = rows_by_key.get((q["question_id"], st, prompts.PROMPT_ID), [])
                ok = [r for r in versions if not is_error(r.get("raw_response"))]
                if ok:
                    done.add(q["question_id"])
                    r = ok[0]
                    if r.get("probability") in ("", None):
                        abstained += 1
                        bad_json += malformed(r.get("raw_response", ""))
                elif versions:
                    failed += 1
            missing = len(eligible) - len(done) - failed
            rate = abstained / len(done) if done else 0.0
            mrate = bad_json / len(done) if done else 0.0
            report.append(f"{st:34s} {len(done):>9d} {missing:>8d} {failed:>7d} {rate:>8.1%} {mrate:>9.1%}")
            if st in expected and missing:
                problems.append(f"{s}: {st} is missing {missing} of {len(eligible)} questions (run not finished?)")
            if st not in expected:
                problems.append(f"{s}: unexpected setup {st} (not in the queue)")
            if failed:
                problems.append(f"{s}: {st} has {failed} failed calls with no successful retry (re-run the queue)")
            if done and rate > max_abstain:
                problems.append(f"{s}: {st} abstained on {rate:.0%} of answered questions (limit {max_abstain:.0%})")
            if done and mrate > max_malformed:
                problems.append(f"{s}: {st} gave malformed replies on {mrate:.0%} (limit {max_malformed:.0%})")

        for r in rows:
            if r["setup"].startswith("council:") and not is_error(r.get("raw_response")):
                members = r.get("members") or "[]"
                names = re.findall(r'"([^"]+)"', members)
                if len(names) < 2 or not set(names) <= singles_here:
                    problems.append(f"{s}: {r['setup']} on {r['question_id']} has members {members}")
                    break
        mismatched = [r["question_id"] for r in rows
                      if _float(r.get("market_price_at_forecast")) is not None
                      and _float(by_id[r["question_id"]].get("market_price")) is not None
                      and abs(_float(r["market_price_at_forecast"]) - _float(by_id[r["question_id"]]["market_price"])) > 1e-9]
        if mismatched:
            problems.append(f"{s}: {len(set(mismatched))} questions were forecast with a different market price than "
                            f"data/questions.csv has (stale questions file on spark?), e.g. {sorted(set(mismatched))[:3]}")

    for line in log_overrides(log_path, sets):
        problems.append(f"seed/temperature override in the command log: {line}")
    unknown = sorted({r["question_id"] for r in spark_rows} - set(by_id))
    if unknown:
        problems.append(f"{len(unknown)} forecast rows are for questions not in data/questions.csv, e.g. {unknown[:3]}")
    return problems, report


def run(args) -> int:
    spark = _read(Path(args.spark))
    questions = _read(Path(args.questions))
    problems, report = validate(spark, questions, args.sets, Path(args.log) if args.log else None,
                                max_abstain=args.max_abstain, max_malformed=args.max_malformed)
    print(f"# Spark run check: {args.spark} ({len(spark)} rows)")
    print("\n".join(report))
    if problems:
        print(f"\n## {len(problems)} problem(s); nothing was merged\n" + "\n".join(f"- {p}" for p in problems))
        return 1
    print("\nAll checks passed.")
    if args.dry_run:
        return 0
    n = merge([args.spark], Path(args.into))
    print(f"Merged: {n} new rows appended to {args.into}")
    if not args.no_build:
        subprocess.run(["make", "results", "dashboard"], cwd=ROOT, check=True)
        print("Rebuilt results/ and the dashboard. Review `git diff --stat`, then commit on a branch.")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spark", help="forecasts file copied back from spark")
    ap.add_argument("--log", default=str(ROOT / "logs" / "cmds_spark.log"), help="spark's command log")
    ap.add_argument("--questions", default=str(ROOT / "data" / "questions.csv"))
    ap.add_argument("--into", default=str(ROOT / "data" / "forecasts.csv"))
    ap.add_argument("--sets", nargs="+", default=list(QUEUE))
    ap.add_argument("--max-abstain", type=float, default=MAX_ABSTAIN)
    ap.add_argument("--max-malformed", type=float, default=MAX_MALFORMED)
    ap.add_argument("--dry-run", action="store_true", help="check only; don't merge or rebuild")
    ap.add_argument("--no-build", action="store_true", help="merge but don't run make results dashboard")
    sys.exit(run(ap.parse_args()))


if __name__ == "__main__":
    main()
