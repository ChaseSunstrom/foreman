"""Old import path, kept for two releases (T-2742): the module is sampo.drill."""
import sys
import sampo.drill
sys.modules[__name__] = sys.modules["sampo.drill"]
