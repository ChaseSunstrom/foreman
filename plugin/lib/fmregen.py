"""Old import path, kept for two releases (T-2742): the module is sampo.regen."""
import sys
import sampo.regen
sys.modules[__name__] = sys.modules["sampo.regen"]
