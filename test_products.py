from products import Product, NonStockedProduct, LimitedProduct
import pytest


# Class Product
def test_product_instantiation():
    """Test correct instantiation of Product object"""
    product = Product("MacBook Air M2", price=10, quantity=100)
    assert isinstance(product, Product), "product has not created a Product"
    assert product.name == "MacBook Air M2", "product has wrong name"
    assert product.price == 10, "product has wrong price"
    assert product._quantity == 100, "product has wrong quantity"
    assert product.is_active(), "product is not active"


def test_product_without_name():
    """Test that omitting name when instantiating Product raises ValueError"""
    with pytest.raises(ValueError) as error:
        Product("", price=1450, quantity=100)
    assert str(error.value) == "Product name must have at least one letter!"


def test_product_with_negative_price():
    """Test that a negative price when instantiating a Product
    raises an ValueError
    """
    with pytest.raises(ValueError) as error:
        Product("MacBook Air M2", price=-10, quantity=100)
    assert str(error.value) == "Price must be 0 or positive!"


def test_price_type():
    """Test that a wrong price types raise a TypeError"""
    price_arguments = ["ten", "", None, True, [1, "", "Hello"], False, [], {}]

    for argument in price_arguments:
        with pytest.raises(TypeError) as error:
            Product("MacBook Air M2", price=argument, quantity=100)
        assert (
            str(error.value) == "Price must be an integer or a float!"
        ), f"Failed with type:'{type(argument)}'"


def test_quantity_update():
    product = Product("MacBook Air M2", price=10, quantity=10)
    product.quantity -= 9
    assert product.quantity == 1, "product has wrong quantity"


# Test that when a product reaches 0 quantity, it becomes inactive.
def test_product_inactive():
    product = Product("MacBook Air M2", price=10, quantity=0)

    assert not product.is_active(), "product was not set to inactive"


# Test that product purchase modifies the quantity and returns the right output.
def test_product_buy():
    product = Product("MacBook Air M2", price=10, quantity=10)
    product.buy(5)
    assert product.quantity == 5, "left quantity is not correct"
    product.buy(4)
    assert product.quantity == 1, "left quantity is not correct"


# Test that buying a larger quantity than exists invokes exception.
def test_exceed_quantity():
    product = Product("MacBook Air M2", price=10, quantity=10)
    with pytest.raises(ValueError) as error:
        product.buy(11)
    assert (
        str(error.value)
        == f"Cannot buy more {product.name}'s than {product.quantity}"
    )


# ----------------------------------------------------------------------------


# Class NonStockedProduct
def test_non_stocked_product_instantiation():
    product = NonStockedProduct("Windows License", price=125)
    assert isinstance(
        product, NonStockedProduct
    ), "product has not created a Product"
    assert product.name == "Windows License", "product has wrong name"
    assert product.price == 125, "product has wrong price"
    assert product._quantity == 0, "product has wrong quantity"
    assert product.is_active(), "product is not active"


def test_quantity_not_zero():
    product = NonStockedProduct("Windows License", price=125)
    quantities = [1, 12, -11, -1]
    for quantity in quantities:
        with pytest.raises(ValueError) as error:
            product.quantity = 10
        assert str(error.value) == "Non stocked products have no quantity"

    assert product.quantity == 0


# ----------------------------------------------------------------------------


# Class LimitedProduct
def test_limited_product_instantiation():
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    assert isinstance(
        product, LimitedProduct
    ), "product has not created a Product"
    assert product.name == "Shipping", "product has wrong name"
    assert product.price == 10, "product has wrong price"
    assert product._quantity == 250, "product has wrong quantity"
    assert product._maximum == 1, "product has wrong maximum"
    assert product.is_active(), "product is not active"
