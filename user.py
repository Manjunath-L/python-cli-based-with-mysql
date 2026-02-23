from db import get_cursor


def login(username: str, password: str):
    """
    Simple username/password check.
    Returns role string (e.g. 'admin', 'cashier') or None if invalid.
    """
    conn, cur = get_cursor()
    try:
        cur.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password),
        )
        row = cur.fetchone()
        if row:
            print(f"✅ Login successful as {row[0]}")
            return row[0]
        return None
    finally:
        conn.close()


def register_user():
    """
    Register a new user as admin or cashier.
    Stores the record in the users table.
    """
    conn, cur = get_cursor()
    try:
        username = input("Choose a username: ").strip()
        password = input("Choose a password: ").strip()
        if not username or not password:
            print("Username and password cannot be empty.")
            return

        # Check if username already exists
        cur.execute("SELECT 1 FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            print("❌ Username already exists, try another.")
            return

        print("Select role:")
        print("1. Admin")
        print("2. Cashier")
        role_choice = input("Choice (1/2): ").strip()
        if role_choice == "1":
            role = "admin"
        elif role_choice == "2":
            role = "cashier"
        else:
            print("Invalid role choice.")
            return

        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
            (username, password, role),
        )
        conn.commit()
        print(f"✅ User '{username}' registered as {role}.")
    finally:
        conn.close()
