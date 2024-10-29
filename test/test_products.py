import pytest
from app.products import LimitedProduct, NonStockedProduct, Product
from app.promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree


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
    """Test that product quantity updates correctly when modified"""
    product = Product("MacBook Air M2", price=10, quantity=10)
    product.quantity -= 9
    assert product.quantity == 1, "product has wrong quantity"


# Test that when a product reaches 0 quantity, it becomes inactive.
def test_product_inactive():
    """Test that product becomes inactive when quantity reaches zero"""
    product = Product("MacBook Air M2", price=10, quantity=0)

    assert not product.is_active(), "product was not set to inactive"


# Test that product purchase modifies the quantity and returns the right output.
def test_product_buy():
    """Test that product purchase updates quantity correctly and returns expected value"""
    product = Product("MacBook Air M2", price=10, quantity=10)
    product.buy(5)
    assert product.quantity == 5, "left quantity is not correct"
    product.buy(4)
    assert product.quantity == 1, "left quantity is not correct"


# ----------------------------------------------------------------------------


# Class NonStockedProduct
def test_non_stocked_product_instantiation():
    """Test correct instantiation of NonStockedProduct object"""
    product = NonStockedProduct("Windows License", price=125)
    assert isinstance(
        product, NonStockedProduct
    ), "product has not created a Product"
    assert product.name == "Windows License", "product has wrong name"
    assert product.price == 125, "product has wrong price"
    assert product._quantity == 0, "product has wrong quantity"
    assert product.is_active(), "product is not active"


def test_quantity_not_zero():
    """Test that quantity remains zero for NonStockedProduct instances"""
    product = NonStockedProduct("Windows License", price=125)
    quantities = [1, 12, -11, -1]
    for quantity in quantities:
        with pytest.raises(ValueError) as error:
            product.quantity = 10
        assert str(error.value) == "Non stocked products have no quantity"

    assert product.quantity == 0, "quantity is not set to zero"


# ----------------------------------------------------------------------------


# Class LimitedProduct
def test_limited_product_instantiation():
    """Test correct instantiation of LimitedProduct object"""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    assert isinstance(
        product, LimitedProduct
    ), "product has not created a Product"
    assert product.name == "Shipping", "product has wrong name"
    assert product.price == 10, "product has wrong price"
    assert product._quantity == 250, "product has wrong quantity"
    assert product._maximum == 1, "product has wrong maximum"
    assert product.is_active(), "product is not active"


def test_maximum():
    """Test that LimitedProduct obeys maximum quantity per purchase"""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    assert product.buy(1) == 10
    assert product.quantity == 249
    assert product.buy(2) == 10
    assert product.quantity == 248


# ----------------------------------------------------------------------------


# Class Promotion
def initiate_promotions():
    """Initiates product and promotion instances for testing"""
    product_list = [
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        Product("Shipping", price=10, quantity=250),
    ]

    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[2].set_promotion(thirty_percent)

    return product_list


def test_promotion_instantiation():
    """Test that promotions are instantiated and set correctly on products"""
    second_half, third_free, thirty_percent = initiate_promotions()
    assert isinstance(second_half, Product)
    assert second_half.promotion == "Second Half price!"
    assert isinstance(third_free, Product)
    assert third_free.promotion == "Third One Free!"
    assert isinstance(thirty_percent, Product)
    assert thirty_percent.promotion == "30% off!"


def test_promotion_calculation():
    """Test that promotion discounts are calculated correctly"""
    second_half, third_free, thirty_percent = initiate_promotions()

    assert second_half.buy(1) == 500, "wrong calculation"
    assert second_half.buy(2) == 750, "wrong calculation"
    assert second_half.buy(3) == 1250, "wrong calculation"

    assert third_free.buy(1) == 125, "wrong calculation"
    assert third_free.buy(2) == 250, "wrong calculation"
    assert third_free.buy(3) == 250, "wrong calculation"
    assert third_free.buy(4) == 375, "wrong calculation"

    assert thirty_percent.buy(1) == 7, "wrong calculation"
    assert thirty_percent.buy(2) == 14, "wrong calculation"
