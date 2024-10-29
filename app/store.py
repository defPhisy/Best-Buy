"""
Represents a store that contains a collection of products.

Attributes:
    products (list): A list of Product objects available in the store.
"""

from app.products import NonStockedProduct


class Store:
    def __init__(self, products) -> None:
        self.products = [*products]

    def add_product(self, product) -> None:
        self.products.append(product)

    def remove_product(self, product) -> None:
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        return len(self.products)

    def get_all_products(self) -> list:
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products

    def order(self, shopping_list: list[tuple]) -> str:
        """Get total price of ordered items from shopping_list
        and update quantity of products in Store.

        Arguments:
            shopping_list -- [(product_obj, quantity_to_order)]

        Returns:
            Total price of all items
        """
        total_price = 0

        for product, quantity in shopping_list:
            if quantity > product.quantity and not isinstance(
                product, NonStockedProduct
            ):
                message = (
                    "Error while making order! "
                    + "Quantity larger than what exists\n"
                    + f"Quantity of {product.name}: {product.quantity}\n"
                    + f"Order cost: ${total_price:.2f}"
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
