# watchlist-stocks
Flask web application that allows users to explore stock data, compare tickers, and maintain a personal watchlist.

The app integrates with the **Alpha Vantage API** to retrieve daily stock price data and visualize it using interactive charts.

---

## Features

- Search for a stock ticker and view its daily closing price chart
- Compare two stock tickers on the same chart
- Save and remove tickers in a persistent watchlist
- SQLite-backed storage for saved tickers
- Error handling for invalid symbols and API limits

---

## Tech Stack

- **Python 3.11**
- **Flask** (web framework)
- **Alpha Vantage API** (stock data)
- **Plotly.js** (charting)
- **SQLite** (watchlist persistence)
- **Pytest** (testing)
- **GitHub Actions** (continuous integration)

--

## Setup Instructions

### 1. Create and activate a viral environment (recommended)

Using conda:
'''bash
conda create -n watchlist-stocks python=3.11 -y
conda activate watchlist-stocks

## Install Dependencies
pip install -r requirements.txt

Add API Key (create a .env file in the project root with your Alpha Vantage API key:

## Running the App
python -m web_app.web_app

## Open your browser and go to:
http://127.0.0.1

## Running Tests
pytest -q


