"""
debate.py
---------
Debate, round 2: do the members themselves improve by deliberating? Each member is shown its own
first-round answer and the other members' answers (anonymised, in a fixed order) and may revise
once. Round 1 is the stored single-model answers in data/forecasts.csv, so a round costs one call
per member per question. Pre-registered in docs/decisions.md (2026-10-20).

For every question the members and round-1 answers are exactly those of the main council's row
(its `members` column), and the question block and market price are the same; a question without
one is skipped. Members use the same system prompt as in round 1.

Setups written:  debate-r2:<model> (the member's revised forecast). Rows go to
data/debate/forecasts.csv, never to the main file, and keep the members' prompt id. Re-running
resumes; failed calls are retried. analysis/debate.py scores them.

Backtest sets only (settled, settled-ext): a live member asked now would see a later date.

Run from the repo root on spark (after the ablation queue):
  python3 -m forecast.debate --set settled --no-think

Try it without models:
  python3 -m forecast.debate --backend fake --limit 3 --out /tmp/test_debate.csv
"""

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from forecast import prompts
from forecast.rechair import BACKTEST_SETS, DEFAULT_MEMBERS, load_backtest_questions, load_main, member_answers
from forecast.run_forecasts import (DEFAULT_QUESTIONS, ROOT, FakeBackend, OllamaBackend, append_rows,
                                    as_of_date, load_existing, make_row)

DEFAULT_OUT = ROOT / "data" / "debate" / "forecasts.csv"


def setup_name(model: str) -> str:
    return f"debate-r2:{model}"


def run(args) -> None:
    backend = FakeBackend() if args.backend == "fake" else OllamaBackend(
        args.host, args.temperature, args.seed, args.timeout, args.no_think)
    questions = load_backtest_questions(Path(args.questions), args.set)
    if args.limit:
        questions = questions[:args.limit]
    singles, councils = load_main(Path(args.members_from))
    out = Path(args.out)
    existing = load_existing(out)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"{len(questions)} questions → {out}")

    skipped = 0
    for i, q in enumerate(questions, 1):
        qid = q["question_id"]
        council = councils.get(qid)
        as_of = as_of_date(q, today)
        answers = member_answers(qid, council, singles) if council else None
        if as_of is None or answers is None:
            skipped += 1
            continue
        members = json.loads(council["members"])
        needed = [k for k, m in enumerate(members) if (qid, setup_name(m), prompts.PROMPT_ID) not in existing]
        if not needed:
            continue
        block = prompts.question_block(q["question_text"], q["resolution_date"][:10],
                                       q.get("resolution_criteria", ""), as_of)
        print(f"[{i}/{len(questions)}] {q['question_text'][:80]}")
        for k in needed:
            own_p, own_reasoning = answers[k]
            others = [a for j, a in enumerate(answers) if j != k]
            user = prompts.REVISE_USER.format(question_block=block, own_p=own_p, own_reasoning=own_reasoning.strip(),
                                              member_answers=prompts.member_answers_text(others))
            t0 = time.time()
            try:
                raw = backend.ask(members[k], prompts.FORECAST_SYSTEM, user)
            except Exception as e:
                raw = f"ERROR: {e}"
            row = make_row(qid, setup_name(members[k]), members[k], members, raw,
                           council.get("market_price_at_forecast") or None, False)
            append_rows(out, [row])
            existing[(qid, row["setup"], prompts.PROMPT_ID)] = row
            print(f"    {members[k]:28s} {own_p:.2f} → {row['probability'] or 'abstained'}  ({time.time() - t0:.0f}s)")
    if skipped:
        print(f"{skipped} questions skipped: no main council row with usable member answers yet (or no price date before close)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", nargs="+", choices=BACKTEST_SETS, default=["settled"])
    ap.add_argument("--questions", default=str(DEFAULT_QUESTIONS))
    ap.add_argument("--members-from", default=str(DEFAULT_MEMBERS), help="main forecasts file with the round-1 answers")
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
