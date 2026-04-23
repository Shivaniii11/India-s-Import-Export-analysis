# ================================
# India Import-Export Analysis
# ================================

import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 1. Load Dataset
# -------------------------------
df = pd.read_csv("india_trade.csv")

# Create Date column
df["Date"] = pd.to_datetime(df[["Year", "Month"]].assign(DAY=1))

print("Dataset Loaded Successfully!\n")
print(df.head())

# -------------------------------
# 2. Imports vs Exports Trend
# -------------------------------
trade_trend = df.groupby(["Year", "Trade_Type"])["Trade_Value_USD"].sum().unstack()

plt.figure()
trade_trend.plot(marker="o")
plt.title("India Imports vs Exports Trend")
plt.xlabel("Year")
plt.ylabel("Trade Value (USD)")
plt.grid()
plt.show()

# -------------------------------
# 3. Trade Deficit
# -------------------------------
imports = df[df["Trade_Type"] == "Import"].groupby("Year")["Trade_Value_USD"].sum()
exports = df[df["Trade_Type"] == "Export"].groupby("Year")["Trade_Value_USD"].sum()

trade_deficit = imports - exports

plt.figure()
trade_deficit.plot(kind="bar")
plt.title("Trade Deficit (Imports - Exports)")
plt.xlabel("Year")
plt.ylabel("Deficit (USD)")
plt.grid()
plt.show()

# -------------------------------
# 4. Top Products
# -------------------------------
top_products = df.groupby("Product")["Trade_Value_USD"].sum().sort_values(ascending=False).head(10)

plt.figure()
top_products.plot(kind="bar")
plt.title("Top 10 Traded Products")
plt.xlabel("Product")
plt.ylabel("Trade Value")
plt.xticks(rotation=45)
plt.show()

# -------------------------------
# 5. Top Countries
# -------------------------------
top_countries = df.groupby("Country")["Trade_Value_USD"].sum().sort_values(ascending=False).head(10)

plt.figure()
top_countries.plot(kind="bar")
plt.title("Top Trade Partner Countries")
plt.xlabel("Country")
plt.ylabel("Trade Value")
plt.xticks(rotation=45)
plt.show()

# -------------------------------
# 6. Oil Price vs Imports
# -------------------------------
oil_import = df[df["Trade_Type"] == "Import"].groupby("Year").agg({
    "Trade_Value_USD": "sum",
    "Oil_Price_USD": "mean"
})

fig, ax1 = plt.subplots()

ax1.plot(oil_import.index, oil_import["Trade_Value_USD"], marker="o")
ax1.set_ylabel("Import Value")

ax2 = ax1.twinx()
ax2.plot(oil_import.index, oil_import["Oil_Price_USD"], linestyle="dashed")
ax2.set_ylabel("Oil Price")

plt.title("Oil Price vs Import Value")
plt.show()

# -------------------------------
# 7. Trade vs GDP
# -------------------------------
gdp_trade = df.groupby("Year").agg({
    "Trade_Value_USD": "sum",
    "GDP_USD": "mean"
})

plt.figure()
gdp_trade.plot()
plt.title("Trade vs GDP Growth")
plt.xlabel("Year")
plt.ylabel("Value")
plt.grid()
plt.show()

# -------------------------------
# 8. Inflation vs Trade Value
# -------------------------------
plt.figure()
plt.scatter(df["Inflation_%"], df["Trade_Value_USD"])
plt.title("Inflation vs Trade Value")
plt.xlabel("Inflation (%)")
plt.ylabel("Trade Value")
plt.show()

# -------------------------------
# 9. Import vs Export by Product
# -------------------------------
pivot = df.pivot_table(
    values="Trade_Value_USD",
    index="Product",
    columns="Trade_Type",
    aggfunc="sum"
)

plt.figure()
pivot.plot(kind="bar", stacked=True)
plt.title("Import vs Export by Product")
plt.xticks(rotation=45)
plt.show()

# -------------------------------
# 10. Key Insights
# -------------------------------
print("\n===== KEY INSIGHTS =====")

top_import_product = df[df["Trade_Type"]=="Import"].groupby("Product")["Trade_Value_USD"].sum().idxmax()
top_export_product = df[df["Trade_Type"]=="Export"].groupby("Product")["Trade_Value_USD"].sum().idxmax()
top_country = df.groupby("Country")["Trade_Value_USD"].sum().idxmax()

print(f"Top Import Product: {top_import_product}")
print(f"Top Export Product: {top_export_product}")
print(f"Top Trade Country: {top_country}")

print("\nAnalysis Completed Successfully!")