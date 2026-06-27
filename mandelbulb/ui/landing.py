import streamlit as st


def render_landing():
    # Hero section
    st.markdown("""
    <div style='text-align:center; padding: 3rem 1rem 2rem;'>
        <div style='font-size:4rem; margin-bottom:1rem;'>🛒</div>
        <h1 style='font-size:3rem; font-weight:800; margin:0;'>
            <span class='gradient-text'>RetailMart Analytics</span>
        </h1>
        <p style='font-size:1.1rem; color:#94a3b8; margin-top:0.8rem; max-width:600px; margin-left:auto; margin-right:auto;'>
            Enterprise-grade Retail Data Engineering & Analytics Platform.
            Transform raw CSV data into actionable business intelligence — in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ETL Workflow Diagram
    st.markdown("<div class='section-title'>⚡ ETL Pipeline Architecture</div>", unsafe_allow_html=True)

    cols = st.columns(7)
    steps = [
        ("📂", "CSV Upload", "#6366f1"),
        ("⬇️", "", "#334155"),
        ("🔍", "Extract", "#8b5cf6"),
        ("✅", "Validate", "#a78bfa"),
        ("🧹", "Clean", "#ec4899"),
        ("🔄", "Transform", "#f59e0b"),
        ("🗄️", "SQLite", "#10b981"),
    ]

    for i, col in enumerate(cols):
        with col:
            icon, label, color = steps[i]
            if label:
                st.markdown(f"""
                <div style='text-align:center; padding:1rem 0.5rem;
                     background:rgba(255,255,255,0.05); border-radius:12px;
                     border:1px solid {color}44;'>
                    <div style='font-size:1.8rem;'>{icon}</div>
                    <div style='font-size:0.75rem; color:{color}; font-weight:600;
                         margin-top:0.3rem; text-transform:uppercase; letter-spacing:1px;'>{label}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='text-align:center; padding:1.8rem 0; font-size:1.5rem; color:#475569;'>
                    →
                </div>
                """, unsafe_allow_html=True)

    # Second row
    col_spacer, col_arrow, col_analytics = st.columns([6, 0.5, 0.5])
    st.markdown("""
    <div style='text-align:center; margin-top:0.5rem;'>
        <span style='color:#475569; font-size:1.5rem;'>↓</span>
    </div>
    <div style='text-align:center; margin:0.5rem auto; max-width:200px;
         padding:1rem; background:rgba(16,185,129,0.1); border-radius:12px;
         border:1px solid #10b98144;'>
        <div style='font-size:1.8rem;'>📊</div>
        <div style='font-size:0.75rem; color:#10b981; font-weight:600;
             text-transform:uppercase; letter-spacing:1px;'>Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Feature highlights
    st.markdown("<div class='section-title'>✨ Platform Features</div>", unsafe_allow_html=True)

    feat_cols = st.columns(3)
    features = [
        ("🔄", "Automated ETL", "Extract → Validate → Clean → Transform → Load pipeline runs with one click."),
        ("📊", "Interactive Charts", "Plotly-powered charts with hover, zoom, and real-time filter support."),
        ("🧹", "Data Quality", "Automatic duplicate removal, null handling, and quality scoring."),
        ("🏪", "Multi-Store Insights", "Revenue analytics across cities, regions, and individual stores."),
        ("📦", "Product Intelligence", "Category analysis, top-sellers, and performance benchmarking."),
        ("⬇️", "Download Center", "Export cleaned data, reports, and SQLite database with one click."),
    ]

    for i, (icon, title, desc) in enumerate(features):
        with feat_cols[i % 3]:
            st.markdown(f"""
            <div class='kpi-card' style='text-align:left; margin-bottom:1rem;'>
                <div style='font-size:1.5rem; margin-bottom:0.5rem;'>{icon}</div>
                <div style='font-weight:700; color:#e2e8f0; font-size:0.95rem;'>{title}</div>
                <div style='color:#94a3b8; font-size:0.82rem; margin-top:0.3rem;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # CTA Buttons
    st.markdown("<div class='section-title'>🚀 Get Started</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🎯  Use Mock Data for Demo", use_container_width=True, type="primary"):
            st.session_state.use_mock = True
            st.session_state.page = "pipeline"
            st.rerun()
    with c2:
        if st.button("📤  Upload My CSV Files", use_container_width=True):
            st.session_state.use_mock = False
            st.session_state.page = "pipeline"
            st.rerun()

    # Tech stack badges
    st.markdown("""
    <div style='margin-top:2rem; text-align:center;'>
        <span style='background:rgba(99,102,241,0.2); color:#6366f1; padding:0.3rem 0.8rem;
              border-radius:20px; font-size:0.75rem; font-weight:600; margin:0.2rem; display:inline-block;'>Python</span>
        <span style='background:rgba(139,92,246,0.2); color:#8b5cf6; padding:0.3rem 0.8rem;
              border-radius:20px; font-size:0.75rem; font-weight:600; margin:0.2rem; display:inline-block;'>Pandas</span>
        <span style='background:rgba(236,72,153,0.2); color:#ec4899; padding:0.3rem 0.8rem;
              border-radius:20px; font-size:0.75rem; font-weight:600; margin:0.2rem; display:inline-block;'>NumPy</span>
        <span style='background:rgba(16,185,129,0.2); color:#10b981; padding:0.3rem 0.8rem;
              border-radius:20px; font-size:0.75rem; font-weight:600; margin:0.2rem; display:inline-block;'>SQLite</span>
        <span style='background:rgba(245,158,11,0.2); color:#f59e0b; padding:0.3rem 0.8rem;
              border-radius:20px; font-size:0.75rem; font-weight:600; margin:0.2rem; display:inline-block;'>SQLAlchemy</span>
        <span style='background:rgba(59,130,246,0.2); color:#3b82f6; padding:0.3rem 0.8rem;
              border-radius:20px; font-size:0.75rem; font-weight:600; margin:0.2rem; display:inline-block;'>Plotly</span>
        <span style='background:rgba(239,68,68,0.2); color:#ef4444; padding:0.3rem 0.8rem;
              border-radius:20px; font-size:0.75rem; font-weight:600; margin:0.2rem; display:inline-block;'>Streamlit</span>
    </div>
    """, unsafe_allow_html=True)
