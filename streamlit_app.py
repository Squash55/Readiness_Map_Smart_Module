
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Readiness Map with Smart Insights (Artificial data)", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("USAF_100_Base_Data.csv")

df = load_data()

st.title("🗺️ Mission Readiness Map (Artificial data)")
st.markdown("Explore geolocated readiness metrics across synthetic Air Force bases with smart dynamic insights.")

# Map layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[Longitude, Latitude]",
    get_color="[255 - Readiness * 2.5, Readiness * 2.5, 100]",
    get_radius=30000,
    pickable=True,
)

# View settings
view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=4,
    pitch=30,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Base: {Base}\nReadiness: {Readiness}"}
))

# Smart insights
st.subheader("📊 Smart Geographic Insights")

# Regional summary
high_performers = df[df["Readiness"] >= 85]
low_performers = df[df["Readiness"] <= 60]

st.markdown(f"- 🟢 **{len(high_performers)} bases** have high readiness (≥85).")
st.markdown(f"- 🔴 **{len(low_performers)} bases** are critically low (≤60).")

# Top region by average readiness
df["Region"] = pd.cut(df["Latitude"], bins=[24, 30, 36, 42, 50], labels=["South", "Mid-South", "Mid-North", "North"])
region_avg = df.groupby("Region")["Readiness"].mean().sort_values(ascending=False)
best_region = region_avg.idxmax()
worst_region = region_avg.idxmin()

st.markdown(f"- 📍 The **{best_region}** region has the **highest average readiness** ({region_avg.max():.1f}).")
st.markdown(f"- ⚠️ The **{worst_region}** region has the **lowest average readiness** ({region_avg.min():.1f}).")

# Recommendation
st.markdown("**Recommendation:** Prioritize base support and diagnostics in low-performing regions. Watch for clusters of underperformance that may indicate systemic issues.")
