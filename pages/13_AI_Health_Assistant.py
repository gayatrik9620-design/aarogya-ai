import streamlit as st
from src.chatbot import get_chatbot_response

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.

# =========================================================
# PAGE CSS
# =========================================================

st.markdown("""
<style>

/* ---- Chat header ---- */
.chat-header {
    background: linear-gradient(135deg, #6546B8 0%, #8B72D9 60%, #0284C7 100%);
    border-radius: 22px;
    padding: 32px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 24px;
    box-shadow: 0 8px 28px rgba(101,70,184,0.22);
    animation: fadeDown 0.6s ease;
}

.chat-doc-avatar {
    font-size: 72px;
    animation: float 4s ease-in-out infinite;
    flex-shrink: 0;
    filter: drop-shadow(0 8px 16px rgba(0,0,0,0.15));
}

.chat-header-text h1 {
    color: white !important;
    font-size: 26px;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -0.4px;
}

.chat-header-text p {
    color: rgba(255,255,255,0.82);
    font-size: 14px;
    margin: 0;
    line-height: 1.55;
}

.chat-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 600;
    color: white;
    margin-bottom: 10px;
}

/* ---- Safety disclaimer ---- */
.chat-safety {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-left: 4px solid #F59E0B;
    border-radius: 14px;
    padding: 14px 18px;
    font-size: 13px;
    color: #92400E;
    margin: 0 0 22px 0;
    animation: fadeUp 0.7s ease;
}

/* ---- Quick prompt buttons ---- */
.quick-prompt-label {
    font-size: 12px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

/* ---- Feature pills ---- */
.feat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: white;
    border: 1.5px solid #EDE9FA;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
    color: #6546B8;
    margin-right: 8px;
    margin-bottom: 8px;
    box-shadow: 0 2px 8px rgba(139,114,217,0.07);
}

/* ---- Chat area container ---- */
.chat-container {
    background: white;
    border-radius: 20px;
    border: 1px solid #EDE9FA;
    padding: 20px;
    margin-bottom: 16px;
    min-height: 300px;
    box-shadow: 0 2px 14px rgba(139,114,217,0.06);
    animation: fadeUp 0.7s ease;
}

/* ---- Footer ---- */
.chat-footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    padding-top: 18px;
    border-top: 1px solid #EDE9FA;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-8px); }
}

@keyframes fadeDown {
    from { opacity:0; transform:translateY(-18px); }
    to   { opacity:1; transform:translateY(0); }
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:translateY(0); }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="chat-header">
    <div class="chat-doc-avatar">👩‍⚕️</div>
    <div class="chat-header-text">
        <div class="chat-badge">🤖 AI-Powered • Google Gemini</div>
        <h1>Your AI Health Assistant</h1>
        <p>
            Ask questions about general wellness, lifestyle habits and health information.<br>
            I'm here to provide educational guidance on your wellness journey.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SAFETY DISCLAIMER
# =========================================================

st.markdown("""
<div class="chat-safety">
    ⚠️ <b>Medical Safety Notice —</b>
    Aarogya-AI provides general health information only. It does <b>not</b> diagnose diseases
    or prescribe medications. For personal medical concerns, consult a qualified healthcare
    professional. In an emergency call <b>112</b>.
</div>
""", unsafe_allow_html=True)


# =========================================================
# FEATURE PILLS
# =========================================================

st.markdown("""
<div>
    <span class="feat-pill">💬 Natural language</span>
    <span class="feat-pill">🧠 AI-powered insights</span>
    <span class="feat-pill">🛡️ Safety-first design</span>
    <span class="feat-pill">📊 Health-aware context</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)


# =========================================================
# QUICK PROMPTS
# =========================================================

st.markdown('<div class="quick-prompt-label">💡 Quick Prompts</div>', unsafe_allow_html=True)

qp_col1, qp_col2, qp_col3, qp_col4 = st.columns(4)

quick_prompts = [
    "How can I improve my sleep?",
    "Give me healthy lifestyle tips",
    "How can I stay hydrated?",
    "How to improve daily activity?",
]

if "health_messages" not in st.session_state:
    st.session_state.health_messages = []

prompt_clicked = None

with qp_col1:
    if st.button("😴  Sleep Tips", use_container_width=True):
        prompt_clicked = quick_prompts[0]

with qp_col2:
    if st.button("🌿  Lifestyle Tips", use_container_width=True):
        prompt_clicked = quick_prompts[1]

with qp_col3:
    if st.button("💧  Hydration Tips", use_container_width=True):
        prompt_clicked = quick_prompts[2]

with qp_col4:
    if st.button("🏃  Activity Tips", use_container_width=True):
        prompt_clicked = quick_prompts[3]

st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)


# =========================================================
# CLEAR BUTTON
# =========================================================

clear_col, _ = st.columns([1, 5])
with clear_col:
    if st.button("🗑️  Clear Chat", use_container_width=True):
        st.session_state.health_messages = []
        st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.health_messages:
    with st.chat_message(message["role"],
                         avatar="👩‍⚕️" if message["role"] == "assistant" else "🧑"):
        st.markdown(message["content"])


# =========================================================
# USER INPUT
# =========================================================

user_query = st.chat_input("💬 Ask Aarogya-AI a health or wellness question…")

# Handle quick prompt click
if prompt_clicked:
    user_query = prompt_clicked


# =========================================================
# AI RESPONSE
# =========================================================

if user_query:

    st.session_state.health_messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar="👩‍⚕️"):
        with st.spinner("🤖 Aarogya-AI is thinking…"):
            try:
                response = get_chatbot_response(user_query)
                st.markdown(response)
            except Exception as e:
                response = (
                    "I'm unable to process your question right now. "
                    "Please check your API key configuration and try again."
                )
                st.error(response)

    st.session_state.health_messages.append({
        "role": "assistant",
        "content": response
    })


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="chat-footer">
    🩺 Aarogya-AI &nbsp;·&nbsp; AI-powered wellness assistant &nbsp;·&nbsp;
    For educational and general wellness information only.
</div>
""", unsafe_allow_html=True)