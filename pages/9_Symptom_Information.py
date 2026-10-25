import streamlit as st

st.set_page_config(
    page_title="Symptom Information",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Symptom Information Tool")

st.write(
    "Get general information about common symptoms "
    "and basic wellness guidance."
)

st.divider()

# Symptom information
symptoms = {
    "Headache": {
        "info": "Headache can be related to stress, lack of sleep, dehydration, or other factors.",
        "tips": [
            "Get enough rest",
            "Drink enough water",
            "Take breaks from screens",
            "Monitor if the headache keeps returning"
        ]
    },

    "Fever": {
        "info": "Fever can occur with infections or other health conditions.",
        "tips": [
            "Take adequate rest",
            "Stay hydrated",
            "Monitor your temperature",
            "Seek medical advice if fever persists or becomes severe"
        ]
    },

    "Cough": {
        "info": "Cough can occur due to infections, allergies, or irritation.",
        "tips": [
            "Stay hydrated",
            "Avoid smoke and other irritants",
            "Get enough rest",
            "Seek medical advice if the cough persists or worsens"
        ]
    },

    "Stomach Pain": {
        "info": "Stomach pain can have many possible causes, including digestive problems.",
        "tips": [
            "Stay hydrated",
            "Notice foods that trigger discomfort",
            "Eat regular balanced meals",
            "Seek medical advice if pain is severe or persistent"
        ]
    },

    "Fatigue": {
        "info": "Fatigue can be related to poor sleep, stress, lifestyle factors, or other conditions.",
        "tips": [
            "Maintain regular sleep",
            "Eat balanced meals",
            "Stay hydrated",
            "Consult a healthcare professional if fatigue persists"
        ]
    }
}

# Select symptom
selected_symptom = st.selectbox(
    "Select a symptom:",
    list(symptoms.keys())
)

# Button
if st.button("🔍 Get Information"):

    data = symptoms[selected_symptom]

    st.subheader(f"ℹ️ About {selected_symptom}")

    st.write(data["info"])

    st.subheader("💡 General Wellness Tips")

    for tip in data["tips"]:
        st.write("•", tip)

    st.divider()

    st.warning(
        "⚠️ This tool provides general health information only. "
        "It cannot diagnose a medical condition."
    )

    st.error(
        "🚨 If you experience severe symptoms such as chest pain, "
        "severe difficulty breathing, unconsciousness, uncontrolled bleeding, "
        "or other emergency symptoms, seek urgent medical help."
    )

    st.caption(
        "Disclaimer: Aarogya AI is an AI-based wellness assistant, "
        "not a doctor. Please consult a qualified healthcare professional "
        "for personal medical advice."
    )