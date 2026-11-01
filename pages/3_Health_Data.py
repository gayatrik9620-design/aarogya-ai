import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.

# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect("health_data.db", check_same_thread=False)

conn.execute("""
CREATE TABLE IF NOT EXISTS health_data (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    date    TEXT,
    weight  REAL,
    steps   INTEGER,
    sleep   REAL
)
""")
conn.commit()


# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

.form-card {
    background: white;
    border-radius: 22px;
    padding: 28px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 4px 20px rgba(139,114,217,0.07);
    margin-bottom: 24px;
    animation: fadeUp 0.6s ease;
}

.form-card-title {
    font-size: 17px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.tip-card {
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border: 1px solid rgba(139,114,217,0.15);
    border-left: 4px solid #8B72D9;
    border-radius: 14px;
    padding: 16px 18px;
    font-size: 13px;
    color: #4C3599;
    margin: 16px 0;
    animation: fadeUp 0.7s ease;
}

.chart-card {
    background: white;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(139,114,217,0.08);
    box-shadow: 0 2px 12px rgba(139,114,217,0.06);
    margin-bottom: 20px;
    animation: fadeUp 0.75s ease;
}

.chart-title {
    font-size: 15px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 14px;
}

.empty-state {
    text-align: center;
    padding: 52px 32px;
    background: white;
    border-radius: 20px;
    border: 1px dashed #DDD6FE;
    margin: 20px 0;
}

.empty-state-icon { font-size: 64px; display: block; margin-bottom: 16px; }
.empty-state-title { font-size: 18px; font-weight: 700; color: #1E293B; margin-bottom: 8px; }
.empty-state-desc  { font-size: 14px; color: #94A3B8; }

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
    <h1>❤️ Your Health Data</h1>
    <p>Track your daily wellness measurements — weight, activity and sleep.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

def load_data():
    return pd.read_sql_query(
        "SELECT date, weight, steps, sleep FROM health_data ORDER BY date DESC, rowid DESC",
        conn
    )

df = load_data()


# =========================================================
# LATEST METRICS
# =========================================================

if not df.empty:
    latest = df.iloc[0]

    st.markdown('<div class="section-title">📊 Your Latest Overview</div>', unsafe_allow_html=True)

    mc1, mc2, mc3, mc4 = st.columns(4)

    with mc1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">⚖️</span>
            <div class="metric-label">Latest Weight</div>
            <div class="metric-value">{latest['weight']:.1f} kg</div>
        </div>""", unsafe_allow_html=True)

    with mc2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">👣</span>
            <div class="metric-label">Latest Steps</div>
            <div class="metric-value">{int(latest['steps']):,}</div>
        </div>""", unsafe_allow_html=True)

    with mc3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">😴</span>
            <div class="metric-label">Latest Sleep</div>
            <div class="metric-value">{latest['sleep']:.1f} hrs</div>
        </div>""", unsafe_allow_html=True)

    with mc4:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">📅</span>
            <div class="metric-label">Total Records</div>
            <div class="metric-value">{len(df)}</div>
        </div>""", unsafe_allow_html=True)


# =========================================================
# RECORD FORM
# =========================================================

st.markdown('<div class="section-title">📝 Record Today\'s Health Data</div>', unsafe_allow_html=True)

st.markdown('<div class="form-card">', unsafe_allow_html=True)

with st.form("health_entry_form"):

    st.markdown('<div class="form-card-title">📋 Enter your measurements below</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)

    with fc1:
        health_date = st.date_input("📅 Date", value=date.today())
        weight = st.number_input(
            "⚖️ Weight (kg)",
            min_value=0.0, max_value=500.0,
            value=50.0, step=0.1,
            format="%.1f"
        )

    with fc2:
        steps = st.number_input(
            "👣 Daily Steps",
            min_value=0, max_value=200000,
            value=0, step=100
        )
        sleep = st.number_input(
            "😴 Sleep (hours)",
            min_value=0.0, max_value=24.0,
            value=7.0, step=0.5,
            format="%.1f"
        )

    submitted = st.form_submit_button(
        "💾  Save Health Data",
        use_container_width=True,
        type="primary"
    )

    if submitted:
        conn.execute(
            "INSERT INTO health_data (date, weight, steps, sleep) VALUES (?, ?, ?, ?)",
            (str(health_date), weight, int(steps), sleep)
        )
        conn.commit()
        st.success("✅ Health data saved successfully! Your record has been added.")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# REFRESH DATA
# =========================================================

df = load_data()


# =========================================================
# CHARTS + RECORDS
# =========================================================

if not df.empty:

    st.markdown("""
    <div class="tip-card">
        💡 <b>Tracking Tip:</b> Regularly recording weight, activity and sleep
        helps you understand your personal wellness patterns over time.
    </div>
    """, unsafe_allow_html=True)

    # Prepare chart data
    chart_df = df.copy()
    chart_df["date"] = pd.to_datetime(chart_df["date"])
    chart_df = chart_df.sort_values("date")

    # Charts
    st.markdown('<div class="section-title">📈 Wellness Trends</div>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div class="chart-card"><div class="chart-title">👣 Activity Trend — Daily Steps</div>', unsafe_allow_html=True)
        st.line_chart(chart_df.set_index("date")["steps"], height=250, color="#8B72D9")
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-card"><div class="chart-title">😴 Sleep Trend — Hours per Day</div>', unsafe_allow_html=True)
        st.line_chart(chart_df.set_index("date")["sleep"], height=250, color="#0284C7")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card"><div class="chart-title">⚖️ Weight Trend — kg over Time</div>', unsafe_allow_html=True)
    st.line_chart(chart_df.set_index("date")["weight"], height=240, color="#0F766E")
    st.markdown('</div>', unsafe_allow_html=True)

    # Records table
    st.markdown('<div class="section-title">📋 Health Records</div>', unsafe_allow_html=True)

    display_df = df.copy()
    display_df.columns = ["Date", "Weight (kg)", "Steps", "Sleep (hrs)"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Export
    st.markdown('<div class="section-title">📥 Export Your Data</div>', unsafe_allow_html=True)

    csv_data = df.to_csv(index=False).encode("utf-8")

    dl1, dl2 = st.columns([2, 5])
    with dl1:
        st.download_button(
            label="📄  Download Health Report (CSV)",
            data=csv_data,
            file_name="aarogya_health_report.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    st.markdown("""
    <div class="empty-state">
        <span class="empty-state-icon">👩‍⚕️</span>
        <div class="empty-state-title">No health records yet</div>
        <div class="empty-state-desc">
            Add your first health record using the form above to start<br>
            building your personal wellness history.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SAFETY NOTICE
# =========================================================

st.markdown("""
<div class="safety-card">
    🛡️ <b>Medical Safety Notice:</b>
    Aarogya-AI is designed for health tracking and general wellness information.
    It does not diagnose medical conditions or replace professional medical advice.
</div>
""", unsafe_allow_html=True)


conn.close()