"""
run_forecasts.py
----------------
Asks each model, and the council, for a probability on every open question,
and appends the results to data/forecasts.csv (shared record format).

  1. Single models: every model answers each question with the same prompt.
  2. Council: those same answers go, anonymised, to a chairman model, which
     gives the panel's final probability. One council per chairman.

Rows are only ever appended. Re-running skips (question, setup, prompt) rows
that already exist, so an interrupted run resumes where it stopped and a
locked forecast is never redone. A reply that doesn't contain a usable
probability is recorded as an abstention, never as a made-up number.

Run from the repo root (on the GPU server, where Ollama is running):
  python3 -m forecast.run_forecasts --set live --lock \\
      --models llama3.1:8b mistral:latest qwen3:8b gemma2:9b phi3:medium deepseek-r1:8b \\
      --chairmen llama3.1:8b qwen3:8b

Try the whole pipeline without any models (random-but-repeatable answers):
  python3 -m forecast.run_forecasts --backend fake --limit 3 --out /tmp/test_forecasts.csv
"""

import argparse
import csv
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from forecast import prompts

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_QUESTIONS = ROOT / "data" / "questions.csv"
DEFAULT_OUT = ROOT / "data" / "forecasts.csv"

COLUMNS = [
    "question_id", "setup", "model", "members", "probability", "abstained",
    "raw_response", "prompt_id", "forecast_at", "market_price_at_forecast",
    "locked", "origin",
]


# ── Parsing ───────────────────────────────────────────────────────────────────

THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
PROB_RE = re.compile(r'"?probability"?\s*[:=]\s*"?([0-9]*\.?[0-9]+)\s*(%?)', re.IGNORECASE)


def _normalise(value: Any, percent: bool = False) -> Optional[float]:
    try:
        p = float(value)
    except (TypeError, ValueError):
        return None
    # "70%" or a whole number like 70 means 0.70; something like 1.7 is just invalid
    if percent or (1 < p <= 100 and p == int(p)):
        p /= 100
    return p if 0 <= p <= 1 else None


def parse_response(text: str) -> Tuple[Optional[float], str]:
    """Pull (probability, reasoning) out of a model reply. Probability is None if there isn't a usable one."""
    if not text:
        return None, ""
    text = THINK_RE.sub("", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            obj = json.loads(text[start:end + 1])
            if isinstance(obj, dict) and "probability" in obj:
                return _normalise(obj["probability"]), str(obj.get("reasoning", "")).strip()
        except json.JSONDecodeError:
            pass
    m = PROB_RE.search(text)
    if m:
        return _normalise(m.group(1), percent=bool(m.group(2))), text
    return None, text


# ── Model backends ────────────────────────────────────────────────────────────

class OllamaBackend:
    def __init__(self, host: str, temperature: float, seed: int, timeout: int, no_think: bool):
        self.url = host.rstrip("/") + "/api/chat"
        self.options = {"temperature": temperature, "seed": seed}
        self.timeout = timeout
        self.no_think = no_think

    def _post(self, payload: Dict[str, Any]) -> str:
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.load(r).get("message", {}).get("content", "")

    def ask(self, model: str, system: str, user: str) -> str:
        payload = {
            "model": model, "stream": False, "format": prompts.RESPONSE_SCHEMA,
            "options": self.options,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        }
        if self.no_think:
            payload["think"] = False
        try:
            return self._post(payload)
        except urllib.error.HTTPError as e:
            if e.code == 400 and "think" in payload:  # model doesn't support the think switch
                payload.pop("think")
                return self._post(payload)
            raise


class FakeBackend:
    """Repeatable pseudo-random answers, for testing the pipeline without models."""

    def ask(self, model: str, system: str, user: str) -> str:
        h = int(hashlib.sha256((model + user).encode()).hexdigest(), 16)
        p = round((h % 1000) / 1000, 3)
        return json.dumps({"probability": p, "reasoning": f"fake answer from {model}"})


# ── Records ───────────────────────────────────────────────────────────────────

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_questions(path: Path, which_set: str) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    now = datetime.now(timezone.utc)
    usable = []
    for r in rows:
        if which_set != "all" and r.get("set") != which_set:
            continue
        if r.get("outcome"):  # already resolved
            continue
        close = r.get("resolution_date") or ""
        if which_set == "live" and close and datetime.fromisoformat(close.replace("Z", "+00:00")) <= now:
            continue  # closed already; a forecast now wouldn't be a real forecast
        usable.append(r)
    return usable


def load_existing(path: Path) -> Dict[Tuple[str, str, str], Dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        return {(r["question_id"], r["setup"], r["prompt_id"]): r for r in csv.DictReader(f)}


def append_rows(path: Path, rows: List[Dict[str, Any]]) -> None:
    new_file = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        if new_file:
            w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in COLUMNS})


def make_row(question_id, setup, model, members, raw, market_price, lock) -> Dict[str, Any]:
    p, _ = parse_response(raw)
    return {
        "question_id": question_id, "setup": setup, "model": model,
        "members": json.dumps(members) if members else "",
        "probability": "" if p is None else round(p, 4),
        "abstained": p is None,
        "raw_response": raw, "prompt_id": prompts.PROMPT_ID,
        "forecast_at": utc_now_iso(),
        "market_price_at_forecast": market_price,
        "locked": lock, "origin": "this-project",
    }


# ── Main loop ─────────────────────────────────────────────────────────────────

def run(args) -> None:
    backend = FakeBackend() if args.backend == "fake" else OllamaBackend(
        args.host, args.temperature, args.seed, args.timeout, args.no_think)
    questions = load_questions(Path(args.questions), args.set)
    if args.limit:
        questions = questions[:args.limit]
    out = Path(args.out)
    existing = load_existing(out)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"{len(questions)} questions, {len(args.models)} models, {len(args.chairmen)} chairmen → {out}")

    for i, q in enumerate(questions, 1):
        qid = q["question_id"]
        block = prompts.question_block(q["question_text"], q["resolution_date"][:10],
                                       q.get("resolution_criteria", ""), today)
        needed_single = [m for m in args.models if (qid, f"single:{m}", prompts.PROMPT_ID) not in existing]
        needed_council = [c for c in args.chairmen if (qid, f"council:chair={c}", prompts.PROMPT_ID) not in existing]
        if not needed_single and not needed_council:
            continue
        print(f"[{i}/{len(questions)}] {q['question_text'][:80]}")

        market_price = None
        if args.backend != "fake" and not args.no_prices:
            from collect.prices import current_price
            market_price = current_price(qid)

        # 1. Single models (these are also the council's members' answers)
        for m in needed_single:
            t0 = time.time()
            try:
                raw = backend.ask(m, prompts.FORECAST_SYSTEM, prompts.FORECAST_USER.format(question_block=block))
            except Exception as e:
                raw = f"ERROR: {e}"
            row = make_row(qid, f"single:{m}", m, None, raw, market_price, args.lock)
            append_rows(out, [row])
            existing[(qid, row["setup"], prompts.PROMPT_ID)] = row
            print(f"    {m:28s} p={row['probability'] or 'abstained'}  ({time.time() - t0:.0f}s)")

        # 2. Council, built from the members' answers
        answers, members = [], []
        for m in args.models:
            r = existing.get((qid, f"single:{m}", prompts.PROMPT_ID))
            p, reasoning = parse_response(r["raw_response"]) if r else (None, "")
            if p is not None:
                answers.append((p, reasoning))
                members.append(m)
        for c in needed_council:
            if len(answers) < 2:
                raw = "ERROR: fewer than 2 members gave a usable answer"
            else:
                user = prompts.CHAIRMAN_USER.format(question_block=block,
                                                    member_answers=prompts.member_answers_text(answers))
                try:
                    raw = backend.ask(c, prompts.CHAIRMAN_SYSTEM, user)
                except Exception as e:
                    raw = f"ERROR: {e}"
            row = make_row(qid, f"council:chair={c}", "council", members, raw, market_price, args.lock)
            append_rows(out, [row])
            existing[(qid, row["setup"], prompts.PROMPT_ID)] = row
            print(f"    council chair={c:17s} p={row['probability'] or 'abstained'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", nargs="+", default=["llama3.1:8b", "mistral:latest", "qwen3:8b"])
    ap.add_argument("--chairmen", nargs="*", default=["llama3.1:8b"])
    ap.add_argument("--set", choices=["live", "settled", "contamination", "all"], default="live")
    ap.add_argument("--lock", action="store_true", help="mark rows as locked (use for the live set)")
    ap.add_argument("--questions", default=str(DEFAULT_QUESTIONS))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--limit", type=int, default=0, help="only the first N questions (0 = all)")
    ap.add_argument("--backend", choices=["ollama", "fake"], default="ollama")
    ap.add_argument("--host", default="http://localhost:11434", help="Ollama server")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--timeout", type=int, default=600, help="seconds per model call")
    ap.add_argument("--no-think", action="store_true", help="ask reasoning models (qwen3, deepseek-r1) not to think")
    ap.add_argument("--no-prices", action="store_true", help="don't fetch the market price at forecast time")
    run(ap.parse_args())


if __name__ == "__main__":
    main()
