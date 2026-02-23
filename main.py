from billing import create_bill
from db import init_db, seed_data
from product import delete_product, search_product, update_product
from reports import best_selling
from user import login, register_user
from utils import menu


def auth_flow():
    """Handle login / registration selection and return (username, role) or (None, None)."""
    while True:
        menu("AUTH MENU", {1: "Login", 2: "Register", 0: "Exit"})
        choice = input("Choice: ").strip()

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            role = login(username, password)
            if not role:
                print("❌ Login failed")
                continue
            return username, role

        elif choice == "2":
            register_user()

        elif choice == "0":
            return None, None

        else:
            print("Invalid choice, try again.")


def main():
    # Ensure tables exist and some dummy data is present
    init_db()
    seed_data()

    username, role = auth_flow()
    if not username:
        print("Goodbye!")
        return

    while True:
        # Role-based menu: admin has full access; cashier can only bill
        if role == "admin":
            options = {
                1: "Billing",
                2: "Search Product",
                3: "Update Product",
                4: "Delete Product",
                5: "Best Selling Products",
                0: "Exit",
            }
        else:  # cashier or any non-admin
            options = {
                1: "Billing",
                0: "Exit",
            }

        menu("MAIN MENU", options)
        choice = input("Choice: ").strip()

        if choice == "1":
            try:
                n = int(input("No of items: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            items = []
            for _ in range(n):
                name = input("Product name: ")
                try:
                    qty = int(input("Qty: "))
                except ValueError:
                    print("Invalid quantity, skipping item.")
                    continue
                items.append((name, qty))

            try:
                discount = float(input("Discount (₹): "))
            except ValueError:
                print("Invalid discount, using 0.")
                discount = 0.0

            create_bill(items, discount)

        elif choice == "2" and role == "admin":
            search_product(input("Search: "))

        elif choice == "3" and role == "admin":
            name = input("Product name: ")
            try:
                price = float(input("New price: "))
                qty = int(input("New qty: "))
            except ValueError:
                print("Invalid price/qty.")
                continue
            update_product(name, price=price, qty=qty)

        elif choice == "4" and role == "admin":
            delete_product(input("Product name: "))

        elif choice == "5" and role == "admin":
            best_selling()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()