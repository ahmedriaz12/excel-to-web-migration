# SMA and EMA calculations. Full precision, no rounding until display.

from __future__ import annotations
from typing import List, Optional
import pandas as pd


def compute_sma(prices: pd.Series, window: int) -> pd.Series:
    # Average of the last N closes. First few values are NaN until we have enough data.
    return prices.rolling(window=window, min_periods=window).mean()


def compute_ema(prices: pd.Series, span: int) -> pd.Series:
    # Standard EMA: seed with SMA of first N, then close * k + prev_ema * (1-k)
    k = 2.0 / (span + 1)

    sma_seed = prices.iloc[:span].mean()

    ema_values: List[Optional[float]] = [None] * (span - 1)
    ema_values.append(sma_seed)

    for i in range(span, len(prices)):
        ema_values.append(prices.iloc[i] * k + ema_values[-1] * (1 - k))

    return pd.Series(ema_values, index=prices.index, dtype="float64")


def build_indicator_df(
    dates: pd.Series,
    prices: pd.Series,
    window: int,
    mode: str = "SMA",
) -> pd.DataFrame:
    # Builds a table with Date, Close, and the chosen indicator. Expects dates oldest-first.
    df = pd.DataFrame({"Date": dates, "Close": prices.values})
    df = df.sort_values("Date").reset_index(drop=True)
    close = df["Close"].astype(float)

    if mode.upper() == "SMA":
        df["Indicator"] = compute_sma(close, window)
        df["Indicator_Label"] = f"SMA({window})"
    elif mode.upper() == "EMA":
        df["Indicator"] = compute_ema(close, window)
        df["Indicator_Label"] = f"EMA({window})"
    else:
        raise ValueError(f"Unknown mode '{mode}'; expected 'SMA' or 'EMA'")

    return df
