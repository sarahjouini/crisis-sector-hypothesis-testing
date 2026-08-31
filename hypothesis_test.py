"""
Legge data/returns.csv e testa se i rendimenti medi giornalieri
del settore bancario differiscono statisticamente da quelli del
settore tech nel periodo scelto.
"""

import pandas as pd
from scipy import stats


def load_returns(path="data/returns.csv"):
    return pd.read_csv(path, index_col=0, parse_dates=True)


def test_normality(series, name):
    stat, p = stats.shapiro(series)
    is_normal = p > 0.05
    print(f"Shapiro-Wilk su {name}: p-value = {p:.4f} "
          f"({'normale' if is_normal else 'NON normale'})")
    return is_normal


def compare_groups(bank, tech):
    bank_normal = test_normality(bank, "bank_returns")
    tech_normal = test_normality(tech, "tech_returns")

    if bank_normal and tech_normal:
        stat, p = stats.ttest_ind(bank, tech)
        test_name = "t-test"
    else:
        stat, p = stats.mannwhitneyu(bank, tech)
        test_name = "Mann-Whitney U"

    print(f"\n{test_name}: statistic = {stat:.4f}, p-value = {p:.4f}")
    if p < 0.05:
        print("=> Differenza statisticamente significativa (rifiuto H0)")
    else:
        print("=> Nessuna evidenza sufficiente di differenza (non rifiuto H0)")

    return p


def main():
    df = load_returns()
    print(f"Osservazioni caricate: {len(df)}\n")
    print(df.describe(), "\n")
    compare_groups(df["bank_returns"], df["tech_returns"])


if __name__ == "__main__":
    main()