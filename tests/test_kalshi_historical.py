"""Kalshi /historical collection path. Offline tests always run; the real-API test runs only with
KALSHI_NETWORK_TESTS=1 (it fetches a few 2025 Fed-decision markets)."""

import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from collect.kalshi_historical import candle_price, historical_markets, historical_price_at, market_row

ROOT = Path(__file__).resolve().parent.parent
utc = lambda *a: datetime(*a, tzinfo=timezone.utc)
START, END, WEEK = utc(2025, 7, 1), utc(2026, 6, 30, 23, 59, 59), timedelta(days=7)
EV = {"event_ticker": "KXFED-25SEP", "series_ticker": "KXFED", "category": "Economics", "title": "Fed decision in Sep 2025?"}


def _market(**kw):
    m = {"ticker": "KXFED-25SEP-C25", "market_type": "binary", "result": "yes", "volume_fp": "9000.00",
         "close_time": "2025-09-17T17:55:00Z", "settlement_ts": "2025-09-17T19:01:42Z", "open_time": "2025-07-30T14:00:00Z",
         "title": "Will the Fed cut rates by 25bps in September 2025?", "yes_sub_title": "Cut 25bps",
         "rules_primary": "Resolves Yes if the Fed cuts by 25bps."}
    m.update(kw)
    return m


def test_candle_price_reads_historical_and_live_formats():
    hist = [{"yes_bid": {"close": "0.8100"}, "yes_ask": {"close": "0.8200"}, "price": {"close": "0.82"}}]
    live = [{"yes_bid": {"close_dollars": "0.40"}, "yes_ask": {"close_dollars": "0.44"}, "price": {"close_dollars": "0.41"}}]
    wide = [{"yes_bid": {"close": "0.10"}, "yes_ask": {"close": "0.60"}, "price": {"close": "0.33"}}]
    assert candle_price(hist) == 0.815 and candle_price(live) == 0.42
    assert candle_price(wide) == 0.33          # spread over 10 cents: last trade
    assert candle_price([]) is None


def test_market_row_applies_the_settled_rules():
    seen = []
    price = lambda ticker, at: seen.append((ticker, at)) or 0.8
    row = market_row(EV, _market(), START, END, 500, WEEK, "kalshi-historical", "2026-10-17T00:00:00Z", price)
    assert row["question_id"] == "kalshi:KXFED-25SEP-C25" and row["outcome"] == 1 and row["market_price"] == 0.8
    assert seen == [("KXFED-25SEP-C25", utc(2025, 9, 10, 17, 55))]     # 7 days before close (earlier than settlement)
    assert row["price_time"] == "2025-09-10T17:55:00Z" and row["resolved_at"] == "2025-09-17T19:01:42Z"
    reject = lambda **kw: market_row(EV, _market(**kw), START, END, 500, WEEK, "x", "t", price) is None
    assert reject(result="")                                            # not settled Yes/No
    assert reject(market_type="scalar")
    assert reject(volume_fp="100")                                      # below min volume
    assert reject(close_time="2025-05-01T00:00:00Z", settlement_ts="2025-05-01T01:00:00Z")   # outside the window
    assert reject(settlement_ts="2026-08-01T00:00:00Z")                 # settled after the window
    assert reject(open_time="2025-09-15T00:00:00Z")                     # opened after the price date
    assert reject(ticker="KXMVE-123")                                   # multivariate combo
    assert market_row(EV, _market(), START, END, 500, WEEK, "x", "t", lambda t, a: None) is None   # no price


def test_refuses_to_write_the_questions_file():
    res = subprocess.run([sys.executable, "-m", "collect.kalshi_historical", "--series", "X",
                          "--out", "data/questions.csv"], cwd=ROOT, capture_output=True, text=True)
    assert res.returncode != 0 and "Refusing to write data/questions.csv" in res.stderr


@pytest.mark.skipif(os.environ.get("KALSHI_NETWORK_TESTS") != "1", reason="set KALSHI_NETWORK_TESTS=1 to hit the real API")
def test_real_api_few_markets():
    markets = {m["ticker"]: m for m in historical_markets("KXFEDDECISION-25SEP")}
    m = markets["KXFEDDECISION-25SEP-C25"]
    assert m["result"] == "yes" and m["market_type"] == "binary"
    ev = {"event_ticker": "KXFEDDECISION-25SEP", "series_ticker": "KXFEDDECISION", "category": "Economics",
          "title": "Fed decision in Sep 2025?"}
    row = market_row(ev, m, START, END, 500, WEEK, "kalshi-historical", "t")
    assert row and 0.5 < row["market_price"] < 1 and row["outcome"] == 1   # the cut was priced in a week before
    assert historical_price_at("KXFEDDECISION-25SEP-H26", utc(2025, 9, 10, 17, 55)) is not None
