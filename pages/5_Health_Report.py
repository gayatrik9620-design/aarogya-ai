import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.

# =========================================================
# DATABASE
# =========================================================

@st.cache_data(ttl=60)
def _load_report_data():
    try:
        conn = sqlite3.connect("health_data.db")
        df = pd.read_sql_query(
            "SELECT date, weight, steps, sleep FROM health_data ORDER BY date DESC",
            conn
        )
        conn.close()
        return df
    except Exception:
        return None

_df_result = _load_report_data()
if _df_result is None:
    st.error("Unable to load health data.")
    st.stop()
df = _df_result


# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

.report-info-card {
    background: white;
    border-radius: 18px;
    padding: 24px 28px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    display: flex;
    gap: 32px;
    align-items: center;
    margin-bottom: 24px;
    animation: fadeUp 0.6s ease;
    flex-wrap: wrap;
}

.report-info-item {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.report-info-label {
    font-size: 11px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.report-info-value {
    font-size: 16px;
    font-weight: 700;
    color: #1E293B;
}

.report-summary-card {
    background: linear-gradient(135deg, #F0EDFD 0%, #F8F7FC 100%);
    border: 1px solid rgba(139,114,217,0.12);
    border-left: 4px solid #8B72D9;
    border-radius: 16px;
    padding: 24px 28px;
    margin: 16px 0;
    line-height: 1.8;
    animation: fadeUp 0.75s ease;
}

.download-section {
    background: white;
    border-radius: 18px;
    padding: 24px 28px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 2px 12px rgba(139,114,217,0.05);
    margin-top: 16px;
    animation: fadeUp 0.8s ease;
}

.download-title {
    font-size: 16px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 8px;
}

.download-desc {
    font-size: 13px;
    color: #64748B;
    margin-bottom: 16px;
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
    <h1>📄 Your Health Report</h1>
    <p>A comprehensive overview of your recorded wellness data and health measurements.</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# NO DATA
# =========================================================

if df.empty:
    st.markdown("""
    <div style="text-align:center;padding:60px 32px;background:white;border-radius:20px;border:1px dashed #DDD6FE;">
        <span style="font-size:64px;display:block;margin-bottom:16px;">👩‍⚕️</span>
        <div style="font-size:18px;font-weight:700;color:#1E293B;margin-bottom:8px;">No health data available</div>
        <div style="font-size:14px;color:#94A3B8;">
            Please add your data from the ❤️ Health Data page to generate a report.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# =========================================================
# DATA PROCESSING
# =========================================================

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

if df.empty:
    st.warning("⚠️ No valid health records available.")
    st.stop()

df = df.sort_values("date", ascending=False).reset_index(drop=True)
latest = df.iloc[0]

avg_weight = df["weight"].mean()
avg_steps  = df["steps"].mean()
avg_sleep  = df["sleep"].mean()

generated_time = datetime.now().strftime("%d %B %Y, %I:%M %p")


# =========================================================
# REPORT INFO BAR
# =========================================================

st.markdown(f"""
<div class="report-info-card">
    <div class="report-info-item">
        <div class="report-info-label">📅 Report Generated</div>
        <div class="report-info-value">{generated_time}</div>
    </div>
    <div class="report-info-item">
        <div class="report-info-label">📊 Total Records</div>
        <div class="report-info-value">{len(df)}</div>
    </div>
    <div class="report-info-item">
        <div class="report-info-label">🗓️ Date Range</div>
        <div class="report-info-value">{df["date"].min().strftime("%d %b %Y")} → {df["date"].max().strftime("%d %b %Y")}</div>
    </div>
    <div class="report-info-item">
        <div class="report-info-label">🩺 Powered By</div>
        <div class="report-info-value">Aarogya-AI</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# LATEST METRICS
# =========================================================

st.markdown('<div class="section-title">📌 Latest Health Summary</div>', unsafe_allow_html=True)

lc1, lc2, lc3 = st.columns(3)

with lc1:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">⚖️</span>
        <div class="metric-label">Latest Weight</div>
        <div class="metric-value">{latest['weight']:.1f} kg</div>
    </div>""", unsafe_allow_html=True)

with lc2:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">👣</span>
        <div class="metric-label">Latest Steps</div>
        <div class="metric-value">{int(latest['steps']):,}</div>
    </div>""", unsafe_allow_html=True)

with lc3:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">😴</span>
        <div class="metric-label">Latest Sleep</div>
        <div class="metric-value">{latest['sleep']:.1f} hrs</div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# AVERAGE METRICS
# =========================================================

st.markdown('<div class="section-title">📊 Overall Statistics</div>', unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns(3)

with sc1:
    st.metric("Average Weight", f"{avg_weight:.2f} kg")

with sc2:
    st.metric("Average Steps", f"{avg_steps:.0f}")

with sc3:
    st.metric("Average Sleep", f"{avg_sleep:.2f} hrs")


# =========================================================
# REPORT SUMMARY
# =========================================================

st.markdown('<div class="section-title">📝 Report Summary</div>', unsafe_allow_html=True)

st.markdown(f"""
### 🩺 Health Data Summary

Your latest recorded weight is **{latest['weight']:.1f} kg**.

You recorded **{int(latest['steps']):,} steps** on the latest available date.

Your latest recorded sleep duration is **{latest['sleep']:.1f} hours**.

---

### 📊 Overall Recorded Data

- ⚖️ Average weight: **{avg_weight:.2f} kg**
- 👣 Average daily steps: **{avg_steps:.0f}**
- 😴 Average sleep duration: **{avg_sleep:.2f} hours**
- 📅 Total health records: **{len(df)}**
""")


# =========================================================
# COMPLETE RECORDS
# =========================================================

st.markdown('<div class="section-title">📑 Complete Health Records</div>', unsafe_allow_html=True)

display_df = df.copy()
display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
display_df = display_df.rename(columns={
    "date":   "Date",
    "weight": "Weight (kg)",
    "steps":  "Steps",
    "sleep":  "Sleep (hrs)"
})

st.dataframe(display_df, use_container_width=True, hide_index=True)


# =========================================================
# DOWNLOAD
# =========================================================

st.markdown('<div class="section-title">📥 Download Report</div>', unsafe_allow_html=True)

st.markdown("""
<div class="download-section">
    <div class="download-title">⬇️ Export Health Report</div>
    <div class="download-desc">
        Download your complete recorded health data as a CSV file for personal reference or sharing with a healthcare professional.
    </div>
</div>
""", unsafe_allow_html=True)

csv_data = display_df.to_csv(index=False).encode("utf-8")

dl1, _ = st.columns([2, 5])
with dl1:
    st.download_button(
        label="📄  Download Health Report (CSV)",
        data=csv_data,
        file_name="Aarogya_AI_Health_Report.csv",
        mime="text/csv",
        use_container_width=True
    )


# =========================================================
# SAFETY NOTICE
# =========================================================

st.markdown("""
<div class="safety-card">
    ⚠️ <b>Safety Notice:</b>
    This report summarizes recorded wellness data only. It does not diagnose diseases,
    predict medical conditions, or replace professional medical advice.
    Please consult a qualified healthcare professional for personal medical concerns.
</div>
""", unsafe_allow_html=True)