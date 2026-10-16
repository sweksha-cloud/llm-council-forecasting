"""
collect_settled.py
------------------
Collects SETTLED (already resolved) Yes/No questions from Polymarket and
Kalshi, with the outcome and the market price from N days before the market
closed, taken from each market's price history.

Output: appended to data/questions.csv with set = "settled". Questions
already in the file are kept unchanged.

The price is taken N days before the scheduled close, or before the resolution if
that came first, so the "as of" date given to the models is always before the event.

`--reprice-late` fixes questions already in the file whose price was taken later than N days
before the earlier of close and resolution (collected before that rule; Polymarket only).

Usage (run from the repo root):
  python3 -m collect.collect_settled                         # resolved 2026-07-01 → yesterday, 200 per source
  python3 -m collect.collect_settled --from 2026-07-01 --horizon-days 7 --per-source 200
  python3 -m collect.collect_settled --dry-run
"""

import argparse
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from collect.collect_live import (DEFAULT_OUT, KALSHI_EVENTS_URL, KALSHI_EXCLUDED_CATEGORIES,
                                  POLYMARKET_EVENTS_URL, POLYMARKET_EXCLUDED_TAGS, get_json,
                                  has_excluded_phrase, iso, kalshi_question_text, load_existing,
                                  parse_dt, parse_json_list, pick_top, to_float, utc_now,
                                  write_rows)

POLYMARKET_HISTORY_URL = "https://clob.polymarket.com/prices-history"
POLYMARKET_MARKET_URL = "https://gamma-api.polymarket.com/markets/{id}"
KALSHI_CANDLES_URL = "https://api.elections.kalshi.com/trade-api/v2/series/{series}/markets/{ticker}/candlesticks"

POLYMARKET_TOPICS = ("Politics", "Sports", "Science", "Tech", "Culture", "Economy", "World",
                     "Business", "Geopolitics", "Elections", "Entertainment", "Weather")


# ── Price history ─────────────────────────────────────────────────────────────

def polymarket_price_at(token_id: str, at: datetime) -> Optional[float]:
    """Last traded Yes price at or before `at` (searches the two days before it)."""
    params = {"market": token_id, "startTs": int((at - timedelta(days=2)).timestamp()),
              "endTs": int(at.timestamp()), "fidelity": 60}
    try:
        history = get_json(POLYMARKET_HISTORY_URL, params).get("history") or []
    except Exception:
        return None
    points = [h for h in history if h.get("t", 0) <= at.timestamp()]
    return to_float(points[-1]["p"]) if points else None


def kalshi_price_at(series: str, ticker: str, at: datetime) -> Optional[float]:
    """Yes price at `at` from hourly candles: bid/ask midpoint if quoted, else the last trade."""
    params = {"start_ts": int((at - timedelta(days=2)).timestamp()), "end_ts": int(at.timestamp()),
              "period_interval": 60}
    try:
        candles = get_json(KALSHI_CANDLES_URL.format(series=series, ticker=ticker), params).get("candlesticks") or []
    except Exception:
        return None
    for c in reversed(candles):
        bid = to_float((c.get("yes_bid") or {}).get("close_dollars"))
        ask = to_float((c.get("yes_ask") or {}).get("close_dollars"))
        if bid is not None and ask is not None and 0 < bid <= ask < 1 and ask - bid <= 0.10:
            return round((bid + ask) / 2, 4)
        last = to_float((c.get("price") or {}).get("close_dollars"))
        if last is not None and last > 0:
            return last
    return None


# ── Polymarket ────────────────────────────────────────────────────────────────

def parse_closed_time(s: Optional[str]) -> Optional[datetime]:
    """Polymarket's closedTime looks like '2026-09-16 20:02:43+00'."""
    if not s:
        return None
    s = s.strip().replace(" ", "T")
    if s.endswith("+00"):
        s += ":00"
    return parse_dt(s)


def polymarket_candidates(start: datetime, end: datetime, min_volume: float,
                          pages_per_chunk: int = 3) -> List[Dict[str, Any]]:
    """Results come highest-volume first, so a few pages per 2-day window are enough."""
    out, seen = [], set()
    chunk_start = start
    while chunk_start < end:
        chunk_end = min(chunk_start + timedelta(days=2), end)
        offset = 0
        while True:
            params = {"closed": "true", "limit": 100, "offset": offset,
                      "end_date_min": iso(chunk_start), "end_date_max": iso(chunk_end),
                      "order": "volume", "ascending": "false"}
            try:
                batch = get_json(POLYMARKET_EVENTS_URL, params)
            except Exception:
                break  # page limit reached; the rest is the lowest-volume tail
            if not batch:
                break
            for ev in batch:
                out.extend(polymarket_event_rows(ev, min_volume, seen, start, end))
            if len(batch) < 100 or offset >= 100 * (pages_per_chunk - 1):
                break
            offset += 100
            time.sleep(0.3)
        print(f"  {chunk_start.date()}: {len(out)} candidates so far", flush=True)
        chunk_start = chunk_end
    return out


def polymarket_event_rows(ev, min_volume, seen, start: Optional[datetime] = None,
                          end: Optional[datetime] = None) -> Iterable[Dict[str, Any]]:
    """Yes/No markets of one closed event. The API filters events by the event's end date, but a
    market inside an event can close or resolve much earlier or later, so with a window
    (start, end) each market's own scheduled close and resolution must both fall inside it."""
    tags = [str(t.get("label", "")) for t in (ev.get("tags") or [])]
    if {t.lower() for t in tags} & POLYMARKET_EXCLUDED_TAGS:
        return []
    topic = next((t for t in tags if t in POLYMARKET_TOPICS), "")
    rows = []
    for m in ev.get("markets") or []:
        mid = str(m.get("id"))
        question = (m.get("question") or "").strip()
        outcomes = [o.lower() for o in parse_json_list(m.get("outcomes"))]
        prices = parse_json_list(m.get("outcomePrices"))
        tokens = parse_json_list(m.get("clobTokenIds"))
        volume = to_float(m.get("volumeNum")) or 0.0
        close_dt = parse_dt(m.get("endDate"))
        resolved_dt = parse_closed_time(m.get("closedTime")) or close_dt
        if start and end and not (close_dt and start <= close_dt <= end and start <= resolved_dt <= end):
            continue
        if (mid in seen or not question or outcomes != ["yes", "no"] or prices not in (["1", "0"], ["0", "1"])
                or not m.get("closed") or not tokens or close_dt is None
                or volume < min_volume or has_excluded_phrase(question)):
            continue
        seen.add(mid)
        rows.append({
            "question_id": f"polymarket:{mid}", "source": "polymarket",
            "question_text": question,
            "resolution_criteria": (m.get("description") or "").strip(),
            "answer_type": "binary", "choices": json.dumps(["Yes", "No"]), "set": "settled",
            "topic": topic, "url": f"https://polymarket.com/event/{ev.get('slug', '')}",
            "resolution_date": iso(close_dt), "volume": round(volume, 2),
            "outcome": 1 if prices == ["1", "0"] else 0,
            "resolved_at": iso(resolved_dt),
            "_event": f"polymarket:{ev.get('id')}",
            # Price before whichever came first: the scheduled close or the resolution. Polymarket
            # can resolve days after the scheduled close, and the event is over by then.
            "_price_key": tokens[0], "_close": min(close_dt, resolved_dt),
        })
    return rows


# ── Kalshi ────────────────────────────────────────────────────────────────────

def kalshi_candidates(start: datetime, end: datetime, min_volume: float, max_pages: int = 100) -> List[Dict[str, Any]]:
    out, cursor = [], None
    for _ in range(max_pages):
        params = {"status": "settled", "with_nested_markets": "true", "limit": 200,
                  "min_close_ts": int(start.timestamp()), "max_close_ts": int(end.timestamp())}
        if cursor:
            params["cursor"] = cursor
        try:
            data = get_json(KALSHI_EVENTS_URL, params)
        except Exception as e:
            print(f"  Kalshi: stopping pagination ({e})")
            break
        for ev in data.get("events") or []:
            out.extend(kalshi_event_rows(ev, start, end, min_volume))
        print(f"  Kalshi page: {len(out)} candidates so far", flush=True)
        cursor = data.get("cursor")
        if not cursor:
            break
        time.sleep(0.3)
    return out


def kalshi_event_rows(ev, start, end, min_volume) -> Iterable[Dict[str, Any]]:
    category = (ev.get("category") or "").strip()
    if category.lower() in KALSHI_EXCLUDED_CATEGORIES:
        return []
    rows = []
    for m in ev.get("markets") or []:
        ticker = m.get("ticker") or ""
        close_dt = parse_dt(m.get("close_time"))
        volume = to_float(m.get("volume_fp")) or 0.0
        question = kalshi_question_text(ev, m)
        if (ticker.startswith("KXMVE") or m.get("market_type") != "binary"
                or m.get("result") not in ("yes", "no")
                or close_dt is None or not (start <= close_dt <= end)
                or volume < min_volume or not question or has_excluded_phrase(question)):
            continue
        series = ev.get("series_ticker") or ev.get("event_ticker") or ""
        rows.append({
            "question_id": f"kalshi:{ticker}", "source": "kalshi",
            "question_text": question,
            "resolution_criteria": (m.get("rules_primary") or "").strip(),
            "answer_type": "binary", "choices": json.dumps(["Yes", "No"]), "set": "settled",
            "topic": category, "url": f"https://kalshi.com/markets/{series.lower()}",
            "resolution_date": iso(close_dt), "volume": round(volume, 2),
            "outcome": 1 if m.get("result") == "yes" else 0,
            "resolved_at": iso(close_dt),
            "_event": f"kalshi:{ev.get('event_ticker')}",
            "_price_key": (series, ticker), "_close": close_dt,
            "_open": parse_dt(m.get("open_time")),
        })
    return rows


# ── Main ──────────────────────────────────────────────────────────────────────

def add_prices(candidates: List[Dict[str, Any]], horizon: timedelta, want: int,
               max_per_event: int, max_topic_share: float) -> List[Dict[str, Any]]:
    """Look up the pre-close price for the best candidates until `want` have one.
    Questions with no price history at that point (e.g. the market opened later) are dropped."""
    ranked = pick_top(candidates, len(candidates), max_per_event, 1.0)  # dedupe + one per event
    with_price = []
    for c in ranked:
        at = c["_close"] - horizon
        if c.get("_open") and c["_open"] > at:
            continue
        if c["source"] == "polymarket":
            price = polymarket_price_at(c["_price_key"], at)
        else:
            price = kalshi_price_at(*c["_price_key"], at)
        if price is None:
            continue
        c["market_price"], c["price_time"] = price, iso(at)
        with_price.append(c)
        if len(with_price) % 50 == 0:
            print(f"  prices found: {len(with_price)}", flush=True)
        if len(with_price) >= want * 2:  # enough spare to apply the topic cap
            break
        time.sleep(0.15)
    return pick_top(with_price, want, max_per_event, max_topic_share)


def priced_too_late(r: Dict[str, str], horizon: timedelta) -> bool:
    """True if a backtest question's price was taken later than `horizon` before the earlier of its
    scheduled close and its resolution (1 hour of slack for timestamp rounding)."""
    close, priced = parse_dt(r.get("resolution_date")), parse_dt(r.get("price_time"))
    resolved = parse_dt(r.get("resolved_at")) or close
    if r.get("set") == "live" or not close or not priced:
        return False
    return priced > min(close, resolved) - horizon + timedelta(hours=1)


def reprice_late(path: Path, horizon: timedelta, dry_run: bool) -> None:
    """Re-take the price `horizon` before the earlier of close and resolution, for backtest questions
    priced later than that (collected under the old rule, which anchored on the resolution only).
    Where there was no trade at the new date, the price is cleared and the question is skipped."""
    rows = load_existing(path)
    fixed, cleared = 0, 0
    for r in rows:
        if not priced_too_late(r, horizon):
            continue
        close = parse_dt(r.get("resolution_date"))
        resolved = parse_dt(r.get("resolved_at")) or close
        if not r["question_id"].startswith("polymarket:"):
            print(f"  ! {r['question_id']}: only Polymarket can be repriced; drop it or fix by hand")
            continue
        market = get_json(POLYMARKET_MARKET_URL.format(id=r["question_id"].split(":", 1)[1]), {})
        tokens = parse_json_list(market.get("clobTokenIds"))
        at = min(close, resolved) - horizon
        price = polymarket_price_at(tokens[0], at) if tokens else None
        print(f"  {r['question_id']}: {r['price_time']} p={r['market_price']} → {iso(at)} p={price}"
              f"  {r['question_text'][:60]}")
        if price is None:
            print("    no trade at the new date: price cleared, the question will be skipped")
            r["market_price"], r["price_time"] = "", ""
            cleared += 1
            continue
        r["market_price"], r["price_time"] = price, iso(at)
        fixed += 1
    print(f"Repriced {fixed} questions, cleared {cleared}")
    if (fixed or cleared) and not dry_run:
        write_rows(path, rows)
        print(f"Saved to {path}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="start", default="2026-07-01", help="earliest close date (UTC, YYYY-MM-DD)")
    ap.add_argument("--to", dest="end", default=None, help="latest close date (default: yesterday)")
    ap.add_argument("--horizon-days", type=float, default=7, help="take the market price this long before close")
    ap.add_argument("--per-source", type=int, default=200)
    ap.add_argument("--max-per-event", type=int, default=1)
    ap.add_argument("--max-topic-share", type=float, default=0.4)
    ap.add_argument("--min-volume-polymarket", type=float, default=5000)
    ap.add_argument("--min-volume-kalshi", type=float, default=500)
    ap.add_argument("--set-name", default="settled",
                    help='value for the "set" column, e.g. "contamination" for the Week 8 older subset')
    ap.add_argument("--skip-kalshi", action="store_true", help="Kalshi's public API has no markets before ~2025")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reprice-late", action="store_true",
                    help="only fix existing questions priced later than N days before close/resolution")
    args = ap.parse_args()
    if args.reprice_late:
        reprice_late(Path(args.out), timedelta(days=args.horizon_days), args.dry_run)
        return

    start = datetime.fromisoformat(args.start).replace(tzinfo=timezone.utc)
    end = (datetime.fromisoformat(args.end).replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
           if args.end else utc_now() - timedelta(days=1))
    horizon = timedelta(days=args.horizon_days)
    collected_at = iso(utc_now())
    print(f"Closed between {iso(start)} and {iso(end)}; price taken {args.horizon_days:g} days before close")

    print("Polymarket…")
    poly = add_prices(polymarket_candidates(start, end, args.min_volume_polymarket), horizon,
                      args.per_source, args.max_per_event, args.max_topic_share)
    print(f"  {len(poly)} questions")
    kal = []
    if not args.skip_kalshi:
        print("Kalshi…")
        kal = add_prices(kalshi_candidates(start, end, args.min_volume_kalshi), horizon,
                         args.per_source, args.max_per_event, args.max_topic_share)
        print(f"  {len(kal)} questions")

    out_path = Path(args.out)
    existing = load_existing(out_path)
    known = {r["question_id"] for r in existing}
    new = [dict(r, collected_at=collected_at, set=args.set_name) for r in poly + kal if r["question_id"] not in known]
    print(f"\nAlready in file: {len(existing)}   New: {len(new)}   Total: {len(existing) + len(new)}")
    if args.dry_run:
        for r in new[:10]:
            print(f"  [{r['source']}] p={r['market_price']} outcome={r['outcome']} {r['resolution_date'][:10]}  {r['question_text'][:80]}")
        return
    write_rows(out_path, existing + new)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
