from db import get_cursor
from product import check_stock, update_stock
from invoice import generate_invoice
from datetime import datetime

GST_RATE = 0.18

def create_bill(items, discount=0):
    conn, cur = get_cursor()

    bill_items = []
    subtotal = 0

    for name, qty in items:
        if not check_stock(name, qty):
            print(f"❌ Insufficient stock for {name}")
            return

        cur.execute("SELECT price FROM product WHERE product_name=%s", (name,))
        price = cur.fetchone()[0]

        total_price = price * qty
        subtotal += total_price
        bill_items.append((name, qty, price, total_price))

        update_stock(name, qty)

    gst = round(subtotal * GST_RATE, 2)
    grand_total = round(subtotal + gst - discount, 2)

    cur.execute(
        "INSERT INTO bill (bill_date, total_amount) VALUES (%s,%s)",
        (datetime.now(), grand_total)
    )
    bill_id = cur.lastrowid
    conn.commit()
    conn.close()

    pdf_path = generate_invoice(
        bill_id, bill_items, subtotal, gst, discount, grand_total
    )

    print(f"\n✅ Bill Created | Bill ID: {bill_id}")
    print(f"📄 Invoice saved at: {pdf_path}")