"""CLI to make orders from Store"""

from typing import NoReturn
from products import Product
from store import Store


def main() -> NoReturn:
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
    ]
    best_buy = Store(product_list)
    start(best_buy)


def start(store_obj) -> NoReturn:
    """Start CLI of store_obj"""
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
    """Get dictionary with menu structure and corresponding functions"""
    MENU = {
        1: ["List all products in store", print_all_products],
        2: ["Show total amount in store", print_total_amount],
        3: ["Make an order", make_order],
        4: ["Quit", quit],
    }
    return MENU


def print_menu() -> None:
    """Print menu from menu dictionary"""
    print("\tStore Menu")
    print("\t----------")
    menu = get_menu_dict()
    for i, item_lst in menu.items():
        print(f"{i}. {item_lst[0]}")


def call_command(num: int, store_obj):
    """Pick and call function from menu dictionary"""
    menu = get_menu_dict()
    # num 4 = quit app
    if num != 4:
        return menu[num][1](store_obj)
    else:
        return menu[num][1]()


def print_all_products(store_obj) -> None:
    """Print all products with name, price and quantity"""
    print("----------")
    products = store_obj.get_all_products()
    for i, product in enumerate(products):
        print(f"{i + 1}. {product.show()}")
    print("----------")


def print_total_amount(store_obj) -> None:
    """Print total amount of all items in store"""
    products = store_obj.get_all_products()
    quantity = sum([product.quantity for product in products])
    print(f"Total of {quantity} items in store")


def make_order(store_obj) -> None:
    """Run order process.
    User can add items to shopping cart and buy them, if available"""
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
        quantity = get_amount_from_user(product, quantity_message)

        if product_index and quantity:
            order_list.append((product, quantity))
            print("Product added to list!")
            print()
        else:
            break

    if order_list:
        print(store_obj.order(order_list))
        print()


def get_product_index_from_user(store_obj, message) -> int | None:
    """Prompts user and validates input for a product index"""
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


def get_amount_from_user(product, message) -> int | None:
    """Prompts user and validates input for a product quantity"""
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
                if product.quantity < num:
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
