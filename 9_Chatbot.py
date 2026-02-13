import streamlit as st
from chatbot.chatbot_logic import chatbot_answer

st.title("🤖 UrbanBot AI Assistant")
st.caption("AI-powered Smart City Decision Support System")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask UrbanBot a question")

if st.button("Send") and user_input:
    response = chatbot_answer(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("UrbanBot", response))

for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 {msg}**")
    else:
        st.markdown(f"**🤖 {msg}**")
