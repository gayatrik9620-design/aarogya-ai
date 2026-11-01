import streamlit as st

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.
# Removed duplicate st.set_page_config() that was here before.

# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

.med-shield-header {
    background: linear-gradient(135deg, #6546B8 0%, #8B72D9 60%, #0284C7 100%);
    border-radius: 22px;
    padding: 32px 36px;
    margin-bottom: 26px;
    display: flex;
    align-items: center;
    gap: 22px;
    box-shadow: 0 8px 28px rgba(101,70,184,0.22);
    animation: fadeDown 0.6s ease;
}

.shield-icon {
    font-size: 60px;
    flex-shrink: 0;
    animation: pulse 3s ease-in-out infinite;
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));
}

.med-header-text h1 {
    color: white !important;
    font-size: 26px;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -0.4px;
}

.med-header-text p {
    color: rgba(255,255,255,0.82);
    font-size: 14px;
    margin: 0;
    line-height: 1.55;
}

.topic-select-card {
    background: white;
    border-radius: 20px;
    padding: 26px 28px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    margin-bottom: 22px;
    animation: fadeUp 0.6s ease;
}

.topic-info-card {
    background: white;
    border-radius: 20px;
    padding: 28px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 4px 20px rgba(139,114,217,0.08);
    margin-bottom: 22px;
    animation: fadeUp 0.7s ease;
}

.topic-title {
    font-size: 20px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.med-point {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 12px 14px;
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border-radius: 12px;
    font-size: 14px;
    color: #1E293B;
    margin-bottom: 10px;
    line-height: 1.55;
}

.med-point-icon {
    font-size: 16px;
    margin-top: 1px;
    flex-shrink: 0;
}

.section-divider {
    height: 1px;
    background: #EDE9FA;
    margin: 22px 0;
}

.never-do-card {
    background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
    border: 1px solid #FECDD3;
    border-left: 4px solid #DC2626;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 16px 0;
    font-size: 13px;
    color: #9F1239;
    line-height: 1.65;
}

.consult-card {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border: 1px solid #86EFAC;
    border-left: 4px solid #16A34A;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 16px 0;
    font-size: 13px;
    color: #14532D;
    line-height: 1.65;
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:translateY(0); }
}

@keyframes fadeDown {
    from { opacity:0; transform:translateY(-18px); }
    to   { opacity:1; transform:translateY(0); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.06); }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="med-shield-header">
    <div class="shield-icon">🛡️</div>
    <div class="med-header-text">
        <h1>Medication Safety</h1>
        <p>
            Educational medication awareness information designed to promote safety.
            This tool does not prescribe medicines or recommend dosages.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SAFETY DATA
# =========================================================

topics = {
    "💊 Taking Medicines Safely": {
        "icon": "💊",
        "points": [
            "Take medicines only as directed by a qualified healthcare professional.",
            "Read the medicine label and instructions carefully before taking.",
            "Do not share prescription medicines with other people.",
            "Keep medicines away from children and store them safely.",
            "Complete prescribed courses even if you feel better early."
        ]
    },
    "⚠️ Possible Side Effects": {
        "icon": "⚠️",
        "points": [
            "Some medicines can cause side effects — these vary by person and medicine.",
            "Read the information leaflet provided with your medicine carefully.",
            "If you notice unusual or severe symptoms, contact a healthcare professional.",
            "Do not stop a prescribed medicine suddenly without medical advice."
        ]
    },
    "🔗 Medicine Interactions": {
        "icon": "🔗",
        "points": [
            "Some medicines can interact with other medicines, foods or supplements.",
            "Tell your doctor or pharmacist about all medicines and supplements you take.",
            "Do not start or stop a prescribed medicine without professional advice.",
            "Herbal supplements can also interact with prescription medicines."
        ]
    },
    "🏠 Storage & Expiry": {
        "icon": "🏠",
        "points": [
            "Store medicines according to the instructions on the label.",
            "Keep medicines in a safe, dry place away from heat and moisture.",
            "Check the expiry date before using any medicine.",
            "Keep all medicines out of reach of children.",
            "Dispose of expired medicines safely — do not flush down drains."
        ]
    },
    "📋 Missed Dose": {
        "icon": "📋",
        "points": [
            "Follow the instructions provided with your medicine for missed doses.",
            "Do not automatically take a double dose to make up for a missed one.",
            "If you are unsure what to do, ask your doctor or pharmacist.",
            "Set reminders to help you maintain a consistent medication schedule."
        ]
    },
    "🏥 Emergency Situations": {
        "icon": "🏥",
        "points": [
            "If you suspect a medicine overdose, seek immediate medical attention.",
            "In India, call 112 (Emergency) or 108 (Ambulance) for urgent help.",
            "Keep packaging and medicine name available for emergency responders.",
            "Do not induce vomiting unless specifically directed by a medical professional."
        ]
    },
}


# =========================================================
# TOPIC SELECTION
# =========================================================

st.markdown('<div class="topic-select-card">', unsafe_allow_html=True)
st.markdown('<div style="font-size:15px;font-weight:700;color:#1E293B;margin-bottom:12px;">📖 Choose a Safety Topic</div>', unsafe_allow_html=True)

selected_topic = st.selectbox(
    "Choose a topic:",
    list(topics.keys()),
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔍  Show Safety Information", use_container_width=False, type="primary"):
    st.session_state["med_topic"] = selected_topic

if "med_topic" in st.session_state and st.session_state["med_topic"] in topics:
    topic_key = st.session_state["med_topic"]
    topic = topics[topic_key]

    points_html = "".join(
        f'<div class="med-point"><span class="med-point-icon">✅</span>{p}</div>'
        for p in topic["points"]
    )

    st.markdown(f"""
    <div class="topic-info-card">
        <div class="topic-title">{topic["icon"]} {topic_key.split(' ', 1)[-1]}</div>
        {points_html}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="never-do-card">
        🚫 <b>Important:</b>
        If you experience a serious or unexpected reaction after taking a medicine,
        seek urgent medical help immediately. Call <b>112</b> in India.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="consult-card">
        👩‍⚕️ <b>Always Consult a Professional:</b>
        For any personal medication questions, dosage concerns or health decisions,
        please consult a qualified doctor or licensed pharmacist.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# ALWAYS VISIBLE IMPORTANT NOTES
# =========================================================

st.markdown('<div class="section-title">⚠️ Important Safety Principles</div>', unsafe_allow_html=True)

ic1, ic2, ic3 = st.columns(3)

safety_cards = [
    ("💊", "Medication Awareness", "Always follow professional medical guidance when using any medicine."),
    ("⚠️", "Know Your Medicine", "Understand what you are taking — read labels and ask questions."),
    ("👩‍⚕️", "Consult a Professional", "A doctor or pharmacist is your best resource for medication questions."),
]

for col, (icon, title, desc) in zip([ic1, ic2, ic3], safety_cards):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">{icon}</span>
            <div class="metric-label">{title}</div>
            <div class="metric-value" style="font-size:14px;font-weight:600;color:#475569;margin-top:6px;">{desc}</div>
        </div>""", unsafe_allow_html=True)


# =========================================================
# SAFETY NOTICE
# =========================================================

st.markdown("""
<div class="safety-card">
    ⚠️ <b>Disclaimer:</b>
    Aarogya-AI does not prescribe medicines, recommend dosages, or diagnose medical conditions.
    This page is for general medication safety awareness only.
    Please consult a qualified healthcare professional for all personal medical decisions.
</div>
""", unsafe_allow_html=True)