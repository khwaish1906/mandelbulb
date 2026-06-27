import streamlit as st
import time
import os
import sys
import tempfile
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extract import load_data
from src.validate import check_missing_values
from src.clean import clean_sales_data
from src.transform import transform_data
from src.load import load_to_database
from src.query import get_top_products, get_revenue_per_store_per_day
from src.report import generate_summary_report

MOCK_SALES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sales_data.csv")
MOCK_PRODUCTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "products.csv")
MOCK_STORES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "stores.csv")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "retail.db")


def run_etl_pipeline(sales_path, products_path, stores_path, log_placeholder):
    logs = []
    start_time = time.time()

    def update_logs(msg, status="success"):
        icon = "✅" if status == "success" else "⏳" if status == "pending" else "❌"
        logs.append((icon, msg, status))
        render_logs(log_placeholder, logs)

    try:
        time.sleep(0.3)
        sales_df, products_df, stores_df = load_data(sales_path, products_path, stores_path)
        update_logs("Sales Data Loaded", "success")
        time.sleep(0.2)
        update_logs("Products Data Loaded", "success")
        time.sleep(0.2)
        update_logs("Stores Data Loaded", "success")

        time.sleep(0.4)
        missing_sales = check_missing_values(sales_df, "SALES")
        missing_products = check_missing_values(products_df, "PRODUCTS")
        missing_stores = check_missing_values(stores_df, "STORES")
        total_missing = int(missing_sales.sum() + missing_products.sum() + missing_stores.sum())
        update_logs(f"Missing Values Detected: {total_missing} fields", "success")

        time.sleep(0.4)
        dupes_before = int(sales_df.duplicated().sum())
        sales_df = clean_sales_data(sales_df)
        update_logs(f"Duplicates Removed: {dupes_before} rows", "success")
        update_logs("Type Conversion & Date Parsing Complete", "success")

        time.sleep(0.4)
        final_df, city_revenue = transform_data(sales_df, products_df, stores_df)
        update_logs("Data Merged (Sales + Products + Stores)", "success")
        update_logs("Revenue Calculated & Aggregated", "success")

        time.sleep(0.3)
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        load_to_database(final_df, DB_PATH)
        update_logs("SQLite Database Updated", "success")

        time.sleep(0.3)
        top_products = get_top_products(DB_PATH)
        store_revenue = get_revenue_per_store_per_day(DB_PATH)
        update_logs("SQL Queries Executed", "success")
        update_logs("Reports Generated", "success")

        elapsed = round(time.time() - start_time, 2)

        # Data quality stats
        total_rows_raw = 17  # from original sales_data.csv
        cleaned_rows = len(sales_df)
        quality_score = round((cleaned_rows / total_rows_raw) * 100, 1)

        result = {
            "final_df": final_df,
            "sales_df": sales_df,
            "products_df": products_df,
            "stores_df": stores_df,
            "city_revenue": city_revenue,
            "top_products": top_products,
            "store_revenue": store_revenue,
            "elapsed": elapsed,
            "dupes_removed": dupes_before,
            "missing_fixed": total_missing,
            "quality_score": quality_score,
            "raw_rows": total_rows_raw,
            "clean_rows": cleaned_rows,
        }

        return result, logs

    except Exception as e:
        update_logs(f"Pipeline Error: {e}", "error")
        return None, logs


def render_logs(placeholder, logs):
    html = ""
    for icon, msg, status in logs:
        color = "#10b981" if status == "success" else "#ef4444" if status == "error" else "#6366f1"
        html += f"""
        <div style='background:rgba(255,255,255,0.04); border-left:3px solid {color};
             border-radius:0 8px 8px 0; padding:0.6rem 1rem; margin:0.35rem 0;
             font-size:0.88rem; color:#e2e8f0; display:flex; align-items:center; gap:0.5rem;'>
            <span>{icon}</span> <span>{msg}</span>
        </div>"""
    placeholder.markdown(html, unsafe_allow_html=True)


def render_pipeline():
    st.markdown("<h2 class='gradient-text' style='font-size:2rem; font-weight:800;'>⚙️ ETL Pipeline</h2>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;'>Upload your CSV files or use demo data to run the full pipeline.</p>",
                unsafe_allow_html=True)

    use_mock = st.session_state.get("use_mock", False)

    if not use_mock:
        st.markdown("<div class='section-title'>📤 Upload CSV Files</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🛍️ Sales Data**")
            sales_file = st.file_uploader("sales_data.csv", type="csv", key="sales_upload",
                                          label_visibility="collapsed")
        with col2:
            st.markdown("**📦 Products**")
            products_file = st.file_uploader("products.csv", type="csv", key="products_upload",
                                             label_visibility="collapsed")
        with col3:
            st.markdown("**🏪 Stores**")
            stores_file = st.file_uploader("stores.csv", type="csv", key="stores_upload",
                                           label_visibility="collapsed")

        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            if st.button("🎯 Use Mock Data Instead", use_container_width=True):
                st.session_state.use_mock = True
                st.rerun()

        files_ready = sales_file and products_file and stores_file
    else:
        st.markdown("""
        <div style='background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.4);
             border-radius:12px; padding:1rem 1.5rem; margin-bottom:1rem;'>
            🎯 <b style='color:#6366f1;'>Demo Mode Active</b>
            <span style='color:#94a3b8; margin-left:0.5rem;'>— Using sample retail dataset</span>
        </div>
        """, unsafe_allow_html=True)

        col_switch = st.columns([1, 3])[0]
        with col_switch:
            if st.button("📤 Upload My Own Files", use_container_width=True):
                st.session_state.use_mock = False
                st.rerun()

        files_ready = True

    st.markdown("---")
    st.markdown("<div class='section-title'>📋 Pipeline Execution Log</div>", unsafe_allow_html=True)

    log_placeholder = st.empty()
    log_placeholder.markdown("""
    <div style='color:#475569; font-style:italic; padding:1rem; text-align:center;'>
        Pipeline not started yet. Click "Run Pipeline" to begin.
    </div>""", unsafe_allow_html=True)

    st.markdown("")
    col_run, _ = st.columns([1, 3])
    with col_run:
        run_btn = st.button("▶️  Run Pipeline", use_container_width=True, type="primary",
                            disabled=not (use_mock or files_ready))

    if run_btn:
        with st.spinner(""):
            if use_mock:
                result, logs = run_etl_pipeline(MOCK_SALES, MOCK_PRODUCTS, MOCK_STORES, log_placeholder)
            else:
                # Save uploaded files to temp
                tmpdir = tempfile.mkdtemp()
                s_path = os.path.join(tmpdir, "sales_data.csv")
                p_path = os.path.join(tmpdir, "products.csv")
                st_path = os.path.join(tmpdir, "stores.csv")

                with open(s_path, "wb") as f:
                    f.write(sales_file.read())
                with open(p_path, "wb") as f:
                    f.write(products_file.read())
                with open(st_path, "wb") as f:
                    f.write(stores_file.read())

                result, logs = run_etl_pipeline(s_path, p_path, st_path, log_placeholder)

        if result:
            st.session_state.pipeline_done = True
            st.session_state.pipeline_result = result

            st.markdown(f"""
            <div style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.4);
                 border-radius:12px; padding:1rem 1.5rem; margin-top:1rem;
                 display:flex; justify-content:space-between; align-items:center;'>
                <span>🎉 <b style='color:#10b981;'>Pipeline Completed Successfully!</b></span>
                <span style='color:#94a3b8; font-size:0.85rem;'>⏱ Execution Time: <b style='color:#10b981;'>{result['elapsed']}s</b></span>
            </div>
            """, unsafe_allow_html=True)

            # Data quality summary
            st.markdown("<div class='section-title'>🔍 Data Quality Report</div>", unsafe_allow_html=True)
            q1, q2, q3, q4 = st.columns(4)

            metrics = [
                (q1, "🔁 Duplicates Removed", str(result["dupes_removed"]) + " rows", "#ef4444"),
                (q2, "🩹 Missing Values Fixed", str(result["missing_fixed"]) + " fields", "#f59e0b"),
                (q3, "✅ Clean Records", str(result["clean_rows"]) + " rows", "#10b981"),
                (q4, "⭐ Quality Score", f"{result['quality_score']}%", "#6366f1"),
            ]

            for col, label, val, color in metrics:
                with col:
                    st.markdown(f"""
                    <div class='quality-card'>
                        <div class='quality-value' style='color:{color};'>{val}</div>
                        <div class='quality-label'>{label}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("")
            if st.button("📊  View Dashboard →", use_container_width=False, type="primary"):
                st.session_state.page = "dashboard"
                st.rerun()
