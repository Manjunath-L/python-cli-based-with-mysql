from db import get_cursor
from tabulate import tabulate

def search_product(name):
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM product WHERE product_name LIKE %s", (f"%{name}%",))
    rows = cur.fetchall()
    print(tabulate(rows, headers=[i[0] for i in cur.description], tablefmt="rounded_outline"))
    conn.close()

def update_product(name, price=None, qty=None):
    conn, cur = get_cursor()
    if price:
        cur.execute("UPDATE product SET price=%s WHERE product_name=%s", (price, name))
    if qty:
        cur.execute("UPDATE product SET quantity=%s WHERE product_name=%s", (qty, name))
    conn.commit()
    conn.close()

def delete_product(name):
    conn, cur = get_cursor()
    cur.execute("DELETE FROM product WHERE product_name=%s", (name,))
    conn.commit()
    conn.close()
    