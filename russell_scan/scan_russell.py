"""Scan a ticker list for: daily Low touches/undercuts EMA100 AND EMA200, and RSI(14) < 30.

Usage: python3 scan_russell.py tickers.csv [out.csv]
tickers.csv needs a column named Ticker (e.g. an iShares holdings export).
"""
import sys
import pandas as pd
import yfinance as yf


def rsi_wilder(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    down = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / down)


def main(path: str, out: str = "signals.csv") -> None:
    tickers = (
        pd.read_csv(path)["Ticker"].astype(str).str.strip()
        .str.replace(".", "-", regex=False).tolist()
    )
    rows = []
    for i in range(0, len(tickers), 100):
        batch = tickers[i:i + 100]
        df = yf.download(batch, period="3y", interval="1d", group_by="ticker",
                         auto_adjust=True, progress=False, threads=True)
        for t in batch:
            try:
                s = df[t].dropna(subset=["Close"])
            except KeyError:
                continue
            if len(s) < 220:
                continue
            close, low = s["Close"], s["Low"]
            ema100 = close.ewm(span=100, adjust=False).mean()
            ema200 = close.ewm(span=200, adjust=False).mean()
            rsi = rsi_wilder(close)
            touch100 = low.iloc[-1] <= ema100.iloc[-1]
            touch200 = low.iloc[-1] <= ema200.iloc[-1]
            r = rsi.iloc[-1]
            if touch100 and touch200 and r < 30:
                rows.append({
                    "Ticker": t,
                    "Date": s.index[-1].date(),
                    "Close": round(close.iloc[-1], 2),
                    "EMA100": round(ema100.iloc[-1], 2),
                    "EMA200": round(ema200.iloc[-1], 2),
                    "RSI14": round(r, 1),
                })
        print(f"processed {min(i + 100, len(tickers))}/{len(tickers)}", file=sys.stderr)
    cols = ["Ticker", "Date", "Close", "EMA100", "EMA200", "RSI14"]
    pd.DataFrame(rows, columns=cols).sort_values("RSI14").to_csv(out, index=False)
    print(f"{len(rows)} signals -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])
