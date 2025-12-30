import mysql.connector
from tabulate import tabulate


my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234manju@2004@#$",
    database="python_db",  # Localhost for local connection
)

my_cursor = my_db.cursor()

# my_cursor.execute("""CREATE TABLE product ( product_id INT PRIMARY KEY AUTO_INCREMENT,
#                   product_name VARCHAR(100) NOT NULL, 
#                   price DECIMAL(10,2) NOT NULL, 
#                   quantity INT NOT NULL, 
#                   category VARCHAR(50));""")



pro_list = input("Do you want to see all product type : (Yes or No) : ").lower()
if pro_list == "yes":
  my_cursor.execute("Select * from product")
  res = my_cursor.fetchall()
  list_item = [list(i) for i in res]
  headers = [col[0] for col in my_cursor.description]
  table = tabulate(list_item,headers=headers,tablefmt="rounded_outline")
  print(table)


desc = int(input("Enter your choice 1 for billing 2 for adding product :"))
if desc == 1:
  num_pro = int(input("Enter number of product ordered by customer :"))
  sql = "Select price from product where product_name = %s"
  total_price = 0
  count = 0
  order_data = []
  for i in range(num_pro):
    pro_name = input("Enter product name :")
    my_cursor.execute(sql,(pro_name,))
    price = my_cursor.fetchone()
    price_float = float(price[0])
    total_price += price_float
    count += 1
    order_data.append([count,pro_name,f"₹{price_float}"])
  order_data.append(["","Total-price :",f"₹{total_price}"])
  print(tabulate(order_data,headers=["No","Order_items","Price"],tablefmt="rounded_outline"))
elif desc == 2:
  sql = "INSERT INTO product (product_name,price,quantity,category) VALUES (%s,%s,%s,%s)"
  val = []
  n = int(input("Enter a how many product you want insert :"))
  for _ in range(n):
    pro_nm = input("Enter a product name :")
    price = float(input("Enter product price :"))
    quantiles = int(input("Enter product quantity :"))
    category = input("Enter product Category :")
    val.append((pro_nm,price,quantiles,category))
  my_cursor.executemany(sql, val)
  my_db.commit()
  print(f"✅ {my_cursor.rowcount} products inserted successfully!")


my_cursor.close()
my_db.close()