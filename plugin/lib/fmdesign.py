"""Old import path, kept for two releases (T-2742): the module is sampo.design."""
import sys
import sampo.design
sys.modules[__name__] = sys.modules["sampo.design"]
