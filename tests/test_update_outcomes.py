from collect.update_outcomes import kalshi_resolution, polymarket_resolution


def test_polymarket_resolved_yes_and_no():
    yes = {"closed": True, "outcomes": '["Yes", "No"]', "outcomePrices": '["1", "0"]',
           "closedTime": "2026-09-16 20:02:43+00"}
    no = {**yes, "outcomePrices": '["0", "1"]'}
    assert polymarket_resolution(yes) == (1, "2026-09-16T20:02:43Z")
    assert polymarket_resolution(no)[0] == 0


def test_polymarket_not_resolved_yet():
    assert polymarket_resolution({"closed": False, "outcomes": '["Yes", "No"]',
                                  "outcomePrices": '["0.62", "0.38"]'}) is None
    # closed for trading but price not settled to 1/0 yet
    assert polymarket_resolution({"closed": True, "outcomes": '["Yes", "No"]',
                                  "outcomePrices": '["0.99", "0.01"]'}) is None


def test_kalshi_resolution():
    assert kalshi_resolution({"result": "yes", "settlement_ts": "2026-10-12T14:05:00Z"}) == (1, "2026-10-12T14:05:00Z")
    assert kalshi_resolution({"result": "no", "close_time": "2026-10-12T14:00:00Z"}) == (0, "2026-10-12T14:00:00Z")
    assert kalshi_resolution({"result": ""}) is None
