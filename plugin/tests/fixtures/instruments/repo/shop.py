"""A small shop: carts, discounts and tax (fixture for fm sym)."""
from decimal import Decimal

TAX_RATE = Decimal("0.2")


def apply_discount(price, pct):
    """Price after a percentage discount."""
    return price - price * pct / 100


def unrelated_report(rows):
    """A long function fm sym must not print when asked for Cart.total."""
    out = []
    for r in rows:
        out.append(f"report row {r}")
        out.append(f"report row {r} again")
        out.append(f"report row {r} once more")
    out.sort()
    out.reverse()
    out.append("report end")
    return out


class Cart:
    def __init__(self, items, discount=0):
        self.items = items
        self.discount = discount

    def subtotal(self):
        return sum(price * qty for price, qty in self.items)

    def total(self):
        """What the customer pays: the discounted subtotal plus tax."""
        net = apply_discount(self.subtotal(), self.discount)
        return net + net * TAX_RATE * 100

    def describe(self):
        return f"{len(self.items)} items, {self.discount}% off"
