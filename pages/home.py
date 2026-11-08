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
                "SELECT weight, steps, sleep FROM health_data "
                "ORDER BY date DESC, rowid DESC LIMIT 1"
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

# Format display values
weight_val = f"{health['weight']:.1f}" if health["weight"] else "—"
steps_val  = f"{int(health['steps']):,}" if health["steps"]  else "—"
sleep_val  = f"{health['sleep']:.1f}"  if health["sleep"]   else "—"
rec_val    = str(health["records"])

# Steps goal progress
steps_raw     = health["steps"] or 0
steps_goal    = 10000
steps_pct     = min(int(steps_raw / steps_goal * 100), 100)
steps_display = f"{int(steps_raw):,} / {steps_goal:,}"

# =========================================================
# FONTS + TAILWIND + CUSTOM STYLES
# =========================================================

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>

<style>
/* ---- Override Streamlit defaults so the design shows cleanly ---- */
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
section.main > div { padding-top: 0 !important; padding-left: 0 !important; padding-right: 0 !important; }

.font-outfit { font-family: 'Outfit', sans-serif !important; }

/* Body-level colours rendered inside Streamlit */
.aarogya-root {
    font-family: 'Inter', sans-serif;
    background: radial-gradient(125% 125% at 50% 10%, #EFE8FF 0%, #E2D5FF 40%, #D8C7FF 100%);
    min-height: 100vh;
    padding: 24px 28px 32px 28px;
    position: relative;
    overflow-x: hidden;
}

/* ---- Glass variants ---- */
.glass-primary {
    background: linear-gradient(135deg,
        rgba(139,92,246,0.45) 0%,
        rgba(79,70,229,0.35) 50%,
        rgba(14,165,233,0.40) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1.5px solid rgba(255,255,255,0.40);
    box-shadow: 0 20px 50px rgba(99,102,241,0.25),
                inset 0 1px 2px rgba(255,255,255,0.60),
                0 0 20px rgba(168,85,247,0.30);
}

.glass-secondary {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.45) 0%,
        rgba(238,230,255,0.35) 100%);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1.5px solid rgba(255,255,255,0.60);
    box-shadow: 0 20px 40px rgba(139,92,246,0.18),
                inset 0 1px 3px rgba(255,255,255,0.80);
}

.glass-stat {
    background: rgba(255,255,255,0.35);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.60);
    box-shadow: 0 8px 20px rgba(112,0,255,0.08),
                inset 0 1px 1px rgba(255,255,255,0.80);
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
.glass-stat:hover {
    transform: translateY(-6px) scale(1.03);
    background: rgba(255,255,255,0.55);
    box-shadow: 0 14px 28px rgba(139,92,246,0.25),
                inset 0 1px 2px rgba(255,255,255,1);
}

.glass-chip {
    background: rgba(255,255,255,0.50);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.70);
    box-shadow: 0 4px 15px rgba(139,92,246,0.15);
    transition: all 0.3s ease;
}
.glass-chip:hover {
    transform: translateY(-3px) scale(1.08);
    background: rgba(255,255,255,0.80);
}

/* ---- Animations ---- */
@keyframes float {
    0%,100% { transform: translateY(0px) rotate(0deg); }
    50%      { transform: translateY(-12px) rotate(2deg); }
}
@keyframes float-slow {
    0%,100% { transform: translateY(0px) scale(1); }
    50%      { transform: translateY(-18px) scale(1.03); }
}
@keyframes pulse-glow {
    0%,100% { opacity:.6; filter:drop-shadow(0 0 15px rgba(168,85,247,.6)); }
    50%      { opacity:.9; filter:drop-shadow(0 0 30px rgba(56,189,248,.8)); }
}
@keyframes sparkle {
    0%,100% { transform:scale(.8) rotate(0deg);  opacity:.5; }
    50%      { transform:scale(1.2) rotate(45deg); opacity:1; }
}
@keyframes shimmer {
    0%   { transform: translateX(-100%) rotate(30deg); }
    100% { transform: translateX(100%)  rotate(30deg); }
}

.anim-float      { animation: float      5s ease-in-out infinite; }
.anim-float-slow { animation: float-slow 7s ease-in-out infinite; }
.anim-crystal    { animation: float 4s ease-in-out infinite,
                              pulse-glow 3s ease-in-out infinite; }
.anim-sparkle    { animation: sparkle 3s ease-in-out infinite; }

/* shimmer overlay */
.shimmer { position:relative; overflow:hidden; }
.shimmer::after {
    content:'';
    position:absolute; top:-50%; left:-50%;
    width:200%; height:200%;
    background: linear-gradient(60deg,
        transparent 30%, rgba(255,255,255,.15) 50%, transparent 70%);
    animation: shimmer 6s infinite;
}

/* ---- Hero grid ---- */
.hero-grid {
    display: grid;
    grid-template-columns: 7fr 5fr;
    gap: 24px;
    align-items: stretch;
}
@media (max-width: 900px) {
    .hero-grid { grid-template-columns: 1fr; }
}

/* ---- Stat mini cards row ---- */
.stat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }

/* ---- Quick action grid ---- */
.quick-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}
@media (max-width: 700px) {
    .quick-grid { grid-template-columns: repeat(2,1fr); }
}

/* ---- Orbs (decorative) ---- */
.orb {
    position:absolute; border-radius:50%;
    filter: blur(72px); pointer-events:none; z-index:0;
}

/* ---- Floating chip positions ---- */
.chip-tl  { position:absolute; top:-12px;  left:24px; }
.chip-ml  { position:absolute; top:40px;   left:80px; }
.chip-tr  { position:absolute; top:16px;   right:80px; }
.chip-mr  { position:absolute; top:64px;   right:24px; }

/* ---- Btn styles ---- */
.btn-white {
    background:white; color:#581c87;
    padding:12px 24px; border-radius:16px;
    font-weight:700; font-size:14px;
    box-shadow:0 4px 16px rgba(0,0,0,.12);
    display:inline-flex; align-items:center; gap:8px;
    cursor:pointer; border:none; transition:all .2s ease;
}
.btn-white:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,0,0,.16); }

.btn-ghost {
    background:rgba(255,255,255,.15);
    color:white; padding:12px 24px; border-radius:16px;
    font-weight:600; font-size:14px;
    border:1.5px solid rgba(255,255,255,.30);
    backdrop-filter:blur(8px);
    display:inline-flex; align-items:center; gap:8px;
    cursor:pointer; transition:all .2s ease;
}
.btn-ghost:hover { background:rgba(255,255,255,.25); transform:translateY(-2px); }

/* ---- Navbar ---- */
.nav-bar {
    display:flex; align-items:center; justify-content:space-between;
    padding:16px 24px; border-radius:20px; margin-bottom:20px;
}

.nav-logo-box {
    width:40px; height:40px; border-radius:12px;
    background:linear-gradient(135deg,#7c3aed,#4338ca);
    display:flex; align-items:center; justify-content:center;
    box-shadow:0 4px 16px rgba(124,58,237,.35);
}

.nav-links { display:flex; gap:28px; align-items:center; font-weight:500; color:rgba(30,10,60,.75); }
.nav-links a { text-decoration:none; color:inherit; transition:color .2s; font-size:14px; }
.nav-links a:hover { color:#7c3aed; }

.avatar-ring {
    width:38px; height:38px; border-radius:50%;
    background:linear-gradient(135deg,#c084fc,#f472b6);
    padding:2px;
}
.avatar-ring img { width:100%; height:100%; border-radius:50%; background:white; }

/* ---- Quick action card ---- */
.qa-card {
    border-radius:20px; padding:18px 14px;
    display:flex; flex-direction:column;
    align-items:center; text-align:center;
    cursor:pointer; transition:all .25s ease;
}
.qa-card:hover { transform:scale(1.06); }

.qa-icon {
    width:52px; height:52px; border-radius:18px;
    display:flex; align-items:center; justify-content:center;
    font-size:26px; margin-bottom:10px;
    transition:transform .25s ease;
}
.qa-card:hover .qa-icon { transform:rotate(12deg); }
.qa-title  { font-weight:700; font-size:14px; color:#1e0a3c; }
.qa-sub    { font-size:12px;  color:rgba(109,40,217,.65); margin-top:3px; }

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width:8px; }
::-webkit-scrollbar-track { background:rgba(226,213,255,.5); }
::-webkit-scrollbar-thumb { background:rgba(139,92,246,.4); border-radius:4px; }

</style>
""", unsafe_allow_html=True)


# =========================================================
# BUILD THE COMPLETE PAGE
# =========================================================

page_html = f"""
<div class="aarogya-root">

  <!-- Background orbs -->
  <div class="orb" style="width:384px;height:384px;background:rgba(167,139,250,.30);top:5%;left:5%;"></div>
  <div class="orb" style="width:384px;height:384px;background:rgba(99,102,241,.25);bottom:10%;right:5%;"></div>
  <div class="orb anim-float-slow" style="width:128px;height:64px;background:rgba(255,255,255,.45);border-radius:50%;filter:blur(12px);top:24px;left:32px;"></div>
  <div class="orb anim-float"      style="width:80px; height:80px; background:rgba(255,255,255,.30);border-radius:50%;filter:blur(6px); top:96px;left:96px;"></div>

  <!-- ===== NAVBAR ===== -->
  <div class="nav-bar glass-secondary" style="position:relative;z-index:10;">

    <!-- Logo -->
    <div style="display:flex;align-items:center;gap:12px;">
      <div class="nav-logo-box">
        <!-- sparkle SVG icon -->
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none"
             stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 3 L13.5 8.5 L19 10 L13.5 11.5 L12 17 L10.5 11.5 L5 10 L10.5 8.5 Z"/>
          <path d="M19 3 L19.7 5.3 L22 6 L19.7 6.7 L19 9 L18.3 6.7 L16 6 L18.3 5.3 Z"/>
          <path d="M5 17 L5.5 18.8 L7 19.5 L5.5 20.2 L5 22 L4.5 20.2 L3 19.5 L4.5 18.8 Z"/>
        </svg>
      </div>
      <span class="font-outfit" style="font-weight:800;font-size:22px;background:linear-gradient(90deg,#3b0764,#4338ca,#5b21b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        Aarogya <span style="color:#7c3aed;">AI</span>
      </span>
    </div>

    <!-- Nav links (hidden on small screens via inline style) -->
    <nav class="nav-links" style="display:flex;">
      <a href="#">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:4px"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
        Overview
      </a>
      <a href="#">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:4px"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
        Health Vitals
      </a>
      <a href="#">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:4px"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
        AI Consult
      </a>
      <a href="#">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:4px"><path d="M11 11.5v-1a1.5 1.5 0 0 1 3 0v1"/><path d="M17 11.5V11a1.5 1.5 0 0 1 3 0v.5"/><path d="M6 11V10a1.5 1.5 0 0 1 3 0v1"/><path d="M2.5 13.5h19"/><path d="M20.5 13.5C20.5 18 17 21 12 21s-8.5-3-8.5-7.5"/></svg>
        Records
      </a>
    </nav>

    <!-- Right side -->
    <div style="display:flex;align-items:center;gap:12px;">
      <button style="padding:10px;border-radius:12px;background:rgba(255,255,255,.4);border:1px solid rgba(255,255,255,.6);color:#3b0764;cursor:pointer;">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>
      </button>
      <div style="width:1px;height:32px;background:#e9d5ff;margin:0 4px;"></div>
      <div class="avatar-ring">
        <img src="https://api.dicebear.com/7.x/bottts/svg?seed=AarogyaUser" alt="User Avatar">
      </div>
    </div>
  </div>

  <!-- ===== HERO GRID ===== -->
  <div class="hero-grid" style="margin-bottom:24px;position:relative;z-index:5;">

    <!-- LEFT CARD: Welcome -->
    <div class="glass-primary shimmer" style="border-radius:28px;padding:40px;display:flex;flex-direction:column;justify-content:space-between;position:relative;overflow:hidden;min-height:420px;color:white;">

      <!-- Ambient blobs inside card -->
      <div style="position:absolute;top:-96px;right:-96px;width:256px;height:256px;background:rgba(34,211,238,.30);border-radius:50%;filter:blur(32px);"></div>
      <div style="position:absolute;bottom:-96px;left:-96px;width:256px;height:256px;background:rgba(147,51,234,.40);border-radius:50%;filter:blur(32px);"></div>

      <!-- Top content -->
      <div style="position:relative;z-index:2;">
        <!-- Badge -->
        <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.20);backdrop-filter:blur(8px);padding:6px 16px;border-radius:30px;border:1px solid rgba(255,255,255,.30);font-size:13px;font-weight:600;color:rgba(237,233,254,1);margin-bottom:20px;">
          <svg class="anim-sparkle" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="#fbbf24" stroke="none"><path d="M12 3 L13.5 8.5 L19 10 L13.5 11.5 L12 17 L10.5 11.5 L5 10 L10.5 8.5 Z"/></svg>
          AI-Powered Wellness Platform
        </div>

        <!-- Headline -->
        <h1 class="font-outfit" style="font-size:clamp(32px,4vw,52px);font-weight:900;line-height:1.1;letter-spacing:-1px;color:white;margin-bottom:16px;text-shadow:0 2px 16px rgba(0,0,0,.15);">
          Your Health.<br>
          <span style="background:linear-gradient(90deg,#ffffff,#e0d7ff,#a5f3fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            Smarter with AI.
          </span>
        </h1>

        <!-- Subtext -->
        <p style="font-size:16px;color:rgba(237,233,254,.88);line-height:1.7;max-width:460px;font-weight:400;margin:0;">
          Personalized wellness insights, health tracking and AI-powered guidance —
          all in one place, designed for modern living.
        </p>
      </div>

      <!-- Bottom: Buttons + Crystal -->
      <div style="position:relative;z-index:2;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-top:32px;padding-top:24px;border-top:1px solid rgba(255,255,255,.15);">
        <div style="display:flex;flex-wrap:wrap;gap:12px;">
          <button class="btn-white">
            Explore Health Insights
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#581c87" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </button>
          <button class="btn-ghost">
            Ask AI Assistant <span style="font-size:18px;">🤖</span>
          </button>
        </div>

        <!-- Crystal SVG -->
        <div class="anim-crystal" style="flex-shrink:0;">
          <svg width="80" height="90" viewBox="0 0 100 110" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 5L90 35L50 105L10 35L50 5Z" fill="url(#cg1)" opacity=".85"/>
            <path d="M50 5L90 35L50 55L10 35L50 5Z"  fill="url(#cg2)" opacity=".90"/>
            <path d="M50 55L90 35L50 105L50 55Z"      fill="url(#cg3)" opacity=".95"/>
            <path d="M50 55L10 35L50 105L50 55Z"      fill="url(#cg4)" opacity=".75"/>
            <defs>
              <linearGradient id="cg1" x1="10" y1="5"  x2="90" y2="105" gradientUnits="userSpaceOnUse"><stop stop-color="#c084fc"/><stop offset="1" stop-color="#38bdf8"/></linearGradient>
              <linearGradient id="cg2" x1="10" y1="5"  x2="90" y2="55"  gradientUnits="userSpaceOnUse"><stop stop-color="#f472b6"/><stop offset="1" stop-color="#c084fc"/></linearGradient>
              <linearGradient id="cg3" x1="50" y1="35" x2="90" y2="105" gradientUnits="userSpaceOnUse"><stop stop-color="#38bdf8"/><stop offset="1" stop-color="#818cf8"/></linearGradient>
              <linearGradient id="cg4" x1="10" y1="35" x2="50" y2="105" gradientUnits="userSpaceOnUse"><stop stop-color="#e879f9"/><stop offset="1" stop-color="#60a5fa"/></linearGradient>
            </defs>
          </svg>
        </div>
      </div>
    </div>

    <!-- RIGHT CARD: Doctor + Stats -->
    <div class="glass-secondary" style="border-radius:28px;padding:28px;display:flex;flex-direction:column;justify-content:space-between;position:relative;min-height:420px;">

      <!-- Floating chips -->
      <div class="glass-chip anim-float chip-tl" style="padding:10px;border-radius:18px;z-index:20;">
        <div style="width:32px;height:32px;border-radius:12px;background:rgba(239,68,68,.18);display:flex;align-items:center;justify-content:center;">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#ef4444" stroke="none"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
        </div>
      </div>

      <div class="glass-chip anim-float chip-ml" style="padding:8px;border-radius:14px;z-index:20;animation-delay:-1.5s;">
        <div style="width:28px;height:28px;border-radius:10px;background:rgba(99,102,241,.18);display:flex;align-items:center;justify-content:center;">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6"  x2="6"  y1="20" y2="14"/></svg>
        </div>
      </div>

      <div class="glass-chip anim-float chip-tr" style="padding:8px;border-radius:14px;z-index:20;animation-delay:-3s;">
        <div style="width:28px;height:28px;border-radius:10px;background:rgba(6,182,212,.18);display:flex;align-items:center;justify-content:center;">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0891b2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
      </div>

      <div class="glass-chip anim-float chip-mr" style="padding:10px;border-radius:18px;z-index:20;animation-delay:-2s;">
        <div style="width:32px;height:32px;border-radius:12px;background:rgba(168,85,247,.18);display:flex;align-items:center;justify-content:center;font-size:18px;">
          👣
        </div>
      </div>

      <!-- Doctor character -->
      <div style="display:flex;justify-content:center;align-items:center;padding:16px 0;position:relative;z-index:10;">
        <div style="position:absolute;width:180px;height:180px;background:rgba(196,181,253,.40);border-radius:50%;filter:blur(28px);animation:pulse-glow 3s ease-in-out infinite;"></div>
        <div class="anim-float-slow" style="width:170px;height:170px;cursor:pointer;filter:drop-shadow(0 8px 24px rgba(139,92,246,.35));">
          <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
            <defs>
              <linearGradient id="hoodie" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%"   stop-color="#A855F7"/>
                <stop offset="100%" stop-color="#7C3AED"/>
              </linearGradient>
              <linearGradient id="skin" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%"   stop-color="#FFDFC4"/>
                <stop offset="100%" stop-color="#F0B796"/>
              </linearGradient>
              <linearGradient id="hair" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%"   stop-color="#5C3A21"/>
                <stop offset="100%" stop-color="#3A2212"/>
              </linearGradient>
              <radialGradient id="cheekL" cx="50%" cy="50%" r="50%">
                <stop offset="0%"   stop-color="#FF8A8A" stop-opacity="0.5"/>
                <stop offset="100%" stop-color="#FF8A8A" stop-opacity="0"/>
              </radialGradient>
              <radialGradient id="cheekR" cx="50%" cy="50%" r="50%">
                <stop offset="0%"   stop-color="#FF8A8A" stop-opacity="0.5"/>
                <stop offset="100%" stop-color="#FF8A8A" stop-opacity="0"/>
              </radialGradient>
            </defs>
            <!-- Hair bun -->
            <circle cx="100" cy="45" r="24" fill="url(#hair)"/>
            <circle cx="100" cy="40" r="18" fill="#6E4528" opacity="0.5"/>
            <!-- Hair base -->
            <path d="M60 85 C55 55,145 55,140 85 C140 100,60 100,60 85Z" fill="url(#hair)"/>
            <!-- Head -->
            <circle cx="100" cy="92" r="38" fill="url(#skin)"/>
            <!-- Bangs -->
            <path d="M65 80 C75 60,100 75,100 70 C100 75,125 60,135 80 C125 70,75 70,65 80Z" fill="url(#hair)"/>
            <!-- Left eye -->
            <circle cx="85" cy="88" r="5.5" fill="#2E1C11"/>
            <circle cx="86.5" cy="86.5" r="2" fill="#FFF"/>
            <circle cx="87.5" cy="87.5" r="0.8" fill="#FFF"/>
            <!-- Right eye (wink) -->
            <path d="M110 88 Q115 82 120 88" stroke="#2E1C11" stroke-width="2.8" stroke-linecap="round" fill="none"/>
            <!-- Cheeks -->
            <ellipse cx="78"  cy="98" rx="7" ry="5" fill="url(#cheekL)"/>
            <ellipse cx="122" cy="98" rx="7" ry="5" fill="url(#cheekR)"/>
            <!-- Smile -->
            <path d="M92 103 Q100 114 108 103" stroke="#B84A39" stroke-width="2.8" stroke-linecap="round" fill="none"/>
            <!-- Hoodie body -->
            <path d="M45 180 C45 130,155 130,155 180 L165 200 L35 200 Z" fill="url(#hoodie)"/>
            <!-- Collar -->
            <path d="M85 132 L100 155 L115 132" fill="none" stroke="#6D28D9" stroke-width="3" stroke-linecap="round"/>
            <!-- White coat lapels -->
            <path d="M70 135 L85 132 L80 160 L60 155 Z" fill="white" opacity="0.88"/>
            <path d="M130 135 L115 132 L120 160 L140 155 Z" fill="white" opacity="0.88"/>
            <!-- Stethoscope -->
            <path d="M72 145 C72 175,128 175,128 145" fill="none" stroke="#CBD5E1" stroke-width="3.5" stroke-linecap="round"/>
            <circle cx="100" cy="168" r="8" fill="#94A3B8" stroke="#FFF" stroke-width="2"/>
            <circle cx="100" cy="168" r="4" fill="#64748B"/>
          </svg>
        </div>
      </div>

      <!-- Stats: 3-col grid -->
      <div class="stat-grid">
        <div class="glass-stat" style="border-radius:18px;padding:14px 10px;text-align:center;cursor:pointer;">
          <div class="font-outfit" style="font-size:22px;font-weight:900;color:#1e0a3c;line-height:1.2;">
            {weight_val} <span style="font-size:11px;font-weight:700;color:#7c3aed;">kg</span>
          </div>
          <div style="font-size:12px;color:rgba(109,40,217,.75);font-weight:600;margin-top:4px;">⚖️ Weight</div>
        </div>

        <div class="glass-stat" style="border-radius:18px;padding:14px 10px;text-align:center;cursor:pointer;">
          <div class="font-outfit" style="font-size:22px;font-weight:900;color:#1e0a3c;line-height:1.2;">
            {steps_val}
          </div>
          <div style="font-size:12px;color:rgba(109,40,217,.75);font-weight:600;margin-top:4px;">👣 Steps</div>
        </div>

        <div class="glass-stat" style="border-radius:18px;padding:14px 10px;text-align:center;cursor:pointer;">
          <div class="font-outfit" style="font-size:22px;font-weight:900;color:#1e0a3c;line-height:1.2;">
            {sleep_val} <span style="font-size:11px;font-weight:700;color:#7c3aed;">hrs</span>
          </div>
          <div style="font-size:12px;color:rgba(109,40,217,.75);font-weight:600;margin-top:4px;">😴 Sleep</div>
        </div>
      </div>

      <!-- Records row -->
      <div class="glass-stat" style="border-radius:18px;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;cursor:pointer;margin-top:12px;">
        <div style="display:flex;align-items:center;gap:12px;">
          <div style="width:36px;height:36px;border-radius:12px;background:rgba(168,85,247,.20);color:#7c3aed;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:15px;">{rec_val}</div>
          <span style="font-weight:600;font-size:14px;color:#1e0a3c;">Medical Records Synced</span>
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
      </div>
    </div>
  </div>

  <!-- ===== QUICK HEALTH OVERVIEW ===== -->
  <div style="margin-bottom:8px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
      <h2 class="font-outfit" style="font-size:20px;font-weight:800;color:#1e0a3c;display:flex;align-items:center;gap:8px;">
        💖 Your Health Overview
      </h2>
      <a href="#" style="font-size:14px;font-weight:700;color:#7c3aed;text-decoration:none;">View All Trends →</a>
    </div>

    <div class="quick-grid">

      <!-- BMI -->
      <div class="qa-card glass-secondary">
        <div class="qa-icon" style="background:#fef3c7;color:#d97706;">⚖️</div>
        <div class="qa-title">BMI Tracker</div>
        <div class="qa-sub">Optimal Range</div>
      </div>

      <!-- Steps -->
      <div class="qa-card glass-secondary">
        <div class="qa-icon" style="background:#ede9fe;color:#7c3aed;">👣</div>
        <div class="qa-title">Activity Goal</div>
        <div class="qa-sub">{steps_display}</div>
      </div>

      <!-- Sleep -->
      <div class="qa-card glass-secondary">
        <div class="qa-icon" style="background:#e0e7ff;color:#4338ca;">😴</div>
        <div class="qa-title">Sleep Quality</div>
        <div class="qa-sub">{sleep_val} hrs logged</div>
      </div>

      <!-- Schedule -->
      <div class="qa-card glass-secondary">
        <div class="qa-icon" style="background:#fce7f3;color:#db2777;">📅</div>
        <div class="qa-title">Schedule</div>
        <div class="qa-sub">AI Consult Ready</div>
      </div>

    </div>
  </div>

  <!-- Safety notice -->
  <div style="margin-top:24px;background:rgba(255,255,255,.35);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.60);border-left:4px solid #0f766e;border-radius:16px;padding:16px 20px;font-size:13px;color:#134e4a;line-height:1.65;">
    🛡️ <b>Medical Safety Notice:</b> Aarogya-AI is a general wellness and educational platform.
    It does not diagnose diseases, prescribe medications or replace professional medical advice.
    For personal medical concerns please consult a qualified healthcare professional.
    In an emergency call <b>112</b>.
  </div>

</div>
"""

st.markdown(page_html, unsafe_allow_html=True)