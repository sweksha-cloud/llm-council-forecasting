"""Current market price for a question, so forecasts can record the market at forecast time."""

from typing import Optional

from collect.collect_live import get_json, kalshi_price, parse_json_list, to_float

POLYMARKET_MARKET_URL = "https://gamma-api.polymarket.com/markets/{id}"
KALSHI_MARKET_URL = "https://api.elections.kalshi.com/trade-api/v2/markets/{ticker}"


def current_price(question_id: str) -> Optional[float]:
    """Market probability of Yes right now, or None if it can't be fetched."""
    source, _, key = question_id.partition(":")
    try:
        if source == "polymarket":
            m = get_json(POLYMARKET_MARKET_URL.format(id=key), {})
            prices = parse_json_list(m.get("outcomePrices"))
            return to_float(prices[0]) if prices else None
        if source == "kalshi":
            data = get_json(KALSHI_MARKET_URL.format(ticker=key), {})
            return kalshi_price(data.get("market") or {})
    except Exception:
        return None
    return None
