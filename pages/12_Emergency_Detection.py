import streamlit as st

st.set_page_config(
    page_title="Emergency Detection",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Emergency Detection")

st.write(
    "This tool helps identify symptoms that may require urgent medical attention."
)

st.warning(
    "⚠️ This is only an awareness tool. It cannot diagnose an emergency."
)

st.divider()

st.subheader("🩺 Select the symptoms you are experiencing")

emergency_symptoms = [
    "Chest pain or pressure",
    "Severe difficulty breathing",
    "Sudden loss of consciousness",
    "Severe bleeding that does not stop",
    "Sudden weakness or numbness",
    "Severe confusion",
    "Seizure",
    "Severe allergic reaction",
    "Thoughts of self-harm or suicide"
]

selected_symptoms = st.multiselect(
    "Choose one or more symptoms:",
    emergency_symptoms
)

if st.button("🚨 Check Emergency Status"):

    if len(selected_symptoms) > 0:

        st.error("🚨 URGENT MEDICAL ATTENTION MAY BE REQUIRED")

        st.write(
            "You selected symptoms that can be serious. "
            "Please seek urgent medical attention instead of relying "
            "on this application."
        )

        st.subheader("Selected Symptoms")

        for symptom in selected_symptoms:
            st.write("•", symptom)

        st.divider()

        st.info(
            "📞 In India, you can call **112** for emergency assistance."
        )

        st.warning(
            "Do not delay professional medical care while using this tool."
        )

    else:

        st.success(
            "🟢 No emergency symptoms were selected."
        )

        st.write(
            "If you develop severe or rapidly worsening symptoms, "
            "seek urgent medical help."
        )

st.divider()

st.caption(
    "Disclaimer: Aarogya AI is not an emergency medical service, "
    "doctor, or diagnostic system. This tool is for general awareness only."
)