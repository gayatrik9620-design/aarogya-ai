import streamlit as st
import sqlite3
import pandas as pd

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.
# Removed duplicate st.set_page_config() that was here before.

# =========================================================
# DATABASE
# =========================================================

try:
    conn = sqlite3.connect("health_data.db")
    df = pd.read_sql_query(
        "SELECT date, weight, steps, sleep FROM health_data ORDER BY date DESC",
        conn
    )
    conn.close()
except Exception:
    df = pd.DataFrame()


# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

.rec-card {
    background: white;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    transition: all 0.25s ease;
    animation: fadeUp 0.7s ease;
    height: 100%;
}

.rec-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 28px rgba(139,114,217,0.15);
    border-color: rgba(139,114,217,0.25);
}

.rec-icon {
    font-size: 34px;
    display: block;
    margin-bottom: 12px;
}

.rec-title {
    font-size: 16px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 8px;
}

.rec-desc {
    font-size: 13px;
    color: #64748B;
    line-height: 1.6;
    margin-bottom: 12px;
}

.rec-tip {
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #6546B8;
    display: flex;
    align-items: flex-start;
    gap: 6px;
}

.data-insight-card {
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border: 1px solid rgba(139,114,217,0.15);
    border-left: 4px solid #8B72D9;
    border-radius: 14px;
    padding: 20px 24px;
    margin: 16px 0;
    animation: fadeUp 0.7s ease;
}

.insight-row {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.insight-item {
    font-size: 14px;
    color: #1E293B;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    line-height: 1.5;
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
# HEADER
# =========================================================

st.markdown("""
<div class="page-header">
    <h1>💡 Personalized Recommendations</h1>
    <p>Simple wellness suggestions based on your recorded health patterns and general wellness principles.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# DATA-DRIVEN INSIGHTS
# =========================================================

if not df.empty:
    latest = df.iloc[0]
    steps_val = latest["steps"]
    sleep_val = latest["sleep"]

    # Build personalized messages
    if steps_val < 3000:
        activity_msg = "Your recorded activity is low. Try adding short walks throughout your day."
        activity_type = "warn"
    elif steps_val < 7000:
        activity_msg = "Your activity level can be improved. Try adding more walking during the day."
        activity_type = "insight"
    else:
        activity_msg = "Your recorded daily activity looks great. Continue maintaining regular movement!"
        activity_type = "good"

    if sleep_val < 6:
        sleep_msg = "Your sleep is below recommended levels. Try to maintain a regular sleep schedule."
        sleep_type = "warn"
    elif sleep_val < 7:
        sleep_msg = "You may benefit from getting a little more sleep each night."
        sleep_type = "insight"
    else:
        sleep_msg = "Your recorded sleep duration looks reasonable. Keep up the healthy sleep habit!"
        sleep_type = "good"

    color_map = {
        "good":    ("#F0FDF4", "#16A34A", "#14532D"),
        "warn":    ("#FFFBEB", "#F59E0B", "#78350F"),
        "insight": ("#F0EDFD", "#8B72D9", "#4C3599"),
    }

    def insight_card(icon, title, msg, ctype):
        bg, border, text = color_map[ctype]
        return f"""
        <div style="background:{bg};border:1px solid {border}33;border-left:4px solid {border};
                    border-radius:14px;padding:16px 20px;margin:8px 0;animation:fadeUp 0.7s ease;">
            <b style="color:{text};">{icon} {title}</b><br>
            <span style="font-size:13px;color:{text};opacity:0.85;">{msg}</span>
        </div>"""

    st.markdown('<div class="section-title">📊 Your Personalized Insights</div>', unsafe_allow_html=True)
    st.markdown(
        insight_card("👣", "Activity:", activity_msg, activity_type) +
        insight_card("😴", "Sleep:", sleep_msg, sleep_type) +
        insight_card("⚖️", "Weight:", "Continue monitoring your weight regularly and focus on balanced nutrition.", "insight"),
        unsafe_allow_html=True
    )
else:
    st.markdown("""
    <div style="background:#F0EDFD;border:1px solid #C4B5FD;border-radius:14px;padding:18px 22px;margin:10px 0;font-size:14px;color:#4C3599;">
        📭 No health data found. Add your data from the ❤️ Health Data page for personalized insights.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# GENERAL RECOMMENDATION CARDS
# =========================================================

st.markdown('<div class="section-title">🌿 General Wellness Recommendations</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">These are general educational wellness suggestions, not personalized medical advice.</div>', unsafe_allow_html=True)

recommendations = [
    {
        "icon":  "💧",
        "title": "Hydration",
        "desc":  "Staying well-hydrated supports energy levels, cognitive function and overall body performance.",
        "tip":   "💡 Try drinking a glass of water first thing in the morning and keep a water bottle with you throughout the day."
    },
    {
        "icon":  "🥗",
        "title": "Nutrition",
        "desc":  "A balanced diet rich in vegetables, fruits, whole grains and lean proteins supports overall wellness.",
        "tip":   "💡 Focus on adding more colorful vegetables to your meals. Variety in your diet helps ensure diverse nutrient intake."
    },
    {
        "icon":  "🏃",
        "title": "Physical Activity",
        "desc":  "Regular physical movement supports cardiovascular health, mood and energy throughout the day.",
        "tip":   "💡 Aim for short, consistent activity sessions. Even 10-minute walks throughout the day add up significantly."
    },
    {
        "icon":  "😴",
        "title": "Sleep Quality",
        "desc":  "Quality sleep is essential for physical recovery, mental clarity and emotional wellbeing.",
        "tip":   "💡 Try maintaining a consistent sleep schedule and create a relaxing pre-bed routine to improve sleep quality."
    },
    {
        "icon":  "🧘",
        "title": "Stress & Relaxation",
        "desc":  "Managing stress through mindfulness, breathing exercises or relaxing activities supports mental wellness.",
        "tip":   "💡 Try a 5-minute breathing exercise: inhale for 4 counts, hold for 4, exhale for 6. Repeat 3–5 times."
    },
    {
        "icon":  "🌿",
        "title": "Healthy Habits",
        "desc":  "Small consistent habits — regular sleep, movement, hydration and social connection — compound into major wellness gains.",
        "tip":   "💡 Choose one small healthy habit to focus on this week and build from there."
    },
]

rc1, rc2, rc3 = st.columns(3)

for i, rec in enumerate(recommendations):
    col = [rc1, rc2, rc3][i % 3]
    with col:
        st.markdown(f"""
        <div class="rec-card">
            <span class="rec-icon">{rec['icon']}</span>
            <div class="rec-title">{rec['title']}</div>
            <div class="rec-desc">{rec['desc']}</div>
            <div class="rec-tip">{rec['tip']}</div>
        </div>
        """, unsafe_allow_html=True)
    if i == 2:
        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)


# =========================================================
# SAFETY
# =========================================================

st.markdown("""
<div class="safety-card">
    ⚠️ <b>Safety Notice:</b>
    These recommendations are general wellness suggestions and are not a medical diagnosis or treatment.
    Aarogya-AI is an AI-based wellness assistant, not a doctor.
    Please consult a qualified healthcare professional for personal medical advice.
</div>
""", unsafe_allow_html=True)