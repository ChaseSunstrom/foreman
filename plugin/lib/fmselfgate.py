"""Old import path, kept for two releases (T-2742): the module is sampo.selfgate."""
import sys
import sampo.selfgate
sys.modules[__name__] = sys.modules["sampo.selfgate"]
