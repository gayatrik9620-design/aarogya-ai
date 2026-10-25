import streamlit as st

from src.ui import (
    inject_custom_css,
    render_page_header,
    render_metric_card,
    render_insight_card,
    render_safety_disclaimer,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Aarogya-AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Apply Custom UI
# --------------------------------------------------

inject_custom_css()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="
            padding: 10px 5px 25px 5px;
            text-align: center;
        ">
            <div style="font-size: 38px;">🩺</div>
            <h2 style="
                margin: 5px 0 0 0;
                color: #0F766E;
            ">
                Aarogya-AI
            </h2>
            <p style="
                color: #64748B;
                font-size: 13px;
                margin-top: 5px;
            ">
                Your AI Health Companion
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### Navigation")

    st.page_link("app.py", label="🏠  Dashboard")

    st.markdown("### Health")

    st.page_link(
        "pages/2_Chatbot.py",
        label="💬  AI Chatbot"
    )

    st.page_link(
        "pages/3_Health_Data.py",
        label="📊  Health Data"
    )

    st.markdown("---")

    st.caption("Aarogya-AI • AI-powered wellness")

# --------------------------------------------------
# Main Header
# --------------------------------------------------

render_page_header(
    "Welcome to Aarogya-AI 👋",
    "Your personalized AI-powered health companion."
)

# --------------------------------------------------
# Overview Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_metric_card(
        "WEIGHT",
        "40 kg",
        "Current"
    )

with col2:
    render_metric_card(
        "STEPS",
        "6,240",
        "Today"
    )

with col3:
    render_metric_card(
        "SLEEP",
        "7.2 hrs",
        "Last night"
    )

with col4:
    render_metric_card(
        "HEALTH SCORE",
        "82/100",
        "Good"
    )

# --------------------------------------------------
# AI Insight
# --------------------------------------------------

render_insight_card(
    "Your health journey is looking positive",
    "Keep tracking your daily activity, sleep and health data "
    "to understand your personal trends better."
)

# --------------------------------------------------
# Quick Actions
# --------------------------------------------------

st.markdown("### Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💬 Ask AI", use_container_width=True):
        st.switch_page("pages/2_Chatbot.py")

with col2:
    if st.button("📊 View Health Data", use_container_width=True):
        st.switch_page("pages/3_Health_Data.py")

with col3:
    if st.button("❤️ Health Overview"):
        st.toast("Your health overview is ready!")

# --------------------------------------------------
# Medical Safety Notice
# --------------------------------------------------

render_safety_disclaimer()