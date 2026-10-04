import streamlit as st
from src.chatbot import get_chatbot_response

st.title("💬 Aarogya AI Chatbot")

st.write("Ask me a general health or wellness question.")

user_query = st.text_input(
    "Enter your question:",
    placeholder="Example: How can I improve my sleep?"
)

if st.button("Ask Aarogya AI"):
    if user_query:
        with st.spinner("Aarogya AI is thinking..."):
            response = get_chatbot_response(user_query)

        st.write("### 🩺 Aarogya AI")
        st.write(response)
    else:
        st.warning("Please enter a question.")