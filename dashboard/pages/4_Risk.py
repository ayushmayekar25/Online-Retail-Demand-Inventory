from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Inventory Risk Analysis",
    page_icon="⚠️",
    layout="wide"
)


# ============================================================
# FILE PATH
# ============================================================

# Project structure:
#
# Online-retail-demand-forcasting-main
# │
# ├── dashboard
# │   ├── app.py
# │   └── pages
# │       └── 4_Risk.py
# │
# └── Datasets
#     └── inventory_risk_scoring (1).csv
#
# __file__ = dashboard/pages/4_Risk.py
# parents[2] = Online-retail-demand-forcasting-main

BASE_DIR = Path(__file__).resolve().parents[2]

RISK_FILE = BASE_DIR / "Datasets" / "inventory_risk_scoring (1).csv"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_risk_data():

    if not RISK_FILE.exists():
        return None

    return pd.read_csv(RISK_FILE)


risk_df = load_risk_data()


# ============================================================
# ERROR HANDLING
# ============================================================

if risk_df is None:

    st.error("⚠️ Inventory risk dataset could not be found.")

    st.write("Python is looking for the file at:")

    st.code(str(RISK_FILE))

    st.info(
        "Make sure that 'inventory_risk_scoring (1).csv' "
        "is inside the 'Datasets' folder."
    )

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("⚠️ Inventory Risk Analysis")

st.markdown(
    "Analyze inventory risk indicators and identify "
    "potential stock-related issues."
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.subheader("📌 Dataset Information")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    f"{len(risk_df):,}"
)

col2.metric(
    "Total Columns",
    f"{len(risk_df.columns):,}"
)

col3.metric(
    "Missing Values",
    f"{risk_df.isnull().sum().sum():,}"
)

numeric_columns = risk_df.select_dtypes(
    include="number"
).columns.tolist()

col4.metric(
    "Numeric Metrics",
    f"{len(numeric_columns):,}"
)


# ============================================================
# DATA PREVIEW
# ============================================================

with st.expander("👀 View Risk Dataset"):

    st.dataframe(
        risk_df,
        use_container_width=True
    )


# ============================================================
# NUMERIC COLUMNS
# ============================================================

numeric_columns = risk_df.select_dtypes(
    include="number"
).columns.tolist()


# ============================================================
# RISK METRIC ANALYSIS
# ============================================================

if numeric_columns:

    st.subheader("📊 Risk Metric Analysis")

    selected_metric = st.selectbox(
        "Select Risk Metric",
        numeric_columns
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # HISTOGRAM
    # --------------------------------------------------------

    with col1:

        fig_hist = px.histogram(
            risk_df,
            x=selected_metric,
            title=f"{selected_metric} Distribution",
            nbins=30
        )

        fig_hist.update_layout(
            xaxis_title=selected_metric,
            yaxis_title="Count"
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    # --------------------------------------------------------
    # BOX PLOT
    # --------------------------------------------------------

    with col2:

        fig_box = px.box(
            risk_df,
            y=selected_metric,
            title=f"{selected_metric} Risk Spread"
        )

        fig_box.update_layout(
            yaxis_title=selected_metric
        )

        st.plotly_chart(
            fig_box,
            use_container_width=True
        )


# ============================================================
# CATEGORICAL RISK ANALYSIS
# ============================================================

categorical_columns = risk_df.select_dtypes(
    exclude="number"
).columns.tolist()


if categorical_columns:

    st.subheader("🚨 Risk Categories")

    selected_category = st.selectbox(
        "Select Risk Category",
        categorical_columns
    )

    risk_counts = (
        risk_df[selected_category]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        selected_category,
        "Count"
    ]

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    with col1:

        fig_pie = px.pie(
            risk_counts,
            names=selected_category,
            values="Count",
            title=f"{selected_category} Distribution"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    with col2:

        fig_bar = px.bar(
            risk_counts,
            x=selected_category,
            y="Count",
            title=f"{selected_category} Count"
        )

        fig_bar.update_layout(
            xaxis_title=selected_category,
            yaxis_title="Count"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )


# ============================================================
# RISK SCORE SUMMARY
# ============================================================

if "risk_score" in risk_df.columns:

    st.subheader("🎯 Risk Score Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Risk Score",
        f"{risk_df['risk_score'].mean():.2f}"
    )

    col2.metric(
        "Highest Risk Score",
        f"{risk_df['risk_score'].max():.2f}"
    )

    col3.metric(
        "Lowest Risk Score",
        f"{risk_df['risk_score'].min():.2f}"
    )


# ============================================================
# RISK LEVEL SUMMARY
# ============================================================

if "risk_level" in risk_df.columns:

    st.subheader("🚨 Risk Level Summary")

    risk_level_counts = (
        risk_df["risk_level"]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    risk_level_counts.columns = [
        "Risk Level",
        "Count"
    ]

    st.dataframe(
        risk_level_counts,
        use_container_width=True
    )


# ============================================================
# DATASET TABLE
# ============================================================

st.subheader("📋 Complete Risk Dataset")

st.dataframe(
    risk_df,
    use_container_width=True
)