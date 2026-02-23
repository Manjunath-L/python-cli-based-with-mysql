from user import login
from billing import create_bill
from product import *
from reports import *
from utils import menu

username = input("Username: ")
password = input("Password: ")

role = login(username, password)
if not role:
    print("❌ Login failed")
    exit()

while True:
    menu("MAIN MENU", {
        1: "Billing",
        2: "Search Product",
        3: "Update Product",
        4: "Delete Product",
        5: "Best Selling Products",
        0: "Exit"
    })

    choice = input("Choice: ")

    if choice == "1":
        n = int(input("No of items: "))
        items = []
        for _ in range(n):
            items.append((
                input("Product name: "),
                int(input("Qty: "))
            ))
        discount = float(input("Discount (₹): "))
        create_bill(items, discount)

    elif choice == "2":
        search_product(input("Search: "))

    elif choice == "3" and role == "admin":
        update_product(
            input("Product name: "),
            price=float(input("New price: ")),
            qty=int(input("New qty: "))
        )

    elif choice == "4" and role == "admin":
        delete_product(input("Product name: "))

    elif choice == "5":
        best_selling()

    elif choice == "0":
        break