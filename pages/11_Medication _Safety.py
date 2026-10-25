import streamlit as st

st.set_page_config(
    page_title="Medication Safety",
    page_icon="💊",
    layout="wide"
)

st.title("💊 Medication Safety Information")

st.write(
    "Learn basic medication-safety information. "
    "This tool does not prescribe medicines or provide dosages."
)

st.divider()

st.subheader("🔎 Select a Safety Topic")

topics = {
    "Taking Medicines Safely": [
        "Take medicines only as directed by a qualified healthcare professional.",
        "Read the medicine label and instructions carefully.",
        "Do not share prescription medicines with other people.",
        "Keep medicines away from children."
    ],

    "Possible Side Effects": [
        "Some medicines can cause side effects.",
        "Read the information provided with your medicine.",
        "If you notice unusual or severe symptoms, contact a healthcare professional."
    ],

    "Medicine Interactions": [
        "Some medicines can interact with other medicines or substances.",
        "Tell your doctor or pharmacist about medicines and supplements you are taking.",
        "Do not start or stop a prescribed medicine without professional advice."
    ],

    "Storage": [
        "Store medicines according to the instructions on the label.",
        "Keep medicines in a safe and dry place when required.",
        "Check the expiry date before using a medicine.",
        "Keep medicines out of reach of children."
    ],

    "Missed Dose": [
        "Follow the instructions provided with your medicine.",
        "Do not automatically take extra medicine to make up for a missed dose.",
        "If you are unsure what to do, ask a doctor or pharmacist."
    ]
}

selected_topic = st.selectbox(
    "Choose a topic:",
    list(topics.keys())
)

if st.button("📖 Show Information"):

    st.subheader(f"ℹ️ {selected_topic}")

    for point in topics[selected_topic]:
        st.write("•", point)

    st.divider()

    st.warning(
        "⚠️ This information is for general education only. "
        "It does not replace professional medical advice."
    )

    st.error(
        "🚨 If you experience a serious or unexpected reaction "
        "after taking a medicine, seek urgent medical help."
    )

    st.caption(
        "Disclaimer: Aarogya AI does not prescribe medicines, "
        "recommend dosages, or diagnose medical conditions. "
        "Please consult a qualified healthcare professional."
    )