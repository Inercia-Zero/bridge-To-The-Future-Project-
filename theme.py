import streamlit as st


def apply_theme():
    st.markdown("""
    <style>

    /* ===== FUNDO ===== */
    .stApp {
        background: radial-gradient(circle at top, #0f172a, #020617);
        color: #e2e8f0;
    }

    /* ===== TEXTO ===== */
    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    p, span, div {
        color: #cbd5e1;
    }

    /* ===== INPUT ===== */
    input, textarea {
        background: #020617 !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    /* ===== BOTÃO ===== */
    .stButton button {
        background: linear-gradient(135deg, #1e293b, #020617);
        color: #e2e8f0;
        border-radius: 10px;
        border: 1px solid #1e293b;
        transition: 0.2s;
    }

    .stButton button:hover {
        border: 1px solid #38bdf8;
        box-shadow: 0 0 12px rgba(56,189,248,0.4);
    }

    /* ===== CARDS ===== */
    .landing-card {
        background: rgba(2,6,23,0.85);
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 16px;
        transition: 0.2s;
    }

    .landing-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 20px rgba(56,189,248,0.25);
        border: 1px solid #38bdf8;
    }

    /* ===== FALLBACK (SEM IMAGEM) ===== */
    .landing-fallback-inner {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 180px;
        background: linear-gradient(135deg, #1f2937, #111827);
        border-radius: 16px;
        color: #cbd5e1;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 10px 22px rgba(0,0,0,0.22);
        font-weight: 800;
        letter-spacing: 0.08em;
    }

    .landing-fallback-inner span {
        font-size: 2.2rem;
    }

    /* ===== CHAT ===== */
    .message-user {
        background: #1e293b;
        border-radius: 12px;
        padding: 10px;
        margin: 6px 0;
    }

    .message-assistant {
        background: #020617;
        border-radius: 12px;
        padding: 10px;
        margin: 6px 0;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid #1e293b;
    }

    </style>
    """, unsafe_allow_html=True)
