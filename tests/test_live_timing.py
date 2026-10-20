"""Live forecasts made after their market ended are not scored (docs/decisions.md, 2026-10-20)."""

import csv
from pathlib import Path

from scoring.report import load, made_after_resolution

LIVE = {"set": "live", "resolved_at": "2026-10-11T20:07:29Z"}


def test_made_after_resolution():
    assert made_after_resolution(LIVE, {"forecast_at": "2026-10-13T00:52:45Z"})       # game already played
    assert made_after_resolution(LIVE, {"forecast_at": "2026-10-11T20:07:29Z"})       # at the moment it ended
    assert not made_after_resolution(LIVE, {"forecast_at": "2026-10-11T20:07:28Z"})
    assert not made_after_resolution({"set": "live", "resolved_at": ""}, {"forecast_at": "2026-10-13T00:00:00Z"})
    # backtests are asked after resolution by design (as of an earlier date)
    assert not made_after_resolution({**LIVE, "set": "settled"}, {"forecast_at": "2026-10-13T00:52:45Z"})


def _write(path: Path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def test_load_drops_the_forecast_and_its_market_price(tmp_path):
    q, fc = tmp_path / "q.csv", tmp_path / "f.csv"
    _write(q, [{"question_id": "early", "set": "live", "outcome": "1", "market_price": "0.6",
                "resolved_at": "2026-10-11T20:00:00Z"},
               {"question_id": "ok", "set": "live", "outcome": "0", "market_price": "0.4",
                "resolved_at": "2026-10-20T00:00:00Z"}])
    _write(fc, [{"question_id": qid, "setup": "single:a", "probability": p, "raw_response": "{}",
                 "prompt_id": "v2", "members": "", "forecast_at": "2026-10-13T00:00:00Z",
                 "market_price_at_forecast": price}
                for qid, p, price in (("early", "0.99", "0.99"), ("ok", "0.3", "0.35"))])
    outcomes, probs, _, market = load([str(q)], [str(fc)], "live")
    assert probs["single:a"] == {"ok": 0.3}
    assert market == {"early": 0.6, "ok": 0.35}   # the settled 0.99 isn't used; the collected price is
