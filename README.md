# SMA / EMA Analyzer

This is the web version of the Excel workbook. It computes Simple Moving
Average (SMA) and Exponential Moving Average (EMA) using daily closing
prices.

The SMA calculations were validated directly against the Excel workbook
using the exact same exported close prices. The results match within
normal floating-point precision.

The live web app currently pulls prices from Yahoo Finance. Because
different providers may handle price adjustments and calendars
differently, live values may not be identical to MS365/Refinitiv. The
calculation logic itself is the same.

------------------------------------------------------------------------

## How to run

    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload --port 8000

Open:

http://localhost:8000

------------------------------------------------------------------------

## Excel inputs (SMA_Graph sheet)

The Excel sheet allows changing:

-   B1 -- Ticker\
-   B2 -- Moving average window (days)\
-   B3 -- Start date\
-   B4 -- End date

In the web app these correspond to:

-   Ticker\
-   Moving average window\
-   Start date

The end date defaults to the most recent available trading day.

------------------------------------------------------------------------

## SMA definition

SMA is the average of the last N trading-day closing prices.

For example, a 10-day SMA on 2026-02-03 averages the closes from
2026-02-03 back through the previous 9 trading days.

The Excel sheet stores dates newest-first and uses `AVERAGE()` across N
consecutive cells.\
The web engine produces the same result using a trailing rolling mean.

No rounding is applied during calculation. Values are rounded only for
display in the UI.

------------------------------------------------------------------------

## EMA definition

EMA uses exponential weighting:

    k = 2 / (N + 1)
    EMA(t) = Close(t) × k + EMA(t-1) × (1 − k)

Seeding method:

The first EMA value is the SMA of the first N closing prices.

The current Excel workbook does not compute EMA, so there is no Excel
baseline for comparison.\
If a different EMA convention is preferred (e.g., different seeding),
the calculation can be adjusted easily.

------------------------------------------------------------------------

## Parity validation (SMA)

Validation was performed using the same close prices exported from the
Excel workbook.

Process:

1.  Extracted 48 trading days of MMM data from the Excel `SMA_Graph`
    sheet.
2.  Recomputed SMA(10) in Python using the same closes.
3.  Compared values row by row.

Results:

-   Rows compared: 39\
-   Max absolute difference: 5.68e-14\
-   Mean absolute difference: 1.02e-14\
-   Threshold: 1e-12\
-   Status: PASS

The differences observed are normal floating-point precision noise.

To re-run validation:

    python validation/validate_parity.py

This generates:

    validation/diff_report.csv

------------------------------------------------------------------------

## API endpoints

    GET /                Web UI
    GET /api/analyze     Returns price + indicator data
    GET /api/diff-report Downloads SMA parity report

Parameters for `/api/analyze`:

-   ticker (default MMM)\
-   start_date (default 2016-01-01)\
-   window (default 10)\
-   mode (SMA or EMA)

------------------------------------------------------------------------

## What the web UI provides

-   Ticker input\
-   Start date selection\
-   Moving average window selection\
-   SMA / EMA toggle\
-   Interactive chart (price + indicator)\
-   Data table (most recent dates at top)\
-   CSV export\
-   Diff report download

------------------------------------------------------------------------

## Project structure

    app/
      main.py
      engine.py
      data_provider.py
      static/index.html

    validation/
      validate_parity.py
      diff_report.csv

    validation_mmm_full.csv
    validation_sma_graph.csv
    example.xlsm
    requirements.txt
    README.md
