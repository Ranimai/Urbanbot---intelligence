
import streamlit as st

st.set_page_config(
    page_title="UrbanBot Intelligence System",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FA;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)



st.title("🏙️ UrbanBot Intelligence Dashboard")
st.subheader("AI-powered Smart City Monitoring Platform")

st.markdown("---")

st.write("""
Welcome to **UrbanBot Intelligence**, a unified smart city analytics platform
that leverages Artificial Intelligence to monitor, analyze, and respond to
urban challenges in real time.
""")

st.header("📌 Available Modules")

st.markdown("""
- 🛣️ Road Damage Detection  
- 🚑 Accident Detection & Alerts  
- 👥 Crowd Density Monitoring  
- 🌫️ Air Quality Forecasting  
- 🚦 Traffic Congestion Prediction  
- 🗣️ Citizen Complaint Sentiment Analysis  
- 🤖 AI-powered Chatbot (RAG-based)  
""")

st.info("👉 Use the sidebar to navigate through different modules.")

st.markdown("---")
st.caption("UrbanBot Intelligence | Smart Cities powered by AI")
