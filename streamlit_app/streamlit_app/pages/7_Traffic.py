import streamlit as st
import numpy as np
import os
from tensorflow.keras.models import load_model
from datetime import datetime
from dotenv import load_dotenv
import pymysql
import smtplib
from email.message import EmailMessage

# ================= ENV =================
load_dotenv()

# ================= CONFIG =================
MODEL_PATH = "models/traffic_lstm_model.h5"

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

# ================= LOAD MODEL =================
@st.cache_resource
def load_traffic_model():
    return load_model(MODEL_PATH, compile=False)

model = load_traffic_model()

# ================= PAGE =================
st.set_page_config(page_title="Traffic Forecasting", layout="wide")
st.title("🚦 Traffic Congestion Prediction System")
st.caption("LSTM-based traffic forecasting for proactive traffic management")

# ================= CITY / AREA / LOCATION =================

CITY_DATA = {
    "Hyderabad": {
        "Hitech City": (17.4483, 78.3915),
        "Gachibowli": (17.4401, 78.3489),
        "Madhapur": (17.4486, 78.3935),
        "Kukatpally": (17.4948, 78.3996),
        "Secunderabad": (17.4399, 78.4983)
    },

    "Bengaluru": {
        "Electronic City": (12.8399, 77.6770),
        "Whitefield": (12.9698, 77.7500),
        "Silk Board": (12.9165, 77.6229),
        "Hebbal Flyover": (13.0358, 77.5970),
        "KR Puram": (13.0075, 77.6959)
    },

    "Pune": {
        "Hinjewadi": (18.5913, 73.7389),
        "Wakad": (18.5993, 73.7641),
        "Baner Road": (18.5590, 73.7868),
        "Hadapsar": (18.5089, 73.9259),
        "Shivaji Nagar": (18.5308, 73.8475)
    },

    "Mumbai": {
        "Bandra Kurla Complex": (19.0671, 72.8670),
        "Andheri East": (19.1136, 72.8697),
        "Dadar": (19.0178, 72.8478),
        "Powai": (19.1176, 72.9060),
        "Lower Parel": (18.9977, 72.8376)
    },

    "Delhi": {
        "Connaught Place": (28.6315, 77.2167),
        "Dwarka": (28.5921, 77.0460),
        "Saket": (28.5245, 77.2066),
        "Lajpat Nagar": (28.5677, 77.2433),
        "Rohini": (28.7499, 77.0565)
    }
}

# ================= LAYOUT =================
left, right = st.columns([1.1, 1])

# ================= INPUT =================
with left:
    st.subheader("📥 Input")

    city = st.selectbox("City", list(CITY_DATA.keys()))
    area = st.selectbox("Area", list(CITY_DATA[city].keys()))

    latitude, longitude = CITY_DATA[city][area]
    
    c1, c2 = st.columns(2)
    c1.text_input("Latitude", latitude, disabled=True)
    c2.text_input("Longitude", longitude, disabled=True)

    st.markdown("**Simulated recent traffic volume (last 60 time-steps)**")      # 1 hour of traffic

    min_val, max_val = st.slider(
        "Vehicle Count Range",
        min_value=10,
        max_value=100,
        value=(15, 40)
    )

    predict_btn = st.button("📈 Predict Traffic")

# ================= OUTPUT =================
with right:
    st.subheader("📊 Output")

    if predict_btn:

        # Simulated time-series input
        input_series = np.random.randint(min_val, max_val, size=(60, 1))
        input_series = input_series / 100.0               # Normalization factor = 100.0
        input_series = np.expand_dims(input_series, axis=0)

        predicted_value = model.predict(input_series)[0][0]
        predicted_traffic = int(predicted_value * 100)

        # Congestion logic
        if predicted_traffic < 30:
            congestion = "Low"
        elif predicted_traffic < 50:
            congestion = "Moderate"
        else:
            congestion = "High"

        st.metric("🚗 Predicted Vehicle Count", predicted_traffic)
        st.metric("🚦 Congestion Level", congestion)

        # ================= SAVE TO DB =================
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO traffic_events
                (city, area, latitude, longitude,
                 predicted_traffic, congestion_level, model_used)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                city,
                area,
                latitude,
                longitude,
                predicted_traffic,
                congestion,
                "LSTM"
            ))

            conn.commit()
            cursor.close()
            conn.close()

            st.success("✅ Traffic prediction saved to database")

        except Exception as e:
            st.error(f"❌ DB error: {e}")

        # ================= EMAIL ALERT =================
        if congestion == "High":
            email_body = f"""
🚦 TRAFFIC CONGESTION ALERT 🚦

City: {city}
Area: {area}
Predicted Vehicle Count: {predicted_traffic}
Congestion Level: HIGH
Suggested Actions:
• Signal timing optimization
• Route diversion
• Traffic personnel deployment

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

            if send_email_alert("🚦 UrbanBot Traffic Alert", email_body):
                st.info("📧 Traffic alert sent to Traffic Control Room")

    else:
        st.info("Click Predict Traffic to generate forecast")


