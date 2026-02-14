import streamlit as st
import cv2
import os
import numpy as np
from ultralytics import YOLO
from dotenv import load_dotenv
from datetime import datetime
import pymysql
import smtplib
from email.message import EmailMessage


# ================= LOAD ENV =================
load_dotenv()

# ================= CONFIG =================
MODEL_PATH = "models/accident_yolov8_best.pt"
UPLOAD_DIR = "uploads/accident"
CONF_THRESHOLD = 0.25
# ===========================================

os.makedirs(UPLOAD_DIR, exist_ok=True)

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

    except Exception as e:
        st.warning(f"📧 Email failed: {e}")
        return False

# ================= STREAMLIT PAGE =================
st.set_page_config(page_title="Accident Detection", layout="wide")
st.title("🚑 Accident Detection System")
st.caption("YOLOv8-based accident detection with real-time alerts")

# ================= CITY DATA (NEW NAMES) =================
CITY_DATA = {
    "Coimbatore": ["Gandhipuram", "RS Puram", "Peelamedu"],
    "Madurai": ["Anna Nagar", "KK Nagar", "Thirunagar"],
    "Trichy": ["Srirangam", "Thillai Nagar"],
    "Salem": ["Fairlands", "Hasthampatti"],
    "Erode": ["Perundurai", "Chennimalai"]
}

CAMERA_LOCATIONS = {
    "CAM-1": (11.0168, 76.9558),   # Coimbatore
    "CAM-2": (10.7905, 78.7047),   # Trichy
    "CAM-3": (9.9252, 78.1198),    # Madurai
    "CAM-4": (13.0827, 80.2707)    # Chennai
}

# ---------- Camera & Location ----------
cam1, cam2, cam3 = st.columns(3)

with cam1:
    camera_id = st.selectbox(
        "Camera ID",
        list(CAMERA_LOCATIONS.keys())
    )

latitude, longitude = CAMERA_LOCATIONS[camera_id]

with cam2:
    st.text_input("Latitude", value=f"{latitude}", disabled=True)

with cam3:
    st.text_input("Longitude", value=f"{longitude}", disabled=True)


# ================= LOAD MODEL =================
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

# ================= LAYOUT =================
col1, col2 = st.columns(2)

# ================= LEFT PANEL =================
with col1:
    st.subheader("📥 Input")

    city = st.selectbox("City", CITY_DATA.keys())
    area = st.selectbox("Area", CITY_DATA[city])

    uploaded_file = st.file_uploader(
        "Upload Accident Image",
        ["jpg", "jpeg", "png"]
    )

    detect_btn = st.button("🚨 Detect Accident")

# ================= RIGHT PANEL =================
with col2:
    st.subheader("📊 Output")

    if detect_btn and uploaded_file:

        #  Save image
        image_path = os.path.join(
            UPLOAD_DIR,
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )

        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())

        #  Read image
        image = cv2.imread(image_path)

        #  YOLO inference
        results = model.predict(image, conf=CONF_THRESHOLD)
        boxes = results[0].boxes

        vehicle_count = len(boxes) if boxes is not None else 0
        avg_conf = float(boxes.conf.mean()) if vehicle_count > 0 else 0.0

        #  Severity logic
        if vehicle_count == 0:
            severity = "No Accident"
        elif vehicle_count == 1:
            severity = "Minor"
        elif vehicle_count == 2:
            severity = "Moderate"
        else:
            severity = "Severe"
        
        

        #  Show image
        annotated = results[0].plot()
        st.image(annotated, channels="BGR", use_container_width=True)

        #  Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("🚗 Vehicles Detected",vehicle_count)
        c2.metric("📊 Avg Confidence", f"{avg_conf:.2f}")
        c3.metric("🚦 Severity", severity)

        # ================= DB INSERT =================
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO accident_events
                (city, area, latitude, longitude, severity, confidence_score, image_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                city,
                area,
                latitude,
                longitude,
                severity,
                avg_conf,
                os.path.basename(image_path)
            ))

            conn.commit()
            cursor.close()
            conn.close()

            st.success("✅ Accident data saved to MYSQL")

        except Exception as e:
            st.error(f"❌ DB error: {e}")

        # ================= EMAIL ALERT TRIGGER =================
        
        if severity in ["Moderate", "Severe"]:

            email_body = f"""
🚨 URGENT: ROAD ACCIDENT DETECTED 🚨


City: {city}
Area: {area}
Severity: {severity}
Camera ID: {camera_id}
Vehicles Detected: {vehicle_count}
Confidence: {avg_conf:.2f}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

            sent = send_email_alert(
                "🚑 UrbanBot Accident Alert",
                email_body
            )

            if sent:
                st.info("📧 Email alert sent to Public Safety Control Room")

    else:
        st.info("Upload an image and click Detect Accident")

