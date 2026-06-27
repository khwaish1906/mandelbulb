import streamlit as st


def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }

    /* Cards */
    .kpi-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99,102,241,0.8);
        box-shadow: 0 8px 32px rgba(99,102,241,0.2);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }
    .kpi-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }

    /* Log cards */
    .log-item {
        background: rgba(255,255,255,0.04);
        border-left: 3px solid #10b981;
        border-radius: 0 8px 8px 0;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.9rem;
        color: #e2e8f0;
    }
    .log-item.pending {
        border-left-color: #6366f1;
        opacity: 0.6;
    }

    /* Section headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 1.5rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(99,102,241,0.4);
    }

    /* Quality card */
    .quality-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .quality-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #10b981;
    }
    .quality-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Insight card */
    .insight-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .insight-icon { font-size: 1.5rem; }
    .insight-title { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .insight-value { font-size: 1rem; font-weight: 600; color: #e2e8f0; }

    /* Hero gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 500;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99,102,241,0.2) !important;
        color: #6366f1 !important;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03);
        border: 2px dashed rgba(99,102,241,0.4);
        border-radius: 12px;
        padding: 1rem;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(99,102,241,0.2);
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Progress */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        border-radius: 10px;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 8px !important;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)
