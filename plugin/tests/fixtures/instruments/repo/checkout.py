from shop import Cart


def checkout(items, code=None):
    cart = Cart(items, discount=10 if code == "TEN" else 0)
    return round(cart.total(), 2)


def receipt(items):
    return f"{Cart(items).describe()}: {checkout(items)}"


HELP = "cart.total() prices a cart"  # a string, not a call
