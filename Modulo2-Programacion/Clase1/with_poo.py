class Category:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description or ''

    def __repr__(self):
        return f"Category(name='{self.name}', description='{self.description}')"


class Tag:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Tag(name='{self.name}')"


class Product:
    def __init__(self, name, sku, price, current_stock=0, categories=None, tags=None):
        self.name = name
        self.sku = sku
        self.price = price
        self.current_stock = current_stock
        self.categories = categories or []
        self.tags = tags or []
        self.price_history = [(price, 'Initial Price')]

    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category):
        if category in self.categories:
            self.categories.remove(category)

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def update_stock(self, amount):
        self.current_stock += amount

    def is_in_stock(self):
        return self.current_stock > 0

    def apply_discount(self, percentage):
        self.price -= self.price * (percentage / 100)
        self.price_history.append((self.price, f"Discount applied: {percentage}%"))

    def calculate_total_value_in_stock(self):
        return self.price * self.current_stock

    def get_info(self):
        categories = ', '.join([cat.name for cat in self.categories]) or 'None'
        tags = ', '.join([tag.name for tag in self.tags]) or 'None'
        return f"Product: {self.name} (SKU: {self.sku}) - Price: ${self.price:.2f}, Stock: {self.current_stock}, Categories: [{categories}], Tags: [{tags}]"

    def __repr__(self):
        return f"Product(name='{self.name}', sku='{self.sku}', price={self.price}, current_stock={self.current_stock})"


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.sku not in self.products:
            self.products[product.sku] = product

    def remove_product(self, sku):
        if sku in self.products:
            del self.products[sku]

    def get_product(self, sku):
        return self.products.get(sku)

    def list_products(self):
        return list(self.products.values())

    def find_by_name(self, name):
        return [p for p in self.products.values() if name.lower() in p.name.lower()]

    def get_total_inventory_value(self):
        return sum(p.calculate_total_value_in_stock() for p in self.products.values())

    def generate_inventory_report(self):
        report = [p.get_info() for p in self.products.values()]
        return '\n'.join(report)

    def __repr__(self):
        return f"Inventory({len(self.products)} products)"


class Order:
    def __init__(self, order_id, products=None):
        self.order_id = order_id
        self.products = products or {}

    def add_product(self, product, quantity):
        if product.sku in self.products:
            self.products[product.sku]['quantity'] += quantity
        else:
            self.products[product.sku] = {'product': product, 'quantity': quantity}

    def remove_product(self, product_sku):
        if product_sku in self.products:
            del self.products[product_sku]

    def calculate_total(self):
        return sum(item['product'].price * item['quantity'] for item in self.products.values())

    def get_order_summary(self):
        lines = [f"{item['product'].name} (x{item['quantity']}) - ${item['product'].price * item['quantity']:.2f}" for item in self.products.values()]
        return f"Order ID: {self.order_id}\n" + '\n'.join(lines) + f"\nTotal: ${self.calculate_total():.2f}"

    def buy(self):
        total = self.calculate_total()
        for sku, item in self.products.items():
            product = item['product']
            quantity = item['quantity']
            if product.current_stock < quantity:
                raise ValueError(f"Insufficient stock for {product.name}. Available: {product.current_stock}, Requested: {quantity}")
            product.update_stock(-quantity)
        return f"Order ID: {self.order_id} - Total: ${total:.2f} - Purchase Completed"

    def __repr__(self):
        return f"Order(order_id='{self.order_id}', total_items={len(self.products)})"


if __name__ == "__main__":
    # Crear inventario
    inventory = Inventory()

    # Crear productos
    p1 = Product("Laptop", "SKU123", 1200, 10)
    p2 = Product("Mouse", "SKU456", 25, 100)
    p3 = Product("Keyboard", "SKU789", 50, 50)
    p4 = Product("Monitor", "SKU101", 300, 20)

    # Añadir productos al inventario
    inventory.add_product(p1)
    inventory.add_product(p2)
    inventory.add_product(p3)
    inventory.add_product(p4)

    # Crear pedidos
    order1 = Order("ORDER001")
    order1.add_product(p1, 2)
    order1.add_product(p2, 5)

    order2 = Order("ORDER002")
    order2.add_product(p3, 3)
    order2.add_product(p4, 1)

    order3 = Order("ORDER003")
    order3.add_product(p2, 10)
    order3.add_product(p4, 2)
    print(order3.get_order_summary())

    # Procesar compras
    print(order1.buy())
    print(order2.buy())
    print(order3.buy())

    # Mostrar estado final del inventario
    print("\nInventory Report:\n")
    print(inventory.generate_inventory_report())
