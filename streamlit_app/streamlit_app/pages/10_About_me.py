import streamlit as st

st.set_page_config(page_title="About Me", layout="wide")

# ---------- Custom Styling ----------
st.markdown("""
<style>
.stApp {
    background-color: #f4f6fb;
}

.section-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

h2 {
    color: #1f2937;
}

h4 {
    color: #2563eb;
}

</style>
""", unsafe_allow_html=True)

st.title("👩‍💻 Rani — AI Engineer & Smart City Developer")
st.caption("Building Intelligent Urban Systems with AI, ML & LLMs")

# ---------- ABOUT ----------
st.markdown("""
<div class="section-card">
<h2>👩 About Me</h2>

I am an aspiring AI Engineer passionate about building real-world intelligent systems.  
My focus is on Smart City solutions using Computer Vision, NLP, Forecasting, and LLM-powered decision support systems.

UrbanBot Intelligence is my full-stack AI platform designed to assist city administrators with:
• Accident Detection  
• Road Damage Monitoring  
• Crowd Density Analysis  
• Traffic Prediction  
• AQI Forecasting  
• NLP Complaint Classification  
• RAG-powered LLM Decision Assistant  

I enjoy transforming data into intelligent automation systems.
</div>
""", unsafe_allow_html=True)

# ---------- EDUCATION ----------
st.markdown("""
<div class="section-card">
<h2>🎓 Education</h2>

• Bachelor & Master Degree in [B.Com.(C.A) & M.Com]  
• Specialization in Artificial Intelligence & Machine Learning  
• Completed Capstone Project: UrbanBot Intelligence  

Focused on:
- Deep Learning
- Data Science
- NLP
- Time Series Forecasting
- Cloud Deployment (AWS)
</div>
""", unsafe_allow_html=True)

# ---------- EXPERIENCE ----------
st.markdown("""I have worked in Apollo Speciality Hospital as a Secretary on 2016 - 2025""")


# ---------- SKILLS ----------
st.markdown("""
<div class="section-card">
<h2>💻 Technical Skills</h2>

🔹 Programming: Python  
🔹 Frameworks: Streamlit, TensorFlow, Keras  
🔹 Machine Learning: CNN, LSTM, ARIMA  
🔹 NLP: TextBlob, VADER  
🔹 Database: MySQL (RDS Ready)  
🔹 Cloud: AWS (S3, RDS, EC2)  
🔹 LLM Integration: GROQ API  
🔹 Version Control: Git  
🔹 Data Visualization: Plotly, Matplotlib  

</div>
""", unsafe_allow_html=True)

# ---------- PROJECT ----------
st.markdown("""
<div class="section-card">
<h2>🚀 Featured Project — UrbanBot Intelligence</h2>

An Enterprise-Style AI Smart City Platform integrating:

✔ Computer Vision (Accident, Crowd, Road Damage Detection)  
✔ Traffic Forecasting (LSTM)  
✔ AQI Forecasting (ARIMA)  
✔ NLP Complaint Classification  
✔ Unified Executive Dashboard  
✔ RAG-Powered LLM Chatbot  
✔ Email Alert Agent  
✔ Report Generation Agent  
✔ MySQL Database Integration  
✔ AWS Deployment Architecture  

This system provides real-time city analytics and AI-driven decision support.
</div>
""", unsafe_allow_html=True)

# ---------- ACHIEVEMENTS ----------
st.markdown("""
<div class="section-card">
<h2>🏆 Achievements</h2>

• Developed end-to-end AI Smart City Platform  
• Built Modular Enterprise-Level RAG Architecture  
• Implemented AI Agents (Email, Report, SQL Agent)  
• Integrated Multiple ML Models into Production Dashboard  

Continuously learning and building scalable AI systems.
</div>
""", unsafe_allow_html=True)

# ---------- CONTACT ----------
st.markdown("""
<div class="section-card">
<h2>📧 Contact</h2>

📩 Email: ranivika89@gmail.com 
🔗 LinkedIn: https://linkedin.com/in/yourprofile  
💻 GitHub: https://github.com/yourprofile  

Capstone Project: Smart City AI Intelligence Platform / Data Scientist / ML Developer opportunities.
</div>
""", unsafe_allow_html=True)
