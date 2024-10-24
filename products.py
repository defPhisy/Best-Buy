"""
Represents a product in an inventory.

Class Attributes:
    total_quantity (int): Tracks the total quantity of all products.

Instance Attributes:
    name (str): The name of the product.
    price (float): The price of the product.
    quantity (int): The available quantity of the product.
    active (bool): The status of the product (active or inactive).
"""


class Product:
    total_quantity = 0

    def __init__(self, name: str, price: float, quantity: int) -> None:
        if self.name_is_valid(name):
            self.name = name

        if self.price_is_valid(price):
            self.price = price

        if self.quantity_is_valid(quantity):
            self.quantity = quantity

        self.active = True

        Product.total_quantity += quantity

    def name_is_valid(self, name):
        if name:
            return True
        else:
            raise ValueError("Name must have at leas one letter!")

    def price_is_valid(self, price):
        if type(price) is float or type(price is int):
            return True
        else:
            raise TypeError("Price must be a float!")

    def quantity_is_valid(self, quantity):
        if type(quantity) is int and quantity >= 0:
            return True
        else:
            raise Exception("Quantity must be a positive integer")

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        """Sets the quantity of the product
        and deactivates it if the quantity is zero."""
        if self.quantity_is_valid(quantity):
            self.quantity = quantity
            if self.quantity == 0:
                self.active = False

    def is_active(self) -> bool:
        return self.active

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """Reduces the product quantity by the specified amount,
        deducts from total quantity,
        and returns the total price for the quantity bought."""
        self.set_quantity(self.quantity - quantity)
        Product.total_quantity -= quantity
        return self.price * quantity
