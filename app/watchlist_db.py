import sqlite3
from typing import List

DB_PATH_DEFAULT = "watchlist.sqlite3"

def init_db(db_path: str = DB_PATH_DEFAULT) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS watchlist (
              symbol TEXT PRIMARY KEY,
              created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()

def add_symbol(symbol: str, db_path: str = DB_PATH_DEFAULT) -> None:
    sym = symbol.strip().upper()
    if not sym.isalpha():
        raise ValueError("Symbol must be letters only.")
    with sqlite3.connect(db_path) as conn:
        conn.execute("INSERT OR IGNORE INTO watchlist (symbol) VALUES (?);", (sym,))
        conn.commit()

def remove_symbol(symbol: str, db_path: str = DB_PATH_DEFAULT) -> None:
    sym = symbol.strip().upper()
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM watchlist WHERE symbol = ?;", (sym,))
        conn.commit()

def list_symbols(db_path: str = DB_PATH_DEFAULT) -> List[str]:
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT symbol FROM watchlist ORDER BY created_at DESC;").fetchall()
    return [r[0] for r in rows]
