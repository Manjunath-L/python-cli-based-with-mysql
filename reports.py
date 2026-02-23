from db import get_cursor
from tabulate import tabulate

def best_selling():
    conn, cur = get_cursor()
    cur.execute("""
        SELECT product_name, SUM(quantity)
        FROM bill_items
        GROUP BY product_name
        ORDER BY SUM(quantity) DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Product", "Sold Qty"], tablefmt="rounded_outline"))
    conn.close()