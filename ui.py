import streamlit as st

def inject_custom_css():
    """
    Injects a modern, light-mode healthcare CSS theme into Streamlit.
    """
    st.markdown(
        """
        <style>
        /* Modern Healthcare Theme Variables */
        :root {
            --bg-color: #F8FAFC;
            --card-bg: #FFFFFF;
            --primary: #0F766E;        /* Dark Teal */
            --primary-hover: #115E59;
            --secondary: #0284C7;      /* Soft Blue */
            --text-dark: #0F172A;      /* Navy */
            --text-muted: #64748B;     /* Slate */
            --border-color: #E2E8F0;
            --success-bg: #ECFDF5;
            --success-text: #047857;
            --warning-bg: #FFFBEB;
            --warning-text: #B45309;
            --danger-bg: #FEF2F2;
            --danger-text: #B91C1C;
            --radius-md: 10px;
            --radius-lg: 16px;
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        /* App Background Reset */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-dark);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid var(--border-color);
        }

        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background-color: rgba(255,255,255,0);}

        /* Modern Card Containers */
        .ui-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow-sm);
            transition: box-shadow 0.2s ease-in-out;
        }

        .ui-card:hover {
            box-shadow: var(--shadow-md);
        }

        .ui-card-title {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .ui-card-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-dark);
            line-height: 1.2;
        }

        .ui-card-subtitle {
            font-size: 0.8125rem;
            color: var(--text-muted);
            margin-top: 0.35rem;
        }

        /* Section Headers */
        .page-header {
            margin-bottom: 1.5rem;
        }

        .page-header h1 {
            color: var(--text-dark);
            font-size: 1.875rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .page-header p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin: 0;
        }

        /* Banner Alerts (Medical/Disclaimer) */
        .alert-box {
            padding: 1rem 1.25rem;
            border-radius: var(--radius-md);
            margin-bottom: 1.25rem;
            font-size: 0.875rem;
            line-height: 1.5;
            border: 1px solid transparent;
        }

        .alert-info {
            background-color: #F0F9FF;
            color: #0369A1;
            border-color: #BAE6FD;
        }

        .alert-warning {
            background-color: var(--warning-bg);
            color: var(--warning-text);
            border-color: #FDE68A;
        }

        .alert-danger {
            background-color: var(--danger-bg);
            color: var(--danger-text);
            border-color: #FECACA;
        }

        /* Primary Button Styling */
        div.stButton > button {
            background-color: var(--primary);
            color: #FFFFFF;
            border-radius: var(--radius-md);
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            width: 100%;
            transition: background-color 0.2s ease;
        }

        div.stButton > button:hover {
            background-color: var(--primary-hover);
            color: #FFFFFF;
        }

        /* Custom Chat Bubble Container */
        .chat-row-user {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 1rem;
        }
        .chat-bubble-user {
            background-color: var(--primary);
            color: white;
            padding: 0.75rem 1rem;
            border-radius: 16px 16px 2px 16px;
            max-width: 80%;
            font-size: 0.95rem;
        }
        .chat-row-ai {
            display: flex;
            justify-content: flex-start;
            margin-bottom: 1rem;
        }
        .chat-bubble-ai {
            background-color: #FFFFFF;
            border: 1px solid var(--border-color);
            color: var(--text-dark);
            padding: 0.75rem 1rem;
            border-radius: 16px 16px 16px 2px;
            max-width: 80%;
            font-size: 0.95rem;
            box-shadow: var(--shadow-sm);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_page_header(title: str, subtitle: str):
    """Renders a standard clean top header for any page."""
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_metric_card(title: str, value: str, subtitle: str = ""):
    """Renders a modern metric block."""
    st.markdown(
        f"""
        <div class="ui-card">
            <div class="ui-card-title">{title}</div>
            <div class="ui-card-value">{value}</div>
            <div class="ui-card-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_insight_card(title: str, content: str, tag: str = "Aarogya-AI Insight"):
    """Renders AI insights in a structured visual wrapper."""
    st.markdown(
        f"""
        <div class="ui-card" style="border-left: 4px solid var(--primary);">
            <div class="ui-card-title" style="color: var(--primary);">{tag}</div>
            <h4 style="margin: 0 0 0.5rem 0; color: var(--text-dark); font-size: 1.1rem;">{title}</h4>
            <p style="margin: 0; color: var(--text-muted); font-size: 0.925rem; line-height: 1.5;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_safety_disclaimer():
    """Responsible medical disclaimer alert box."""
    st.markdown(
        """
        <div class="alert-box alert-warning">
            <strong>Medical Safety Notice:</strong> Aarogya-AI provides health informational insights powered by AI. It is not a licensed physician or a diagnostic tool. Do not alter medications or treatment plans without consulting a qualified medical practitioner.
        </div>
        """,
        unsafe_allow_html=True,
    )