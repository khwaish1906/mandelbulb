import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import os

PLOTLY_THEME = "plotly_dark"
PRIMARY = "#6366f1"
SECONDARY = "#8b5cf6"
SUCCESS = "#10b981"
WARNING = "#f59e0b"
DANGER = "#ef4444"
PINK = "#ec4899"
BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(15,12,41,0.0)"

CHART_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=BG,
    font=dict(family="Inter", color="#e2e8f0"),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
)


def styled_chart(fig):
    fig.update_layout(**CHART_LAYOUT)
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                     tickfont=dict(color="#94a3b8"))
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                     tickfont=dict(color="#94a3b8"))
    return fig


def kpi_card(icon, label, value, sub=""):
    return f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>{icon}</div>
        <div class='kpi-value'>{value}</div>
        <div class='kpi-label'>{label}</div>
        {"<div style='font-size:0.7rem;color:#64748b;margin-top:0.2rem;'>" + sub + "</div>" if sub else ""}
    </div>
    """


def render_dashboard():
    result = st.session_state.pipeline_result
    final_df = result["final_df"].copy()
    products_df = result["products_df"].copy()
    stores_df = result["stores_df"].copy()
    top_products = result["top_products"]
    store_revenue = result["store_revenue"]

    # Ensure sale_date is datetime
    final_df["sale_date"] = pd.to_datetime(final_df["sale_date"])

    # ─── Sidebar Filters ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<div style='color:#6366f1; font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; margin-top:1rem;'>🎛 Filters</div>", unsafe_allow_html=True)

        cities = ["All"] + sorted(final_df["city"].dropna().unique().tolist())
        sel_city = st.selectbox("🏙️ City", cities)

        regions = ["All"] + sorted(final_df["region"].dropna().unique().tolist())
        sel_region = st.selectbox("🗺️ Region", regions)

        products = ["All"] + sorted(final_df["product_name"].dropna().unique().tolist())
        sel_product = st.selectbox("📦 Product", products)

        min_date = final_df["sale_date"].min().date()
        max_date = final_df["sale_date"].max().date()
        date_range = st.date_input("📅 Date Range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)

        rev_min = float(final_df["total_revenue"].min())
        rev_max = float(final_df["total_revenue"].max())
        rev_range = st.slider("💰 Revenue Range", rev_min, rev_max,
                              (rev_min, rev_max), step=500.0)

    # Apply filters
    df = final_df.copy()
    if sel_city != "All":
        df = df[df["city"] == sel_city]
    if sel_region != "All":
        df = df[df["region"] == sel_region]
    if sel_product != "All":
        df = df[df["product_name"] == sel_product]
    if len(date_range) == 2:
        df = df[(df["sale_date"].dt.date >= date_range[0]) & (df["sale_date"].dt.date <= date_range[1])]
    df = df[(df["total_revenue"] >= rev_range[0]) & (df["total_revenue"] <= rev_range[1])]

    # ─── Header ───────────────────────────────────────────────────────
    st.markdown("""
    <h2 class='gradient-text' style='font-size:2rem; font-weight:800;'>📊 Analytics Dashboard</h2>
    <p style='color:#94a3b8; margin-top:-0.5rem;'>Live business intelligence powered by your retail data.</p>
    """, unsafe_allow_html=True)

    # ─── TABS ─────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🏠 Overview", "📦 Products", "🏪 Stores", "💡 Insights", "🗃️ Raw Data"]
    )

    # ════════════════════════════════════════════════
    # TAB 1 — Overview
    # ════════════════════════════════════════════════
    with tab1:
        st.markdown("<div class='section-title'>📈 Key Performance Indicators</div>", unsafe_allow_html=True)

        total_rev = df["total_revenue"].sum()
        avg_rev = df["total_revenue"].mean()
        city_rev = df.groupby("city")["total_revenue"].sum()
        top_city = city_rev.idxmax() if not city_rev.empty else "N/A"
        top_city_val = city_rev.max() if not city_rev.empty else 0

        kpis = [
            ("🧾", "Total Transactions", f"{len(df):,}"),
            ("💰", "Total Revenue", f"₹{total_rev:,.0f}"),
            ("🏙️", "Cities Covered", f"{df['city'].nunique()}"),
            ("📦", "Unique Products", f"{df['product_name'].nunique()}"),
            ("📊", "Avg Revenue/Sale", f"₹{avg_rev:,.0f}"),
            ("🏆", "Top Revenue City", top_city),
        ]

        cols = st.columns(3)
        for i, (icon, label, val) in enumerate(kpis):
            with cols[i % 3]:
                st.markdown(kpi_card(icon, label, val), unsafe_allow_html=True)
                st.markdown("")

        st.markdown("<div class='section-title'>📊 Revenue by City</div>", unsafe_allow_html=True)
        city_df = df.groupby("city")["total_revenue"].sum().reset_index().sort_values("total_revenue", ascending=False)
        fig1 = px.bar(city_df, x="city", y="total_revenue", color="total_revenue",
                      color_continuous_scale=[[0, "#6366f1"], [0.5, "#8b5cf6"], [1, "#ec4899"]],
                      labels={"total_revenue": "Revenue (₹)", "city": "City"}, title="Revenue by City")
        fig1 = styled_chart(fig1)
        fig1.update_coloraxes(showscale=False)
        st.plotly_chart(fig1, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='section-title'>📈 Revenue Trend</div>", unsafe_allow_html=True)
            trend_df = df.groupby(df["sale_date"].dt.date)["total_revenue"].sum().reset_index()
            trend_df.columns = ["date", "revenue"]
            fig2 = px.line(trend_df, x="date", y="revenue", markers=True,
                           title="Daily Revenue Trend",
                           labels={"revenue": "Revenue (₹)", "date": "Date"})
            fig2.update_traces(line=dict(color=PRIMARY, width=3), marker=dict(color=SECONDARY, size=8))
            fig2 = styled_chart(fig2)
            st.plotly_chart(fig2, use_container_width=True)

        with c2:
            st.markdown("<div class='section-title'>🥧 Revenue by Region</div>", unsafe_allow_html=True)
            region_df = df.groupby("region")["total_revenue"].sum().reset_index()
            fig3 = px.pie(region_df, names="region", values="total_revenue",
                          title="Revenue Share by Region",
                          color_discrete_sequence=[PRIMARY, SECONDARY, PINK, WARNING, SUCCESS])
            fig3.update_traces(textposition="inside", textinfo="percent+label",
                               hole=0.4, marker=dict(line=dict(color="rgba(0,0,0,0.3)", width=2)))
            fig3 = styled_chart(fig3)
            st.plotly_chart(fig3, use_container_width=True)

    # ════════════════════════════════════════════════
    # TAB 2 — Products
    # ════════════════════════════════════════════════
    with tab2:
        st.markdown("<div class='section-title'>🏆 Best Selling Products</div>", unsafe_allow_html=True)

        prod_df = df.groupby("product_name").agg(
            total_qty=("quantity", "sum"),
            total_rev=("total_revenue", "sum")
        ).reset_index().sort_values("total_rev", ascending=False)

        fig4 = px.bar(prod_df, x="total_rev", y="product_name", orientation="h",
                      color="total_rev",
                      color_continuous_scale=[[0, "#6366f1"], [1, "#ec4899"]],
                      labels={"total_rev": "Revenue (₹)", "product_name": "Product"},
                      title="Product Revenue Ranking")
        fig4 = styled_chart(fig4)
        fig4.update_coloraxes(showscale=False)
        fig4.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig4, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='section-title'>📂 Category Analysis</div>", unsafe_allow_html=True)
            cat_df = df.groupby("category")["total_revenue"].sum().reset_index()
            fig5 = px.pie(cat_df, names="category", values="total_revenue",
                          title="Revenue by Category",
                          color_discrete_sequence=[PRIMARY, SECONDARY, PINK, WARNING, SUCCESS, DANGER])
            fig5.update_traces(hole=0.35, textinfo="percent+label",
                               marker=dict(line=dict(color="rgba(0,0,0,0.3)", width=2)))
            fig5 = styled_chart(fig5)
            st.plotly_chart(fig5, use_container_width=True)

        with c2:
            st.markdown("<div class='section-title'>📦 Quantity vs Revenue</div>", unsafe_allow_html=True)
            fig6 = px.scatter(prod_df, x="total_qty", y="total_rev", text="product_name",
                              size="total_rev", color="total_rev",
                              color_continuous_scale=[[0, "#6366f1"], [1, "#ec4899"]],
                              title="Quantity vs Revenue (bubble = revenue)",
                              labels={"total_qty": "Total Quantity", "total_rev": "Revenue (₹)"})
            fig6.update_traces(textposition="top center")
            fig6 = styled_chart(fig6)
            fig6.update_coloraxes(showscale=False)
            st.plotly_chart(fig6, use_container_width=True)

        st.markdown("<div class='section-title'>📋 Product Performance Table</div>", unsafe_allow_html=True)
        display_prod = prod_df.copy()
        display_prod.columns = ["Product", "Total Quantity", "Total Revenue (₹)"]
        display_prod["Total Revenue (₹)"] = display_prod["Total Revenue (₹)"].map("₹{:,.0f}".format)
        st.dataframe(display_prod, use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════
    # TAB 3 — Stores
    # ════════════════════════════════════════════════
    with tab3:
        st.markdown("<div class='section-title'>🏪 Store Performance</div>", unsafe_allow_html=True)

        store_df = df.groupby(["store_name", "city", "region"])["total_revenue"].sum().reset_index()
        store_df = store_df.sort_values("total_revenue", ascending=False)

        fig7 = px.bar(store_df, x="store_name", y="total_revenue", color="region",
                      color_discrete_sequence=[PRIMARY, SECONDARY, PINK, WARNING, SUCCESS],
                      title="Revenue by Store",
                      labels={"total_revenue": "Revenue (₹)", "store_name": "Store"})
        fig7 = styled_chart(fig7)
        st.plotly_chart(fig7, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='section-title'>🗺️ Revenue by Region</div>", unsafe_allow_html=True)
            reg_df = df.groupby("region")["total_revenue"].sum().reset_index()
            fig8 = px.funnel(reg_df, x="total_revenue", y="region",
                             title="Regional Revenue Funnel",
                             labels={"total_revenue": "Revenue (₹)", "region": "Region"})
            fig8 = styled_chart(fig8)
            st.plotly_chart(fig8, use_container_width=True)

        with c2:
            st.markdown("<div class='section-title'>📅 Store Revenue per Day</div>", unsafe_allow_html=True)
            if not store_revenue.empty:
                store_revenue["sale_date"] = pd.to_datetime(store_revenue["sale_date"])
                fig9 = px.line(store_revenue, x="sale_date", y="revenue",
                               color="store_name", markers=True,
                               title="Daily Revenue per Store",
                               labels={"revenue": "Revenue (₹)", "sale_date": "Date"})
                fig9 = styled_chart(fig9)
                st.plotly_chart(fig9, use_container_width=True)

        st.markdown("<div class='section-title'>📋 Store Summary Table</div>", unsafe_allow_html=True)
        disp_store = store_df.copy()
        disp_store.columns = ["Store", "City", "Region", "Total Revenue (₹)"]
        disp_store["Total Revenue (₹)"] = disp_store["Total Revenue (₹)"].map("₹{:,.0f}".format)
        st.dataframe(disp_store, use_container_width=True, hide_index=True)

    # ════════════════════════════════════════════════
    # TAB 4 — Insights
    # ════════════════════════════════════════════════
    with tab4:
        st.markdown("<div class='section-title'>💡 Automated Business Insights</div>", unsafe_allow_html=True)

        city_rev = df.groupby("city")["total_revenue"].sum()
        prod_rev = df.groupby("product_name")["total_revenue"].sum()
        prod_qty = df.groupby("product_name")["quantity"].sum()
        store_rev_tab = df.groupby("store_name")["total_revenue"].sum()
        cat_rev = df.groupby("category")["total_revenue"].sum()
        trend = df.groupby(df["sale_date"].dt.date)["total_revenue"].sum()

        insights = []
        if not city_rev.empty:
            insights.append(("🏆", "Top Revenue City", city_rev.idxmax(),
                             f"₹{city_rev.max():,.0f} total revenue"))
        if not prod_qty.empty:
            insights.append(("🛍️", "Best Selling Product", prod_qty.idxmax(),
                             f"{prod_qty.max():,} units sold"))
        if not store_rev_tab.empty:
            insights.append(("🏪", "Highest Revenue Store", store_rev_tab.idxmax(),
                             f"₹{store_rev_tab.max():,.0f} earned"))
        if not cat_rev.empty:
            insights.append(("💹", "Most Profitable Category", cat_rev.idxmax(),
                             f"₹{cat_rev.max():,.0f} revenue"))
        if not prod_rev.empty:
            insights.append(("💎", "Highest Value Product", prod_rev.idxmax(),
                             f"₹{prod_rev.max():,.0f} revenue"))
        if len(trend) >= 2:
            trend_vals = trend.values
            growth = ((trend_vals[-1] - trend_vals[0]) / trend_vals[0]) * 100 if trend_vals[0] else 0
            dir_icon = "📈" if growth >= 0 else "📉"
            insights.append((dir_icon, "Revenue Growth Trend",
                             f"{'+' if growth >= 0 else ''}{growth:.1f}%",
                             "from first to last recorded day"))

        for icon, title, value, sub in insights:
            st.markdown(f"""
            <div class='insight-card'>
                <div class='insight-icon'>{icon}</div>
                <div>
                    <div class='insight-title'>{title}</div>
                    <div class='insight-value'>{value}</div>
                    <div style='font-size:0.75rem; color:#64748b;'>{sub}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Heatmap - product × city revenue
        st.markdown("<div class='section-title'>🔥 Revenue Heatmap (Product × City)</div>", unsafe_allow_html=True)
        if "city" in df.columns and "product_name" in df.columns:
            heat_df = df.groupby(["product_name", "city"])["total_revenue"].sum().reset_index()
            heat_pivot = heat_df.pivot(index="product_name", columns="city", values="total_revenue").fillna(0)
            fig10 = go.Figure(data=go.Heatmap(
                z=heat_pivot.values,
                x=heat_pivot.columns.tolist(),
                y=heat_pivot.index.tolist(),
                colorscale=[[0, "#0f0c29"], [0.5, "#6366f1"], [1, "#ec4899"]],
                hoverongaps=False,
                text=[[f"₹{v:,.0f}" for v in row] for row in heat_pivot.values],
                texttemplate="%{text}",
                textfont={"size": 10}
            ))
            fig10.update_layout(title="Revenue Heatmap", **CHART_LAYOUT)
            st.plotly_chart(fig10, use_container_width=True)

    # ════════════════════════════════════════════════
    # TAB 5 — Raw Data
    # ════════════════════════════════════════════════
    with tab5:
        st.markdown("<div class='section-title'>🗃️ Filtered Dataset</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#94a3b8;'>Showing <b style='color:#6366f1;'>{len(df):,}</b> records after filters.</p>",
                    unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("<div class='section-title'>⬇️ Download Center</div>", unsafe_allow_html=True)
        dl1, dl2, dl3, dl4 = st.columns(4)

        # Cleaned CSV
        with dl1:
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Cleaned Dataset", data=csv_data,
                               file_name="cleaned_retail_data.csv", mime="text/csv",
                               use_container_width=True)

        # Revenue report
        with dl2:
            rev_report = df.groupby("city")["total_revenue"].sum().reset_index()
            rev_csv = rev_report.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Revenue Report", data=rev_csv,
                               file_name="revenue_report.csv", mime="text/csv",
                               use_container_width=True)

        # Product report
        with dl3:
            prod_report = df.groupby("product_name").agg(
                qty=("quantity", "sum"), rev=("total_revenue", "sum")
            ).reset_index()
            prod_csv = prod_report.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Product Report", data=prod_csv,
                               file_name="product_report.csv", mime="text/csv",
                               use_container_width=True)

        # SQLite DB
        with dl4:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                   "database", "retail.db")
            if os.path.exists(db_path):
                with open(db_path, "rb") as f:
                    db_bytes = f.read()
                st.download_button("📥 SQLite Database", data=db_bytes,
                                   file_name="retail.db", mime="application/octet-stream",
                                   use_container_width=True)
            else:
                st.button("📥 SQLite Database", disabled=True, use_container_width=True)

        # Products & Stores raw tables
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='section-title'>📦 Products Master</div>", unsafe_allow_html=True)
            st.dataframe(result["products_df"], use_container_width=True, hide_index=True)
        with c2:
            st.markdown("<div class='section-title'>🏪 Stores Master</div>", unsafe_allow_html=True)
            st.dataframe(result["stores_df"], use_container_width=True, hide_index=True)
