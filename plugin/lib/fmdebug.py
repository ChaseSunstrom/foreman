"""Old import path, kept for two releases (T-2742): the module is sampo.debug."""
import sys
import sampo.debug
sys.modules[__name__] = sys.modules["sampo.debug"]
