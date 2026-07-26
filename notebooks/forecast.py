import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from prophet import Prophet
import logging
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)
logging.getLogger("prophet").setLevel(logging.WARNING)

df = pd.read_csv('data/clean_energy_data.csv')
aggregates = ["ASEAN (Ember)", "CIS (EI)", "EU (Ember)", "G20 (Ember)", "G7 (Ember)",
              "Latin America and Caribbean (Ember)", "Other CIS (EI)", "Other Caribbean (EI)"]
country_df = df[~df["country"].isin(aggregates)].copy()

yearly = country_df.groupby("year")["renewables_electricity"].sum()
# Drop 2025 if it looks like a partial/incomplete year (sanity check vs 2024)
yearly = yearly[(yearly.index >= 1985) & (yearly.index <= 2024)]

# ---------------------------------------------------------
# Model 1: Linear Regression
# ---------------------------------------------------------
X = yearly.index.values.reshape(-1, 1)
y = yearly.values

lr = LinearRegression()
lr.fit(X, y)
r2 = r2_score(y, lr.predict(X))

future_years = np.arange(2025, 2036).reshape(-1, 1)
lr_preds = lr.predict(future_years)

print("=== LINEAR REGRESSION ===")
print(f"R^2 on historical data: {r2:.3f}")
print(f"Slope: {lr.coef_[0]:.1f} TWh/year")
for yr, pred in zip(future_years.flatten(), lr_preds):
    print(f"{yr}: {pred:.0f} TWh")

# ---------------------------------------------------------
# Model 2: Prophet
# ---------------------------------------------------------
prophet_df = pd.DataFrame({
    "ds": pd.to_datetime(yearly.index, format="%Y"),
    "y": yearly.values
})

m = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False,
            changepoint_prior_scale=0.5)
m.fit(prophet_df)

future = m.make_future_dataframe(periods=12, freq="YE")
forecast = m.predict(future)

prophet_future = forecast[forecast["ds"].dt.year >= 2025][["ds", "yhat", "yhat_lower", "yhat_upper"]]
print("\n=== PROPHET FORECAST ===")
for _, row in prophet_future.iterrows():
    print(f"{row['ds'].year}: {row['yhat']:.0f} TWh  (range: {row['yhat_lower']:.0f} - {row['yhat_upper']:.0f})")

# ---------------------------------------------------------
# Plot both models together
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(yearly.index, yearly.values, "o-", color="#333333", label="Historical (1985-2024)", markersize=4)
ax.plot(future_years.flatten(), lr_preds, "--", color="#1E88E5", linewidth=2.5, label="Linear Regression Forecast")
ax.plot(prophet_future["ds"].dt.year, prophet_future["yhat"], "--", color="#2E7D32", linewidth=2.5, label="Prophet Forecast")
ax.fill_between(prophet_future["ds"].dt.year, prophet_future["yhat_lower"], prophet_future["yhat_upper"],
                color="#2E7D32", alpha=0.15, label="Prophet 80% Confidence Interval")
ax.set_title("Global Renewable Electricity Generation Forecast to 2035", fontsize=13, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("TWh")
ax.legend()
plt.tight_layout()
plt.savefig("C:/Users/TAUHEED/Downloads", dpi=150)
plt.close()

# Save forecast table
result = pd.DataFrame({
    "year": future_years.flatten(),
    "linear_regression_twh": lr_preds.round(0),
    "prophet_twh": prophet_future["yhat"].values.round(0),
    "prophet_lower_80": prophet_future["yhat_lower"].values.round(0),
    "prophet_upper_80": prophet_future["yhat_upper"].values.round(0),
})
# result.to_csv("C:/Users/TAUHEED/Downloads/forecast_results.csv", index=False)
# print("\nSaved forecast_results.csv")
