import os
import sqlite3
import streamlit as st

# =========================================================
# DATABASE — read latest snapshot for hero metrics
# =========================================================

@st.cache_data(ttl=30)
def get_health_snapshot():
    snap = {"weight": None, "steps": None, "sleep": None, "records": 0}
    db_path = "health_data.db"
    if not os.path.exists(db_path):
        return snap
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM health_data")
        snap["records"] = cursor.fetchone()[0]
        if snap["records"] > 0:
            cursor.execute(
                "SELECT weight, steps, sleep FROM health_data ORDER BY date DESC, rowid DESC LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                snap["weight"] = row[0]
                snap["steps"]  = row[1]
                snap["sleep"]  = row[2]
        conn.close()
    except Exception:
        pass
    return snap


health = get_health_snapshot()

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<style>

/* ---- Hero ---- */
.hero-wrap {
    background: linear-gradient(135deg, #6546B8 0%, #8B72D9 50%, #0284C7 100%);
    border-radius: 28px;
    padding: 52px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    animation: fadeDown 0.7s ease;
}

.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}

.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 30px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    color: white;
    margin-bottom: 18px;
    backdrop-filter: blur(8px);
}

.hero-headline {
    font-size: 46px;
    font-weight: 800;
    color: white;
    line-height: 1.15;
    letter-spacing: -1px;
    margin-bottom: 16px;
}

.hero-headline span {
    color: #C4B5FD;
}

.hero-sub {
    font-size: 16px;
    color: rgba(255,255,255,0.82);
    line-height: 1.65;
    max-width: 480px;
    margin-bottom: 28px;
    font-weight: 400;
}

.hero-btn-primary {
    display: inline-block;
    background: white;
    color: #6546B8;
    font-weight: 700;
    font-size: 14px;
    padding: 12px 24px;
    border-radius: 12px;
    text-decoration: none;
    margin-right: 12px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.15);
    transition: all 0.2s ease;
}

.hero-btn-secondary {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    color: white;
    font-weight: 600;
    font-size: 14px;
    padding: 12px 24px;
    border-radius: 12px;
    text-decoration: none;
    border: 1.5px solid rgba(255,255,255,0.35);
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
}

/* ---- Doctor Illustration ---- */
.doctor-figure {
    text-align: center;
    position: relative;
    padding: 10px;
}

.doctor-avatar {
    font-size: 110px;
    display: block;
    animation: float 4s ease-in-out infinite;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.2));
    line-height: 1;
}

.float-icon {
    position: absolute;
    font-size: 22px;
    background: rgba(255,255,255,0.22);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 12px;
    padding: 8px;
    backdrop-filter: blur(8px);
    animation: float 3s ease-in-out infinite;
}

.float-icon.i1 { top:  5%; left:  5%; animation-delay: 0.0s; }
.float-icon.i2 { top:  5%; right: 5%; animation-delay: 0.5s; }
.float-icon.i3 { top: 40%; left:  0%; animation-delay: 1.0s; }
.float-icon.i4 { top: 40%; right: 0%; animation-delay: 1.5s; }
.float-icon.i5 { bottom:8%; left: 15%; animation-delay: 0.7s; }
.float-icon.i6 { bottom:8%; right:12%; animation-delay: 1.2s; }

/* ---- Stat bar ---- */
.hero-stats {
    display: flex;
    gap: 24px;
    margin-top: 28px;
    flex-wrap: wrap;
}

.hero-stat {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 14px;
    padding: 12px 18px;
    backdrop-filter: blur(8px);
    min-width: 100px;
}

.hero-stat-val {
    font-size: 20px;
    font-weight: 800;
    color: white;
}

.hero-stat-lbl {
    font-size: 11px;
    color: rgba(255,255,255,0.7);
    font-weight: 500;
    margin-top: 2px;
}

/* ---- Feature cards ---- */
.feat-card {
    background: white;
    border-radius: 20px;
    padding: 22px;
    border: 1px solid rgba(139,114,217,0.1);
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    height: 100%;
    transition: all 0.25s ease;
    animation: fadeUp 0.7s ease;
    cursor: default;
}

.feat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 28px rgba(139,114,217,0.15);
    border-color: rgba(139,114,217,0.25);
}

.feat-icon {
    font-size: 30px;
    margin-bottom: 12px;
    display: block;
}

.feat-title {
    font-size: 15px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 6px;
}

.feat-desc {
    font-size: 13px;
    color: #64748B;
    line-height: 1.55;
}

/* ---- Metric overview ---- */
.ov-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid rgba(139,114,217,0.08);
    box-shadow: 0 2px 12px rgba(139,114,217,0.06);
    text-align: center;
    transition: all 0.25s ease;
    animation: fadeUp 0.65s ease;
}

.ov-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 22px rgba(139,114,217,0.13);
}

.ov-icon { font-size: 32px; display: block; margin-bottom: 8px; }
.ov-val  { font-size: 24px; font-weight: 800; color: #1E293B; }
.ov-lbl  { font-size: 12px; color: #94A3B8; font-weight: 500; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.4px; }

/* ---- AI feature banner ---- */
.ai-banner {
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border: 1px solid rgba(139,114,217,0.2);
    border-radius: 20px;
    padding: 28px 32px;
    margin-top: 10px;
    display: flex;
    align-items: center;
    gap: 20px;
    animation: fadeUp 0.8s ease;
}

.ai-banner-icon {
    font-size: 48px;
    animation: pulse 3s ease-in-out infinite;
    flex-shrink: 0;
}

.ai-banner-title {
    font-size: 18px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 6px;
}

.ai-banner-desc {
    font-size: 14px;
    color: #64748B;
    line-height: 1.55;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-8px); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.06); }
}

@keyframes fadeDown {
    from { opacity:0; transform:translateY(-20px); }
    to   { opacity:1; transform:translateY(0); }
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-badge">✨ AI-Powered Wellness Platform</div>
        <div class="hero-headline">
            Your Health.<br>
            <span>Smarter with AI.</span>
        </div>
        <div class="hero-sub">
            Personalized wellness insights, health tracking and AI-powered
            guidance — all in one place, designed for modern living.
        </div>
        <div>
            <a class="hero-btn-primary">Explore Health Insights →</a>
            <a class="hero-btn-secondary">Ask AI Assistant 🤖</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    weight_val = f"{health['weight']:.1f} kg" if health["weight"] else "—"
    steps_val  = f"{int(health['steps']):,}"  if health["steps"]  else "—"
    sleep_val  = f"{health['sleep']:.1f} hrs" if health["sleep"]  else "—"
    rec_val    = str(health["records"])

    st.markdown(f"""
    <div class="hero-wrap" style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:36px 32px;">
        <div class="doctor-figure" style="position:relative;margin-bottom:16px;">
            <span class="float-icon i1">❤️</span>
            <span class="float-icon i2">🛡️</span>
            <span class="float-icon i3">📊</span>
            <span class="float-icon i4">👣</span>
            <span class="float-icon i5">😴</span>
            <span class="float-icon i6">🤖</span>
            <span class="doctor-avatar">👩‍⚕️</span>
        </div>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-val">{weight_val}</div>
                <div class="hero-stat-lbl">⚖️ Weight</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-val">{steps_val}</div>
                <div class="hero-stat-lbl">👣 Steps</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-val">{sleep_val}</div>
                <div class="hero-stat-lbl">😴 Sleep</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-val">{rec_val}</div>
                <div class="hero-stat-lbl">📅 Records</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# HEALTH OVERVIEW METRICS
# =========================================================

st.markdown('<div class="section-title">❤️ Your Health Overview</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    val = f"{health['weight']:.1f} kg" if health["weight"] else "No data"
    sub = "Latest recorded"
    st.markdown(f"""
    <div class="ov-card">
        <span class="ov-icon">⚖️</span>
        <div class="ov-val">{val}</div>
        <div class="ov-lbl">{sub}</div>
    </div>""", unsafe_allow_html=True)

with m2:
    val = f"{int(health['steps']):,}" if health["steps"] else "No data"
    st.markdown(f"""
    <div class="ov-card">
        <span class="ov-icon">👣</span>
        <div class="ov-val">{val}</div>
        <div class="ov-lbl">Daily Steps</div>
    </div>""", unsafe_allow_html=True)

with m3:
    val = f"{health['sleep']:.1f} hrs" if health["sleep"] else "No data"
    st.markdown(f"""
    <div class="ov-card">
        <span class="ov-icon">😴</span>
        <div class="ov-val">{val}</div>
        <div class="ov-lbl">Sleep Duration</div>
    </div>""", unsafe_allow_html=True)

with m4:
    val = str(health["records"]) if health["records"] else "0"
    st.markdown(f"""
    <div class="ov-card">
        <span class="ov-icon">📅</span>
        <div class="ov-val">{val}</div>
        <div class="ov-lbl">Health Records</div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# FEATURE CARDS
# =========================================================

st.markdown('<div class="section-title">⚡ Platform Features</div>', unsafe_allow_html=True)

features = [
    ("❤️", "Health Tracking",      "Log weight, steps and sleep daily. Build your personal wellness history over time."),
    ("🤖", "AI Health Assistant",  "Ask natural-language health questions powered by Google Gemini AI."),
    ("📊", "Health Analysis",      "Visualize trends and patterns in your recorded wellness data."),
    ("📄", "Smart Health Reports", "Generate and download professional wellness reports as CSV."),
    ("🎯", "Health Goals",         "Set daily targets and track your progress with visual dashboards."),
    ("🛡️", "Medication Safety",    "Access curated medication awareness and safety information."),
]

col_a, col_b, col_c = st.columns(3)

for i, (icon, title, desc) in enumerate(features):
    col = [col_a, col_b, col_c][i % 3]
    with col:
        st.markdown(f"""
        <div class="feat-card">
            <span class="feat-icon">{icon}</span>
            <div class="feat-title">{title}</div>
            <div class="feat-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    if i == 2:
        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)


# =========================================================
# AI INTELLIGENCE BANNER
# =========================================================

st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="ai-banner">
    <div class="ai-banner-icon">🤖</div>
    <div>
        <div class="ai-banner-title">Aarogya-AI Intelligence — Powered by Google Gemini</div>
        <div class="ai-banner-desc">
            Ask questions about general wellness, lifestyle habits, nutrition, sleep and daily activity.
            Aarogya-AI provides informational guidance to help you understand your health journey better.
            <br><br>
            <b>Try asking:</b> "How can I improve my sleep quality?" &nbsp;·&nbsp;
            "Give me healthy lifestyle tips." &nbsp;·&nbsp;
            "How many steps should I walk daily?"
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SAFETY NOTICE
# =========================================================

st.markdown("""
<div class="safety-card" style="margin-top:28px;">
    <b>🛡️ Medical Safety Notice</b><br>
    Aarogya-AI is a general wellness and educational platform. It does not diagnose diseases,
    prescribe medications or replace professional medical advice. For personal medical concerns,
    please consult a qualified healthcare professional. In an emergency, call <b>112</b>.
</div>
""", unsafe_allow_html=True)