import pytest
from app.stocks_service import parse_time_series_points, latest_close

SAMPLE = {
  "Time Series (Daily)": {
    "2025-12-18": {"4. close": "100.00"},
    "2025-12-19": {"4. close": "110.50"}
  }
}

def test_parse_points_sorted():
    pts = parse_time_series_points(SAMPLE)
    assert pts[0].date.isoformat() == "2025-12-18"
    assert pts[-1].date.isoformat() == "2025-12-19"

def test_latest_close():
    pts = parse_time_series_points(SAMPLE)
    d, c = latest_close(pts)
    assert d.isoformat() == "2025-12-19"
    assert c == 110.50

def test_parse_raises_if_missing_series():
    with pytest.raises(KeyError):
        parse_time_series_points({})
