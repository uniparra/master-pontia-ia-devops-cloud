def show_inventory(inventory):
    for p in inventory.values():
        name = p["name"]
        price = p["price"]
        current_stock = p["current_stock"]
        categories = p["categories"]
        tags = p["tags"]

        #* Mostramos los 3 primeros valores
        print(f'Nombre del producto: {name}')
        print(f'Precio: {price}')
        print(f'Stock actual: {current_stock}')

        #* Mostramos las categorías
        # for c in categories:
        #     print(f'--> Categoría: {c["name"]} ({c["description"]})')
        categories_str = ', '.join([category["name"] + category["description"] for category in categories])
        print(f'--> Categories: {categories_str}')

        #* Mostramos los Tags
        tags_str = ', '.join([tag["name"] for tag in tags])
        print(f'--> Tags: {tags_str}')

        print('---------------------------------------')

def update_stock(product, units_sold):
    current_stock = product["current_stock"]
    final_stock = current_stock - units_sold
    product["current_stock"] = final_stock
    print(f'Your new stock for product {product["name"]} is {final_stock} units')
    return product

def check_stock_for_product(product, requested_units):
    exist_stock = product["current_stock"] >= requested_units
    product_stock = product["current_stock"]

    if exist_stock : 
        return exist_stock, requested_units
    else:
        return exist_stock , product_stock

def process_orders(orders):
    print("Hola")
    for order in orders:
        order_id = order["order_id"]
        items = order["items"]
        total = 0

        print(order_id, items, total)

        for sku, requested_units in items.items():
            product = inventory.get(sku)

            stock_available, units_sol = check_stock_for_product(product, requested_units)

            if stock_available:

                update_stock(product, units_sol)
        # Calcular precio total y mostrarlo.

    show_inventory(inventory)


# Gestión de categorías...
categories = [
    {"name": "Electronics", "description": "Devices and gadgets"},
    {"name": "Office", "description": "Office supplies and equipment"}
]

# Gestión de etiquetas (tags)
tags = [
    {"name": "On Sale"},
    {"name": "New Arrival"},
    {"name": "Best Seller"}
]

# Gestión de productos
products = [
    {"name": "Laptop", "sku": "SKU123", "price": 1200, "current_stock": 10, "categories": [categories[0], categories[1]], "tags": [tags[1], tags[2]]},
    {"name": "Mouse", "sku": "SKU456", "price": 25, "current_stock": 100, "categories": [], "tags": [tags[0]]},
    {"name": "Keyboard", "sku": "SKU789", "price": 50, "current_stock": 50, "categories": [categories[1]], "tags": [tags[2]]},
    {"name": "Monitor", "sku": "SKU101", "price": 300, "current_stock": 20, "categories": [categories[0]], "tags": []}
]

# Gestión del inventario
inventory = {product["sku"]: product for product in products}

# Procesar pedidos
orders = [
    {"order_id": "ORDER001", "items": {"SKU123": 17, "SKU456": 5}},
    {"order_id": "ORDER002", "items": {"SKU123": 5, "SKU789": 3, "SKU101": 1}},
    {"order_id": "ORDER003", "items": {"SKU456": 10, "SKU101": 2}}
]
process_orders(orders)
# print(f"Order ID: {order_id} - Total: ${total:.2f} - Purchase Completed")

import time
time.sleep(10)

orders_afternoon = [
    {"order_id": "ORDER001", "items": {"SKU123": 17, "SKU456": 5}},
]
process_orders(orders_afternoon)
