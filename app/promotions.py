"""
Promotions Module for Store Products

This module defines various promotional discounts that can be applied
to products within a store. Each promotion class extends the
base `Promotion` class, allowing for different discount types such as
percentage discounts, "second half-price" deals, and "third item free" offers.

Usage:
    Each promotion class has an `apply_promotions` method that takes a product
    and quantity, calculates the total price after applying the promotion,
    and reduces the product's quantity if applicable.

Dependencies:
    Requires the `products` module for product classes and inventory management.
"""

from abc import ABC
import app.products as products


class Promotion(ABC):
    def __init__(self, name) -> None:
        self.name = name

    def apply_promotions(self, product, quantity) -> float:
        return float(product.price * quantity)


class PercentDiscount(Promotion):
    """Promotion that applies a percentage discount to the product price.

    Args:
        name (str): The name of the promotion.
        percent (float): The percentage discount to apply.
    """

    def __init__(self, name, percent) -> None:
        super().__init__(name)
        self.percent = percent

    def apply_promotions(self, product, quantity) -> float:
        """Applies the percentage discount to the product's price."""

        discount_multiplier = 1 - (self.percent / 100)
        discounted_price = product.price * discount_multiplier
        if not isinstance(product, products.NonStockedProduct):
            product.quantity -= quantity
            products.Product.total_quantity -= quantity
        return discounted_price * quantity


class SecondHalfPrice(Promotion):
    """Promotion where every second item is half-price.

    Args:
        name (str): The name of the promotion.
    """

    def __init__(self, name) -> None:
        super().__init__(name)

    def apply_promotions(self, product, quantity) -> float:
        """Applies the second-half price promotion to the product's price."""
        total_price = 0
        for n in range(1, quantity + 1):
            if n % 2 == 0:
                total_price += product.price / 2
            else:
                total_price += product.price
            if not isinstance(product, products.NonStockedProduct):
                product.quantity -= 1
                products.Product.total_quantity -= 1
        return total_price


class ThirdOneFree(Promotion):
    """Promotion where every third item is free.

    Args:
        name (str): The name of the promotion.
    """

    def __init__(self, name) -> None:
        super().__init__(name)

    def apply_promotions(self, product, quantity) -> float:
        """Applies the third-one-free promotion to the product's price."""

        total_price = 0
        for n in range(1, quantity + 1):
            if n % 3 == 0:
                pass
            else:
                total_price += product.price
            if not isinstance(product, products.NonStockedProduct):
                product.quantity -= quantity
                products.Product.total_quantity -= quantity
        return total_price
