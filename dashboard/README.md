# 🌍 Renewable Energy Production and Consumption Analytics

An end-to-end data analytics project analyzing global renewable energy trends — data cleaning, exploratory analysis, correlation studies, forecasting, and an interactive dashboard, all built on real-world data from Our World in Data.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Prophet](https://img.shields.io/badge/Prophet-Forecasting-0072C6)
![scikit--learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**[🚀 Live Dashboard](your-streamlit-url-here)** &nbsp;•&nbsp; [Data Origin](#-data-origin) &nbsp;•&nbsp; [Methodology](#-methodology) &nbsp;•&nbsp; [Key Findings](#-key-findings--outcomes) &nbsp;•&nbsp; [Setup](#-how-to-reproduce)

---

## 📌 Overview

This project analyzes renewable energy generation trends across countries, identifies which sources are growing fastest, quantifies how economic and demographic factors relate to renewable adoption, forecasts future production out to 2035, and presents everything through an interactive dashboard.

**Questions this project answers:**
- 🌱 Which renewable energy source is growing fastest?
- 🌎 Which countries produce the most renewable energy — and which rely on it most heavily?
- 📈 How has global renewable production changed over time?
- 🔗 What factors correlate with renewable adoption?
- 🔮 Can future renewable energy generation be predicted?

## 🖼️ Dashboard Preview

> ![Global trend](images/01_global_trend.png)
> ![Forecast to 2035](images/07_forecast.png)

---

## 📊 Data Origin

**Source:** [Our World in Data — Energy Dataset](https://github.com/owid/energy-data), pulled directly from the official OWID GitHub repository (`owid-energy-data.csv` + `owid-energy-codebook.csv`).

| | |
|---|---|
| **Rows × Columns** | 23,377 × 130 |
| **Coverage** | 314 countries and regional/income-group aggregates |
| **Years** | 1900–2025 |
| **Key metrics** | Generation by source (TWh), renewable share of energy, GDP, population, GHG emissions |

---

## 🛠️ Methodology

| Phase | What was done |
|---|---|
| **1. Planning** | Defined business questions and key metrics (production, renewable share, growth rate, emissions) |
| **2. Data Collection** | Downloaded raw CSV + codebook directly from the OWID GitHub repo |
| **3. Data Cleaning** | Removed aggregate/region rows, dropped duplicates, forward-filled missing values per-country, fixed data types, nulled invalid negatives → [`reports/data_cleaning_steps.md`](reports/data_cleaning_steps.md) |
| **4. EDA** | Global trend, source comparison (solar/wind/hydro), top-producing and top-adopting countries |
| **5. Advanced Analytics** | YoY growth rates + correlation analysis (GDP, population, renewable share, emissions) |
| **6. Forecasting** | Linear Regression + Prophet models projecting generation to 2035 |
| **7. Dashboard** | Built in both Power BI and Streamlit (4 pages each: Overview, Source Analysis, Country Analysis, Forecasting) |
| **8. Insights** | Distilled into the findings below |
| **9. Documentation** | This README + cleaning report |

> ⚠️ **Known limitation:** a handful of aggregate entities (`ASEAN (Ember)`, `G7 (Ember)`, `G20 (Ember)`, `CIS (EI)`) weren't caught by the initial keyword filter and were excluded manually during analysis instead. A cleaner long-term fix would be filtering on `iso_code` (real countries always have one).

---

## 🔍 Key Findings & Outcomes

### 📈 Global Trend
Global renewable electricity generation grew **~432%** from 1985 to 2025, reaching **~10,211 TWh** in 2025, with an average YoY growth rate of **4.31%**.

### ⚡ Fastest-Growing Source
Since 2010, **solar grew ~8,284%** (32 → 2,699 TWh) — far outpacing wind (~678%) and hydro (~19%, essentially plateaued).

### 🏭 Leading Producers (2025)
🥇 China (~3,920 TWh) → 🇺🇸 United States → 🇧🇷 Brazil → 🇮🇳 India → 🇨🇦 Canada

### 🌿 Leading Adopters by Share (2025, pop > 1M)
🇳🇴 Norway (71.8%) → 🇸🇪 Sweden (51.3%) → 🇧🇷 Brazil (49.6%) → 🇦🇹 Austria (43.3%) → 🇳🇿 New Zealand (42.6%)

> Notably, none of the top raw producers make this list — their renewable share is diluted by much larger fossil fuel bases.

### 🔗 Correlation Highlights

| Relationship | Correlation | Interpretation |
|---|---|---|
| GDP vs. renewable generation | **0.91** | Larger economies produce more (mostly a scale effect) |
| Population vs. renewable generation | **0.76** | Same scale effect |
| Renewable share vs. carbon intensity | **-0.74** | Higher renewable share → meaningfully cleaner grids |
| Renewable share vs. GDP | **-0.07** | Wealth doesn't predict renewable *share* — policy & geography matter more |

### 🔮 Forecast to 2035

| Model | 2025 | 2035 |
|---|---|---|
| Linear Regression | ~7,675 TWh | ~9,424 TWh |
| Prophet | ~10,460 TWh | ~15,221 TWh *(80% CI: 14,475–15,928)* |

The models diverge because Linear Regression fits one straight line across 1985–2024 (pulled down by slower early growth), while Prophet weights recent acceleration in solar/wind more heavily. **Prophet's trajectory is likely the more realistic projection**, with Linear Regression as a conservative floor.

---

## 📂 Repository Structure

```
Renewable-Energy-Analytics/
│
├── data/
│   ├── owid-energy-data.csv           # Raw source dataset
│   ├── owid-energy-codebook.csv       # Column definitions
│   ├── clean_energy_data.csv          # Cleaned dataset (Phase 3 output)
│   ├── forecast_results.csv           # Linear Regression + Prophet forecasts
│   ├── powerbi_yearly_totals.csv      # Pre-aggregated: global yearly totals
│   ├── powerbi_country_summary.csv    # Pre-aggregated: country snapshot, latest year
│   ├── powerbi_top10_countries.csv    # Pre-aggregated: top 10 producers
│   └── powerbi_country_timeseries.csv # Pre-aggregated: full country-year series
│
├── notebooks/
│   ├── eda.py                         # Phase 4: EDA script
│   ├── phase5.py                      # Phase 5: growth rate & correlation analysis
│   └── forecast.py                    # Phase 6: forecasting models
│
├── dashboard/
│   ├── app.py                         # Streamlit dashboard
│   ├── requirements.txt
│   └── README.md                      # Streamlit run/deploy instructions
│
├── reports/
│   └── data_cleaning_steps.md         # Phase 3: documented cleaning steps + script
│
├── images/
│   ├── 01_global_trend.png
│   ├── 02_source_comparison.png
│   ├── 03_top10_countries.png
│   ├── 04_top10_renewable_share.png
│   ├── 05_growth_rate.png
│   ├── 06_correlation_heatmap.png
│   └── 07_forecast.png
│
└── README.md                          # This file
```

---

## 🧰 Tech Stack

- [Python](https://www.python.org/) — core language
- [Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) — data wrangling
- [Matplotlib](https://matplotlib.org/) / [Seaborn](https://seaborn.pydata.org/) / [Plotly](https://plotly.com/) — visualization
- [scikit-learn](https://scikit-learn.org/) — Linear Regression forecasting
- [Prophet](https://facebook.github.io/prophet/) — time-series forecasting
- [Streamlit](https://streamlit.io/) — interactive web dashboard
- [Power BI](https://powerbi.microsoft.com/) — business intelligence dashboard

---

## 📺 Dashboard

- **Streamlit (live, public, no login required):** deploy via [share.streamlit.io](https://share.streamlit.io) pointing at `dashboard/app.py` — full steps in [`dashboard/README.md`](dashboard/README.md). Once live, replace the badge link at the top of this file.
- **Power BI:** `.pbix` built from the `powerbi_*.csv` tables in `data/`. Publish via *Power BI Service → Publish to web* for a public embeddable link.

---

## ⚙️ How to Reproduce

Clone the repo and install dependencies:

```bash
git clone https://github.com/<your-username>/Renewable-Energy-Analytics.git
cd Renewable-Energy-Analytics
pip install -r dashboard/requirements.txt
pip install numpy matplotlib seaborn scikit-learn prophet
```

Run the pipeline:

```bash
# 1. Clean the raw data
python reports/clean_energy_data.py

# 2. Run the analysis
python notebooks/eda.py
python notebooks/phase5.py
python notebooks/forecast.py

# 3. Launch the dashboard
cd dashboard
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`) in your browser.

## 📄 License

This project is licensed under the MIT License.
