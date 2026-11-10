# Russell scan notes (run 2026-11-10)
Rule: Low <= EMA100 AND Low <= EMA200 AND RSI14 (Wilder) < 30, daily bars, 3y, auto_adjust.
## Result
- 5,512 US-listed non-ETF tickers (Nasdaq Trader lists) -> 432 raw hits (signals.csv)
- Filter close>=$1 and mktcap>=$150M -> 150 hits (signals_russell_sized.csv). Sorted by RSI.
## Fixes / findings
- Script bug fixed: empty result crashed sort_values.
- Universe is NOT the Russell index (iShares IWV CSV blocked by bot check; not circumvented). Mktcap/price filter is an approximation.
- Raw hits are mostly junk: sub-$1 microcaps, reverse-split-distorted EMAs (CDT, RUBI, CETX).
- Last bar 2026-11-10 may be an unfinished session -> rerun after close before acting.
- Foreign ADRs (e.g. PBR) are in the list but not Russell members.
- 150 hits incl. NVDA, CAT, INTC, NOW, FTNT, DDD = broad selloff, not stock-specific.
## Rerun
pip install yfinance pandas; python3 scan_russell.py tickers.csv signals.csv
