"""Old import path, kept for two releases (T-2742): the module is sampo.extras."""
import sys
import sampo.extras
sys.modules[__name__] = sys.modules["sampo.extras"]
