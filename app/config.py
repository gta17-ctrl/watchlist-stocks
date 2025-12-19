import os
from dotenv import load_dotenv

load_dotenv()

def get_alpha_vantage_key() -> str:
    key = os.getenv("ALPHAVANTAGE_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing ALPHAVANTAGE_API_KEY. Create a .env file based on .env.example.")
    return key
