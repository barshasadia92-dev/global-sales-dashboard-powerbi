"""Recompute the headline dashboard figures from the raw data.

Usage:  python analysis/verify_kpis.py
Reads data/100000_Sales_Records.csv.zip (pandas reads zipped CSVs directly).
"""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "100000_Sales_Records.csv.zip"
df = pd.read_csv(DATA, parse_dates=["Order Date", "Ship Date"])

bn = lambda s: s.sum() / 1e9
margin = lambda g: g["Total Profit"].sum() / g["Total Revenue"].sum() * 100

print(f"Rows: {len(df):,} | Orders from {df['Order Date'].min():%Y-%m-%d} to {df['Order Date'].max():%Y-%m-%d}")
print(f"Total revenue : {bn(df['Total Revenue']):.2f} bn")
print(f"Total cost    : {bn(df['Total Cost']):.2f} bn")
print(f"Total profit  : {bn(df['Total Profit']):.2f} bn  (margin {margin(df):.1f}%)")
print(f"Avg unit price: {df['Unit Price'].mean():.2f}\n")

by_region = df.groupby("Region").apply(
    lambda g: pd.Series({"Profit_bn": bn(g["Total Profit"]), "Margin_%": margin(g), "Orders": len(g)}))
print("Profit by region\n", by_region.sort_values("Profit_bn", ascending=False).round(2), "\n")

by_item = df.groupby("Item Type").apply(
    lambda g: pd.Series({"Profit_bn": bn(g["Total Profit"]), "Margin_%": margin(g)}))
print("Profit by item type\n", by_item.sort_values("Profit_bn", ascending=False).round(2), "\n")

by_channel = df.groupby("Sales Channel").apply(
    lambda g: pd.Series({"Profit_bn": bn(g["Total Profit"]), "Orders": len(g)}))
print("Profit by sales channel\n", by_channel.round(2))
