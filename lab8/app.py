"""
Streamlit app for managing and visualising sales stored in an SQLite database
(sales.db). Place this file (app.py) in the same folder as *sales.db* and run:
    streamlit run app.py
"""

import os
import sqlite3
from datetime import date as dt_date

import pandas as pd
import streamlit as st
import altair as alt

DB_PATH = os.getenv("SALES_DB", "sales.db")

# Database helpers

def get_connection():
    # Cache the connection so every rerun re‑uses the same handle.
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
        """
    )
    conn.commit()


# Initialise the database exactly once (runs on every first execution after
# a change or server restart)
init_db()

# Data access layer

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load the *sales* table into a DataFrame. Returns empty DF if missing."""
    conn = get_connection()
    try:
        return pd.read_sql_query("SELECT * FROM sales", conn)
    except (sqlite3.OperationalError, pd.io.sql.DatabaseError):
        # Table was dropped between reruns – recreate and return empty DF
        init_db()
        return pd.DataFrame(columns=["id", "product", "quantity", "price", "date"])


def insert_sale(product: str, quantity: int, price: float, sale_date: dt_date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO sales (product, quantity, price, date) VALUES (?,?,?,?)",
        (product, quantity, price, sale_date.isoformat()),
    )
    conn.commit()


# Sidebar –  input form

st.sidebar.header("Dodaj nową sprzedaż 🛒")
with st.sidebar.form(key="add_sale_form"):
    col1, col2 = st.columns(2)
    with col1:
        product_input = st.text_input("Produkt")
        quantity_input = st.number_input("Ilość", min_value=1, value=1, step=1)
    with col2:
        price_input = st.number_input("Cena (PLN)", min_value=0.0, value=0.0, step=0.01)
        date_input = st.date_input("Data", value=dt_date.today())

    submitted = st.form_submit_button("Dodaj")
    if submitted:
        if product_input and price_input > 0:
            insert_sale(
                product_input, int(quantity_input), float(price_input), date_input
            )
            st.success("Zapisano nową sprzedaż!")
            st.balloons()
            # Clear cache to reload data on next rerun
            load_data.clear()
        else:
            st.error("Wprowadź poprawne dane (produkt, cena > 0)")

# Main layout

st.title("📊 Panel sprzedaży")

# Load data (could be empty after first run)
try:
    sales_df = load_data()
except Exception as exc:
    st.error(f"Nie udało się wczytać danych: {exc}")
    sales_df = pd.DataFrame(columns=["id", "product", "quantity", "price", "date"])

# Filters
with st.expander("Filtry", expanded=False):
    unique_products = sorted(sales_df["product"].unique()) if not sales_df.empty else []
    selected_product = st.selectbox(
        "Wybierz produkt (puste = wszystkie)", [""] + unique_products, index=0
    )

    if selected_product:
        filtered_df = sales_df.query("product == @selected_product")
    else:
        filtered_df = sales_df

    show_table = st.checkbox("Pokaż tabelę danych", value=True)

# Data table
if show_table:
    st.subheader("Tabela sprzedaży")
    st.dataframe(
        filtered_df.sort_values("date", ascending=False).reset_index(drop=True),
        use_container_width=True,
    )

# Charts


def add_value_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["value"] = df["quantity"] * df["price"]
    return df


chart_df = add_value_column(filtered_df) if not filtered_df.empty else filtered_df

# Daily sales value
st.subheader("Sprzedaż dzienna (wartość)")
if not chart_df.empty:
    daily = chart_df.groupby("date", as_index=False)["value"].sum().sort_values("date")
    daily_chart = (
        alt.Chart(daily)
        .mark_bar()
        .encode(x="date:T", y="value:Q", tooltip=["date:T", "value:Q"])
        .properties(height=350)
    )
    st.altair_chart(daily_chart, use_container_width=True)
else:
    st.info("Brak danych do wyświetlenia.")

# Total quantity by product
st.subheader("Łączna ilość sprzedanych produktów")
if not chart_df.empty:
    by_product = (
        chart_df.groupby("product", as_index=False)["quantity"]
        .sum()
        .sort_values("quantity", ascending=False)
    )
    product_chart = (
        alt.Chart(by_product)
        .mark_bar()
        .encode(
            x="quantity:Q",
            y=alt.Y("product:N", sort="-x"),
            tooltip=["product:N", "quantity:Q"],
        )
        .properties(height=350)
    )
    st.altair_chart(product_chart, use_container_width=True)
else:
    st.info("Brak danych do wyświetlenia.")

st.caption("© 2025 Streamlit Sales Dashboard – demo")
