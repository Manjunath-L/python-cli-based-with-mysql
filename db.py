import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "passwd": "1234manju@2004@#$",
    "database": "python_db",
}


def get_connection():
    """Return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


def get_cursor():
    """
    Helper used by other modules.
    Returns (connection, cursor); caller must close connection.
    """
    conn = get_connection()
    return conn, conn.cursor()


def init_db():
    """Create required tables if they don't already exist."""
    conn, cur = get_cursor()
    try:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS product (
                product_id INT PRIMARY KEY AUTO_INCREMENT,
                product_name VARCHAR(100) NOT NULL UNIQUE,
                price DECIMAL(10,2) NOT NULL,
                quantity INT NOT NULL,
                category VARCHAR(50)
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bill (
                bill_id INT PRIMARY KEY AUTO_INCREMENT,
                bill_date DATETIME NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bill_items (
                id INT PRIMARY KEY AUTO_INCREMENT,
                bill_id INT NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (bill_id) REFERENCES bill(bill_id)
                    ON DELETE CASCADE
            )
            """
        )

        conn.commit()
    finally:
        conn.close()


def seed_data():
    """
    Insert some dummy users and products if tables are empty.
    Safe to call multiple times.
    """
    conn, cur = get_cursor()
    try:
        # Seed users
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            users = [
                ("admin", "admin123", "admin"),
                ("cashier", "cashier123", "cashier"),
            ]
            cur.executemany(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                users,
            )

        # Seed products
        cur.execute("SELECT COUNT(*) FROM product")
        if cur.fetchone()[0] == 0:
            products = [
                ("Apple", 50.0, 100, "Fruit"),
                ("Banana", 20.0, 150, "Fruit"),
                ("Milk 1L", 60.0, 80, "Dairy"),
                ("Bread", 40.0, 60, "Bakery"),
                ("Eggs (12pc)", 75.0, 50, "Dairy"),
            ]
            cur.executemany(
                "INSERT INTO product (product_name, price, quantity, category) "
                "VALUES (%s, %s, %s, %s)",
                products,
            )

        conn.commit()
    finally:
        conn.close()