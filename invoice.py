from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_invoice(bill_id, items, subtotal, gst, discount, total):
    os.makedirs("invoices", exist_ok=True)

    file_path = f"invoices/invoice_{bill_id}.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "INVOICE")
    y -= 40

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Bill ID: {bill_id}")
    c.drawString(350, y, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    y -= 30

    c.drawString(50, y, "Item")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Price")
    c.drawString(380, y, "Total")
    y -= 15

    c.line(50, y, 500, y)
    y -= 20

    for name, qty, price, total_price in items:
        c.drawString(50, y, name)
        c.drawString(250, y, str(qty))
        c.drawString(300, y, f"{price}")
        c.drawString(380, y, f"{total_price}")
        y -= 20

    y -= 10
    c.line(50, y, 500, y)
    y -= 20

    c.drawString(300, y, "Subtotal:")
    c.drawString(380, y, f"{subtotal}")
    y -= 20

    c.drawString(300, y, "GST:")
    c.drawString(380, y, f"{gst}")
    y -= 20

    c.drawString(300, y, "Discount:")
    c.drawString(380, y, f"-{discount}")
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(300, y, "Grand Total:")
    c.drawString(380, y, f"{total}")

    c.save()
    return file_path