"""
kalshi_historical.py
--------------------
Collection path for older settled Kalshi markets (next-semester work; nothing here is used by
the current question sets, see docs/decisions.md 2026-10-16).

Kalshi's regular endpoints stop serving a market's details some time after it settles: the event
is still listed, but `/markets?event_ticker=...` comes back empty. Those markets are served by
`/historical/markets`, with price history at `/historical/markets/{ticker}/candlesticks`.
`/historical/markets` ignores close-date filters, so markets are found series by series:

  /series                                   every series (about 15,000; filter by category)
  /events?series_ticker=S&status=settled    that series' settled events (still listed)
  /historical/markets?event_ticker=E        the event's markets
  /historical/markets/{T}/candlesticks      hourly candles, for the price N days before close

The filters and the price rule are the ones the settled collector uses: binary markets with a
Yes/No result, minimum volume, excluded categories and phrases, scheduled close and settlement
inside the window, price N days before the earlier of close and settlement (bid/ask midpoint if
the spread is at most 10 cents, else the last trade). Output rows are in the questions format.

This never writes data/questions.csv: --out must be a different file, and the rows are meant to
be reviewed (and deduplicated, one per event, topic cap) before any of them join a question set.

Usage (from the repo root):
  python3 -m collect.kalshi_historical --series KXFEDDECISION KXCPIYOY --from 2025-07-01 --to 2026-06-30 \\
      --out data/tmp/kalshi_hist.csv
  python3 -m collect.kalshi_historical --categories Economics Politics --max-series 50 --out data/tmp/k.csv
"""

import argparse
import csv
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from collect.collect_live import (KALSHI_EXCLUDED_CATEGORIES, get_json, has_excluded_phrase, iso,
                                  kalshi_question_text, parse_dt, to_float)

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.elections.kalshi.com/trade-api/v2"
COLUMNS = ["question_id", "source", "question_text", "resolution_criteria", "answer_type", "choices", "set",
           "topic", "url", "collected_at", "resolution_date", "market_price", "price_time", "volume",
           "outcome", "resolved_at"]


def _paged(path: str, params: Dict[str, Any], key: str, max_pages: int = 50) -> Iterable[Dict[str, Any]]:
    cursor = None
    for _ in range(max_pages):
        page = get_json(API + path, {**params, **({"cursor": cursor} if cursor else {})})
        yield from page.get(key) or []
        cursor = page.get("cursor")
        if not cursor:
            return
        time.sleep(0.1)


def list_series(categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Every series, optionally only some categories; excluded categories (e.g. crypto) are dropped."""
    out = []
    for s in _paged("/series", {}, "series"):
        cat = (s.get("category") or "").strip()
        if cat.lower() in KALSHI_EXCLUDED_CATEGORIES or (categories and cat not in categories):
            continue
        out.append(s)
    return out


def settled_events(series_ticker: str) -> List[Dict[str, Any]]:
    return list(_paged("/events", {"series_ticker": series_ticker, "status": "settled", "limit": 200}, "events"))


def historical_markets(event_ticker: str) -> List[Dict[str, Any]]:
    return list(_paged("/historical/markets", {"event_ticker": event_ticker, "limit": 200}, "markets"))


def _candle_value(c: Dict[str, Any], side: str) -> Optional[float]:
    """Closing value of one side of a candle; historical candles use `close`, live ones `close_dollars`."""
    part = c.get(side) or {}
    return to_float(part.get("close_dollars", part.get("close")))


def candle_price(candles: List[Dict[str, Any]]) -> Optional[float]:
    """Latest usable Yes price: bid/ask midpoint if quoted with a spread of at most 10 cents, else the last trade."""
    for c in reversed(candles):
        bid, ask = _candle_value(c, "yes_bid"), _candle_value(c, "yes_ask")
        if bid is not None and ask is not None and 0 < bid <= ask < 1 and ask - bid <= 0.10:
            return round((bid + ask) / 2, 4)
        last = _candle_value(c, "price")
        if last is not None and last > 0:
            return last
    return None


def historical_price_at(ticker: str, at: datetime) -> Optional[float]:
    """Yes price at `at` from the two days of hourly candles before it."""
    params = {"start_ts": int((at - timedelta(days=2)).timestamp()), "end_ts": int(at.timestamp()),
              "period_interval": 60}
    try:
        candles = get_json(f"{API}/historical/markets/{ticker}/candlesticks", params).get("candlesticks") or []
    except Exception:
        return None
    return candle_price(candles)


def market_row(ev: Dict[str, Any], m: Dict[str, Any], start: datetime, end: datetime, min_volume: float,
               horizon: timedelta, set_name: str, collected_at: str, price_fn=historical_price_at) -> Optional[Dict]:
    """One question row, or None if the market doesn't qualify or has no price at the horizon."""
    ticker = m.get("ticker") or ""
    close = parse_dt(m.get("close_time"))
    settled = parse_dt(m.get("settlement_ts")) or close
    question = kalshi_question_text(ev, m)
    if (ticker.startswith("KXMVE") or m.get("market_type") != "binary" or m.get("result") not in ("yes", "no")
            or not close or not (start <= close <= end) or not (start <= settled <= end)
            or (to_float(m.get("volume_fp")) or 0) < min_volume or not question or has_excluded_phrase(question)):
        return None
    at = min(close, settled) - horizon
    opened = parse_dt(m.get("open_time"))
    if opened and opened > at:
        return None
    price = price_fn(ticker, at)
    if price is None:
        return None
    series = ev.get("series_ticker") or ""
    return {"question_id": f"kalshi:{ticker}", "source": "kalshi", "question_text": question,
            "resolution_criteria": (m.get("rules_primary") or "").strip(), "answer_type": "binary",
            "choices": json.dumps(["Yes", "No"]), "set": set_name, "topic": (ev.get("category") or "").strip(),
            "url": f"https://kalshi.com/markets/{series.lower()}", "collected_at": collected_at,
            "resolution_date": iso(close), "market_price": price, "price_time": iso(at),
            "volume": round(to_float(m.get("volume_fp")) or 0, 2), "outcome": 1 if m["result"] == "yes" else 0,
            "resolved_at": iso(settled)}


def collect(series: List[str], start: datetime, end: datetime, min_volume: float, horizon: timedelta,
            set_name: str) -> List[Dict]:
    collected_at = iso(datetime.now(timezone.utc))
    rows = []
    for s in series:
        events = settled_events(s)
        kept = 0
        for ev in events:
            strike = parse_dt(ev.get("strike_date"))
            if strike and not (start - timedelta(days=30) <= strike <= end + timedelta(days=30)):
                continue  # far outside the window; skip the market lookups
            for m in historical_markets(ev["event_ticker"]):
                row = market_row(ev, m, start, end, min_volume, horizon, set_name, collected_at)
                if row:
                    rows.append(row)
                    kept += 1
        print(f"  {s}: {len(events)} settled events, {kept} markets kept", flush=True)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--series", nargs="*", help="series tickers (default: every series in --categories)")
    ap.add_argument("--categories", nargs="*", help="Kalshi categories, e.g. Economics Politics")
    ap.add_argument("--max-series", type=int, default=0, help="stop after this many series (0 = all)")
    ap.add_argument("--from", dest="start", default="2025-07-01")
    ap.add_argument("--to", dest="end", default="2026-06-30")
    ap.add_argument("--horizon-days", type=float, default=7)
    ap.add_argument("--min-volume", type=float, default=500)
    ap.add_argument("--set-name", default="kalshi-historical")
    ap.add_argument("--out", required=True, help="a separate CSV for review (never data/questions.csv)")
    args = ap.parse_args()
    out = Path(args.out).resolve()
    if out == (ROOT / "data" / "questions.csv").resolve():
        raise SystemExit("Refusing to write data/questions.csv; write to a separate file and review it first.")
    start = datetime.fromisoformat(args.start).replace(tzinfo=timezone.utc)
    end = datetime.fromisoformat(args.end).replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
    series = args.series or [s["ticker"] for s in list_series(args.categories)]
    if args.max_series:
        series = series[:args.max_series]
    print(f"{len(series)} series; settled markets closing {args.start} to {args.end}")
    rows = collect(series, start, end, args.min_volume, timedelta(days=args.horizon_days), args.set_name)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} markets written to {out}")


if __name__ == "__main__":
    main()
