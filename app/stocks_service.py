from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Dict, List, Tuple

import requests
import pandas as pd

from app.config import get_alpha_vantage_key

ALPHA_URL = "https://www.alphavantage.co/query"

@dataclass(frozen=True)
class StockPoint:
    date: dt.date
    close: float

def format_usd(value: float) -> str:
    return f"${value:,.2f}"

def fetch_daily_time_series(symbol: str, session: requests.Session | None = None) -> Dict:
    sym = symbol.strip().upper()
    if not sym.isalpha():
        raise ValueError("Symbol must be letters only (e.g., AAPL).")

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": sym,
        "apikey": get_alpha_vantage_key(),
        "outputsize": "compact",
    }

    sess = session or requests.Session()
    resp = sess.get(ALPHA_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if "Error Message" in data:
        raise RuntimeError("Alpha Vantage error: invalid symbol or request.")
    if "Note" in data:
        raise RuntimeError("Alpha Vantage rate limit hit. Try again in a minute.")
    if "Time Series (Daily)" not in data:
        raise RuntimeError("Unexpected API response (missing time series).")

    return data

def parse_time_series_points(data: Dict) -> List[StockPoint]:
    series = data["Time Series (Daily)"]
    points: List[StockPoint] = []

    for date_str, row in series.items():
        close_str = row.get("4. close")
        if close_str is None:
            continue
        points.append(
            StockPoint(
                date=dt.date.fromisoformat(date_str),
                close=float(close_str),
            )
        )

    points.sort(key=lambda p: p.date)
    if not points:
        raise RuntimeError("No data points parsed from API response.")
    return points

def points_to_dataframe(points: List[StockPoint]) -> pd.DataFrame:
    return pd.DataFrame(
        {"date": [p.date.isoformat() for p in points], "close": [p.close for p in points]}
    )

def latest_close(points: List[StockPoint]) -> Tuple[dt.date, float]:
    last = points[-1]
    return last.date, last.close
