"""Old import path, kept for two releases (T-2742): the module is sampo.lib."""
import sys
import sampo.lib
sys.modules[__name__] = sys.modules["sampo.lib"]
