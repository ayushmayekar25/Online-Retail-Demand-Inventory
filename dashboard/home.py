import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛍️ Retail Dashboard")

st.sidebar.caption(
    "Retail Demand Forecasting & Business Intelligence"
)

st.sidebar.divider()

st.sidebar.success(
    "🏠 You are currently on the Home page."
)


# ============================================================
# HERO SECTION
# ============================================================

st.title("🛍️ Retail Demand Forecasting")

st.subheader(
    "A centralized business intelligence dashboard "
    "for understanding retail sales performance, "
    "demand patterns, forecasting and inventory "
    "decision-making."
)

st.divider()


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.header("📈 Executive Overview")

st.subheader(
    "Welcome to the Retail Analytics Dashboard"
)

st.write(
    "This dashboard is designed to provide a clear "
    "and professional view of retail business "
    "performance. It combines sales analysis, "
    "demand forecasting and inventory intelligence "
    "into a single analytics platform."
)


# ============================================================
# PROJECT HIGHLIGHTS
# ============================================================

st.header("🚀 Project Highlights")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📊 Sales Analytics",
        "Available"
    )

    st.caption(
        "Monitor sales performance, revenue, "
        "transactions and sales trends."
    )


with col2:

    st.metric(
        "🔮 Demand Forecast",
        "ML Powered"
    )

    st.caption(
        "Analyze historical demand and "
        "predicted future demand."
    )


with col3:

    st.metric(
        "📦 Inventory",
        "Intelligent"
    )

    st.caption(
        "Monitor stock levels and "
        "inventory conditions."
    )


with col4:

    st.metric(
        "⚠️ Risk Analysis",
        "Automated"
    )

    st.caption(
        "Identify products with "
        "potential inventory risks."
    )


# ============================================================
# BUSINESS OBJECTIVE
# ============================================================

st.divider()

st.header("🎯 Business Objective")

st.subheader(
    "Turning Retail Data into Business Decisions"
)

st.write(
    "The objective of this project is to transform "
    "large-scale retail transaction data into "
    "meaningful business insights."
)

st.write(
    "The system helps decision-makers understand "
    "historical sales behaviour, identify demand "
    "patterns, forecast future demand and detect "
    "potential inventory risks."
)


# ============================================================
# BUSINESS OBJECTIVES
# ============================================================

objective_col1, objective_col2 = st.columns(2)


with objective_col1:

    st.write("📊 Analyze historical sales performance")

    st.write("📈 Identify sales and demand patterns")

    st.write("🔮 Forecast future demand")


with objective_col2:

    st.write("📦 Monitor inventory conditions")

    st.write("⚠️ Identify inventory risks")

    st.write("💡 Support data-driven decisions")


# ============================================================
# DASHBOARD MODULES
# ============================================================

st.divider()

st.header("📋 Dashboard Modules")


module1, module2, module3 = st.columns(3)


with module1:

    st.subheader("📊 Sales Analytics")

    st.write(
        "Explore sales trends, channels, "
        "stores and overall business performance."
    )


with module2:

    st.subheader("🔮 Demand Forecasting")

    st.write(
        "Analyze historical demand and "
        "machine-learning based forecasts."
    )


with module3:

    st.subheader("📦 Inventory Intelligence")

    st.write(
        "Understand inventory conditions "
        "and identify potential risks."
    )


# ============================================================
# ANALYTICS FLOW
# ============================================================

st.divider()

st.header("🔄 Analytics Flow")

st.info(
    "Sales Data → Sales Analytics → Demand Patterns "
    "→ Forecasting → Inventory Intelligence "
    "→ Business Decisions"
)


# ============================================================
# KEY FEATURES
# ============================================================

st.divider()

st.header("⭐ Key Features")


feature_col1, feature_col2 = st.columns(2)


with feature_col1:

    st.write("✅ Sales performance analysis")

    st.write("✅ Year-wise sales analysis")

    st.write("✅ Channel performance analysis")

    st.write("✅ Product-level analysis")

    st.write("✅ Customer and business insights")


with feature_col2:

    st.write("✅ Demand forecasting")

    st.write("✅ Actual vs predicted demand")

    st.write("✅ Inventory risk scoring")

    st.write("✅ Critical and high-risk identification")

    st.write("✅ Executive-level business summary")


# ============================================================
# HOW TO USE
# ============================================================

st.divider()

st.header("🧭 How to Use This Dashboard")

st.write(
    "Use the navigation menu to explore the different "
    "sections of the Retail Demand Forecasting project."
)


st.write(
    "📊 Sales Analytics — understand sales performance."
)

st.write(
    "🔮 Forecasting — analyze predicted demand."
)

st.write(
    "📦 Inventory — understand stock conditions."
)

st.write(
    "⚠️ Risk Analysis — identify inventory risks."
)

st.write(
    "📈 Executive Summary — view management-level insights."
)


# ============================================================
# PROJECT SUMMARY
# ============================================================

st.divider()

st.header("📌 Project Summary")

st.write(
    "The Retail Demand Forecasting project integrates "
    "data analytics and machine learning to help "
    "retailers understand business performance, "
    "anticipate demand and manage inventory more "
    "effectively."
)

st.write(
    "By combining historical sales data, demand "
    "forecasts and inventory risk analysis, the "
    "dashboard provides a unified platform for "
    "data-driven retail decision-making."
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting Dashboard | "
    "Data Science Project"
)