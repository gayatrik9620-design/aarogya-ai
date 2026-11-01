import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION  (only ONE allowed in the app)
# --------------------------------------------------

st.set_page_config(
    page_title="Aarogya-AI | Intelligent Wellness",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# GLOBAL CSS DESIGN SYSTEM
# --------------------------------------------------

st.markdown("""
<style>

/* ===== FONTS ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ===== APP BACKGROUND ===== */
.stApp {
    background-color: #F8F7FC;
    color: #1E293B;
}

/* ===== HIDE DEFAULT STREAMLIT DECORATION ===== */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ===== MAIN CONTENT AREA ===== */
.block-container {
    padding: 2rem 2.5rem 3rem 2.5rem;
    max-width: 1280px;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #EDE9FA;
    box-shadow: 2px 0 20px rgba(139,114,217,0.06);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 0;
}

/* ===== SIDEBAR BRAND ===== */
.sidebar-brand {
    padding: 28px 20px 20px 20px;
    background: linear-gradient(135deg, #6546B8 0%, #8B72D9 100%);
    margin-bottom: 0;
}

.sidebar-logo {
    font-size: 22px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.3px;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.sidebar-tagline {
    font-size: 11px;
    color: rgba(255,255,255,0.75);
    font-weight: 400;
    letter-spacing: 0.3px;
}

/* ===== SIDEBAR DIVIDER ===== */
.sidebar-divider {
    height: 1px;
    background: #EDE9FA;
    margin: 12px 16px;
}

/* ===== SIDEBAR SECTION LABEL ===== */
.sidebar-section {
    font-size: 10px;
    font-weight: 600;
    color: #94A3B8;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 8px 20px 4px 20px;
}

/* ===== GLOBAL CARD ===== */
.card {
    background: #FFFFFF;
    border-radius: 20px;
    border: 1px solid rgba(139,114,217,0.08);
    box-shadow: 0 2px 16px rgba(139,114,217,0.06);
    padding: 24px;
    transition: all 0.25s ease;
}

.card:hover {
    box-shadow: 0 6px 28px rgba(139,114,217,0.12);
    transform: translateY(-2px);
}

/* ===== PAGE HEADER CARD ===== */
.page-header {
    background: linear-gradient(135deg, #6546B8 0%, #8B72D9 60%, #0284C7 100%);
    border-radius: 22px;
    padding: 32px 36px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 8px 30px rgba(101,70,184,0.25);
    animation: fadeDown 0.6s ease;
}

.page-header h1 {
    color: white !important;
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}

.page-header p {
    color: rgba(255,255,255,0.85);
    font-size: 15px;
    margin: 0;
    font-weight: 400;
}

/* ===== METRIC CARD ===== */
.metric-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid rgba(139,114,217,0.08);
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    transition: all 0.25s ease;
    animation: fadeUp 0.6s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(139,114,217,0.14);
}

.metric-icon {
    font-size: 28px;
    margin-bottom: 10px;
    display: block;
}

.metric-label {
    font-size: 12px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 26px;
    font-weight: 800;
    color: #1E293B;
    letter-spacing: -0.5px;
}

.metric-sub {
    font-size: 12px;
    color: #94A3B8;
    margin-top: 4px;
}

/* ===== SECTION TITLE ===== */
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #1E293B;
    margin: 28px 0 16px 0;
    letter-spacing: -0.3px;
}

.section-subtitle {
    font-size: 14px;
    color: #64748B;
    margin-top: -10px;
    margin-bottom: 18px;
}

/* ===== INSIGHT / INFO CARDS ===== */
.insight-card {
    background: linear-gradient(135deg, #F0EDFD 0%, #EDE9FA 100%);
    border: 1px solid rgba(139,114,217,0.15);
    border-left: 4px solid #8B72D9;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 12px 0;
    color: #1E293B;
    animation: fadeUp 0.7s ease;
}

.success-card {
    background: #F0FDF4;
    border: 1px solid #86EFAC;
    border-left: 4px solid #16A34A;
    border-radius: 14px;
    padding: 18px 20px;
    color: #15803D;
}

.warning-card {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-left: 4px solid #F59E0B;
    border-radius: 14px;
    padding: 18px 20px;
    color: #92400E;
}

.danger-card {
    background: #FFF1F2;
    border: 1px solid #FECDD3;
    border-left: 4px solid #DC2626;
    border-radius: 14px;
    padding: 18px 20px;
    color: #9F1239;
}

.safety-card {
    background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%);
    border: 1px solid #99F6E4;
    border-left: 4px solid #0F766E;
    border-radius: 14px;
    padding: 18px 20px;
    color: #134E4A;
    margin-top: 28px;
}

/* ===== BUTTONS ===== */
div.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    font-size: 14px;
    border: 1.5px solid #E2E8F0;
    transition: all 0.2s ease;
    padding: 8px 20px;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(139,114,217,0.2);
    border-color: #8B72D9;
    color: #6546B8;
}

div.stDownloadButton > button {
    border-radius: 12px;
    font-weight: 600;
    border: 1.5px solid #E2E8F0;
    transition: all 0.2s ease;
}

div.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(139,114,217,0.2);
}

/* ===== FORM ELEMENTS ===== */
div.stTextInput > div > div > input,
div.stNumberInput > div > div > input,
div.stSelectbox > div > div {
    border-radius: 12px;
    border: 1.5px solid #E2E8F0;
    font-size: 14px;
    transition: border-color 0.2s ease;
}

div.stTextInput > div > div > input:focus,
div.stNumberInput > div > div > input:focus {
    border-color: #8B72D9;
    box-shadow: 0 0 0 3px rgba(139,114,217,0.1);
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #EDE9FA;
}

/* ===== PROGRESS BAR ===== */
div.stProgress > div > div > div {
    background: linear-gradient(90deg, #8B72D9, #6546B8);
    border-radius: 10px;
}

div.stProgress > div > div {
    border-radius: 10px;
    background: #EDE9FA;
}

/* ===== CHAT ===== */
[data-testid="stChatMessage"] {
    border-radius: 16px;
    animation: fadeUp 0.3s ease;
    border: 1px solid #F1F5F9;
    margin: 6px 0;
}

.stChatInputContainer {
    border-radius: 18px !important;
    border: 2px solid #EDE9FA !important;
}

/* ===== RADIO (SIDEBAR NAV) ===== */
div[data-testid="stSidebar"] .stRadio > label {
    display: none;
}

div[data-testid="stSidebar"] .stRadio > div {
    gap: 3px;
    padding: 8px 12px;
}

div[data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] p {
    font-size: 14px;
    font-weight: 500;
    color: #475569;
    padding: 10px 12px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    margin: 0;
}

div[data-testid="stSidebar"] .stRadio [data-checked="true"] div[data-testid="stMarkdownContainer"] p {
    background: #EDE9FA;
    color: #6546B8;
    font-weight: 600;
}

/* ===== ANIMATIONS ===== */
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.05); }
}

/* ===== MISC ===== */
h1, h2, h3 {
    color: #1E293B;
    letter-spacing: -0.3px;
}

hr {
    border: none;
    border-top: 1px solid #EDE9FA;
    margin: 20px 0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🩺 AAROGYA-AI</div>
        <div class="sidebar-tagline">Intelligent Wellness Companion</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">NAVIGATION</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠  Dashboard",
            "🤖  AI Health Assistant",
            "❤️  Health Data",
            "📊  Health Analysis",
            "📄  Health Report",
            "🎯  Health Goals",
            "💡  Recommendations",
            "🩺  Symptom Information",
            "🛡️  Medication Safety",
            "🚨  Emergency Detection"
        ],
        label_visibility="collapsed"
    )

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:12px 20px;">
        <div style="font-size:11px;color:#94A3B8;line-height:1.6;">
            🛡️ <b style="color:#64748B;">Safety Notice</b><br>
            General wellness only.<br>
            Not a substitute for medical advice.
        </div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# PAGE ROUTER
# --------------------------------------------------

# Clean the page key
page_key = page.strip()

if page_key.startswith("🏠"):
    exec(open("pages/home.py", encoding="utf-8").read())

elif page_key.startswith("🤖"):
    exec(open("pages/13_AI_Health_Assistant.py", encoding="utf-8").read())

elif page_key.startswith("❤️"):
    exec(open("pages/3_Health_Data.py", encoding="utf-8").read())

elif page_key.startswith("📊"):
    exec(open("pages/4_Health_Analysis.py", encoding="utf-8").read())

elif page_key.startswith("📄"):
    exec(open("pages/5_Health_Report.py", encoding="utf-8").read())

elif page_key.startswith("🎯"):
    exec(open("pages/7_Health_Goals.py", encoding="utf-8").read())

elif page_key.startswith("💡"):
    exec(open("pages/10_Health_Recommendations.py", encoding="utf-8").read())

elif page_key.startswith("🩺  Symptom"):
    exec(open("pages/9_Symptom_Information.py", encoding="utf-8").read())

elif page_key.startswith("🛡️"):
    exec(open("pages/11_Medication _Safety.py", encoding="utf-8").read())

elif page_key.startswith("🚨"):
    exec(open("pages/12_Emergency_Detection.py", encoding="utf-8").read())