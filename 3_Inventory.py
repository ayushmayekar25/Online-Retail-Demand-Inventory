from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Inventory Intelligence",
    page_icon="📦",
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
# │       └── 1_Inventory.py
# │
# └── Datasets
#     └── inventory_risk_scoring (1).csv
#
# __file__ points to:
# dashboard/pages/1_Inventory.py
#
# parents[2] points to:
# Online-retail-demand-forcasting-main

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "Datasets"
    / "inventory_risk_scoring (1).csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_inventory_data():

    if not DATA_PATH.exists():
        return None

    return pd.read_csv(DATA_PATH)


inventory_df = load_inventory_data()


# ============================================================
# ERROR HANDLING
# ============================================================

if inventory_df is None:

    st.error("❌ Inventory dataset could not be found.")

    st.write("Python is looking for the file at:")

    st.code(str(DATA_PATH))

    st.info(
        "Make sure that 'inventory_risk_scoring (1).csv' "
        "is inside the 'Datasets' folder."
    )

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("📦 Inventory Intelligence")

st.markdown(
    "Monitor inventory levels, stock distribution "
    "and inventory risk."
)


# ============================================================
# DATA PREVIEW
# ============================================================

with st.expander("👀 View Inventory Dataset"):

    st.dataframe(
        inventory_df,
        use_container_width=True
    )


# ============================================================
# NUMERIC COLUMNS
# ============================================================

numeric_columns = inventory_df.select_dtypes(
    include="number"
).columns.tolist()


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Inventory Overview")

col1, col2, col3, col4 = st.columns(4)


# Total Records

col1.metric(
    "Total Records",
    f"{len(inventory_df):,}"
)


# Numeric metric calculations

if numeric_columns:

    first_numeric = numeric_columns[0]

    col2.metric(
        f"Total {first_numeric}",
        f"{inventory_df[first_numeric].sum():,.0f}"
    )

    col3.metric(
        f"Average {first_numeric}",
        f"{inventory_df[first_numeric].mean():,.2f}"
    )

    col4.metric(
        f"Maximum {first_numeric}",
        f"{inventory_df[first_numeric].max():,.0f}"
    )

else:

    col2.metric(
        "Numeric Columns",
        "0"
    )

    col3.metric(
        "Total Columns",
        f"{len(inventory_df.columns):,}"
    )

    col4.metric(
        "Total Rows",
        f"{len(inventory_df):,}"
    )


# ============================================================
# NUMERIC VISUALIZATION
# ============================================================

if numeric_columns:

    st.subheader("📈 Inventory Metric Analysis")

    selected_column = st.selectbox(
        "Select Inventory Metric",
        numeric_columns
    )

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # HISTOGRAM
    # --------------------------------------------------------

    with col1:

        fig_hist = px.histogram(
            inventory_df,
            x=selected_column,
            title=f"Distribution of {selected_column}",
            nbins=30
        )

        fig_hist.update_layout(
            xaxis_title=selected_column,
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
            inventory_df,
            y=selected_column,
            title=f"{selected_column} Spread"
        )

        fig_box.update_layout(
            yaxis_title=selected_column
        )

        st.plotly_chart(
            fig_box,
            use_container_width=True
        )


# ============================================================
# CATEGORY VISUALIZATION
# ============================================================

categorical_columns = inventory_df.select_dtypes(
    exclude="number"
).columns.tolist()


if categorical_columns:

    st.subheader("📊 Inventory Category Analysis")

    selected_category = st.selectbox(
        "Select Category",
        categorical_columns
    )

    category_counts = (
        inventory_df[selected_category]
        .astype(str)
        .value_counts()
        .head(15)
        .reset_index()
    )

    category_counts.columns = [
        selected_category,
        "Count"
    ]

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    with col1:

        fig_bar = px.bar(
            category_counts,
            x=selected_category,
            y="Count",
            title=f"{selected_category} Distribution"
        )

        fig_bar.update_layout(
            xaxis_title=selected_category,
            yaxis_title="Count"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )


    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    with col2:

        fig_pie = px.pie(
            category_counts,
            names=selected_category,
            values="Count",
            title=f"{selected_category} Share"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


# ============================================================
# INVENTORY RISK ANALYSIS
# ============================================================

if "risk_level" in inventory_df.columns:

    st.subheader("⚠️ Inventory Risk Levels")

    risk_counts = (
        inventory_df["risk_level"]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk Level",
        "Count"
    ]

    st.dataframe(
        risk_counts,
        use_container_width=True
    )

    fig_risk = px.bar(
        risk_counts,
        x="Risk Level",
        y="Count",
        title="Inventory Risk Level Distribution"
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )


# ============================================================
# RISK SCORE ANALYSIS
# ============================================================

if "risk_score" in inventory_df.columns:

    st.subheader("🎯 Risk Score Analysis")

    risk_score_col1, risk_score_col2, risk_score_col3 = st.columns(3)

    risk_score_col1.metric(
        "Average Risk Score",
        f"{inventory_df['risk_score'].mean():.2f}"
    )

    risk_score_col2.metric(
        "Highest Risk Score",
        f"{inventory_df['risk_score'].max():.2f}"
    )

    risk_score_col3.metric(
        "Lowest Risk Score",
        f"{inventory_df['risk_score'].min():.2f}"
    )


# ============================================================
# STOCK COVERAGE ANALYSIS
# ============================================================

if "stock_coverage_days" in inventory_df.columns:

    st.subheader("📦 Stock Coverage Analysis")

    coverage_col1, coverage_col2, coverage_col3 = st.columns(3)

    coverage_col1.metric(
        "Average Coverage",
        f"{inventory_df['stock_coverage_days'].mean():.2f} days"
    )

    coverage_col2.metric(
        "Minimum Coverage",
        f"{inventory_df['stock_coverage_days'].min():.2f} days"
    )

    coverage_col3.metric(
        "Maximum Coverage",
        f"{inventory_df['stock_coverage_days'].max():.2f} days"
    )

    fig_coverage = px.histogram(
        inventory_df,
        x="stock_coverage_days",
        title="Stock Coverage Days Distribution",
        nbins=30
    )

    fig_coverage.update_layout(
        xaxis_title="Stock Coverage Days",
        yaxis_title="Number of Records"
    )

    st.plotly_chart(
        fig_coverage,
        use_container_width=True
    )


# ============================================================
# DATASET INFORMATION
# ============================================================

st.subheader("📋 Dataset Information")

info_col1, info_col2 = st.columns(2)


with info_col1:

    st.write(
        "**Number of rows:**",
        len(inventory_df)
    )

    st.write(
        "**Number of columns:**",
        len(inventory_df.columns)
    )


with info_col2:

    st.write(
        "**Missing values:**",
        int(inventory_df.isnull().sum().sum())
    )

    st.write(
        "**Numeric columns:**",
        len(numeric_columns)
    )


# ============================================================
# COMPLETE DATASET
# ============================================================

st.subheader("📋 Complete Inventory Dataset")

st.dataframe(
    inventory_df,
    use_container_width=True
)