"""
Command-Line Interface (CLI) for managing and purchasing products from a store.

This module provides a CLI for interacting with a `Store` object,
allowing users to view products, check total quantities, and place orders.
Products in the store can have different promotion types,
including "Second Half Price," "Third One Free,"
and percentage-based discounts.


Usage:
    Run the script to start the CLI, view products, and place orders. Example:

    $ python cli.py

Dependencies:
    Requires the `store`, `products`, and `promotions` modules.
"""

from typing import NoReturn
from products import Product, NonStockedProduct, LimitedProduct
from store import Store
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount


def main() -> NoReturn:
    """Initializes the store's product catalog, sets up promotions,
    and starts the CLI."""

    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[2].set_promotion(second_half_price)
    product_list[3].set_promotion(third_one_free)
    product_list[4].set_promotion(thirty_percent)
    best_buy = Store(product_list)
    start(best_buy)


def start(store_obj: Store) -> NoReturn:
    """Starts the command-line interface for the store,
    displaying a menu and handling user input.

    Args:
        store_obj (Store): The store object for managing products
        and handling orders.
    """

    menu = get_menu_dict()
    menu_numbers = [str(number) for number in menu]
    while True:
        print_menu()
        user_input = input("Please choose a number: ")
        if user_input not in menu_numbers:
            print("Error with your choice! Try again!")
            print()
            continue
        else:
            menu_num = int(user_input)

        call_command(menu_num, store_obj)
        print()


def get_menu_dict() -> dict:
    """Returns a dictionary mapping menu options to their descriptions and functions.

    Returns:
        dict: The menu dictionary containing options and corresponding functions.
    """
    MENU = {
        1: ["List all products in store", print_all_products],
        2: ["Show total amount in store", print_total_amount],
        3: ["Make an order", make_order],
        4: ["Quit", quit],
    }
    return MENU


def print_menu() -> None:
    """Displays the store menu options to the user."""

    print("\tStore Menu")
    print("\t----------")
    menu = get_menu_dict()
    for i, item_lst in menu.items():
        print(f"{i}. {item_lst[0]}")


def call_command(num: int, store_obj: Store):
    """Calls the appropriate function from the menu dictionary
    based on user input.

    Args:
        num (int): The menu option selected by the user.
        store_obj (Store): The store object used for executing commands.
    """

    menu = get_menu_dict()
    # num 4 = quit app
    if num != 4:
        return menu[num][1](store_obj)
    else:
        return menu[num][1]()


def print_all_products(store_obj: Store) -> None:
    """Displays all products in the store with their name, price, and quantity.

    Args:
        store_obj (Store): The store object containing the products.
    """
    print("----------")
    products = store_obj.get_all_products()
    for i, product in enumerate(products):
        print(f"{i + 1}. {product.show()}")
    print("----------")


def print_total_amount(store_obj: Store) -> None:
    """Displays the total quantity of all items available in the store.

    Args:
        store_obj (Store): The store object containing the products.
    """

    products = store_obj.get_all_products()
    quantity = sum([product.quantity for product in products])
    print(f"Total of {quantity} items in store")


def make_order(store_obj: Store) -> None:
    """Processes a user's order by adding selected products to the cart
    and completing the purchase.

    Args:
        store_obj (Store): The store object used for retrieving
        product information and processing the order.
    """

    print_all_products(store_obj)
    print()
    print("When you want to finish order, enter empty text.")

    products = store_obj.get_all_products()
    order_list = []
    while True:
        product_message = "Which product # do you want? "
        product_index = get_product_index_from_user(store_obj, product_message)

        if product_index:
            product = products[int(product_index) - 1]
        else:
            product = None

        quantity_message = "What amount do you want? "
        quantity = get_quantity_from_user(product, quantity_message)

        if product_index and quantity:
            order_list.append((product, quantity))
            print("Product added to list!")
            print()
        else:
            break

    if order_list:
        print(store_obj.order(order_list))
        print()


def get_product_index_from_user(store_obj: Store, message: str) -> int | None:
    """Prompts the user to select a product index and validates the input.

    Args:
        store_obj (Store): The store object used for retrieving
        product details.
        message (str): The message displayed to prompt the user.

    Returns:
        int | None: The validated product index, or None if input is empty.
    """

    products = store_obj.get_all_products()
    error = (
        f"Only numbers between 1-{len(products)} are allowed!\n"
        + "Please try again!"
    )

    while True:
        num = input(message)
        if not num:
            return None
        if num == "0":
            print("Only positive numbers are allowed")
            continue
        else:
            try:
                num = int(num)
                if num < 0:
                    print("Only positive numbers are allowed")
                    continue

                product = products[num - 1]

                if not product.active:
                    print(
                        f"There are no {product.name} left. Try another product"
                    )
                    continue
            except ValueError:
                print(error)
                continue
            except IndexError:
                print(error)
                continue
            else:
                break
    return num


def get_quantity_from_user(
    product: Product | None, message: str
) -> int | None:
    """Prompts the user to enter a quantity and validates the input
    against available stock.

    Args:
        product (Product): The product for which quantity is requested.
        message (str): The message displayed to prompt the user.

    Returns:
        int | None: The validated quantity, or None if input is empty.
    """
    if not product:
        input("You picked no product. Enter to leave!")
        return None
    while True:
        num = input(message)
        if not num:
            return None
        if num == "0":
            print("Only positive numbers are allowed")
            continue
        else:
            try:
                num = int(num)
            except ValueError:
                print(
                    f"Must be a positive number between 1-{product.quantity}"
                )
                continue
            else:
                if product.quantity < num and not isinstance(
                    product, NonStockedProduct
                ):
                    print(
                        f"There are only {product.quantity} {product.name} in stock!\n"
                        + f"Amount cannot be higher than {product.quantity}!"
                    )
                    continue
                else:
                    break
    return num


if __name__ == "__main__":
    main()
