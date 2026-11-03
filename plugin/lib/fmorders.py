"""Old import path, kept for two releases (T-2742): the module is sampo.orders."""
import sys
import sampo.orders
sys.modules[__name__] = sys.modules["sampo.orders"]
