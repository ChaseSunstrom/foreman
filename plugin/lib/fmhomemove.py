"""Old import path, kept for two releases (T-2742): the module is sampo.homemove."""
import sys
import sampo.homemove
sys.modules[__name__] = sys.modules["sampo.homemove"]
