import streamlit as st
from src.chatbot import get_chatbot_response

st.set_page_config(
    page_title="Aarogya AI Chatbot",
    page_icon="🏥"
)

st.title("🏥 Aarogya AI Chatbot")
st.write("Your AI-powered healthcare assistant.")

st.info(
    "Ask general questions about health, sleep, physical activity, "
    "hydration, and healthy habits."
)

st.warning(
    "This chatbot provides general information only. "
    "It cannot diagnose diseases or prescribe medicines."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask your health question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Aarogya AI is thinking..."):
            response = get_chatbot_response(question)

        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )