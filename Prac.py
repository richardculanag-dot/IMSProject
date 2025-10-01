import datetime

# ---------- Data Structures ----------
products = {}
suppliers = {}
orders = []
sales = []

# ---------- Product Functions ----------
def add_product():
    product_id = input("Enter product ID: ")
    if product_id in products:
        print("❌ Product ID already exists!")
        return
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter initial stock quantity: "))
    supplier_id = input("Enter supplier ID (leave blank if none): ")

    products[product_id] = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "supplier": supplier_id
    }
    print("✅ Product added successfully!")

def update_product():
    product_id = input("Enter product ID to update: ")
    if product_id not in products:
        print("❌ Product not found!")
        return
    name = input("Enter new name (leave blank to keep current): ")
    price = input("Enter new price (leave blank to keep current): ")
    quantity = input("Enter new quantity (leave blank to keep current): ")

    if name:
        products[product_id]["name"] = name
    if price:
        products[product_id]["price"] = float(price)
    if quantity:
        products[product_id]["quantity"] = int(quantity)

    print("✅ Product updated successfully!")

def delete_product():
    product_id = input("Enter product ID to delete: ")
    if product_id in products:
        del products[product_id]
        print("✅ Product deleted successfully!")
    else:
        print("❌ Product not found!")

def view_products():
    if not products:
        print("📦 No products available.")
        return
    print("\n📦 Product List:")
    for pid, info in products.items():
        print(f"  ID: {pid} | Name: {info['name']} | Price: {info['price']} | Stock: {info['quantity']} | Supplier: {info['supplier']}")

# ---------- Supplier Functions ----------
def add_supplier():
    supplier_id = input("Enter supplier ID: ")
    if supplier_id in suppliers:
        print("❌ Supplier ID already exists!")
        return
    name = input("Enter supplier name: ")
    contact = input("Enter contact number: ")

    suppliers[supplier_id] = {
        "name": name,
        "contact": contact
    }
    print("✅ Supplier added successfully!")

def view_suppliers():
    if not suppliers:
        print("📇 No suppliers available.")
        return
    print("\n📇 Supplier List:")
    for sid, info in suppliers.items():
        print(f"  ID: {sid} | Name: {info['name']} | Contact: {info['contact']}")

# ---------- Order Functions ----------
def create_order():
    supplier_id = input("Enter supplier ID: ")
    if supplier_id not in suppliers:
        print("❌ Supplier not found!")
        return
    product_id = input("Enter product ID to order: ")
    if product_id not in products:
        print("❌ Product not found!")
        return
    quantity = int(input("Enter quantity to order: "))
    expected_date = input("Enter expected delivery date (YYYY-MM-DD): ")

    order = {
        "order_id": len(orders) + 1,
        "supplier_id": supplier_id,
        "product_id": product_id,
        "quantity": quantity,
        "order_date": datetime.date.today(),
        "expected_date": expected_date,
        "status": "Pending"
    }
    orders.append(order)
    print("✅ Order created successfully!")

def view_orders():
    if not orders:
        print("📦 No orders placed.")
        return
    print("\n📦 Orders List:")
    for o in orders:
        print(f"  Order ID: {o['order_id']} | Product: {o['product_id']} | Quantity: {o['quantity']} | Status: {o['status']} | Expected: {o['expected_date']}")

def mark_order_delivered():
    oid = int(input("Enter order ID to mark delivered: "))
    for order in orders:
        if order["order_id"] == oid:
            order["status"] = "Delivered"
            # Auto-increase stock
            products[order["product_id"]]["quantity"] += order["quantity"]
            print("✅ Order marked as delivered. Stock updated.")
            return
    print("❌ Order not found!")

# ---------- Sales Functions ----------
def record_sale():
    product_id = input("Enter product ID sold: ")
    if product_id not in products:
        print("❌ Product not found!")
        return
    quantity = int(input("Enter quantity sold: "))
    if quantity > products[product_id]["quantity"]:
        print("❌ Not enough stock!")
        return

    products[product_id]["quantity"] -= quantity
    sale = {
        "product_id": product_id,
        "quantity": quantity,
        "date": datetime.date.today()
    }
    sales.append(sale)
    print("✅ Sale recorded successfully!")

def view_sales_report():
    if not sales:
        print("📊 No sales recorded.")
        return
    print("\n📊 Sales Report:")
    for s in sales:
        print(f"  Product: {products[s['product_id']]['name']} | Quantity: {s['quantity']} | Date: {s['date']}")

# ---------- Main Menu ----------
def main_menu():
    while True:
        print("\n📦 Inventory Management System")
        print("1. Manage Products")
        print("2. Manage Suppliers")
        print("3. Manage Orders")
        print("4. Record Sales")
        print("5. View Reports")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            manage_products()
        elif choice == "2":
            manage_suppliers()
        elif choice == "3":
            manage_orders()
        elif choice == "4":
            record_sale()
        elif choice == "5":
            view_sales_report()
        elif choice == "0":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice!")

def manage_products():
    while True:
        print("\n📦 Product Management")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. View Products")
        print("0. Back")

        choice = input("Select: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            view_products()
        elif choice == "0":
            break

def manage_suppliers():
    while True:
        print("\n📇 Supplier Management")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("0. Back")

        choice = input("Select: ")
        if choice == "1":
            add_supplier()
        elif choice == "2":
            view_suppliers()
        elif choice == "0":
            break

def manage_orders():
    while True:
        print("\n📦 Order Management")
        print("1. Create Order")
        print("2. View Orders")
        print("3. Mark Order as Delivered")
        print("0. Back")

        choice = input("Select: ")
        if choice == "1":
            create_order()
        elif choice == "2":
            view_orders()
        elif choice == "3":
            mark_order_delivered()
        elif choice == "0":
            break

# ---------- Run Program ----------
if __name__ == "__main__":
    main_menu()
