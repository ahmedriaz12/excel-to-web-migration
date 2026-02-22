# Fetches price data. Right now it's Yahoo Finance. To switch providers,
# change fetch_prices() and nothing else needs to change.

from __future__ import annotations

import pandas as pd
import yfinance as yf


def fetch_prices(
    ticker: str,
    start_date: str,
    end_date: str | None = None,
) -> pd.DataFrame:
    # Daily closing prices, sorted oldest-first.
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No price data returned for '{ticker}' in the requested range")

    # yfinance sometimes returns multi-level columns, flatten to simple names
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    df = data[["Close"]].copy()
    df = df.reset_index()
    df.columns = ["Date", "Close"]
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    df = df.sort_values("Date").reset_index(drop=True)
    return df
