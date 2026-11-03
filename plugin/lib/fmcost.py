"""Old import path, kept for two releases (T-2742): the module is sampo.cost."""
import sys
import sampo.cost
sys.modules[__name__] = sys.modules["sampo.cost"]
