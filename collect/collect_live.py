"""
collect_live.py
---------------
Collects LIVE (still open) Yes/No questions from Polymarket and Kalshi that
resolve inside a date window, and records each one's current market price.

Output: data/questions.csv in the shared record format (docs/record_format.md).

Re-running is safe: questions already in the file are kept exactly as they
were (including the price recorded the first time); only new ones are added.

Usage:
  python3 collect/collect_live.py                       # defaults: now → 2026-11-15, 200 per source
  python3 collect/collect_live.py --end 2026-11-15 --per-source 200
  python3 collect/collect_live.py --dry-run             # print a summary, write nothing

Only the Python standard library is used, and both APIs are public (no keys).
"""

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

POLYMARKET_EVENTS_URL = "https://gamma-api.polymarket.com/events"
KALSHI_EVENTS_URL = "https://api.elections.kalshi.com/trade-api/v2/events"

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "data" / "questions.csv"

COLUMNS = [
    "question_id", "source", "question_text", "resolution_criteria",
    "answer_type", "choices", "set", "topic", "url",
    "collected_at", "resolution_date",
    "market_price", "price_time", "volume",
    "outcome", "resolved_at",
]

# Crypto and finance price questions are excluded (near coin-flips that would
# otherwise dominate the set). Matching is case-insensitive.
POLYMARKET_EXCLUDED_TAGS = {
    "crypto", "crypto prices", "bitcoin", "ethereum", "solana", "xrp",
    "finance", "stocks", "indicies", "indices", "commodities", "forex",
}
KALSHI_EXCLUDED_CATEGORIES = {"crypto", "financials"}
EXCLUDED_PHRASES = [
    "up or down", "price of bitcoin", "price of ethereum", "bitcoin above",
    "bitcoin below", "ethereum above", "ethereum below", "s&p 500", "nasdaq",
    "dow jones", "airdrop", "token launch", "memecoin", "fdv",
]
# Token tickers like "$ARB" or "$PEPE": older markets often lack crypto tags.
TICKER_RE = re.compile(r"\$[A-Z]{2,6}\b")


# ── Small helpers ─────────────────────────────────────────────────────────────

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def to_float(x: Any) -> Optional[float]:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def parse_json_list(x: Any) -> List[str]:
    """Polymarket returns outcomes/prices as JSON-encoded strings."""
    if isinstance(x, list):
        return [str(v) for v in x]
    if isinstance(x, str):
        try:
            val = json.loads(x)
            if isinstance(val, list):
                return [str(v) for v in val]
        except json.JSONDecodeError:
            pass
    return []


def has_excluded_phrase(text: str) -> bool:
    t = text.lower()
    return any(p in t for p in EXCLUDED_PHRASES) or bool(TICKER_RE.search(text))


def get_json(url: str, params: Dict[str, Any], retries: int = 3) -> Any:
    full = url + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(full, headers={"User-Agent": "llm-council-forecasting/0.1"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code < 500 and e.code != 429:  # client errors won't fix themselves
                raise
            if attempt == retries - 1:
                raise
            print(f"    retrying after error: {e}")
            time.sleep(2 * (attempt + 1))
        except Exception as e:  # timeouts, connection resets
            if attempt == retries - 1:
                raise
            print(f"    retrying after error: {e}")
            time.sleep(2 * (attempt + 1))


def pick_top(candidates: List[Dict[str, Any]], per_source: int, max_per_event: int,
             max_topic_share: float) -> List[Dict[str, Any]]:
    """Highest-volume questions first, with limits so no single event, topic or
    duplicate wording dominates the set."""
    max_per_topic = max(1, int(per_source * max_topic_share))
    chosen, per_event, per_topic, texts = [], {}, {}, set()
    for c in sorted(candidates, key=lambda c: c["volume"] or 0, reverse=True):
        ev, topic = c["_event"], c["topic"] or "(none)"
        text = " ".join(c["question_text"].lower().split())
        if per_event.get(ev, 0) >= max_per_event or per_topic.get(topic, 0) >= max_per_topic or text in texts:
            continue
        per_event[ev] = per_event.get(ev, 0) + 1
        per_topic[topic] = per_topic.get(topic, 0) + 1
        texts.add(text)
        chosen.append(c)
        if len(chosen) >= per_source:
            break
    return chosen


# ── Polymarket ────────────────────────────────────────────────────────────────

def polymarket_candidates(start: datetime, end: datetime, min_volume: float) -> List[Dict[str, Any]]:
    out, seen = [], set()
    chunk_start = start
    while chunk_start < end:
        # Small windows, highest volume first: the API stops paging after
        # ~2,000 results, so anything it cuts off is the least-traded.
        chunk_end = min(chunk_start + timedelta(days=2), end)
        offset = 0
        while True:
            params = {
                "active": "true", "closed": "false", "limit": 100, "offset": offset,
                "end_date_min": iso(chunk_start), "end_date_max": iso(chunk_end),
                "order": "volume", "ascending": "false",
            }
            try:
                batch = get_json(POLYMARKET_EVENTS_URL, params)
            except Exception as e:
                print(f"  Polymarket: page limit reached for {chunk_start.date()} at offset {offset}; skipping the lowest-volume rest")
                break
            if not batch:
                break
            for ev in batch:
                out.extend(polymarket_event_to_candidates(ev, start, end, min_volume, seen))
            if len(batch) < 100:
                break
            offset += 100
            time.sleep(0.3)
        chunk_start = chunk_end
    return out


def polymarket_event_to_candidates(ev, start, end, min_volume, seen) -> Iterable[Dict[str, Any]]:
    tags = [str(t.get("label", "")) for t in (ev.get("tags") or [])]
    if {t.lower() for t in tags} & POLYMARKET_EXCLUDED_TAGS:
        return []
    topic = next((t for t in tags if t in ("Politics", "Sports", "Science", "Tech", "Culture",
                                           "Economy", "World", "Business", "Geopolitics",
                                           "Elections", "Entertainment", "Weather")), "")
    rows = []
    for m in ev.get("markets") or []:
        mid = str(m.get("id"))
        if mid in seen:
            continue
        question = (m.get("question") or "").strip()
        outcomes = [o.lower() for o in parse_json_list(m.get("outcomes"))]
        prices = parse_json_list(m.get("outcomePrices"))
        end_dt = parse_dt(m.get("endDate"))
        volume = to_float(m.get("volumeNum")) or 0.0
        if (not question or outcomes != ["yes", "no"] or len(prices) != 2
                or not m.get("active") or m.get("closed") or not m.get("acceptingOrders")
                or end_dt is None or not (start <= end_dt <= end)
                or volume < min_volume or has_excluded_phrase(question)):
            continue
        seen.add(mid)
        rows.append({
            "question_id": f"polymarket:{mid}",
            "source": "polymarket",
            "question_text": question,
            "resolution_criteria": (m.get("description") or "").strip(),
            "answer_type": "binary",
            "choices": json.dumps(["Yes", "No"]),
            "set": "live",
            "topic": topic,
            "url": f"https://polymarket.com/event/{ev.get('slug', '')}",
            "resolution_date": iso(end_dt),
            "market_price": to_float(prices[0]),
            "volume": round(volume, 2),
            "_event": f"polymarket:{ev.get('id')}",
        })
    return rows


# ── Kalshi ────────────────────────────────────────────────────────────────────

def kalshi_price(m: Dict[str, Any]) -> Optional[float]:
    """Midpoint of the Yes bid/ask when there's a real two-sided quote, else last trade."""
    bid, ask = to_float(m.get("yes_bid_dollars")), to_float(m.get("yes_ask_dollars"))
    if bid is not None and ask is not None and 0 < bid <= ask < 1 and ask - bid <= 0.10:
        return round((bid + ask) / 2, 4)
    return to_float(m.get("last_price_dollars"))


def kalshi_question_text(ev: Dict[str, Any], m: Dict[str, Any]) -> str:
    """Kalshi market titles are often fragments ("Canada wins"); give them the event's context."""
    title = (m.get("title") or "").strip()
    ev_title = (ev.get("title") or "").strip()
    sub = (m.get("yes_sub_title") or "").strip()
    if title.endswith("?") and len(title) >= 25:
        # A full question. In multi-option events it can still be the generic
        # event question ("Who will win X?"), so add which option "Yes" means.
        if len(ev.get("markets") or []) > 1 and sub and sub.lower() not in title.lower():
            return f"{title} (Yes = {sub})"
        return title
    base = title or sub
    # A "Context: detail" title already carries its context.
    if ev_title and ":" not in base and ev_title.lower() not in base.lower():
        base = f"{ev_title}: {base}"
    return base if base.endswith("?") else base + "?"


def kalshi_candidates(start: datetime, end: datetime, min_volume: float, max_pages: int = 100) -> List[Dict[str, Any]]:
    out, cursor = [], None
    for _ in range(max_pages):
        params = {"status": "open", "with_nested_markets": "true", "limit": 200,
                  "min_close_ts": int(start.timestamp())}
        if cursor:
            params["cursor"] = cursor
        try:
            data = get_json(KALSHI_EVENTS_URL, params)
        except Exception as e:
            print(f"  Kalshi: stopping pagination ({e})")
            break
        for ev in data.get("events") or []:
            out.extend(kalshi_event_to_candidates(ev, start, end, min_volume))
        cursor = data.get("cursor")
        if not cursor:
            break
        time.sleep(0.3)
    return out


def kalshi_event_to_candidates(ev, start, end, min_volume) -> Iterable[Dict[str, Any]]:
    category = (ev.get("category") or "").strip()
    if category.lower() in KALSHI_EXCLUDED_CATEGORIES:
        return []
    rows = []
    for m in ev.get("markets") or []:
        ticker = m.get("ticker") or ""
        close_dt = parse_dt(m.get("close_time"))
        volume = to_float(m.get("volume_fp")) or 0.0
        question = kalshi_question_text(ev, m)
        if (ticker.startswith("KXMVE")  # multi-leg parlay markets
                or m.get("market_type") != "binary" or m.get("status") != "active"
                or close_dt is None or not (start <= close_dt <= end)
                or volume < min_volume or not question or has_excluded_phrase(question)):
            continue
        series = (ev.get("series_ticker") or ev.get("event_ticker") or "").lower()
        rows.append({
            "question_id": f"kalshi:{ticker}",
            "source": "kalshi",
            "question_text": question,
            "resolution_criteria": (m.get("rules_primary") or "").strip(),
            "answer_type": "binary",
            "choices": json.dumps(["Yes", "No"]),
            "set": "live",
            "topic": category,
            "url": f"https://kalshi.com/markets/{series}",
            "resolution_date": iso(close_dt),
            "market_price": kalshi_price(m),
            "volume": round(volume, 2),
            "_event": f"kalshi:{ev.get('event_ticker')}",
        })
    return rows


# ── Output ────────────────────────────────────────────────────────────────────

def load_existing(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            if not r.get("price_time") and r.get("set") == "live":
                r["price_time"] = r.get("collected_at")  # live prices are taken at collection
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in COLUMNS})


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--end", default="2026-11-15", help="last resolution date to include (UTC, YYYY-MM-DD)")
    ap.add_argument("--per-source", type=int, default=200, help="max questions per market")
    ap.add_argument("--max-per-event", type=int, default=1, help="max questions from any one event")
    ap.add_argument("--max-topic-share", type=float, default=0.4, help="max share of one topic per market")
    ap.add_argument("--min-volume-polymarket", type=float, default=5000, help="min traded volume (USD)")
    ap.add_argument("--min-volume-kalshi", type=float, default=500, help="min traded volume (contracts)")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    start = utc_now() + timedelta(hours=24)  # skip questions closing within a day
    end = datetime.fromisoformat(args.end).replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
    collected_at = iso(utc_now())
    print(f"Window: {iso(start)} → {iso(end)}")

    print("Polymarket…")
    poly = pick_top(polymarket_candidates(start, end, args.min_volume_polymarket),
                    args.per_source, args.max_per_event, args.max_topic_share)
    print(f"  {len(poly)} questions")

    print("Kalshi…")
    kal = pick_top(kalshi_candidates(start, end, args.min_volume_kalshi),
                   args.per_source, args.max_per_event, args.max_topic_share)
    print(f"  {len(kal)} questions")

    out_path = Path(args.out)
    existing = load_existing(out_path)
    known = {r["question_id"] for r in existing}
    new = []
    for r in poly + kal:
        if r["question_id"] not in known:
            r["collected_at"] = collected_at
            new.append(r)

    print(f"\nAlready in file: {len(existing)}   New: {len(new)}   Total: {len(existing) + len(new)}")
    if args.dry_run:
        for r in new[:10]:
            print(f"  [{r['source']}] p={r['market_price']} {r['resolution_date'][:10]}  {r['question_text'][:90]}")
        return
    write_rows(out_path, existing + new)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
