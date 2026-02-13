import streamlit as st
import cv2
import numpy as np
import os
import pymysql
from ultralytics import YOLO
from dotenv import load_dotenv
from datetime import datetime


# Load env variable
load_dotenv()


# ================= CONFIG =================
MODEL_PATH = "models/road_damage_best.pt"
UPLOAD_DIR = "uploads/road_damage"
CONF_THRESHOLD = 0.25
# ========================================


# DB connection
def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306
    )
    

# Create upload folder if it does not exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= STREAMLIT PAGE =================
st.set_page_config(page_title="Road Damage Detection", layout="wide")

st.title("🛣️ Road Damage Detection System")
st.caption("AI-based pothole & crack detection")


# ================= CITY DATA (STATIC DEMO DATA) =================
CITY_DATA = {
    "Chennai": {
        "Anna Nagar": (13.0850, 80.2101),
        "T Nagar": (13.0418, 80.2337),
        "Velachery": (12.9756, 80.2214)
    },
    "Mumbai": {
        "Bandra": (19.0596, 72.8295),
        "Andheri": (19.1136, 72.8697),
        "Dadar": (19.0178, 72.8478)
    },
    "Kolkata": {
        "Howrah": (22.5958, 88.2636),
        "Salt Lake": (22.5726, 88.4315),
        "Garia": (22.4620, 88.3945)
    },
    "Pune": {
        "Hinjewadi": (18.5913, 73.7389),
        "Wakad": (18.5986, 73.7622),
        "Shivajinagar": (18.5308, 73.8475)
    },
    "Bangalore": {
        "Whitefield": (12.9698, 77.7500),
        "Electronic City": (12.8399, 77.6770),
        "Yelahanka": (13.1007, 77.5963)
    },
    "Visakhapatnam": {
        "MVP Colony": (17.7380, 83.3296),
        "Gajuwaka": (17.7006, 83.2160),
        "Maddilapalem": (17.7389, 83.3146)
    }
}


# ================= LOAD MODEL =================
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()


# ================= LAYOUT =================
left, right = st.columns([1.1, 1])

# ================= LEFT PANEL =================
with left:
    st.subheader("📥 Input")

    city = st.selectbox("City", list(CITY_DATA.keys()))
    area = st.selectbox("Area", list(CITY_DATA[city].keys()))

    latitude, longitude = CITY_DATA[city][area]
    st.text_input("Latitude", latitude, disabled=True)
    st.text_input("Longitude", longitude, disabled=True)

    uploaded_file = st.file_uploader(
        "Upload Road Image",
        type=["jpg", "jpeg", "png"]
    )

    detect_btn = st.button("🚀 Detect Road Damage")


# ================= RIGHT PANEL =================
with right:
    st.subheader("📊 Output")

    if uploaded_file and detect_btn:

        # save db image
        image_path = os.path.join(
            UPLOAD_DIR,
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )

        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())

        # Read image
        image = cv2.imread(image_path)

        # Run YOLO
        results = model.predict(image, conf=CONF_THRESHOLD)
        boxes = results[0].boxes
        names = model.names

        detected_classes = []

        if boxes is not None:
            for cls in boxes.cls:
                detected_classes.append(names[int(cls)])

        damage_count = len(detected_classes)
        unique_damages = list(set(detected_classes))

        # Show annotated image
        annotated = results[0].plot()
        st.image(annotated, channels="BGR", use_container_width=True)

        # ================= SEVERITY LOGIC =================
        severity = "LOW"

        if "pothole" in unique_damages and damage_count >= 3:
            severity = "HIGH"
        elif "pothole" in unique_damages:
            severity = "MEDIUM"
        elif "crack" in unique_damages and damage_count >= 3:
            severity = "MEDIUM"
        elif damage_count >= 5:
            severity = "HIGH"
        # ==================================================

        st.metric("Damage Count", damage_count)
        st.metric("Severity", severity)

        if damage_count == 0:
            st.success("✅ No road damage detected")
        else:
            st.error("🚨 Road damage detected")
            st.write("Detected types:", unique_damages)

        # 8️⃣ SAVE TO DATABASE (LAST STEP)
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO road_damage_events
                (city, area, latitude, longitude, damage_count, damage_types, severity, image_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                city,
                area,
                latitude,
                longitude,
                damage_count,
                ", ".join(unique_damages),
                severity,
                os.path.basename(image_path)
            ))

            conn.commit()
            cursor.close()
            conn.close()

            st.success("✅ Data stored in database")

        except Exception as e:
            st.error(f"❌ Database error: {e}")

    else:
        st.info("Upload an image and click Detect")


