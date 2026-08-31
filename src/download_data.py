"""
Scarica prezzi storici per titoli bancari e tech e calcola i rendimenti
giornalieri percentuali. Salva il risultato in data/returns.csv.
"""

import yfinance as yf
import pandas as pd

# Titoli di esempio -- modifica in base al periodo/settore che vuoi studiare
BANK_TICKERS = ["JPM", "BAC", "C"]       # es. banche USA
TECH_TICKERS = ["AAPL", "MSFT", "NVDA"]  # es. tech USA

START_DATE = "2020-01-01"
END_DATE = "2020-06-30"  # periodo che copre la crisi covid di marzo 2020


def download_returns(tickers, start, end):
    """Scarica i prezzi di chiusura e calcola i rendimenti giornalieri."""
    prices = yf.download(tickers, start=start, end=end)["Close"]
    returns = prices.pct_change().dropna()
    return returns


def main():
    bank_returns = download_returns(BANK_TICKERS, START_DATE, END_DATE)
    tech_returns = download_returns(TECH_TICKERS, START_DATE, END_DATE)

    # Rendimento medio giornaliero del settore (media tra i titoli scelti)
    bank_avg = bank_returns.mean(axis=1).rename("bank_returns")
    tech_avg = tech_returns.mean(axis=1).rename("tech_returns")

    combined = pd.concat([bank_avg, tech_avg], axis=1).dropna()
    combined.to_csv("data/returns.csv")
    print(f"Salvate {len(combined)} osservazioni in data/returns.csv")
    print(combined.head())


if __name__ == "__main__":
    main()
