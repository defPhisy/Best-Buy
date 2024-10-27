from products import Product
import pytest


def test_product_instantiation():
    """Test correct instantiation of Product object"""
    product = Product("MacBook Air M2", price=10, quantity=100)
    assert isinstance(product, Product), "product has not created a Product"
    assert product.name == "MacBook Air M2", "product has wrong name"
    assert product.price == 10, "product has wrong price"
    assert product._quantity == 100, "product has wrong quantity"
    assert product.is_active()


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
    price_arguments = ["ten", "", None, True, [1, 3], False, [], {}]

    for argument in price_arguments:
        with pytest.raises(TypeError) as error:
            Product("MacBook Air M2", price=argument, quantity=100)
        assert str(error.value) == "Price must be an integer or a float!"


def test_quantity():
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
