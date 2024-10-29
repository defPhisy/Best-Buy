"""
Module for representing different types of products in an inventory
with support for promotions and stock control.

Classes:
    Product: Basic product with a price, quantity, and optional promotion.
    NonStockedProduct: Product that does not maintain stock
    (always available, quantity set to zero).
    LimitedProduct: Product with a maximum purchase limit per transaction.

Each class includes methods for activating/deactivating products,
displaying product information, and handling purchases.
"""

from promotions import Promotion


class Product:
    total_quantity = 0

    def __init__(self, name: str, price: float, quantity: int) -> None:
        if self.name_is_valid(name):
            self.name = name

        if self.price_is_valid(price):
            self.price = price

        if self.quantity_is_valid(quantity):
            self._quantity = quantity

        if self._quantity == 0:
            self.active = False
        else:
            self.active = True

        self._promotion = None

        Product.total_quantity += quantity

    def __str__(self) -> str:
        """Returns the product name."""
        return self.name

    def name_is_valid(self, name: str) -> bool:
        """Checks if the provided name is valid.

        Args:
            name (str): The name of the product.

        Returns:
            bool: True if the name is valid; raises ValueError otherwise.
        """

        if name:
            return True
        else:
            raise ValueError("Product name must have at least one letter!")

    def price_is_valid(self, price: float) -> bool:
        """Checks if the provided price is valid.

        Args:
            price (float): The price of the product.

        Returns:
            bool: True if the price is valid; raises TypeError
            or ValueError otherwise.
        """

        test = []
        if type(price) is float or type(price) is int:
            test.append(True)
        else:
            raise TypeError("Price must be an integer or a float!")
        if price >= 0:
            test.append(True)
        else:
            raise ValueError("Price must be 0 or positive!")
        return all(test)

    def quantity_is_valid(self, quantity: int) -> bool:
        """Checks if the provided quantity is valid.

        Args:
            quantity (int): The quantity of the product.

        Returns:
            bool: True if the quantity is valid; raises Exception otherwise.
        """

        if type(quantity) is int and quantity >= 0:
            return True
        else:
            raise Exception("Quantity must be a positive integer")

    @property
    def quantity(self) -> int:
        """Returns the current quantity of the product."""

        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int) -> None:
        """Sets the product quantity and deactivates the product
        if quantity reaches zero.

        Args:
            quantity (int): New quantity of the product.
        """

        if self.quantity_is_valid(quantity):
            self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()
        if self._quantity < 0:
            raise ValueError(
                f"Cannot buy more {self.name}'s than {self._quantity}"
            )

    @property
    def promotion(self):
        """Returns the name of the current promotion if any."""

        if self._promotion:
            return self._promotion.name

    @promotion.setter
    def promotion(self, promotion_obj: Promotion) -> None:
        """Sets the product's promotion."""

        self.set_promotion(promotion_obj)

    def set_promotion(self, promotion_obj: Promotion) -> None:
        """Sets a promotion for the product.

        Args:
            promotion_obj (Promotion): The promotion to apply to the product.
        """

        self._promotion = promotion_obj

    def is_active(self) -> bool:
        """Checks if the product is active.

        Returns:
            bool: True if the product is active; False otherwise.
        """

        return self.active

    def activate(self) -> None:
        """Activates the product."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivates the product."""
        self.active = False

    def show(self) -> str:
        """Returns a string describing the product with its name, price,
        quantity, and promotion details.

        Returns:
            str: Description of the product.
        """

        text = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if isinstance(self._promotion, Promotion):
            text += f", Promotion: {self.promotion}"
        return text

    def buy(self, quantity: int) -> float:
        """Processes a purchase of the product, reducing its quantity
        and applying promotions if available.

        Args:
            quantity (int): The amount of product to purchase.

        Returns:
            float: The total price for the quantity bought.
        """
        if isinstance(self._promotion, Promotion):
            return self._promotion.apply_promotions(self, quantity)
        else:
            self._quantity -= quantity
            Product.total_quantity -= quantity
            return self.price * quantity


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int = 0) -> None:
        super().__init__(name, price, quantity)
        self.activate()

    @property
    def quantity(self) -> int:
        """Returns the quantity of the product, always zero."""

        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int) -> None:
        """Prevents changing the quantity;
        always keeps it zero for non-stocked products."""

        if quantity != 0:
            raise ValueError("Non stocked products have no quantity")

        self._quantity = 0

    def show(self) -> str:
        """Returns a string describing the product with its name and price,
        without quantity.

        Returns:
            str: Description of the product.
        """

        text = f"{self.name}, Price: {self.price}"
        if isinstance(self._promotion, Promotion):
            text += f", Promotion: {self.promotion}"
        return text

    def buy(self, quantity: int) -> float:
        """Processes a purchase of the non-stocked product,
        applying promotions if available.

        Args:
            quantity (int): The amount of product to purchase.

        Returns:
            float: The total price for the quantity bought.
        """

        if isinstance(self._promotion, Promotion):
            return self._promotion.apply_promotions(self, quantity)
        else:
            return self.price * quantity


class LimitedProduct(Product):
    def __init__(
        self, name: str, price: float, quantity: int, maximum: int
    ) -> None:
        super().__init__(name, price, quantity)
        self._maximum = maximum

    def show(self) -> str:
        """Returns a string describing the product with its name, price,
        quantity, and maximum purchase limit.

        Returns:
            str: Description of the product.
        """

        text = (
            f"{self.name}, Price: {self.price}, Quantity: {self._quantity}"
            + f", Maximum: {self._maximum}"
        )
        if isinstance(self._promotion, Promotion):
            text += f", Promotion: {self.promotion}"
        return text

    def buy(self, quantity: int) -> float:
        """Processes a purchase of the product, respecting the maximum
        purchase limit and applying promotions if available.

        Args:
            quantity (int): The quantity of the product
            the customer wants to buy.

        Returns:
            float: The total price for the quantity bought,
            adjusted to the maximum if exceeded.

        Note:
            If the requested quantity exceeds the allowed maximum,
            the purchase amount is limited to the maximum quantity
            for this product.
        """

        if quantity > self._maximum:
            print(f"Cannot buy more than {self._maximum} {self.name}'s!")
            quantity = self._maximum
        if isinstance(self._promotion, Promotion):
            return self._promotion.apply_promotions(self, self._maximum)
        else:
            self._quantity -= quantity
            Product.total_quantity -= quantity
            return self.price * quantity
