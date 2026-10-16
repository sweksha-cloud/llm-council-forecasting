"""Market matching for Aye's questions, checked offline (no network calls)."""

import importers.aye_market_prices as amp


def test_yes_token_only_for_yes_no_markets():
    assert amp.yes_token({"outcomes": '["Yes", "No"]', "clobTokenIds": '["111", "222"]'}) == "111"
    assert amp.yes_token({"outcomes": '["Up", "Down"]', "clobTokenIds": '["111", "222"]'}) is None


def test_old_set_matches_market_by_question_text(monkeypatch):
    markets = [{"id": "1", "question": "Will A win?"}, {"id": "2", "question": "Will B win?"}]
    monkeypatch.setattr(amp, "event_markets", lambda slug: markets if slug == "who-wins" else [])
    q = {"question_id": "aye-old:5", "url": "https://polymarket.com/event/who-wins?tid=1",
         "question_text": "will  b win?"}
    assert amp.find_market(q, {})["id"] == "2"
    q["question_text"] = "Will C win?"   # no match among several markets
    assert amp.find_market(q, {}) is None


def test_price_time_is_start_of_collection_day():
    assert amp.price_time("2026-07-15").isoformat() == "2026-07-15T00:00:00+00:00"
