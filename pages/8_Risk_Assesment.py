import streamlit as st

st.set_page_config(
    page_title="Health Risk Assessment",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Health Risk Assessment")

st.write(
    "This tool provides a basic wellness risk assessment based on "
    "the information you enter. It is not a medical diagnosis."
)

st.divider()

st.subheader("📋 Enter Your Information")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=20
)

sleep = st.number_input(
    "Average sleep per day (hours)",
    min_value=0.0,
    max_value=24.0,
    value=7.0
)

steps = st.number_input(
    "Average daily steps",
    min_value=0,
    max_value=100000,
    value=5000
)

water = st.number_input(
    "Approximate water intake (litres/day)",
    min_value=0.0,
    max_value=10.0,
    value=2.0
)

stress = st.slider(
    "Stress level",
    min_value=1,
    max_value=10,
    value=5
)

st.divider()

if st.button("🔍 Assess My Wellness Risk"):

    risk_score = 0
    warnings = []

    # Sleep assessment
    if sleep < 6:
        risk_score += 2
        warnings.append("Your average sleep is quite low.")
    elif sleep < 7:
        risk_score += 1
        warnings.append("You may benefit from getting more sleep.")

    # Physical activity
    if steps < 3000:
        risk_score += 2
        warnings.append("Your daily activity level appears low.")
    elif steps < 5000:
        risk_score += 1
        warnings.append("Try to gradually increase your daily activity.")

    # Hydration
    if water < 1.5:
        risk_score += 2
        warnings.append("Your reported water intake is relatively low.")

    # Stress
    if stress >= 8:
        risk_score += 2
        warnings.append("Your reported stress level is high.")
    elif stress >= 6:
        risk_score += 1
        warnings.append("Your reported stress level is moderately high.")

    st.subheader("📊 Assessment Result")

    if risk_score <= 2:
        st.success("🟢 Lower Wellness Risk")
        st.write(
            "Your entered information does not show many wellness risk indicators."
        )

    elif risk_score <= 5:
        st.warning("🟡 Moderate Wellness Risk")
        st.write(
            "Some lifestyle factors may need attention. "
            "Consider improving sleep, activity, hydration, or stress management."
        )

    else:
        st.error("🔴 Higher Wellness Risk")
        st.write(
            "Several wellness factors may need attention. "
            "Consider discussing persistent concerns with a qualified healthcare professional."
        )

    if warnings:
        st.subheader("💡 Areas to Pay Attention To")

        for warning in warnings:
            st.write("•", warning)

    else:
        st.info("No major wellness warning indicators were detected.")

    st.divider()

    st.caption(
        "Disclaimer: This assessment is for general wellness information only "
        "and is not a medical diagnosis. Please consult a qualified medical "
        "professional for personal medical advice."
    )