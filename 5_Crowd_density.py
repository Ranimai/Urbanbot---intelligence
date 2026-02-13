import streamlit as st 
import pandas as pd 
import numpy as np
import pymysql 
import smtplib
import cv2
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
tf.keras.backend.clear_session()
from tensorflow.keras.models import load_model
from datetime import datetime 
from dotenv import load_dotenv
from email.message import EmailMessage



# load env variable
load_dotenv()

# Config
model_path = "models/crowd_cnn_model.h5"
upload_dir = "uploads/crowd"
img_size = (224, 224)

os.makedirs(upload_dir, exist_ok=True)


# DB Connection
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

# Email function
def send_email_alert(subject, body):
    try:
        msg = EmailMessage()
        msg['From'] = os.getenv("EMAIL_USER")
        msg['TO'] = os.getenv("EMAIL_RECEIVER")
        msg['Subject'] = subject
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
    
# Load Model
@st.cache_resource
def load_crowd_model():
    return load_model(model_path, compile=False)

model = load_crowd_model()

# Page
st.set_page_config(page_title="Crowd Density Monitoring System", layout="wide")
st.title("👥 Crowd Density Monitoring System")
st.caption("CNN-based crowd estimation with safety alerts")


# Camera Mapping
camera_locations = {
    "CAM-1": (11.0168, 76.9558),  # Visakhapatnam
    "CAM-2": (10.7905, 78.7047),  # Trichy
    "CAM-3": (9.9252, 78.1198),   # Madurai
    "CAM-4": (13.0827, 80.2707)   # Chennai
}

city_areas = {
    "Chennai": [
        "T. Nagar",
        "Marina Beach",
        "Koyambedu Bus Stand",
        "Velachery Mall",
        "Tambaram Railway Station"
    ],
    "Madurai": [
        "Meenakshi Amman Temple",
        "Periyar Bus Stand",
        "Anna Nagar",
        "Mattuthavani",
        "Vilakkuthoon"
    ],
    "Trichy": [
        "Chatram Bus Stand",
        "Srirangam Temple",
        "Thillai Nagar",
        "Central Bus Stand",
        "Cantonment Area"
    ],
    "Visakhapatnam": [
        "MVP Colony",
        "Gajuwaka",
        "Maddilapalem"
    ]
}


# Layout
left, right = st.columns([1.1, 1])


# Input panel
with left:
    st.subheader("📥 Input")
    
    city = st.selectbox("City", list(city_areas.keys()))
    area = st.selectbox("Area / Location", city_areas[city])
    
    cam1, cam2, cam3 = st.columns(3)
    with cam1:
        camera_id = st.selectbox("Camera_id", list(camera_locations.keys()))
    latitude, longitude = camera_locations[camera_id]
    
    with cam2:
        st.text_input("Latitude", latitude, disabled=True)
    with cam3:
        st.text_input("Longitude", longitude, disabled=True)

    image_file = st.file_uploader(
        "Upload Crowd Image",
        ["jpg", "jpeg", "png"]
    )

    detect_btn = st.button("🚨 Analyze Crowd")

# ================= OUTPUT PANEL =================
with right:
    st.subheader("📊 Output")

    if image_file and detect_btn:

        image_path = os.path.join(
            upload_dir,
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )

        with open(image_path, "wb") as f:
            f.write(image_file.read())

        img = cv2.imread(image_path)
        img_resized = cv2.resize(img, img_size)
        img_norm = img_resized / 255.0
        img_input = np.expand_dims(img_norm, axis=0)

        # ================= PREDICTION =================
        crowd_count = int(model.predict(img_input)[0][0])

        # ================= SEVERITY LOGIC =================
        if crowd_count < 20:
            severity = "Normal"
        elif crowd_count < 50:
            severity = "Crowded"
        else:
            severity = "Overcrowded"

        st.metric("👥 Estimated Crowd Count", crowd_count)
        st.metric("🚦 Crowd Status", severity)

        st.image(img, channels="BGR", use_container_width=True)

        # ================= SAVE TO DB =================
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO crowd_events
                (city, area, latitude, longitude, camera_id,
                 crowd_count, severity, image_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                city,
                area,
                latitude,
                longitude,
                camera_id,
                crowd_count,
                severity,
                os.path.basename(image_path)
            ))

            conn.commit()
            cursor.close()
            conn.close()

            st.success("✅ Crowd data saved to MYSQL")

        except Exception as e:
            st.error(f"❌ DB error: {e}")

        # ================= EMAIL ALERT =================
        if severity == "Overcrowded":
            email_body = f"""
🚨 CROWD SAFETY ALERT 🚨

City: {city}
Area: {area}
Camera ID: {camera_id}
Latitude: {latitude}
Longitude: {longitude}
Estimated Crowd Count: {crowd_count}
Status: OVERCROWDED
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Immediate crowd control measures are recommended.
"""

            sent = send_email_alert(
                "👥 UrbanBot Crowd Alert",
                email_body
            )

            if sent:
                st.info("📧 Alert message sent to City Surveillance Unit")

    else:
        st.info("Upload an image and click Analyze Crowd")
        
        
        
        