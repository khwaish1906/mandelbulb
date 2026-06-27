
import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="RetailMart Analytics Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import pages
from ui.landing import render_landing
from ui.pipeline import render_pipeline
from ui.dashboard import render_dashboard
from ui.styles import inject_styles

inject_styles()

# Session state init
if "pipeline_done" not in st.session_state:
    st.session_state.pipeline_done = False
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:2.5rem;'>🛒</div>
        <div style='font-size:1.1rem; font-weight:700; color:#6366f1; letter-spacing:1px;'>RetailMart</div>
        <div style='font-size:0.75rem; color:#94a3b8;'>Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    nav_items = [
        ("🏠", "Home", "landing"),
        ("⚙️", "Pipeline", "pipeline"),
        ("📊", "Dashboard", "dashboard"),
    ]

    for icon, label, key in nav_items:
        is_active = st.session_state.page == key
        btn_style = "primary" if is_active else "secondary"
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True, type=btn_style):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")

    dark_label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
    if st.button(dark_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem; color:#64748b; text-align:center;'>
        <b>Tech Stack</b><br>
        Python · Pandas · NumPy<br>
        SQLite · SQLAlchemy<br>
        Plotly · Streamlit
    </div>
    """, unsafe_allow_html=True)

# Route pages
page = st.session_state.page

if page == "landing":
    render_landing()
elif page == "pipeline":
    render_pipeline()
elif page == "dashboard":
    if not st.session_state.pipeline_done:
        st.warning("⚠️ Please run the pipeline first from the **Pipeline** page.")
        if st.button("Go to Pipeline →"):
            st.session_state.page = "pipeline"
            st.rerun()
    else:
        render_dashboard()
