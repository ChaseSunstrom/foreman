"""Prices with VAT (fixture for fm fail and fm trace)."""
RATES = {"standard": 0.2, "reduced": 0.05}


def rate_for(kind):
    return RATES[kind]


def with_vat(amount, kind="std"):
    return round(amount * (1 + rate_for(kind)), 2)


def refund(amount):
    if amount < 0:
        raise ValueError("negative refund")
    return -amount
