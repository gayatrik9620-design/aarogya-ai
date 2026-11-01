import streamlit as st

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.
# Removed duplicate st.set_page_config() that was here before.

# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

/* Emergency page is deliberately DISTINCT from other pages */

.emergency-banner {
    background: linear-gradient(135deg, #7F1D1D 0%, #DC2626 60%, #EF4444 100%);
    border-radius: 22px;
    padding: 32px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 22px;
    box-shadow: 0 8px 30px rgba(220,38,38,0.3);
    animation: fadeDown 0.6s ease;
}

.emergency-siren {
    font-size: 58px;
    flex-shrink: 0;
    animation: siren 1s ease-in-out infinite;
}

.emergency-header-text h1 {
    color: white !important;
    font-size: 26px;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -0.4px;
}

.emergency-header-text p {
    color: rgba(255,255,255,0.88);
    font-size: 14px;
    margin: 0;
    line-height: 1.55;
}

.emergency-numbers-card {
    background: white;
    border-radius: 20px;
    padding: 28px;
    border: 2px solid #FECDD3;
    box-shadow: 0 4px 20px rgba(220,38,38,0.1);
    margin-bottom: 22px;
    animation: fadeUp 0.6s ease;
}

.emergency-numbers-title {
    font-size: 17px;
    font-weight: 700;
    color: #DC2626;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.number-card {
    background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
    border: 1.5px solid #FECDD3;
    border-radius: 14px;
    padding: 18px 22px;
    text-align: center;
    transition: all 0.2s ease;
}

.number-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(220,38,38,0.15);
}

.number-val {
    font-size: 36px;
    font-weight: 900;
    color: #DC2626;
    letter-spacing: -0.5px;
}

.number-label {
    font-size: 13px;
    font-weight: 600;
    color: #9F1239;
    margin-top: 4px;
}

.symptom-select-card {
    background: white;
    border-radius: 20px;
    padding: 26px 28px;
    border: 1px solid rgba(220,38,38,0.12);
    box-shadow: 0 2px 14px rgba(220,38,38,0.05);
    margin-bottom: 22px;
    animation: fadeUp 0.65s ease;
}

.emergency-result-card {
    background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
    border: 2px solid #DC2626;
    border-radius: 18px;
    padding: 28px;
    margin: 16px 0;
    animation: fadeUp 0.5s ease;
}

.emergency-result-title {
    font-size: 20px;
    font-weight: 800;
    color: #DC2626;
    margin-bottom: 12px;
}

.emergency-result-desc {
    font-size: 15px;
    color: #7F1D1D;
    line-height: 1.65;
    margin-bottom: 14px;
}

.selected-symptom-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: white;
    border-radius: 10px;
    border: 1px solid #FECDD3;
    font-size: 14px;
    color: #9F1239;
    margin-bottom: 8px;
    font-weight: 500;
}

.clear-result {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border: 2px solid #86EFAC;
    border-radius: 18px;
    padding: 28px;
    margin: 16px 0;
    text-align: center;
    animation: fadeUp 0.5s ease;
}

.clear-result-icon  { font-size: 48px; display: block; margin-bottom: 12px; }
.clear-result-title { font-size: 18px; font-weight: 700; color: #14532D; margin-bottom: 8px; }
.clear-result-desc  { font-size: 14px; color: #15803D; line-height: 1.6; }

.awareness-only {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border: 1px solid #FDE68A;
    border-left: 4px solid #F59E0B;
    border-radius: 14px;
    padding: 18px 22px;
    font-size: 13px;
    color: #78350F;
    line-height: 1.65;
    margin: 14px 0;
}

@keyframes siren {
    0%, 100% { transform: scale(1) rotate(-5deg); }
    50%       { transform: scale(1.08) rotate(5deg); }
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:translateY(0); }
}

@keyframes fadeDown {
    from { opacity:0; transform:translateY(-18px); }
    to   { opacity:1; transform:translateY(0); }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# EMERGENCY HEADER
# =========================================================

st.markdown("""
<div class="emergency-banner">
    <div class="emergency-siren">🚨</div>
    <div class="emergency-header-text">
        <h1>Emergency Detection</h1>
        <p>
            This tool helps identify symptoms that may require urgent medical attention.
            It is an <b>awareness tool only</b> — it cannot replace emergency medical professionals.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# EMERGENCY NUMBERS — always visible
# =========================================================

st.markdown("""
<div class="emergency-numbers-card">
    <div class="emergency-numbers-title">📞 India Emergency Numbers — Always Available</div>
""", unsafe_allow_html=True)

nc1, nc2, nc3, nc4 = st.columns(4)

numbers = [
    ("112", "National Emergency"),
    ("108", "Ambulance Service"),
    ("102", "Government Ambulance"),
    ("1800-180-1104", "Health Helpline"),
]

for col, (num, label) in zip([nc1, nc2, nc3, nc4], numbers):
    with col:
        st.markdown(f"""
        <div class="number-card">
            <div class="number-val">{num}</div>
            <div class="number-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# AWARENESS NOTICE
# =========================================================

st.markdown("""
<div class="awareness-only">
    ⚠️ <b>Awareness Tool Only:</b>
    This tool is designed for general awareness. It <b>cannot diagnose an emergency</b>
    or replace emergency medical services. If you believe you or someone else is in danger,
    call <b>112</b> immediately without waiting to use this tool.
</div>
""", unsafe_allow_html=True)


# =========================================================
# SYMPTOM SELECTION
# =========================================================

emergency_symptoms = [
    "Chest pain or pressure",
    "Severe difficulty breathing",
    "Sudden loss of consciousness",
    "Severe bleeding that does not stop",
    "Sudden weakness or numbness",
    "Sudden confusion or disorientation",
    "Seizure or convulsions",
    "Severe allergic reaction",
    "Thoughts of self-harm or suicide",
    "Sudden severe headache",
    "Signs of stroke (face drooping, arm weakness, speech difficulty)",
]

st.markdown('<div class="symptom-select-card">', unsafe_allow_html=True)
st.markdown('<div style="font-size:15px;font-weight:700;color:#DC2626;margin-bottom:12px;">🩺 Select Symptoms You Are Experiencing</div>', unsafe_allow_html=True)

selected_symptoms = st.multiselect(
    "Select any symptoms you notice:",
    emergency_symptoms,
    label_visibility="collapsed",
    placeholder="Choose one or more symptoms from the list…"
)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚨  Check Emergency Status", use_container_width=False, type="primary"):

    if len(selected_symptoms) > 0:

        # Build selected list HTML
        symptom_items = "".join(
            f'<div class="selected-symptom-item">🔴 {s}</div>'
            for s in selected_symptoms
        )

        st.markdown(f"""
        <div class="emergency-result-card">
            <div class="emergency-result-title">🚨 URGENT MEDICAL ATTENTION MAY BE REQUIRED</div>
            <div class="emergency-result-desc">
                You have selected symptoms that can indicate a serious medical condition.
                <b>Please seek urgent professional medical assistance immediately.</b>
                Do not delay emergency care while using this application.
            </div>
            <div style="margin-bottom:14px;font-weight:700;font-size:14px;color:#9F1239;">
                Selected symptoms:
            </div>
            {symptom_items}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="emergency-numbers-card" style="border-color:#DC2626;">
            <div class="emergency-numbers-title">📞 Call Emergency Services NOW</div>
        """, unsafe_allow_html=True)

        ec1, ec2 = st.columns(2)
        with ec1:
            st.markdown("""
            <div class="number-card" style="font-size:20px;">
                <div class="number-val">112</div>
                <div class="number-label">National Emergency</div>
            </div>""", unsafe_allow_html=True)
        with ec2:
            st.markdown("""
            <div class="number-card">
                <div class="number-val">108</div>
                <div class="number-label">Ambulance Service</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.warning(
            "🛑 **Do not delay professional medical care while using this tool.** "
            "This application cannot diagnose an emergency condition."
        )

    else:
        st.markdown("""
        <div class="clear-result">
            <span class="clear-result-icon">✅</span>
            <div class="clear-result-title">No emergency symptoms selected</div>
            <div class="clear-result-desc">
                No concerning symptoms were selected at this time.<br>
                If you develop severe or rapidly worsening symptoms, seek urgent medical help immediately.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# DISCLAIMER
# =========================================================

st.markdown("""
<div class="safety-card" style="border-left-color:#DC2626;background:linear-gradient(135deg,#FFF1F2,#FFE4E6);">
    🚨 <b>Disclaimer:</b>
    Aarogya-AI is not an emergency medical service, doctor, or diagnostic system.
    This tool is for general awareness only.
    For any real medical emergency, immediately call <b>112</b> or go to your nearest emergency facility.
</div>
""", unsafe_allow_html=True)