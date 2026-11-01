import streamlit as st
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.

# =========================================================
# DATABASE
# =========================================================

try:
    conn = sqlite3.connect("health_data.db")
    df = pd.read_sql_query(
        "SELECT date, weight, steps, sleep FROM health_data ORDER BY date",
        conn
    )
    conn.close()
except Exception as e:
    st.error(f"Unable to load health data: {e}")
    st.stop()


# =========================================================
# MATPLOTLIB STYLE
# =========================================================

def apply_premium_style(ax, fig):
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAFBFF")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#E2E8F0")
    ax.spines["bottom"].set_color("#E2E8F0")
    ax.tick_params(colors="#64748B", labelsize=9)
    ax.xaxis.label.set_color("#64748B")
    ax.yaxis.label.set_color("#64748B")
    ax.title.set_color("#1E293B")
    plt.xticks(rotation=35, ha="right")


# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

.analysis-insight {
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border: 1px solid rgba(139,114,217,0.18);
    border-left: 4px solid #8B72D9;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 14px 0;
    animation: fadeUp 0.7s ease;
    font-size: 14px;
    color: #1E293B;
    line-height: 1.6;
}

.analysis-insight.good {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border-left-color: #16A34A;
    color: #14532D;
}

.analysis-insight.warn {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border-left-color: #F59E0B;
    color: #78350F;
}

.chart-section {
    background: white;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(139,114,217,0.08);
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    margin-bottom: 20px;
    animation: fadeUp 0.75s ease;
}

.chart-section-title {
    font-size: 16px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.stat-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
}

.stat-pill {
    background: #F8F7FC;
    border: 1px solid #EDE9FA;
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 13px;
    color: #6546B8;
    font-weight: 600;
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
    <h1>📊 Health Analysis</h1>
    <p>Understand your wellness patterns through AI-assisted data insights and trend visualization.</p>
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
            Please add your health data from the ❤️ Health Data page to view analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# =========================================================
# DATA PREP
# =========================================================

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)

if df.empty:
    st.warning("⚠️ No valid health records available.")
    st.stop()

latest      = df.iloc[-1]
avg_weight  = df["weight"].mean()
avg_steps   = df["steps"].mean()
avg_sleep   = df["sleep"].mean()


# =========================================================
# RECORD COUNT BANNER
# =========================================================

st.markdown(f"""
<div class="analysis-insight">
    ✅ <b>{len(df)}</b> health record(s) available for analysis.
    &nbsp;·&nbsp; Data range: <b>{df["date"].min().strftime("%d %b %Y")}</b>
    &nbsp;→&nbsp; <b>{df["date"].max().strftime("%d %b %Y")}</b>
</div>
""", unsafe_allow_html=True)


# =========================================================
# OVERVIEW METRICS
# =========================================================

st.markdown('<div class="section-title">📌 Latest Health Overview</div>', unsafe_allow_html=True)

oc1, oc2, oc3 = st.columns(3)

with oc1:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">⚖️</span>
        <div class="metric-label">Latest Weight</div>
        <div class="metric-value">{latest['weight']:.1f} kg</div>
        <div class="metric-sub">Avg: {avg_weight:.2f} kg</div>
    </div>""", unsafe_allow_html=True)

with oc2:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">👣</span>
        <div class="metric-label">Latest Steps</div>
        <div class="metric-value">{int(latest['steps']):,}</div>
        <div class="metric-sub">Avg: {avg_steps:.0f} steps/day</div>
    </div>""", unsafe_allow_html=True)

with oc3:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">😴</span>
        <div class="metric-label">Latest Sleep</div>
        <div class="metric-value">{latest['sleep']:.1f} hrs</div>
        <div class="metric-sub">Avg: {avg_sleep:.2f} hrs/night</div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# CHARTS
# =========================================================

st.markdown('<div class="section-title">📈 Health Trends</div>', unsafe_allow_html=True)

PURPLE  = "#8B72D9"
TEAL    = "#0F766E"
BLUE    = "#0284C7"

# ---- Weight ----
st.markdown('<div class="chart-section"><div class="chart-section-title">⚖️ Weight Trend</div>', unsafe_allow_html=True)
fig1, ax1 = plt.subplots(figsize=(9, 3.2))
ax1.fill_between(df["date"], df["weight"], alpha=0.12, color=TEAL)
ax1.plot(df["date"], df["weight"], color=TEAL, linewidth=2.2, marker="o", markersize=5)
ax1.set_ylabel("Weight (kg)")
ax1.set_title("")
apply_premium_style(ax1, fig1)
plt.tight_layout()
st.pyplot(fig1, use_container_width=True)
plt.close(fig1)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Steps ----
st.markdown('<div class="chart-section"><div class="chart-section-title">👣 Daily Steps Trend</div>', unsafe_allow_html=True)
fig2, ax2 = plt.subplots(figsize=(9, 3.2))
ax2.fill_between(df["date"], df["steps"], alpha=0.12, color=PURPLE)
ax2.plot(df["date"], df["steps"], color=PURPLE, linewidth=2.2, marker="o", markersize=5)
ax2.axhline(7000, color="#F59E0B", linestyle="--", linewidth=1.2, alpha=0.8, label="7,000 step reference")
ax2.legend(fontsize=9)
ax2.set_ylabel("Steps")
apply_premium_style(ax2, fig2)
plt.tight_layout()
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Sleep ----
st.markdown('<div class="chart-section"><div class="chart-section-title">😴 Sleep Duration Trend</div>', unsafe_allow_html=True)
fig3, ax3 = plt.subplots(figsize=(9, 3.2))
ax3.fill_between(df["date"], df["sleep"], alpha=0.12, color=BLUE)
ax3.plot(df["date"], df["sleep"], color=BLUE, linewidth=2.2, marker="o", markersize=5)
ax3.axhline(7, color="#16A34A", linestyle="--", linewidth=1.2, alpha=0.8, label="7-hr reference")
ax3.legend(fontsize=9)
ax3.set_ylabel("Sleep (hours)")
apply_premium_style(ax3, fig3)
plt.tight_layout()
st.pyplot(fig3, use_container_width=True)
plt.close(fig3)
st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# STATISTICS
# =========================================================

st.markdown('<div class="section-title">📋 Health Statistics</div>', unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns(3)

with sc1:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">⚖️</span>
        <div class="metric-label">Average Weight</div>
        <div class="metric-value">{avg_weight:.2f} kg</div>
    </div>""", unsafe_allow_html=True)

with sc2:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">👣</span>
        <div class="metric-label">Average Steps</div>
        <div class="metric-value">{avg_steps:.0f}</div>
    </div>""", unsafe_allow_html=True)

with sc3:
    st.markdown(f"""
    <div class="metric-card">
        <span class="metric-icon">😴</span>
        <div class="metric-label">Average Sleep</div>
        <div class="metric-value">{avg_sleep:.2f} hrs</div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# WELLNESS INSIGHTS
# =========================================================

st.markdown('<div class="section-title">💡 Wellness Insights</div>', unsafe_allow_html=True)

activity_class = "good" if avg_steps >= 7000 else "warn"
activity_msg   = (
    "Your recorded activity level shows consistent daily movement. Keep it up!"
    if avg_steps >= 7000
    else "Your recorded activity level may benefit from more regular movement."
)

sleep_class = "good" if avg_sleep >= 7 else "warn"
sleep_msg   = (
    "Your recorded average sleep duration is within a commonly recommended range."
    if avg_sleep >= 7
    else "Your recorded average sleep duration is below 7 hours."
)

st.markdown(f"""
<div class="analysis-insight {activity_class}">
    👣 <b>Activity Insight:</b> {activity_msg}
</div>
<div class="analysis-insight {sleep_class}">
    😴 <b>Sleep Insight:</b> {sleep_msg}
</div>
<div class="analysis-insight">
    📊 <b>Data:</b> You currently have <b>{len(df)}</b> health record(s) available.
    Continue adding records for richer trend analysis.
</div>
""", unsafe_allow_html=True)


# =========================================================
# DATA TABLE
# =========================================================

st.markdown('<div class="section-title">📑 Recorded Health Data</div>', unsafe_allow_html=True)

display_df = df.copy()
display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
st.dataframe(display_df, use_container_width=True, hide_index=True)


# =========================================================
# SAFETY NOTICE
# =========================================================

st.markdown("""
<div class="safety-card">
    ⚠️ <b>Safety Notice:</b>
    This analysis summarizes recorded wellness data only.
    It does not diagnose diseases or provide medical advice.
    Please consult a qualified healthcare professional for personal medical concerns.
</div>
""", unsafe_allow_html=True)