from datetime import datetime

from db import get_cursor
from invoice import generate_invoice
from product import check_stock, update_stock
from utils import console, error, print_table, success

GST_RATE = 0.18


def create_bill(items, discount=0):
    conn, cur = get_cursor()

    try:
        bill_items = []
        subtotal = 0

        for name, qty in items:
            if not check_stock(name, qty):
                error(f"Insufficient stock for {name}")
                return

            cur.execute(
                "SELECT price FROM product WHERE product_name=%s", (name,)
            )
            row = cur.fetchone()
            if row is None:
                error(f"Product not found: {name}")
                return

            price = float(row[0])

            total_price = price * qty
            subtotal += total_price
            bill_items.append((name, qty, price, total_price))

            if not update_stock(name, qty):
                error(f"Failed to update stock for {name}")
                return

        if not bill_items:
            error("No valid items to bill.")
            return

        gst = round(subtotal * GST_RATE, 2)
        grand_total = round(subtotal + gst - discount, 2)

        cur.execute(
            "INSERT INTO bill (bill_date, total_amount) VALUES (%s,%s)",
            (datetime.now(), grand_total),
        )
        bill_id = cur.lastrowid

        # Store individual line items for reports
        for name, qty, price, _total_price in bill_items:
            cur.execute(
                """
                INSERT INTO bill_items (bill_id, product_name, quantity, price)
                VALUES (%s,%s,%s,%s)
                """,
                (bill_id, name, qty, price),
            )

        conn.commit()

        # Show a summary table in the CLI
        headers = ["Item", "Qty", "Price", "Total"]
        rows = [(n, q, price, t) for n, q, price, t in bill_items]
        print_table(headers, rows, title=f"Bill #{bill_id}")
        console.print(
            f"\n[bold magenta]Subtotal:[/] {subtotal}  "
            f"[bold magenta]GST (18%):[/] {gst}  "
            f"[bold magenta]Discount:[/] {discount}  "
            f"[bold magenta]Grand Total:[/] [bold green]{grand_total}[/]"
        )

        pdf_path = generate_invoice(
            bill_id, bill_items, subtotal, gst, discount, grand_total
        )

        success(f"Bill Created | Bill ID: {bill_id}")
        console.print(f"[bold cyan]Invoice saved at:[/] {pdf_path}")
    finally:
        conn.close()