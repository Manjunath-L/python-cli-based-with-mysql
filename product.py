from db import get_cursor
from tabulate import tabulate


def search_product(name):
    conn, cur = get_cursor()
    try:
        cur.execute(
            "SELECT * FROM product WHERE product_name LIKE %s", (f"%{name}%",)
        )
        rows = cur.fetchall()
        if not rows:
            print("No matching products.")
            return
        print(
            tabulate(
                rows,
                headers=[i[0] for i in cur.description],
                tablefmt="rounded_outline",
            )
        )
    finally:
        conn.close()


def update_product(name, price=None, qty=None):
    conn, cur = get_cursor()
    try:
        if price is not None:
            cur.execute(
                "UPDATE product SET price=%s WHERE product_name=%s",
                (price, name),
            )
        if qty is not None:
            cur.execute(
                "UPDATE product SET quantity=%s WHERE product_name=%s",
                (qty, name),
            )
        conn.commit()
        print("Product updated.")
    finally:
        conn.close()


def delete_product(name):
    conn, cur = get_cursor()
    try:
        cur.execute("DELETE FROM product WHERE product_name=%s", (name,))
        conn.commit()
        print("Product deleted (if it existed).")
    finally:
        conn.close()


def check_stock(name, qty):
    """Return True if product exists and has at least qty in stock."""
    conn, cur = get_cursor()
    try:
        cur.execute(
            "SELECT quantity FROM product WHERE product_name=%s", (name,)
        )
        row = cur.fetchone()
        if row is None:
            return False
        return row[0] >= qty
    finally:
        conn.close()


def update_stock(name, qty_sold):
    """
    Reduce stock by qty_sold.
    Returns True if stock was updated, False if not enough stock.
    """
    conn, cur = get_cursor()
    try:
        cur.execute(
            "UPDATE product SET quantity = quantity - %s "
            "WHERE product_name=%s AND quantity >= %s",
            (qty_sold, name, qty_sold),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()