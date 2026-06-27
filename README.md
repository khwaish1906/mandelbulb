# 🛒 RetailMart Analytics Platform

> **Enterprise-grade Retail Data Engineering & Analytics Platform** — built with Python, Pandas, SQLite, and Streamlit.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-6.x-purple?style=flat-square&logo=plotly)](https://plotly.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=flat-square&logo=sqlite)](https://sqlite.org)

---

LIVE URL - https://mandelbulb-fsbmq28arbf52jdovtuwtt.streamlit.app/

## 📌 Overview

A complete **end-to-end Data Engineering project** that ingests raw retail CSV files, runs an automated ETL pipeline, stores data in a SQLite warehouse, and serves interactive analytics through a professional Streamlit dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔄 **Automated ETL** | Extract → Validate → Clean → Transform → Load in one click |
| 📊 **Interactive Dashboard** | 10+ Plotly charts with hover, zoom, and real-time filters |
| 🧹 **Data Quality** | Auto duplicate removal, null handling, and quality scoring |
| 🏙️ **Multi-dimensional Analytics** | Revenue by city, region, product, store, and time |
| 💡 **Auto Insights** | AI-generated business insights (top city, best product, growth trend) |
| ⬇️ **Download Center** | Export cleaned data, reports, and SQLite database |
| 🌙 **Dark Mode** | Professional dark glassmorphism UI |

---

## 🏗️ ETL Architecture

```
CSV Files (sales_data, products, stores)
        ↓
   📥 Extract         (src/extract.py)
        ↓
   ✅ Validate        (src/validate.py)
        ↓
   🧹 Clean           (src/clean.py)
        ↓
   🔄 Transform       (src/transform.py)
        ↓
   🗄️ Load → SQLite   (src/load.py)
        ↓
   📊 Analytics       (ui/dashboard.py)
```

---

## 📁 Project Structure

```
mandelbulb/
├── app.py                  # Streamlit entry point
├── config.py               # File paths & DB config
├── requirements.txt
│
├── data/                   # Sample CSV files
│   ├── sales_data.csv
│   ├── products.csv
│   └── stores.csv
│
├── src/                    # ETL modules
│   ├── extract.py
│   ├── validate.py
│   ├── clean.py
│   ├── transform.py
│   ├── load.py
│   ├── query.py
│   └── report.py
│
└── ui/                     # Streamlit frontend
    ├── styles.py           # Global CSS (dark theme)
    ├── landing.py          # Landing page
    ├── pipeline.py         # ETL pipeline page
    └── dashboard.py        # Analytics dashboard
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/khwaish1906/mandelbulb.git
cd mandelbulb/mandelbulb
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 📊 Dashboard Tabs

| Tab | Contents |
|---|---|
| 🏠 **Overview** | KPI cards, Revenue by City, Daily Trend, Region Pie |
| 📦 **Products** | Best sellers, Category analysis, Qty vs Revenue scatter |
| 🏪 **Stores** | Store performance, Regional funnel, Daily store trend |
| 💡 **Insights** | Auto-generated business insights + Revenue heatmap |
| 🗃️ **Raw Data** | Filtered table + Download Center |

---

## 🧰 Tech Stack

- **Python** — Core language
- **Pandas** — Data manipulation
- **NumPy** — Numerical operations
- **SQLite + SQLAlchemy** — Data warehouse
- **Plotly** — Interactive charts
- **Streamlit** — Web framework

---

## 📸 Screenshots

> Landing page → Pipeline logs → Analytics Dashboard

---

## 👤 Author

**Khwaish** — Data Engineering Project

---

## 📄 License

MIT License
