import json
import time
from flask import Blueprint, render_template, request

from app.stocks_service import (
    fetch_daily_time_series,
    parse_time_series_points,
    points_to_dataframe,
    latest_close,
    format_usd,
)

stocks_bp = Blueprint("stocks", __name__, url_prefix="/stocks")

@stocks_bp.get("/form")
def stocks_form():
    return render_template("stocks_form.html", active_page="STOCKS_FORM")

@stocks_bp.post("/dashboard")
def stocks_dashboard_post():
    symbol = request.form.get("symbol", "").strip().upper()
    return _render_dashboard(symbol)

@stocks_bp.get("/dashboard")
def stocks_dashboard_get():
    symbol = request.args.get("symbol", "").strip().upper()
    return _render_dashboard(symbol)

@stocks_bp.get("/compare")
def compare_form():
    return render_template("compare_form.html", active_page="COMPARE")

@stocks_bp.post("/compare")
def compare_post():
    sym_a = request.form.get("symbol_a", "").strip().upper()
    sym_b = request.form.get("symbol_b", "").strip().upper()

    try:
        data_a = fetch_daily_time_series(sym_a)
        pts_a = parse_time_series_points(data_a)
        df_a = points_to_dataframe(pts_a)

        # small delay to reduce Alpha Vantage rate-limit failures
        time.sleep(12)

        data_b = fetch_daily_time_series(sym_b)
        pts_b = parse_time_series_points(data_b)
        df_b = points_to_dataframe(pts_b)

        payload = {
            "a": {"symbol": sym_a, "series": df_a.to_dict(orient="records")},
            "b": {"symbol": sym_b, "series": df_b.to_dict(orient="records")},
        }
        return render_template(
            "compare_dashboard.html",
            active_page="COMPARE",
            payload_json=json.dumps(payload),
        )
    except Exception as e:
        return render_template("error.html", active_page="COMPARE", message=str(e)), 400

def _render_dashboard(symbol: str):
    try:
        data = fetch_daily_time_series(symbol)
        points = parse_time_series_points(data)
        df = points_to_dataframe(points)
        last_date, last_close = latest_close(points)

        return render_template(
            "stocks_dashboard.html",
            active_page="STOCKS_DASHBOARD",
            symbol=symbol,
            latest_date=last_date.isoformat(),
            latest_close=format_usd(last_close),
            series_json=df.to_json(orient="records"),
        )
    except Exception as e:
        return render_template("error.html", active_page="STOCKS_FORM", message=str(e)), 400
