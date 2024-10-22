class Store:
    def __init__(self, products) -> None:
        self.products = [*products]

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        return len(self.products)

    def get_all_products(self) -> list:
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products

    def order(self, shopping_list):
        total_price = 0

        for product, quantity in shopping_list:
            if quantity > product.quantity:
                message = (
                    "Error while making order! "
                    + "Quantity larger than what exists"
                    + f"Quantity of {product.name}: {product.quantity}"
                )
                return message
            elif not product.active:
                message = (
                    "Error while making order! "
                    + f"Product {product.name} is Inactive"
                )
                return message
            else:
                total_price += product.buy(quantity)

        return f"Order cost: ${total_price:.2f}"
