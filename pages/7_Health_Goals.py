import streamlit as st
import sqlite3
import pandas as pd

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.

# =========================================================
# DATABASE
# =========================================================

@st.cache_data(ttl=60)
def _load_goals_data():
    try:
        conn = sqlite3.connect("health_data.db")
        df = pd.read_sql_query(
            "SELECT date, weight, steps, sleep FROM health_data ORDER BY date ASC",
            conn
        )
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

df = _load_goals_data()


# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

.goal-card {
    background: white;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    transition: all 0.25s ease;
    animation: fadeUp 0.7s ease;
    height: 100%;
}

.goal-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(139,114,217,0.14);
}

.goal-icon    { font-size: 32px; display: block; margin-bottom: 10px; }
.goal-label   { font-size: 12px; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.goal-value   { font-size: 26px; font-weight: 800; color: #1E293B; margin-bottom: 2px; }
.goal-target  { font-size: 13px; color: #64748B; margin-bottom: 12px; }
.goal-percent { font-size: 14px; font-weight: 700; color: #6546B8; margin-top: 6px; }

.status-reached {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border: 1px solid #86EFAC;
    border-left: 4px solid #16A34A;
    border-radius: 14px;
    padding: 16px 20px;
    color: #14532D;
    font-size: 14px;
    margin: 10px 0;
    animation: fadeUp 0.7s ease;
}

.status-progress {
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border: 1px solid rgba(139,114,217,0.2);
    border-left: 4px solid #8B72D9;
    border-radius: 14px;
    padding: 16px 20px;
    color: #4C3599;
    font-size: 14px;
    margin: 10px 0;
    animation: fadeUp 0.7s ease;
}

.motivation-card {
    background: linear-gradient(135deg, #6546B8 0%, #8B72D9 100%);
    border-radius: 18px;
    padding: 24px 28px;
    color: white;
    margin-top: 20px;
    animation: fadeUp 0.8s ease;
    text-align: center;
}

.motivation-icon  { font-size: 40px; display: block; margin-bottom: 10px; }
.motivation-title { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
.motivation-desc  { font-size: 14px; color: rgba(255,255,255,0.82); line-height: 1.6; }

.chart-section {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid rgba(139,114,217,0.08);
    box-shadow: 0 2px 12px rgba(139,114,217,0.05);
    margin-bottom: 18px;
    animation: fadeUp 0.8s ease;
}

.chart-title {
    font-size: 15px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 14px;
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
    <h1>🎯 Health Goals & Progress</h1>
    <p>Set wellness targets and monitor your progress using your recorded health data.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# GOAL SETTINGS
# =========================================================

st.markdown('<div class="section-title">⚙️ Set Your Wellness Goals</div>', unsafe_allow_html=True)

gc1, gc2, gc3 = st.columns(3)

with gc1:
    steps_goal = st.number_input(
        "👣 Daily Steps Goal",
        min_value=100, max_value=100000,
        value=5000, step=500
    )

with gc2:
    sleep_goal = st.number_input(
        "😴 Sleep Goal (hours)",
        min_value=1.0, max_value=24.0,
        value=7.0, step=0.5
    )

with gc3:
    weight_goal = st.number_input(
        "⚖️ Weight Tracking Value (kg)",
        min_value=1.0, max_value=300.0,
        value=40.0, step=0.1
    )


# =========================================================
# NO DATA STATE
# =========================================================

if df.empty:
    st.markdown("""
    <div style="text-align:center;padding:60px 32px;background:white;border-radius:20px;border:1px dashed #DDD6FE;margin-top:20px;">
        <span style="font-size:64px;display:block;margin-bottom:16px;">🎯</span>
        <div style="font-size:18px;font-weight:700;color:#1E293B;margin-bottom:8px;">No health data yet</div>
        <div style="font-size:14px;color:#94A3B8;">
            Add your weight, steps and sleep data from the ❤️ Health Data page to start tracking goals.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# =========================================================
# DATA PREP
# =========================================================

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

if df.empty:
    st.warning("⚠️ No valid health records available.")
    st.stop()

df = df.sort_values("date").reset_index(drop=True)
latest = df.iloc[-1]

current_steps  = float(latest["steps"])
current_sleep  = float(latest["sleep"])
current_weight = float(latest["weight"])

steps_progress = min(current_steps / steps_goal, 1.0)
sleep_progress = min(current_sleep / sleep_goal,  1.0)
steps_pct      = min(int(steps_progress * 100), 100)
sleep_pct      = min(int(sleep_progress * 100), 100)


# =========================================================
# GOAL CARDS
# =========================================================

st.markdown('<div class="section-title">📊 Current Progress</div>', unsafe_allow_html=True)

pg1, pg2, pg3 = st.columns(3)

with pg1:
    st.markdown(f"""
    <div class="goal-card">
        <span class="goal-icon">👣</span>
        <div class="goal-label">Daily Steps</div>
        <div class="goal-value">{int(current_steps):,}</div>
        <div class="goal-target">Goal: {int(steps_goal):,} steps</div>
        <div class="goal-percent">{steps_pct}% of goal</div>
    </div>""", unsafe_allow_html=True)
    st.progress(steps_progress)

with pg2:
    st.markdown(f"""
    <div class="goal-card">
        <span class="goal-icon">😴</span>
        <div class="goal-label">Sleep</div>
        <div class="goal-value">{current_sleep:.1f} hrs</div>
        <div class="goal-target">Goal: {sleep_goal:.1f} hours</div>
        <div class="goal-percent">{sleep_pct}% of goal</div>
    </div>""", unsafe_allow_html=True)
    st.progress(sleep_progress)

with pg3:
    st.markdown(f"""
    <div class="goal-card">
        <span class="goal-icon">⚖️</span>
        <div class="goal-label">Weight Tracking</div>
        <div class="goal-value">{current_weight:.1f} kg</div>
        <div class="goal-target">Reference: {weight_goal:.1f} kg</div>
        <div class="goal-percent">Monitoring</div>
    </div>""", unsafe_allow_html=True)
    st.caption("Weight shown for tracking purposes.")


# =========================================================
# GOAL STATUS
# =========================================================

st.markdown('<div class="section-title">✅ Goal Status</div>', unsafe_allow_html=True)

if current_steps >= steps_goal:
    st.markdown("""
    <div class="status-reached">
        🎉 <b>Steps Goal Reached!</b> You have reached your selected daily steps goal. Excellent work!
    </div>""", unsafe_allow_html=True)
else:
    remaining = int(steps_goal - current_steps)
    st.markdown(f"""
    <div class="status-progress">
        🚶 <b>Steps:</b> {remaining:,} more steps needed to reach today's goal.
    </div>""", unsafe_allow_html=True)

if current_sleep >= sleep_goal:
    st.markdown("""
    <div class="status-reached">
        🌙 <b>Sleep Goal Reached!</b> Your latest recorded sleep meets the selected goal.
    </div>""", unsafe_allow_html=True)
else:
    remaining_sleep = sleep_goal - current_sleep
    st.markdown(f"""
    <div class="status-progress">
        😴 <b>Sleep:</b> {remaining_sleep:.1f} more hours needed to reach the selected goal.
    </div>""", unsafe_allow_html=True)


# =========================================================
# MOTIVATION
# =========================================================

if steps_pct >= 100 and sleep_pct >= 100:
    st.markdown("""
    <div class="motivation-card">
        <span class="motivation-icon">🌟</span>
        <div class="motivation-title">Outstanding! All goals achieved!</div>
        <div class="motivation-desc">
            Your latest recorded activity and sleep both meet your selected goals.
            Keep building these positive wellness habits!
        </div>
    </div>""", unsafe_allow_html=True)

elif steps_pct >= 75 or sleep_pct >= 75:
    st.markdown("""
    <div class="motivation-card">
        <span class="motivation-icon">💪</span>
        <div class="motivation-title">Great Progress — Keep Going!</div>
        <div class="motivation-desc">
            You're making strong progress. Keep building consistent wellness habits
            and you'll reach your goals soon.
        </div>
    </div>""", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="motivation-card">
        <span class="motivation-icon">🌱</span>
        <div class="motivation-title">Every Step Counts!</div>
        <div class="motivation-desc">
            Start with small, realistic improvements and track your progress consistently.
            Consistency is the key to lasting wellness.
        </div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# PROGRESS CHARTS
# =========================================================

st.markdown('<div class="section-title">📈 Progress History</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-section"><div class="chart-title">👣 Steps History</div>', unsafe_allow_html=True)
st.line_chart(df.set_index("date")[["steps"]], height=220, color=["#8B72D9"], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-section"><div class="chart-title">😴 Sleep History</div>', unsafe_allow_html=True)
st.line_chart(df.set_index("date")[["sleep"]], height=220, color=["#0284C7"], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-section"><div class="chart-title">⚖️ Weight History</div>', unsafe_allow_html=True)
st.line_chart(df.set_index("date")[["weight"]], height=220, color=["#0F766E"], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# RECORDS
# =========================================================

st.markdown('<div class="section-title">📑 Recorded Progress</div>', unsafe_allow_html=True)

display_df = df.copy()
display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
display_df = display_df.rename(columns={
    "date": "Date", "weight": "Weight (kg)",
    "steps": "Steps", "sleep": "Sleep (hrs)"
})
st.dataframe(display_df, use_container_width=True, hide_index=True)


# =========================================================
# SAFETY
# =========================================================

st.markdown("""
<div class="safety-card">
    ⚠️ <b>Wellness Notice:</b>
    These goals are for general wellness tracking only.
    They are not medical targets or personalized medical advice.
    Please consult a qualified healthcare professional for personal health concerns.
</div>
""", unsafe_allow_html=True)