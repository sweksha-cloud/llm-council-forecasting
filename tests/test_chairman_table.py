import json

import pytest

from analysis.chairman_table import build

MEMBERS = ["a", "b", "c"]


def _f(qid, setup, p, members=None):
    return {"question_id": qid, "setup": setup, "probability": "" if p is None else str(p),
            "members": json.dumps(members) if members else "", "market_price_at_forecast": "0.4",
            "prompt_id": "v2"}


@pytest.fixture
def rows():
    questions = [{"question_id": "q0", "set": "settled", "outcome": "1", "market_price": "0.5"},
                 {"question_id": "q1", "set": "settled", "outcome": "", "market_price": "0.5"},
                 {"question_id": "q2", "set": "live", "outcome": "0", "market_price": "0.5"}]
    forecasts = [_f("q0", "single:a", 0.2), _f("q0", "single:b", 0.4), _f("q0", "single:c", None),
                 _f("q0", "council:chair=a", 0.9, MEMBERS),
                 _f("q0", "council:chair=a", 0.1, MEMBERS),  # later duplicate: ignored
                 _f("q1", "single:a", 0.5), _f("q1", "council:chair=a", 0.5, MEMBERS),
                 _f("q2", "single:a", 0.5), _f("q2", "council:chair=a", 0.5, MEMBERS)]
    return build(questions, forecasts, which_set="settled", resolved_only=True)


def test_one_row_per_resolved_question_in_set(rows):
    assert [r["question_id"] for r in rows] == ["q0"]


def test_member_stats_skip_abstentions(rows):
    r = rows[0]
    assert r["p_c"] is None and r["n_members"] == 2
    assert r["member_mean"] == pytest.approx(0.3) and r["member_sd"] == pytest.approx(0.1)


def test_first_council_forecast_wins_and_range_flag(rows):
    r = rows[0]
    assert r["chair_p"] == 0.9 and r["chair_minus_mean"] == pytest.approx(0.6)
    assert r["chair_outside_range"] is True
    assert r["market_price"] == 0.4
