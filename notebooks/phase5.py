import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/clean_energy_data.csv')
aggregates = ["ASEAN (Ember)", "CIS (EI)", "EU (Ember)", "G20 (Ember)", "G7 (Ember)",
              "Latin America and Caribbean (Ember)", "Other CIS (EI)", "Other Caribbean (EI)"]
country_df = df[~df["country"].isin(aggregates)].copy()

# ---------------------------------------------------------
# Growth rate: year-over-year % change in global renewable generation
# ---------------------------------------------------------
yearly = country_df.groupby("year")["renewables_electricity"].sum()
yearly = yearly[(yearly.index >= 1985) & (yearly.index <= 2025)]
growth = yearly.pct_change() * 100
growth = growth.dropna()

print("=== YEAR-OVER-YEAR GLOBAL GROWTH RATE ===")
print("Highest growth years:")
print(growth.sort_values(ascending=False).head(5))
print("\nLowest growth years:")
print(growth.sort_values(ascending=True).head(5))
print(f"\nAverage annual growth rate: {growth.mean():.2f}%")

fig, ax = plt.subplots(figsize=(9,5))
colors = ["#2E7D32" if v >= 0 else "#C62828" for v in growth.values]
ax.bar(growth.index, growth.values, color=colors)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("YoY Growth Rate - Global Renewable Electricity Generation", fontsize=13, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Growth Rate (%)")
plt.tight_layout()
plt.savefig("C:/Users/TAUHEED/Downloads", dpi=150)
plt.close()

# ---------------------------------------------------------
# Correlation analysis: GDP, population, renewables, emissions
# ---------------------------------------------------------
latest_year = country_df["year"].max()
corr_df = country_df[country_df["year"] == latest_year][
    ["gdp", "population", "renewables_electricity", "renewables_share_energy",
     "greenhouse_gas_emissions", "carbon_intensity_elec"]
].dropna()

print(f"\n=== CORRELATION MATRIX ({latest_year}, n={len(corr_df)} countries) ===")
corr = corr_df.corr()
print(corr.round(2))

fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0, ax=ax,
            cbar_kws={"label": "Correlation"})
ax.set_title(f"Correlation Matrix ({latest_year})", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("C:/Users/TAUHEED/Downloads", dpi=150)
plt.close()

# specific correlations for narrative
print("\nKey correlations:")
print(f"GDP vs renewables_electricity: {corr_df['gdp'].corr(corr_df['renewables_electricity']):.2f}")
print(f"Population vs renewables_electricity: {corr_df['population'].corr(corr_df['renewables_electricity']):.2f}")
print(f"renewables_share_energy vs carbon_intensity_elec: {corr_df['renewables_share_energy'].corr(corr_df['carbon_intensity_elec']):.2f}")
