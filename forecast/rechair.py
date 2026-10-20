"""
rechair.py
----------
Chair ablations: is the council's chair weighing the members' arguments, or just averaging
their numbers? Re-runs only the chair, over the members' answers already in data/forecasts.csv,
so each variant costs one model call per question instead of six. Pre-registered in
docs/decisions.md (2026-10-20).

  full            the chair sees what the main council's chair saw (probability + reasoning);
                  used here only for the chairs the main run didn't have (one per member)
  numbers-only    the chair sees each member's probability, no reasoning
  reasoning-only  the chair sees each member's reasoning, probabilities withheld (and
                  probability-like numbers inside the reasoning redacted)

For every question the members, their order and their answers are exactly those of the main
council's row (its `members` column), and the question block and market price are the same, so
the view is the only difference. A question without a main council row is skipped: rows are
never built from a different set of members.

Setups written:  council:chair=<m> (full, extra chairs), council:numbers-only:chair=<m>,
council:reasoning-only:chair=<m>. Rows go to data/ablation/forecasts.csv, never to the main file,
and keep the members' prompt id. Re-running resumes; failed calls are retried, as in run_forecasts.

Backtest sets only (settled, settled-ext): a live chair asked now would see a later date than its
members did.

Run from the repo root on spark (after the main queue):
  python3 -m forecast.rechair --set settled settled-ext --no-think \\
      --variants numbers-only reasoning-only --chairmen llama3.1:8b qwen3:8b \\
      --full-chairmen mistral:latest gemma2:9b phi3:medium

Try it without models:
  python3 -m forecast.rechair --backend fake --limit 3 --out /tmp/test_ablation.csv
"""

import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from forecast import prompts
from forecast.run_forecasts import (DEFAULT_QUESTIONS, ROOT, FakeBackend, OllamaBackend, append_rows,
                                    as_of_date, is_error, load_existing, make_row, parse_response)

DEFAULT_MEMBERS = ROOT / "data" / "forecasts.csv"
DEFAULT_OUT = ROOT / "data" / "ablation" / "forecasts.csv"
BACKTEST_SETS = ["settled", "settled-ext"]

VIEWS = {
    "full": (prompts.CHAIRMAN_SYSTEM, prompts.CHAIRMAN_USER, prompts.member_answers_text),
    "numbers-only": (prompts.CHAIRMAN_NUMBERS_SYSTEM, prompts.CHAIRMAN_NUMBERS_USER, prompts.member_numbers_text),
    "reasoning-only": (prompts.CHAIRMAN_REASONING_SYSTEM, prompts.CHAIRMAN_REASONING_USER, prompts.member_reasoning_text),
}


def setup_name(view: str, chair: str) -> str:
    return f"council:chair={chair}" if view == "full" else f"council:{view}:chair={chair}"


def load_main(path: Path) -> Tuple[Dict[Tuple[str, str], Dict[str, str]], Dict[str, Dict[str, str]]]:
    """From the main forecasts file: (question, model) -> single-model row, and
    question -> the main council row whose members the ablation reuses (first usable one)."""
    singles, councils = {}, {}
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("prompt_id") != prompts.PROMPT_ID or is_error(r.get("raw_response")):
                continue
            qid = r["question_id"]
            if r["setup"].startswith("single:"):
                singles.setdefault((qid, r["setup"].split(":", 1)[1]), r)
            elif r["setup"].startswith("council:chair=") and r.get("members") and qid not in councils:
                councils[qid] = r
    return singles, councils


def member_answers(qid: str, council: Dict[str, str], singles) -> Optional[List[Tuple[float, str]]]:
    """The main council's members' (probability, reasoning), in its order; None if any is missing."""
    answers = []
    for m in json.loads(council["members"]):
        r = singles.get((qid, m))
        p, reasoning = parse_response(r["raw_response"]) if r else (None, "")
        if p is None:
            return None
        answers.append((p, reasoning))
    return answers if len(answers) >= 2 else None


def load_backtest_questions(path: Path, sets: List[str]) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return [q for q in csv.DictReader(f) if q.get("set") in sets]


def run(args) -> None:
    backend = FakeBackend() if args.backend == "fake" else OllamaBackend(
        args.host, args.temperature, args.seed, args.timeout, args.no_think)
    questions = load_backtest_questions(Path(args.questions), args.set)
    if args.limit:
        questions = questions[:args.limit]
    singles, councils = load_main(Path(args.members_from))
    out = Path(args.out)
    existing = load_existing(out)
    jobs = [(v, c) for v in args.variants for c in args.chairmen] + [("full", c) for c in args.full_chairmen]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"{len(questions)} questions, {len(jobs)} chair setups → {out}")

    skipped = 0
    for i, q in enumerate(questions, 1):
        qid = q["question_id"]
        needed = [(v, c) for v, c in jobs if (qid, setup_name(v, c), prompts.PROMPT_ID) not in existing]
        if not needed:
            continue
        council = councils.get(qid)
        as_of = as_of_date(q, today)
        answers = member_answers(qid, council, singles) if council else None
        if as_of is None or answers is None:
            skipped += 1
            continue
        block = prompts.question_block(q["question_text"], q["resolution_date"][:10],
                                       q.get("resolution_criteria", ""), as_of)
        members = json.loads(council["members"])
        print(f"[{i}/{len(questions)}] {q['question_text'][:80]}")
        for view, chair in needed:
            system, template, render = VIEWS[view]
            t0 = time.time()
            try:
                raw = backend.ask(chair, system, template.format(question_block=block, member_answers=render(answers)))
            except Exception as e:
                raw = f"ERROR: {e}"
            row = make_row(qid, setup_name(view, chair), "council", members, raw,
                           council.get("market_price_at_forecast") or None, False)
            append_rows(out, [row])
            existing[(qid, row["setup"], prompts.PROMPT_ID)] = row
            print(f"    {row['setup']:44s} p={row['probability'] or 'abstained'}  ({time.time() - t0:.0f}s)")
    if skipped:
        print(f"{skipped} questions skipped: no main council row with usable member answers yet (or no price date before close)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", nargs="+", choices=BACKTEST_SETS, default=BACKTEST_SETS)
    ap.add_argument("--variants", nargs="*", choices=["numbers-only", "reasoning-only"],
                    default=["numbers-only", "reasoning-only"])
    ap.add_argument("--chairmen", nargs="*", default=["llama3.1:8b", "qwen3:8b"], help="chairs for the variants")
    ap.add_argument("--full-chairmen", nargs="*", default=[],
                    help="extra chairs shown the full view (the main run already has llama3.1:8b and qwen3:8b)")
    ap.add_argument("--questions", default=str(DEFAULT_QUESTIONS))
    ap.add_argument("--members-from", default=str(DEFAULT_MEMBERS), help="main forecasts file with the members' answers")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--limit", type=int, default=0, help="only the first N questions (0 = all)")
    ap.add_argument("--backend", choices=["ollama", "fake"], default="ollama")
    ap.add_argument("--host", default="http://localhost:11434", help="Ollama server")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--timeout", type=int, default=600, help="seconds per model call")
    ap.add_argument("--no-think", action="store_true", help="ask reasoning models (qwen3) not to think")
    run(ap.parse_args())


if __name__ == "__main__":
    main()
