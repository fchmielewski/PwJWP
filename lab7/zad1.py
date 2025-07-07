import sqlite3, pathlib, sys
import pandas as pd

# Konfiguracja
db_path = pathlib.Path(__file__).with_name(
    "sales.db"
)
table_name = "sales"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Walidacja: czy tabela istnieje?
cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)
)
if not cur.fetchone():
    sys.exit(f"BŁĄD: tabela '{table_name}' nie istnieje w {db_path.resolve()}")

queries = {
    "a) Sprzedaż produktu 'Laptop'": f"SELECT * FROM {table_name} WHERE product = 'Laptop';",
    "b) Sprzedaż z 2025-05-07 i 2025-05-08": f"SELECT * FROM {table_name} WHERE date IN ('2025-05-07','2025-05-08');",
    "c) Cena jednostkowa > 200 zł": f"SELECT * FROM {table_name} WHERE price > 200;",
    "d) Łączna wartość sprzedaży per produkt": f"""
        SELECT product,
               SUM(price * quantity) AS total_sales_value
        FROM {table_name}
        GROUP BY product
        ORDER BY total_sales_value DESC;
        """,
    "e) Dzień z największą liczbą sprzedanych sztuk": f"""
        SELECT date,
               SUM(quantity) AS total_units_sold
        FROM {table_name}
        GROUP BY date
        ORDER BY total_units_sold DESC
        LIMIT 1;
        """,
}


for label, sql in queries.items():
    df = pd.read_sql_query(sql, conn)
    print(f"\n=== {label} ===")
    print(df.to_string(index=False))

conn.close()
