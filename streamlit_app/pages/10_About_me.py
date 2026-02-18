
# Portfolio Updated Version

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Ranimai K B | AI Engineer",
    page_icon="🏙️",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f6fb;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

h1, h2 {
    color: #1f2937;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
profile_image = Image.open("assets/rani_profile.jpg")

col1, col2 = st.columns([1, 3])

with col1:
    st.image(profile_image, width=220)

with col2:
    st.markdown("<h1>Ranimai K B</h1>", unsafe_allow_html=True)
    st.markdown("<h4>AI Engineer | Smart City AI Developer</h4>", unsafe_allow_html=True)
    st.write("""
Building intelligent systems using Machine Learning, NLP, Computer Vision and Cloud Deployment.
""")

st.divider()

# ---------------- PROFESSIONAL SUMMARY ----------------
st.markdown("""
<div class="card">
<h2>Professional Summary</h2>

Dedicated professional with 9 years of experience at Apollo Speciality Hospital, Madurai (2016 - 2025),
where I developed strong coordination, analytical thinking and operational management skills.

Transitioned into Artificial Intelligence and Data Science after completing advanced training,
and successfully built multiple end-to-end Machine Learning systems.

Currently focused on building scalable AI solutions with cloud deployment architecture (AWS).
</div>
""", unsafe_allow_html=True)

# ---------------- EDUCATION ----------------
st.markdown("""
<div class="card">
<h2>Education</h2>

B.Com - Computer Application

Master of Commerce (M.Com)

Specialization in Artificial Intelligence and Machine Learning  
Completed multiple AI capstone projects with hands-on implementation.
</div>
""", unsafe_allow_html=True)

# ---------------- EXPERIENCE ----------------
st.markdown("""
<div class="card">
<h2>Professional Experience</h2>

Apollo Speciality Hospital, Madurai  
2016 - 2025

- Managed administrative operations and coordination
- Developed strong communication and documentation skills
- Handled structured reporting and workflow systems
</div>
""", unsafe_allow_html=True)

# ---------------- TECHNICAL SKILLS ----------------
st.markdown("""
<div class="card">
<h2>Technical Skills</h2>

Programming: Python  

Machine Learning:
- CNN (Accident, Crowd, Road Damage Detection)
- LSTM (Traffic Prediction)
- ARIMA (AQI Forecasting)
- NLP (Sentiment Analysis)

Frameworks and Tools:
- Streamlit
- TensorFlow / Keras
- OpenCV
- Pandas / NumPy

Cloud:
- AWS EC2
- AWS RDS
- AWS S3
- Git and GitHub
</div>
""", unsafe_allow_html=True)

# ---------------- PROJECT PORTFOLIO ----------------
st.markdown("""
<div class="card">
<h2>Capstone Project Portfolio</h2>

Police Accu-Check System  
Indian Agriculture Intelligence System  
Multiple Disease Prediction System  
AI Echo Smart Conversational Partner  
Employee Attrition Analysis and Prediction  

Final Enterprise Project:
UrbanBot Intelligence - AI Powered Smart City Platform integrating
Computer Vision, Forecasting, NLP, Cloud Deployment and LLM-based AI agents.
</div>
""", unsafe_allow_html=True)

# ---------------- PERSONAL ----------------
st.markdown("""
<div class="card">
<h2>Personal Profile</h2>

Hockey Player - Strong teamwork and discipline mindset  
Continuous Learner - Passionate about upgrading technical skills  
Goal-Oriented - Focused on building production-ready AI systems
</div>
""", unsafe_allow_html=True)

# ---------------- CAREER OBJECTIVE ----------------
st.markdown("""
<div class="card">
<h2>Career Objective</h2>

To secure a challenging role in AI / Data Science where I can apply
technical expertise, analytical thinking and cloud deployment skills
to contribute to real-world intelligent systems.
</div>
""", unsafe_allow_html=True)

st.divider()
st.caption("Ranimai K B | AI Engineer Portfolio | UrbanBot Intelligence")


