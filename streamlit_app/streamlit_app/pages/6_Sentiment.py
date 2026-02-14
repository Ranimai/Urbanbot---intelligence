import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import pymysql
import os
import nltk
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=3306
    )


st.set_page_config(
    page_title="Citizen Complaint AI",
    layout="centered"
)

st.title("🧠 Citizen Complaint AI")
st.caption("Automated sentiment analysis & priority routing for smart cities")

sia = SentimentIntensityAnalyzer()



# ---------------- SENTIMENT LOGIC ----------------
def analyze_sentiment(text):
    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "POSITIVE", "LOW"
    elif score <= -0.05:
        return "NEGATIVE", "HIGH"
    else:
        return "NEUTRAL", "MEDIUM"

# ---------------- DB INSERT ----------------
def insert_complaint(city, category, department, text, sentiment, priority):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO nlp_complaints
        (city, category, department, complaint_text, sentiment, priority)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (city, category, department, text, sentiment, priority))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- UI ----------------
st.subheader("📌 Register Complaint")

city = st.selectbox(
    "City",
    ["Chennai", "Delhi", "Hyderabad", "Bangalore", "Mumbai"]
)

category = st.selectbox(
    "Category",
    ["Water", "Road", "Pollution", "streetlight", "Traffic"]
)

department = st.text_input(
    "Department",
    value=f"{category} Department"
)

complaint_text = st.text_area(
    "Complaint Description",
    height=120
)

submit = st.button("🚀 Submit Complaint")

if submit:
    if complaint_text.strip() == "":
        st.error("Complaint description cannot be empty")
    else:
        sentiment, priority = analyze_sentiment(complaint_text)
        insert_complaint(city, category, department, complaint_text, sentiment, priority)

        st.success("✅ Complaint successfully registered")

        st.markdown("### 📊 Analysis Result")
        st.markdown(f"*Sentiment:* {sentiment}")
        st.markdown(f"*Priority:* {priority}")
        
        
        
        
