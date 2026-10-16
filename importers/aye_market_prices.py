"""
aye_market_prices.py
--------------------
Looks up the Polymarket price of each of Aye's questions on the day she collected it,
so her results can be scored against the market (Brier, accuracy, skill vs market).

Her files have no prices. For each Yes/No question in data/imported/aye-2026/questions.csv:
  - new set: her `market_id` column gives the market directly
  - old set: the event slug in her question link gives the event; the market is the one
    whose question text matches hers (or the event's only market)
The price is the last traded Yes price before 00:00 UTC on her collection date, so it's
what the market said before any model was asked (collect.collect_settled.polymarket_price_at).

Results go to data/imported/aye-2026/market_prices.csv, which is committed, so
`python3 -m importers.import_aye` stays offline. Rows already in the file are skipped,
so an interrupted run picks up where it stopped. Needs internet; about 10 minutes.

Usage (from the repo root):
  python3 -m importers.aye_market_prices
  python3 -m importers.import_aye        # merges the prices into questions.csv
"""

import argparse
import csv
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from collect.collect_live import POLYMARKET_EVENTS_URL, get_json, parse_json_list
from collect.collect_settled import polymarket_price_at
from importers.import_aye import DATASETS, OUT, fetch, norm, read_xlsx

PRICES_FILE = OUT / "market_prices.csv"
POLYMARKET_MARKET_URL = "https://gamma-api.polymarket.com/markets/{id}"
COLUMNS = ["question_id", "market_id", "token_id", "market_price", "price_time", "status"]
SLUG = re.compile(r"polymarket\.com/event/([^/?#\s]+)")


def price_time(collected_at: str) -> datetime:
    return datetime.strptime(collected_at[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)


def yes_token(market: Dict) -> Optional[str]:
    outcomes = [o.lower() for o in parse_json_list(market.get("outcomes"))]
    tokens = parse_json_list(market.get("clobTokenIds"))
    if outcomes[:2] != ["yes", "no"] or not tokens:
        return None
    return tokens[0]


_events: Dict[str, List[Dict]] = {}
_events_lock = threading.Lock()


def event_markets(slug: str) -> List[Dict]:
    with _events_lock:
        if slug in _events:
            return _events[slug]
    events = get_json(POLYMARKET_EVENTS_URL, {"slug": slug}) or []
    markets = events[0].get("markets") or [] if events else []
    with _events_lock:
        _events[slug] = markets
    return markets


def find_market(q: Dict[str, str], market_ids: Dict[str, str]) -> Optional[Dict]:
    if q["question_id"] in market_ids:
        return get_json(POLYMARKET_MARKET_URL.format(id=market_ids[q["question_id"]]), {})
    m = SLUG.search(q.get("url") or "")
    if not m:
        return None
    markets = event_markets(m.group(1))
    same = [x for x in markets if norm(x.get("question")) == norm(q["question_text"])]
    if len(same) == 1:
        return same[0]
    return markets[0] if len(markets) == 1 else None


def lookup(q: Dict[str, str], market_ids: Dict[str, str]) -> Dict:
    row = {"question_id": q["question_id"], "market_id": "", "token_id": "", "market_price": "",
           "price_time": price_time(q["collected_at"]).strftime("%Y-%m-%dT%H:%M:%SZ"), "status": ""}
    try:
        market = find_market(q, market_ids)
    except Exception as e:
        row["status"] = f"error: {e}"[:80]
        return row
    if not market:
        row["status"] = "market not found"
        return row
    row["market_id"] = market.get("id", "")
    token = yes_token(market)
    if not token:
        row["status"] = "not a Yes/No market"
        return row
    row["token_id"] = token
    price = polymarket_price_at(token, price_time(q["collected_at"]))
    if price is None:
        row["status"] = "no trades in the 2 days before"
    else:
        row["market_price"], row["status"] = price, "ok"
    return row


def new_set_market_ids() -> Dict[str, str]:
    q_file, _, _, prefix = DATASETS["new"]
    return {f"{prefix}:{r['id']}": str(r["market_id"]) for r in read_xlsx(fetch(q_file)) if r.get("market_id")}


def load_prices(path: Path = PRICES_FILE) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        return {r["question_id"]: r for r in csv.DictReader(f)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--retry-errors", action="store_true", help="look up again rows that ended in an error")
    args = ap.parse_args()

    with (OUT / "questions.csv").open(newline="", encoding="utf-8") as f:
        questions = list(csv.DictReader(f))
    done = load_prices()
    if args.retry_errors:
        done = {k: v for k, v in done.items() if not v["status"].startswith("error")}
    todo = [q for q in questions if q["question_id"] not in done]
    print(f"{len(questions)} questions, {len(done)} already looked up, {len(todo)} to go")
    market_ids = new_set_market_ids()

    results = dict(done)
    with ThreadPoolExecutor(args.workers) as pool:
        futures = [pool.submit(lookup, q, market_ids) for q in todo]
        for i, fut in enumerate(as_completed(futures), 1):
            row = fut.result()
            results[row["question_id"]] = row
            if i % 100 == 0 or i == len(todo):
                save(results, questions)
                print(f"  {i}/{len(todo)}")
    save(results, questions)

    statuses: Dict[str, int] = {}
    for r in results.values():
        key = "error" if r["status"].startswith("error") else r["status"]
        statuses[key] = statuses.get(key, 0) + 1
    print(f"Saved {PRICES_FILE}: " + ", ".join(f"{v} {k}" for k, v in sorted(statuses.items())))


def save(results: Dict[str, Dict], questions: List[Dict[str, str]]) -> None:
    """Written in questions.csv order, so reruns give the same file."""
    PRICES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PRICES_FILE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for q in questions:
            if q["question_id"] in results:
                w.writerow(results[q["question_id"]])


if __name__ == "__main__":
    main()
