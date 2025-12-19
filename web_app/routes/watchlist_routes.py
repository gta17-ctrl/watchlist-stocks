from flask import Blueprint, redirect, render_template, request, url_for
from app.watchlist_db import add_symbol, remove_symbol, list_symbols

watchlist_bp = Blueprint("watchlist", __name__, url_prefix="/watchlist")

@watchlist_bp.get("")
def watchlist_page():
    symbols = list_symbols()
    return render_template("watchlist.html", active_page="WATCHLIST", symbols=symbols)

@watchlist_bp.post("/add")
def add():
    symbol = request.form.get("symbol", "")
    add_symbol(symbol)
    return redirect(url_for("watchlist.watchlist_page"))

@watchlist_bp.post("/remove")
def remove():
    symbol = request.form.get("symbol", "")
    remove_symbol(symbol)
    return redirect(url_for("watchlist.watchlist_page"))
