"""
Renewable Energy Production & Consumption Analytics Dashboard
Data source: Our World in Data (OWID) Energy Dataset
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------
# Page config
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Renewable Energy Analytics",
    page_icon="🌍",
    layout="wide",
)

AGGREGATES = [
    "ASEAN (Ember)", "CIS (EI)", "EU (Ember)", "G20 (Ember)", "G7 (Ember)",
    "Latin America and Caribbean (Ember)", "Other CIS (EI)", "Other Caribbean (EI)",
]

# -----------------------------------------------------------------
# Data loading (cached so it only runs once per session)
# -----------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_energy_data.csv")
    df = df[~df["country"].isin(AGGREGATES)].copy()
    yearly = pd.read_csv("data/powerbi_yearly_totals.csv")
    forecast = pd.read_csv("data/forecast_results.csv")
    return df, yearly, forecast


df, yearly, forecast = load_data()
latest_year = int(df["year"].max())

# -----------------------------------------------------------------
# Sidebar navigation
# -----------------------------------------------------------------
st.sidebar.title("🌍 Renewable Energy Analytics")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Source Analysis", "Country Analysis", "Forecasting"],
)

year_range = st.sidebar.slider(
    "Year range",
    int(df["year"].min()),
    latest_year,
    (1985, latest_year),
)

st.sidebar.markdown("---")
st.sidebar.caption("Data: Our World in Data Energy Dataset (github.com/owid/energy-data)")

filtered_yearly = yearly[(yearly["year"] >= year_range[0]) & (yearly["year"] <= year_range[1])]
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# -----------------------------------------------------------------
# PAGE 1: OVERVIEW
# -----------------------------------------------------------------
if page == "Overview":
    st.title("Overview")
    st.caption(f"Global renewable electricity trends, {year_range[0]}–{year_range[1]}")

    latest_row = filtered_yearly.iloc[-1]
    first_row = filtered_yearly.iloc[0]
    total_growth = (
        (latest_row["total_renewables_twh"] - first_row["total_renewables_twh"])
        / first_row["total_renewables_twh"] * 100
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Generation (latest yr)", f"{latest_row['total_renewables_twh']:,.0f} TWh")
    col2.metric("Avg. Renewable Share", f"{latest_row['avg_renewable_share_pct']:.1f}%")
    col3.metric("YoY Growth (latest yr)", f"{latest_row['yoy_growth_pct']:.1f}%")
    col4.metric(f"Growth since {year_range[0]}", f"{total_growth:,.0f}%")

    fig = px.area(
        filtered_yearly, x="year", y="total_renewables_twh",
        title="Global Renewable Electricity Generation Over Time",
        labels={"total_renewables_twh": "TWh", "year": "Year"},
    )
    fig.update_traces(line_color="#2E7D32", fillcolor="rgba(46,125,50,0.15)")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        filtered_yearly, x="year", y="yoy_growth_pct",
        title="Year-over-Year Growth Rate (%)",
        labels={"yoy_growth_pct": "YoY Growth (%)", "year": "Year"},
    )
    fig2.update_traces(marker_color=filtered_yearly["yoy_growth_pct"].apply(
        lambda v: "#2E7D32" if v >= 0 else "#C62828"
    ))
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------------------------------
# PAGE 2: SOURCE ANALYSIS
# -----------------------------------------------------------------
elif page == "Source Analysis":
    st.title("Source Analysis")
    st.caption("Comparing solar, wind, and hydro generation over time")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_yearly["year"], y=filtered_yearly["total_solar_twh"],
                              name="Solar", line=dict(color="#F9A825", width=3)))
    fig.add_trace(go.Scatter(x=filtered_yearly["year"], y=filtered_yearly["total_wind_twh"],
                              name="Wind", line=dict(color="#1E88E5", width=3)))
    fig.add_trace(go.Scatter(x=filtered_yearly["year"], y=filtered_yearly["total_hydro_twh"],
                              name="Hydro", line=dict(color="#00838F", width=3)))
    fig.update_layout(title="Renewable Generation by Source", xaxis_title="Year", yaxis_title="TWh")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Source share of total renewable generation (latest year)")
    latest = filtered_yearly.iloc[-1]
    source_totals = pd.DataFrame({
        "Source": ["Solar", "Wind", "Hydro"],
        "TWh": [latest["total_solar_twh"], latest["total_wind_twh"], latest["total_hydro_twh"]],
    })
    fig3 = px.pie(source_totals, names="Source", values="TWh", hole=0.4,
                  color="Source",
                  color_discrete_map={"Solar": "#F9A825", "Wind": "#1E88E5", "Hydro": "#00838F"})
    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------------------
# PAGE 3: COUNTRY ANALYSIS
# -----------------------------------------------------------------
elif page == "Country Analysis":
    st.title("Country Analysis")
    st.caption(f"Country-level renewable generation, {year_range[1]}")

    country_year_df = df[df["year"] == year_range[1]].dropna(subset=["renewables_electricity"])

    fig_map = px.choropleth(
        country_year_df, locations="iso_code", color="renewables_share_energy",
        hover_name="country", color_continuous_scale="Greens",
        labels={"renewables_share_energy": "Renewable Share (%)"},
        title=f"Renewable Share of Energy by Country ({year_range[1]})",
    )
    st.plotly_chart(fig_map, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        top10 = country_year_df.sort_values("renewables_electricity", ascending=False).head(10)
        fig4 = px.bar(
            top10.sort_values("renewables_electricity"),
            x="renewables_electricity", y="country", orientation="h",
            title="Top 10 by Total Generation", labels={"renewables_electricity": "TWh", "country": ""},
        )
        fig4.update_traces(marker_color="#43A047")
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        share_df = country_year_df[country_year_df["population"] > 1_000_000]
        top_share = share_df.sort_values("renewables_share_energy", ascending=False).head(10)
        fig5 = px.bar(
            top_share.sort_values("renewables_share_energy"),
            x="renewables_share_energy", y="country", orientation="h",
            title="Top 10 by Renewable Share (%)", labels={"renewables_share_energy": "%", "country": ""},
        )
        fig5.update_traces(marker_color="#00897B")
        st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Explore a country")
    country_choice = st.selectbox("Select a country", sorted(df["country"].unique()))
    country_ts = df[(df["country"] == country_choice) & (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
    fig6 = px.line(country_ts, x="year", y="renewables_electricity",
                    title=f"{country_choice} — Renewable Generation Over Time",
                    labels={"renewables_electricity": "TWh", "year": "Year"})
    st.plotly_chart(fig6, use_container_width=True)

# -----------------------------------------------------------------
# PAGE 4: FORECASTING
# -----------------------------------------------------------------
elif page == "Forecasting":
    st.title("Forecasting")
    st.caption("Global renewable generation projected to 2035")

    historical = yearly[yearly["year"] <= 2024]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historical["year"], y=historical["total_renewables_twh"],
        name="Historical", mode="lines+markers", line=dict(color="#333333", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=forecast["year"], y=forecast["linear_regression_twh"],
        name="Linear Regression Forecast", line=dict(color="#1E88E5", width=3, dash="dash"),
    ))
    fig.add_trace(go.Scatter(
        x=forecast["year"], y=forecast["prophet_twh"],
        name="Prophet Forecast", line=dict(color="#2E7D32", width=3, dash="dash"),
    ))
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast["year"], forecast["year"][::-1]]),
        y=pd.concat([forecast["prophet_upper_80"], forecast["prophet_lower_80"][::-1]]),
        fill="toself", fillcolor="rgba(46,125,50,0.15)", line=dict(color="rgba(0,0,0,0)"),
        name="Prophet 80% CI", showlegend=True,
    ))
    fig.update_layout(title="Global Renewable Generation Forecast to 2035",
                       xaxis_title="Year", yaxis_title="TWh")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Forecast table")
    st.dataframe(forecast, use_container_width=True, hide_index=True)

    st.info(
        "Linear Regression assumes a constant historical growth rate. "
        "Prophet weights recent trend changes more heavily, capturing the recent "
        "acceleration in solar and wind adoption — its curve is likely the more "
        "realistic projection."
    )
