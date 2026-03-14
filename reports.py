from db import get_cursor
from utils import print_table


def best_selling():
    conn, cur = get_cursor()
    try:
        cur.execute(
            """
            SELECT product_name, SUM(quantity)
            FROM bill_items
            GROUP BY product_name
            ORDER BY SUM(quantity) DESC
            LIMIT 5
            """
        )
        rows = cur.fetchall()
        if not rows:
            from utils import info  # local import to avoid circulars at top

            info("No sales data yet.")
            return

        print_table(["Product", "Sold Qty"], rows, title="Best Selling Products")
    finally:
        conn.close()