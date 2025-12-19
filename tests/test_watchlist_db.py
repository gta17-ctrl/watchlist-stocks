from app.watchlist_db import init_db, add_symbol, remove_symbol, list_symbols

def test_watchlist_crud(tmp_path):
    db = str(tmp_path / "test.sqlite3")
    init_db(db)

    add_symbol("AAPL", db)
    add_symbol("AAPL", db)
    add_symbol("MSFT", db)

    syms = list_symbols(db)
    assert "AAPL" in syms
    assert "MSFT" in syms

    remove_symbol("AAPL", db)
    syms2 = list_symbols(db)
    assert "AAPL" not in syms2
