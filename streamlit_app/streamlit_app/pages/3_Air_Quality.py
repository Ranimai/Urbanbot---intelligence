import streamlit as st
import pandas as pd
import pymysql
import pickle
import smtplib
import os
from datetime import datetime
from dotenv import load_dotenv
from email.message import EmailMessage

# ================= LOAD ENV =================
load_dotenv()


# ================= PAGE =================
st.set_page_config(page_title="Air Quality Monitoring", layout="wide")
st.title("🌫️ Air Quality Index (AQI) Forecasting")
st.caption("ARIMA-based air quality forecasting for smart environmental management")


# ================= MODEL PATHS =================
AQI_MODELS = {
    "Chennai": "models/aqi_arima_chennai.pkl",
    "Coimbatore": "models/aqi_arima_coimbatore.pkl",
    "Delhi": "models/aqi_arima_delhi.pkl",
    "Jaipur": "models/aqi_arima_jaipur.pkl"
}

# ================= MONITORING STATIONS =================
AQI_STATIONS = {
    "Chennai": {
        "CAM-AQI-1": (13.0827, 80.2707)
    },
    "Jaipur": {
        "CAM-AQI-2": (26.9124, 75.7873)
    },
    "Coimbatore": {
        "CAM-AQI-3": (11.0168, 76.9558)
    },
    "Delhi": {
        "CAM-AQI-4": (28.6139, 77.2090)
    }
}


# ================= DB CONNECTION =================
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

# ================= EMAIL ALERT =================
def send_email_alert(subject, body):
    try:
        msg = EmailMessage()
        msg["From"] = os.getenv("EMAIL_USER")
        msg["To"] = os.getenv("EMAIL_RECEIVER")
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                os.getenv("EMAIL_USER"),
                os.getenv("EMAIL_PASSWORD")
            )
            server.send_message(msg)

        return True
    except Exception:
        return False

# ================= LOAD ARIMA MODEL =================
@st.cache_resource
def load_arima_model(model_path):
    with open(model_path, "rb") as f:
        return pickle.load(f)


# ================= INPUT =================
left, right = st.columns([1.1, 1])

with left:
    st.subheader("📥 Input")

    city = st.selectbox("Select City", list(AQI_MODELS.keys()))
    station = st.selectbox(
        "Monitoring Station",
        list(AQI_STATIONS[city].keys())
    )

    latitude, longitude = AQI_STATIONS[city][station]

    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Latitude", latitude, disabled=True)
    with c2:
        st.text_input("Longitude", longitude, disabled=True)
        
    forecast_days = st.slider(
        "Forecast Days",
        min_value=1,
        max_value=7,
        value=3
    )

    predict_btn = st.button("📊 Predict AQI")

# ================= OUTPUT =================
with right:
    st.subheader("📊 Output")

    if predict_btn:

        model = load_arima_model(AQI_MODELS[city])

        # Forecast next AQI value
        forecast = model.forecast(steps=forecast_days)
        forecast = forecast.astype(int)
        
        
        df = pd.DataFrame({
            "Day": [f"Day {i+1}" for i in range(forecast_days)],
            "Predicted AQI": forecast
        })
        
        predicted_aqi = int(forecast[-1])
        #predicted_aqi = latest_aqi
        

        # AQI CATEGORY
        if predicted_aqi <= 40:
            category = "Good"
            emoji = "🟢"
        elif predicted_aqi <= 70:
            category = "Moderate"
            emoji = "🟡"
        elif predicted_aqi <= 100:
            category = "Poor"
            emoji = "🟠"
        else:
            category = "Severe"
            emoji = "🔴"
            

        st.metric("🌫️ Predicted AQI", predicted_aqi)
        st.metric("📌 Air Quality Category", f"{category} {emoji}")
        
        
        # -------- DAY-WISE TABLE --------
        st.subheader("📅 Day-wise AQI Forecast")
        st.dataframe(df, use_container_width=True)

        
        # ================= SAVE TO DB =================
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO air_quality_events
            (city, monitoring_station, latitude, longitude, aqi, aqi_category)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            city,
            station,
            latitude,
            longitude,
            predicted_aqi,
            category
        ))


            conn.commit()
            cursor.close()
            conn.close()

            st.success("✅ AQI data saved to database")

        except Exception as e:
            st.error(f"❌ DB error: {e}")

        # ================= EMAIL ALERT =================
        if category in ["Poor", "Severe"]:
            email_body = f"""
🌫️ AIR QUALITY ALERT 🌫️

City: {city}
Monitoring Station: {station}
Latitude: {latitude}
Longitude: {longitude}
Forecast Days: {forecast_days}
Predicted AQI: {predicted_aqi}
Category: {category}

Health Advisory:
• Avoid outdoor activities
• Use masks
• Follow pollution control guidelines

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

            if send_email_alert("🌫️ UrbanBot AQI Alert", email_body):
                st.info("📧 AQI alert sent to Environmental Department")

    else:
        st.info("Click Predict AQI to forecast air quality")

