from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Product Details",
    page_icon="🛍️",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

# Project structure:
#
# Online-retail-demand-forcasting-main
# │
# ├── dashboard
# │   ├── app.py
# │   └── pages
# │       └── 2_Product_Details.py
# │
# └── Datasets
#     ├── sales_transactions_cleaned.csv
#     └── inventory_risk_scoring (1).csv
#
# __file__ = dashboard/pages/2_Product_Details.py
# parents[2] = Online-retail-demand-forcasting-main

BASE_DIR = Path(__file__).resolve().parents[2]


# ============================================================
# DATASET PATHS
# ============================================================

# Exact sales dataset
SALES_PATH = (
    BASE_DIR
    / "Datasets"
    / "sales_transactions_cleaned.csv"
)

# Exact inventory dataset
INVENTORY_PATH = (
    BASE_DIR
    / "Datasets"
    / "inventory_risk_scoring (1).csv"
)


# ============================================================
# LOAD SALES DATA
# ============================================================

@st.cache_data
def load_sales_data():

    if not SALES_PATH.exists():
        return None

    try:
        return pd.read_csv(SALES_PATH)

    except Exception as e:
        st.error(f"Error loading sales dataset: {e}")
        return None


# ============================================================
# LOAD INVENTORY DATA
# ============================================================

@st.cache_data
def load_inventory_data():

    if not INVENTORY_PATH.exists():
        return None

    try:
        return pd.read_csv(INVENTORY_PATH)

    except Exception as e:
        st.warning(
            f"Inventory dataset could not be loaded: {e}"
        )
        return None


# Load both datasets
sales_df = load_sales_data()
inventory_df = load_inventory_data()


# ============================================================
# SALES DATA CHECK
# ============================================================

if sales_df is None:

    st.error("❌ Sales dataset could not be found.")

    st.write("Python is looking for the sales file at:")

    st.code(str(SALES_PATH))

    st.info(
        "Make sure that 'sales_transactions_cleaned.csv' "
        "is inside the 'Datasets' folder."
    )

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🛍️ Product Details")

st.caption(
    "Analyze individual product performance, sales activity "
    "and inventory position."
)

st.divider()


# ============================================================
# DATASET INFORMATION
# ============================================================

with st.expander("📁 Dataset Information"):

    st.write("**Sales dataset:**")

    st.code(str(SALES_PATH))

    st.write("**Inventory dataset:**")

    st.code(str(INVENTORY_PATH))

    st.write(
        "**Sales records:**",
        f"{len(sales_df):,}"
    )

    st.write(
        "**Sales columns:**",
        len(sales_df.columns)
    )


# ============================================================
# DATA PREPARATION
# ============================================================

# Convert date
if "date" in sales_df.columns:

    sales_df["date"] = pd.to_datetime(
        sales_df["date"],
        errors="coerce"
    )


# Convert total value
if "total_value" in sales_df.columns:

    sales_df["total_value"] = pd.to_numeric(
        sales_df["total_value"],
        errors="coerce"
    ).fillna(0)


# Convert quantity
if "quantity" in sales_df.columns:

    sales_df["quantity"] = pd.to_numeric(
        sales_df["quantity"],
        errors="coerce"
    ).fillna(0)


# Convert unit price
if "unit_price" in sales_df.columns:

    sales_df["unit_price"] = pd.to_numeric(
        sales_df["unit_price"],
        errors="coerce"
    ).fillna(0)


# ============================================================
# SALES DATA PREVIEW
# ============================================================

with st.expander("👀 View Sales Dataset"):

    st.dataframe(
        sales_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PRODUCT SELECTION
# ============================================================

st.header("🔎 Select Product")


# Check SKU column
if "sku_id" not in sales_df.columns:

    st.error(
        "❌ 'sku_id' column is not available "
        "in the sales dataset."
    )

    st.write("Available columns:")

    st.write(
        sales_df.columns.tolist()
    )

    st.stop()


# Get products
products = sorted(
    sales_df["sku_id"]
    .dropna()
    .astype(str)
    .unique()
)


if not products:

    st.error(
        "❌ No SKU/product values were found "
        "in the sales dataset."
    )

    st.stop()


# Product dropdown
selected_product = st.selectbox(
    "Choose a SKU",
    products
)


# ============================================================
# FILTER SELECTED PRODUCT
# ============================================================

product_sales = sales_df[
    sales_df["sku_id"].astype(str)
    == selected_product
].copy()


if product_sales.empty:

    st.warning(
        "No sales data available for this product."
    )

    st.stop()


# ============================================================
# PRODUCT KPIs
# ============================================================

total_sales = (
    product_sales["total_value"].sum()
    if "total_value" in product_sales.columns
    else 0
)


total_quantity = (
    product_sales["quantity"].sum()
    if "quantity" in product_sales.columns
    else 0
)


transactions = (
    product_sales["receipt_id"].nunique()
    if "receipt_id" in product_sales.columns
    else len(product_sales)
)


stores = (
    product_sales["store_id"].nunique()
    if "store_id" in product_sales.columns
    else 0
)


average_price = (
    total_sales / total_quantity
    if total_quantity > 0
    else 0
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Product Performance")


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


kpi1.metric(
    "Total Sales",
    f"₹{total_sales:,.0f}"
)


kpi2.metric(
    "Quantity Sold",
    f"{total_quantity:,.0f}"
)


kpi3.metric(
    "Transactions",
    f"{transactions:,}"
)


kpi4.metric(
    "Stores",
    f"{stores:,}"
)


kpi5.metric(
    "Average Price",
    f"₹{average_price:,.2f}"
)


# ============================================================
# PRODUCT INFORMATION
# ============================================================

st.divider()

st.header("ℹ️ Product Information")


info1, info2, info3 = st.columns(3)


# SKU
info1.metric(
    "SKU",
    selected_product
)


# Sales channels
if "channel" in product_sales.columns:

    channel_count = (
        product_sales["channel"].nunique()
    )

else:

    channel_count = 0


info2.metric(
    "Sales Channels",
    f"{channel_count:,}"
)


# First sales date
if "date" in product_sales.columns:

    first_date = product_sales["date"].min()

    if pd.notna(first_date):

        date_range = f"{first_date:%d %b %Y}"

    else:

        date_range = "N/A"

else:

    date_range = "N/A"


info3.metric(
    "First Sales Date",
    date_range
)


# ============================================================
# SALES TREND
# ============================================================

st.divider()

st.header("📈 Product Sales Trend")


if (
    "date" in product_sales.columns
    and "total_value" in product_sales.columns
):

    daily_sales = (
        product_sales
        .dropna(subset=["date"])
        .groupby("date")["total_value"]
        .sum()
        .reset_index()
        .sort_values("date")
    )


    if not daily_sales.empty:

        fig_sales = px.line(
            daily_sales,
            x="date",
            y="total_value",
            title=f"Daily Sales — {selected_product}"
        )


        fig_sales.update_layout(
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Sales (₹)",
            height=450
        )


        st.plotly_chart(
            fig_sales,
            use_container_width=True
        )

    else:

        st.info(
            "No valid date records are available "
            "for this product."
        )

else:

    st.info(
        "Sales trend cannot be displayed because "
        "date or total_value is unavailable."
    )


# ============================================================
# QUANTITY TREND
# ============================================================

st.header("📦 Product Quantity Trend")


if (
    "date" in product_sales.columns
    and "quantity" in product_sales.columns
):

    daily_quantity = (
        product_sales
        .dropna(subset=["date"])
        .groupby("date")["quantity"]
        .sum()
        .reset_index()
        .sort_values("date")
    )


    if not daily_quantity.empty:

        fig_quantity = px.line(
            daily_quantity,
            x="date",
            y="quantity",
            title=f"Daily Quantity Sold — {selected_product}"
        )


        fig_quantity.update_layout(
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Quantity",
            height=450
        )


        st.plotly_chart(
            fig_quantity,
            use_container_width=True
        )

    else:

        st.info(
            "No valid dates are available "
            "for the quantity trend."
        )

else:

    st.info(
        "Quantity trend cannot be displayed because "
        "date or quantity is unavailable."
    )


# ============================================================
# SALES BY CHANNEL
# ============================================================

if (
    "channel" in product_sales.columns
    and "total_value" in product_sales.columns
):

    st.divider()

    st.header("📊 Sales by Channel")


    channel_sales = (
        product_sales
        .groupby("channel")["total_value"]
        .sum()
        .reset_index()
        .sort_values(
            "total_value",
            ascending=False
        )
    )


    channel_left, channel_right = st.columns(2)


    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    with channel_left:

        fig_channel = px.bar(
            channel_sales,
            x="channel",
            y="total_value",
            text="total_value",
            title="Sales by Channel"
        )


        fig_channel.update_traces(
            texttemplate="₹%{y:,.0f}",
            textposition="outside"
        )


        fig_channel.update_layout(
            template="plotly_white",
            xaxis_title="Channel",
            yaxis_title="Sales (₹)",
            height=430
        )


        st.plotly_chart(
            fig_channel,
            use_container_width=True
        )


    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    with channel_right:

        fig_channel_pie = px.pie(
            channel_sales,
            names="channel",
            values="total_value",
            hole=0.45,
            title="Channel Sales Distribution"
        )


        fig_channel_pie.update_layout(
            template="plotly_white",
            height=430
        )


        st.plotly_chart(
            fig_channel_pie,
            use_container_width=True
        )


# ============================================================
# SALES BY STORE
# ============================================================

if (
    "store_id" in product_sales.columns
    and "total_value" in product_sales.columns
):

    st.divider()

    st.header("🏪 Sales by Store")


    store_sales = (
        product_sales
        .groupby("store_id")["total_value"]
        .sum()
        .reset_index()
        .sort_values(
            "total_value",
            ascending=False
        )
    )


    fig_store = px.bar(
        store_sales,
        x="store_id",
        y="total_value",
        text="total_value",
        title=f"Store Performance — {selected_product}"
    )


    fig_store.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="outside"
    )


    fig_store.update_layout(
        template="plotly_white",
        xaxis_title="Store",
        yaxis_title="Sales (₹)",
        height=450
    )


    st.plotly_chart(
        fig_store,
        use_container_width=True
    )


# ============================================================
# INVENTORY INFORMATION
# ============================================================

if inventory_df is not None:

    if "sku_id" in inventory_df.columns:

        product_inventory = inventory_df[
            inventory_df["sku_id"].astype(str)
            == selected_product
        ].copy()


        if not product_inventory.empty:

            st.divider()

            st.header("📦 Inventory Position")


            # ------------------------------------------------
            # STOCK ON HAND
            # ------------------------------------------------

            if "stock_on_hand" in product_inventory.columns:

                stock = pd.to_numeric(
                    product_inventory["stock_on_hand"],
                    errors="coerce"
                ).fillna(0).sum()

            else:

                stock = 0


            # ------------------------------------------------
            # REORDER POINT
            # ------------------------------------------------

            if "reorder_point" in product_inventory.columns:

                reorder_point = pd.to_numeric(
                    product_inventory["reorder_point"],
                    errors="coerce"
                ).fillna(0).sum()

            else:

                reorder_point = 0


            # ------------------------------------------------
            # STOCK COVERAGE
            # ------------------------------------------------

            if "stock_coverage_days" in product_inventory.columns:

                coverage = pd.to_numeric(
                    product_inventory["stock_coverage_days"],
                    errors="coerce"
                ).fillna(0).mean()

            else:

                coverage = 0


            # ------------------------------------------------
            # RISK LEVEL
            # ------------------------------------------------

            if "final_risk_level" in product_inventory.columns:

                risk_level = (
                    product_inventory["final_risk_level"]
                    .astype(str)
                    .iloc[0]
                )

            elif "risk_level" in product_inventory.columns:

                risk_level = (
                    product_inventory["risk_level"]
                    .astype(str)
                    .iloc[0]
                )

            else:

                risk_level = "Not Available"


            # ------------------------------------------------
            # INVENTORY KPI CARDS
            # ------------------------------------------------

            inv1, inv2, inv3, inv4 = st.columns(4)


            inv1.metric(
                "Stock on Hand",
                f"{stock:,.0f}"
            )


            inv2.metric(
                "Reorder Point",
                f"{reorder_point:,.0f}"
            )


            inv3.metric(
                "Stock Coverage",
                f"{coverage:.1f} days"
            )


            inv4.metric(
                "Risk Level",
                risk_level
            )


        else:

            st.info(
                "No inventory information was found "
                "for this SKU."
            )


# ============================================================
# PRODUCT TRANSACTION DETAILS
# ============================================================

st.divider()

st.header("📋 Product Transaction Details")


display_columns = [
    "date",
    "receipt_id",
    "store_id",
    "sku_id",
    "quantity",
    "unit_price",
    "total_value",
    "channel"
]


# Only use columns that actually exist
display_columns = [
    column
    for column in display_columns
    if column in product_sales.columns
]


if display_columns:

    if "date" in product_sales.columns:

        product_table = (
            product_sales[display_columns]
            .sort_values(
                "date",
                ascending=False
            )
        )

    else:

        product_table = product_sales[
            display_columns
        ]


    st.dataframe(
        product_table,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No displayable transaction columns "
        "were found."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Retail Demand Forecasting | Product Details"
)