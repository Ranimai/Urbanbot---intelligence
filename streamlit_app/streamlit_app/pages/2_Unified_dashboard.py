import streamlit as st
import pymysql
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

st.set_page_config(page_title="Unified City Dashboard", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background-color: #f4f6fb;
}
.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    text-align: center;
}
.kpi-number {
    font-size: 28px;
    font-weight: bold;
}
.kpi-title {
    font-size: 14px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

st.title("🏙️ Unified Smart City Command Center")
st.caption("AI-driven Real-Time Urban Intelligence Dashboard")

# ================= DB CONNECTION =================
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

def fetch_query(query):
    try:
        conn = get_connection()
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

# ================= KPI QUERIES =================
accidents = fetch_query("SELECT COUNT(*) total FROM accident_events")
road = fetch_query("SELECT COUNT(*) total FROM road_damage_events")
crowd = fetch_query("SELECT COUNT(*) total FROM crowd_events WHERE severity='Overcrowded'")
traffic = fetch_query("SELECT COUNT(*) total FROM traffic_events WHERE congestion_level='High'")
aqi = fetch_query("SELECT COUNT(*) total FROM air_quality_events WHERE aqi_category IN ('Poor','Severe')")
complaints = fetch_query("SELECT COUNT(*) total FROM nlp_complaints WHERE priority='HIGH'")

# ================= KPI DISPLAY =================
c1, c2, c3, c4, c5, c6 = st.columns(6)

def show_kpi(col, title, value):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-number">{value}</div>
        <div class="kpi-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)

show_kpi(c1, "🚑 Accidents", accidents.iloc[0,0] if not accidents.empty else 0)
show_kpi(c2, "🛣 Road Issues", road.iloc[0,0] if not road.empty else 0)
show_kpi(c3, "👥 Overcrowding", crowd.iloc[0,0] if not crowd.empty else 0)
show_kpi(c4, "🚦 High Traffic", traffic.iloc[0,0] if not traffic.empty else 0)
show_kpi(c5, "🌫 AQI Alerts", aqi.iloc[0,0] if not aqi.empty else 0)
show_kpi(c6, "🗣 High Complaints", complaints.iloc[0,0] if not complaints.empty else 0)

st.divider()

# ================= ANALYTICS CHARTS =================
st.subheader("📊 City-wise Analytics Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👥 Overcrowding Events by City")
    crowd_chart = fetch_query("""
        SELECT city, COUNT(*) total
        FROM crowd_events
        WHERE severity='Overcrowded'
        GROUP BY city
    """)
    if not crowd_chart.empty:
        st.bar_chart(crowd_chart.set_index("city"))

with col2:
    st.markdown("### 🗣 High Priority Complaints by City")
    complaint_chart = fetch_query("""
        SELECT city, COUNT(*) total
        FROM nlp_complaints
        WHERE priority='HIGH'
        GROUP BY city
    """)
    if not complaint_chart.empty:
        st.bar_chart(complaint_chart.set_index("city"))



st.divider()

# ================= LATEST EVENTS =================

st.subheader("📌 Latest Critical Events")

latest_accidents = fetch_query("""
SELECT city, area, severity, event_time
FROM accident_events
ORDER BY event_time DESC
LIMIT 5
""")

latest_road = fetch_query("""
SELECT city, area, severity, event_time
FROM road_damage_events
ORDER BY event_time DESC
LIMIT 5
""")

latest_complaints = fetch_query("""
SELECT city, category, priority, created_at
FROM nlp_complaints
ORDER BY created_at DESC
LIMIT 5
""")

latest_crowd = fetch_query("""
SELECT city, severity, crowd_count, event_time
FROM crowd_events
ORDER BY event_time DESC
LIMIT 5
""")

latest_traffic = fetch_query("""
SELECT city, congestion_level, predicted_traffic, event_time
FROM traffic_events
ORDER BY event_time DESC
LIMIT 5
""")

latest_aqi = fetch_query("""
SELECT city, aqi, aqi_category, timestamp
FROM air_quality_events
ORDER BY timestamp DESC
LIMIT 5
""")


row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row1_col1:
    st.markdown("### 🚑 Recent Accidents")
    st.dataframe(latest_accidents, use_container_width=True)

with row1_col2:
    st.markdown("### 🛣 Road Damage")
    st.dataframe(latest_road, use_container_width=True)

with row1_col3:
    st.markdown("### 👥 Crowd Alerts")
    st.dataframe(latest_crowd, use_container_width=True)

with row2_col1:
    st.markdown("### 🚦 Traffic Alerts")
    st.dataframe(latest_traffic, use_container_width=True)

with row2_col2:
    st.markdown("### 🌫 AQI Alerts")
    st.dataframe(latest_aqi, use_container_width=True)

with row2_col3:
    st.markdown("### 🗣 Recent Complaints")
    st.dataframe(latest_complaints, use_container_width=True)

st.success("✅ Unified Smart City Command Center Operational")


