import streamlit as st

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.
# Removed duplicate st.set_page_config() that was here before.

# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

.symptom-select-card {
    background: white;
    border-radius: 20px;
    padding: 28px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    margin-bottom: 22px;
    animation: fadeUp 0.6s ease;
}

.symptom-info-card {
    background: white;
    border-radius: 20px;
    padding: 28px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 4px 20px rgba(139,114,217,0.08);
    margin-bottom: 20px;
    animation: fadeUp 0.7s ease;
}

.symptom-name {
    font-size: 22px;
    font-weight: 800;
    color: #1E293B;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.symptom-info-text {
    font-size: 14px;
    color: #475569;
    line-height: 1.65;
    margin-bottom: 18px;
}

.tips-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
}

.tip-item {
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 13px;
    color: #4C3599;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    line-height: 1.5;
}

.seek-help-card {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border: 1px solid #FDE68A;
    border-left: 4px solid #F59E0B;
    border-radius: 14px;
    padding: 18px 22px;
    margin-top: 18px;
    font-size: 13px;
    color: #78350F;
    line-height: 1.65;
}

.emergency-note {
    background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
    border: 1px solid #FECDD3;
    border-left: 4px solid #DC2626;
    border-radius: 14px;
    padding: 18px 22px;
    margin-top: 14px;
    font-size: 13px;
    color: #9F1239;
    line-height: 1.65;
}

.tips-label {
    font-size: 14px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 12px;
    margin-top: 4px;
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
# SYMPTOM DATA
# =========================================================

symptoms = {
    "🤕 Headache": {
        "emoji": "🤕",
        "info": "Headache can be related to stress, lack of sleep, dehydration, poor posture, eye strain or other factors. Most headaches are tension-type and resolve with rest.",
        "tips": [
            "Get adequate rest and sleep",
            "Stay well hydrated",
            "Take regular breaks from screens",
            "Practice relaxation techniques",
            "Monitor if headache keeps returning"
        ],
        "seek_help": "Consult a healthcare professional if headaches are frequent, severe, sudden-onset, or accompanied by fever, vision changes or stiff neck.",
    },
    "🌡️ Fever": {
        "emoji": "🌡️",
        "info": "Fever is the body's natural response to infections or other conditions. A raised body temperature often indicates the immune system is responding to something.",
        "tips": [
            "Take adequate rest",
            "Stay well hydrated",
            "Monitor body temperature",
            "Wear light clothing",
            "Seek advice if fever is high or persists"
        ],
        "seek_help": "Seek medical attention if fever is very high (above 39.5°C), lasts more than a few days, or is accompanied by severe symptoms.",
    },
    "😷 Cough": {
        "emoji": "😷",
        "info": "Cough can occur due to infections, allergies, environmental irritants or other causes. Acute coughs are usually short-term while chronic coughs last longer.",
        "tips": [
            "Stay well hydrated",
            "Avoid smoke and irritants",
            "Rest your voice",
            "Use a humidifier if air is dry",
            "See a doctor if cough persists"
        ],
        "seek_help": "Seek medical advice if cough persists for more than 3 weeks, produces blood, or is accompanied by difficulty breathing or chest pain.",
    },
    "🤢 Stomach Pain": {
        "emoji": "🤢",
        "info": "Stomach pain can have many possible causes including digestive problems, gas, food intolerance, infections or stress.",
        "tips": [
            "Stay hydrated",
            "Eat light, easily digestible foods",
            "Note foods that trigger discomfort",
            "Eat regular balanced meals",
            "Avoid very spicy or fatty foods temporarily"
        ],
        "seek_help": "Seek medical advice if pain is severe, persistent, accompanied by vomiting blood, or you experience sudden sharp pain.",
    },
    "😔 Fatigue": {
        "emoji": "😔",
        "info": "Fatigue can be related to poor sleep, stress, lifestyle factors, nutritional deficiencies or other underlying conditions.",
        "tips": [
            "Maintain regular sleep schedule",
            "Eat balanced, nutrient-rich meals",
            "Stay hydrated",
            "Reduce excessive caffeine",
            "Get regular light physical activity"
        ],
        "seek_help": "Consult a healthcare professional if fatigue is persistent, significantly affects daily life, or is accompanied by other unexplained symptoms.",
    },
    "😤 Breathing Difficulty": {
        "emoji": "😤",
        "info": "Breathing difficulty can range from mild (due to anxiety or physical exertion) to severe (requiring immediate medical attention).",
        "tips": [
            "Sit upright in a comfortable position",
            "Breathe slowly and calmly",
            "Avoid triggers if known (dust, smoke)",
            "Note when symptoms started and severity"
        ],
        "seek_help": "⚠️ Seek IMMEDIATE medical attention if breathing difficulty is sudden, severe, or accompanied by chest pain, blue lips or confusion. Call 112.",
    },
}


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="page-header">
    <h1>🩺 Symptom Information</h1>
    <p>Educational health information about common symptoms. This tool is for general awareness only.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SELECTION
# =========================================================

st.markdown('<div class="symptom-select-card">', unsafe_allow_html=True)
st.markdown('<div style="font-size:15px;font-weight:700;color:#1E293B;margin-bottom:12px;">🔍 Select a Symptom</div>', unsafe_allow_html=True)

selected = st.selectbox(
    "Select a symptom to learn about:",
    list(symptoms.keys()),
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

if st.button("📖  Get Symptom Information", use_container_width=False, type="primary"):
    st.session_state["show_symptom"] = selected

if "show_symptom" in st.session_state and st.session_state["show_symptom"] in symptoms:
    sel = st.session_state["show_symptom"]
    data = symptoms[sel]

    # Info card
    st.markdown(f"""
    <div class="symptom-info-card">
        <div class="symptom-name">{data['emoji']} {sel.split(' ', 1)[-1]}</div>
        <div class="symptom-info-text">{data['info']}</div>
        <div class="tips-label">💡 General Wellness Tips</div>
        <div class="tips-grid">
            {''.join(f'<div class="tip-item">✅ {tip}</div>' for tip in data["tips"])}
        </div>
        <div class="seek-help-card" style="margin-top:18px;">
            🩺 <b>When to Seek Professional Help:</b><br>
            {data['seek_help']}
        </div>
        <div class="emergency-note">
            🚨 <b>Emergency Reminder:</b>
            If you experience severe or life-threatening symptoms, seek immediate professional medical assistance.
            In India, call <b>112</b> (Emergency) or <b>108</b> (Ambulance).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="safety-card">
        ⚠️ <b>Important Disclaimer:</b>
        This tool provides general health information only.
        It <b>cannot</b> diagnose a medical condition.
        Aarogya-AI is an AI wellness assistant — not a doctor.
        Please consult a qualified healthcare professional for personal medical advice.
    </div>
    """, unsafe_allow_html=True)