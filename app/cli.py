import sys
from app.stocks_service import fetch_daily_time_series, parse_time_series_points, latest_close, format_usd

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.cli <SYMBOL>")
        raise SystemExit(1)

    symbol = sys.argv[1].strip().upper()
    data = fetch_daily_time_series(symbol)
    points = parse_time_series_points(data)
    d, c = latest_close(points)

    print(f"{symbol} latest close: {format_usd(c)} on {d.isoformat()}")

if __name__ == "__main__":
    main()
