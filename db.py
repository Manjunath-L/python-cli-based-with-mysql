import mysql.connector
from mysql.connector import Error
from tabulate import tabulate


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1234manju@2004@#$",
        database="python_db",
    )


def list_products(cursor):
    cursor.execute("SELECT * FROM product")
    res = cursor.fetchall()
    if not res:
        print("No products found.")
        return

    headers = [col[0] for col in cursor.description]
    table = tabulate([list(row) for row in res], headers=headers, tablefmt="rounded_outline")
    print(table)


def billing_flow(cursor):
    num_pro = int(input("Enter number of products ordered by customer: "))
    sql = "SELECT price FROM product WHERE product_name = %s"
    total_price = 0.0
    count = 0
    order_data = []

    for _ in range(num_pro):
        pro_name = input("Enter product name: ")
        cursor.execute(sql, (pro_name,))
        row = cursor.fetchone()
        if row is None:
            print(f"Product '{pro_name}' not found, skipping.")
            continue

        price = float(row[0])
        total_price += price
        count += 1
        order_data.append([count, pro_name, f"₹{price}"])

    order_data.append(["", "Total-price :", f"₹{total_price}"])
    print(tabulate(order_data, headers=["No", "Order_items", "Price"], tablefmt="rounded_outline"))


def add_products(cursor, conn):
    sql = "INSERT INTO product (product_name, price, quantity, category) VALUES (%s, %s, %s, %s)"
    val = []
    n = int(input("Enter how many products you want to insert: "))
    for _ in range(n):
        pro_nm = input("Enter a product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        category = input("Enter product category: ")
        val.append((pro_nm, price, quantity, category))

    cursor.executemany(sql, val)
    conn.commit()
    print(f"{cursor.rowcount} products inserted successfully!")


def main():
    my_db = None
    my_cursor = None
    try:
        my_db = get_connection()
        my_cursor = my_db.cursor()

        pro_list = input("Do you want to see all product type (Yes or No): ").strip().lower()
        if pro_list == "yes":
            list_products(my_cursor)

        desc = int(input("Enter your choice 1 for billing, 2 for adding product: "))
        if desc == 1:
            billing_flow(my_cursor)
        elif desc == 2:
            add_products(my_cursor, my_db)
        else:
            print("Invalid choice.")
    except Error as e:
        print(f"Database error: {e}")
    except ValueError:
        print("Invalid numeric input.")
    finally:
        if my_cursor is not None:
            my_cursor.close()
        if my_db is not None:
            my_db.close()


if __name__ == "__main__":
    main()