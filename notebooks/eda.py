import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

df = pd.read_csv('data/clean_energy_data.csv')

# Exclude leftover aggregate/group entries for country-level analysis
aggregates = ["ASEAN (Ember)", "CIS (EI)", "EU (Ember)", "G20 (Ember)", "G7 (Ember)",
              "Latin America and Caribbean (Ember)", "Other CIS (EI)", "Other Caribbean (EI)"]
country_df = df[~df["country"].isin(aggregates)].copy()

plt.style.use("seaborn-v0_8-whitegrid")

# ---------------------------------------------------------
# Chart 1: Global renewable electricity generation over time
# ---------------------------------------------------------
yearly = country_df.groupby("year")["renewables_electricity"].sum()
yearly = yearly[yearly.index >= 1985]

fig, ax = plt.subplots(figsize=(9,5))
ax.plot(yearly.index, yearly.values, color="#2E7D32", linewidth=2.5)
ax.fill_between(yearly.index, yearly.values, alpha=0.15, color="#2E7D32")
ax.set_title("Global Renewable Electricity Generation (1985-2025)", fontsize=13, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("TWh")
plt.tight_layout()
plt.savefig("C:/Users/TAUHEED/Downloads", dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 2: Source comparison (solar vs wind vs hydro) over time
# ---------------------------------------------------------
src = country_df.groupby("year")[["solar_electricity","wind_electricity","hydro_electricity"]].sum()
src = src[src.index >= 1985]

fig, ax = plt.subplots(figsize=(9,5))
ax.plot(src.index, src["solar_electricity"], label="Solar", color="#F9A825", linewidth=2.5)
ax.plot(src.index, src["wind_electricity"], label="Wind", color="#1E88E5", linewidth=2.5)
ax.plot(src.index, src["hydro_electricity"], label="Hydro", color="#00838F", linewidth=2.5)
ax.set_title("Renewable Generation by Source (1985-2025)", fontsize=13, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("TWh")
ax.legend()
plt.tight_layout()
plt.savefig("C:/Users/TAUHEED/Downloads", dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 3: Top 10 countries by total renewable generation (latest year)
# ---------------------------------------------------------
latest_year = country_df["year"].max()
latest = country_df[country_df["year"] == latest_year]
top10 = latest.groupby("country")["renewables_electricity"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(9,5))
ax.barh(top10.index[::-1], top10.values[::-1], color="#43A047")
ax.set_title(f"Top 10 Countries by Renewable Generation ({latest_year})", fontsize=13, fontweight="bold")
ax.set_xlabel("TWh")
plt.tight_layout()
plt.savefig("C:/Users/TAUHEED/Downloads", dpi=150)
plt.close()

# ---------------------------------------------------------
# Chart 4: Renewable share of energy - top 10 vs bottom 10 (latest year, min pop filter)
# ---------------------------------------------------------
share_df = latest.dropna(subset=["renewables_share_energy"])
share_df = share_df[share_df["population"] > 1_000_000]  # filter tiny outlier nations
top_share = share_df.sort_values("renewables_share_energy", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(9,5))
ax.barh(top_share["country"][::-1], top_share["renewables_share_energy"][::-1], color="#00897B")
ax.set_title(f"Top 10 Countries by Renewable Share of Energy ({latest_year})", fontsize=13, fontweight="bold")
ax.set_xlabel("Renewable Share (%)")
plt.tight_layout()
plt.savefig("C:/Users/TAUHEED/Downloads", dpi=150)
plt.close()

# ---------------------------------------------------------
# Print numeric findings for narrative
# ---------------------------------------------------------
print("=== GLOBAL TREND ===")
print(yearly.tail(5))
first_val = yearly.iloc[0]
last_val = yearly.iloc[-1]
growth_total = (last_val - first_val) / first_val * 100
print(f"\nTotal growth {yearly.index[0]}->{yearly.index[-1]}: {growth_total:.1f}%")

print("\n=== SOURCE GROWTH (first vs last available year with non-zero) ===")
for col in ["solar_electricity","wind_electricity","hydro_electricity"]:
    s = src[col]
    nz = s[s>0]
    if len(nz) > 1:
        g = (nz.iloc[-1]-nz.iloc[0])/nz.iloc[0]*100
        print(f"{col}: {nz.index[0]}={nz.iloc[0]:.1f} TWh -> {nz.index[-1]}={nz.iloc[-1]:.1f} TWh  ({g:.0f}% growth)")

print("\n=== TOP 10 COUNTRIES (latest year) ===")
print(top10)

print("\n=== TOP 10 RENEWABLE SHARE (latest year, pop>1M) ===")
print(top_share[["country","renewables_share_energy"]])
