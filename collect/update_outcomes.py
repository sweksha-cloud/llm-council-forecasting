"""
update_outcomes.py
------------------
Fills in `outcome` (1 = Yes, 0 = No) and `resolved_at` for questions in
data/questions.csv whose markets have resolved since they were collected.

Only those two columns are ever written, and only where they're empty;
every other value (including the recorded market price) is left untouched.
Run it every few days during the live period (Week 11).

Usage (from the repo root):
  python3 -m collect.update_outcomes
  python3 -m collect.update_outcomes --dry-run
"""

import argparse
import csv
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from collect.collect_live import DEFAULT_OUT, get_json, iso, parse_dt, parse_json_list

POLYMARKET_MARKET_URL = "https://gamma-api.polymarket.com/markets/{id}"
KALSHI_MARKET_URL = "https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}"

Resolution = Optional[Tuple[int, str]]  # (outcome, resolved_at) or None if not resolved yet


def polymarket_resolution(m: Dict[str, Any]) -> Resolution:
    """Resolved only when the market is closed and the Yes price has settled to exactly 1 or 0."""
    if not m.get("closed"):
        return None
    prices = parse_json_list(m.get("outcomePrices"))
    outcomes = [o.lower() for o in parse_json_list(m.get("outcomes"))]
    if outcomes != ["yes", "no"] or prices not in (["1", "0"], ["0", "1"]):
        return None  # closed but not (yet) settled, or settled 50/50
    when = (m.get("closedTime") or "").strip().replace(" ", "T")
    if when.endswith("+00"):
        when += ":00"
    resolved = parse_dt(when) or parse_dt(m.get("endDate"))
    return (1 if prices == ["1", "0"] else 0), (iso(resolved) if resolved else "")


def kalshi_resolution(m: Dict[str, Any]) -> Resolution:
    result = (m.get("result") or "").lower()
    if result not in ("yes", "no"):
        return None
    resolved = (parse_dt(m.get("settlement_ts")) or parse_dt(m.get("expiration_time"))
                or parse_dt(m.get("close_time")))
    return (1 if result == "yes" else 0), (iso(resolved) if resolved else "")


def fetch_resolution(question_id: str) -> Resolution:
    source, _, key = question_id.partition(":")
    if source == "polymarket":
        return polymarket_resolution(get_json(POLYMARKET_MARKET_URL.format(id=key), {}))
    if source == "kalshi":
        return kalshi_resolution(get_json(KALSHI_MARKET_URL.format(ticker=key), {}).get("market") or {})
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--questions", default=str(DEFAULT_OUT))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    path = Path(args.questions)
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        rows = list(reader)

    now = datetime.now(timezone.utc)
    pending = [r for r in rows if not r.get("outcome")
               and (parse_dt(r.get("resolution_date")) or now) <= now]
    print(f"{len(pending)} questions past their closing date without an outcome")

    updated, errors = 0, 0
    for r in pending:
        try:
            res = fetch_resolution(r["question_id"])
        except Exception as e:
            errors += 1
            print(f"  ! {r['question_id']}: {e}")
            continue
        if res is None:
            continue
        r["outcome"], r["resolved_at"] = res
        updated += 1
        print(f"  {'YES' if res[0] else 'NO ':3s}  {r['question_text'][:90]}")
        time.sleep(0.15)

    still = len(pending) - updated - errors
    print(f"\nResolved now: {updated}   Not resolved yet: {still}   Errors: {errors}")
    if args.dry_run or not updated:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved to {path}")


if __name__ == "__main__":
    main()
