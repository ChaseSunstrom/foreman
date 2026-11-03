"""Old import path, kept for two releases (T-2742): the module is sampo.img."""
import sys
import sampo.img
sys.modules[__name__] = sys.modules["sampo.img"]
