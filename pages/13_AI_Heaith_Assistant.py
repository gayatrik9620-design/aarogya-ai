import streamlit as st
from src.chatbot import get_chatbot_response

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Aarogya AI Health Assistant")

st.write(
    "Ask general health and wellness questions and get "
    "AI-powered informational guidance."
)

st.warning(
    "⚠️ Aarogya AI provides general health information only. "
    "It does not diagnose diseases or prescribe medicines."
)

st.divider()


# Chat history
if "health_messages" not in st.session_state:
    st.session_state.health_messages = []


# Display previous messages
for message in st.session_state.health_messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# User input
user_query = st.chat_input(
    "Ask your health question..."
)


if user_query:

    # Display user message
    st.session_state.health_messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.write(user_query)


    # Get AI response
    with st.chat_message("assistant"):

        with st.spinner("Aarogya AI is thinking..."):

            try:
                response = get_chatbot_response(user_query)

                st.write(response)

            except Exception as e:

                response = (
                    "Sorry, I couldn't process your question right now."
                )

                st.error(response)


    # Save AI response
    st.session_state.health_messages.append({
        "role": "assistant",
        "content": response
    })


st.divider()

st.caption(
    "Disclaimer: Aarogya AI is an AI wellness assistant, "
    "not a doctor. Please consult a qualified healthcare "
    "professional for personal medical advice."
)