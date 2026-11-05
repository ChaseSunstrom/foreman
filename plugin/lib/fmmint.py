"""Old import path, kept for two releases (T-2742): the module is sampo.mint."""
import sys
import sampo.mint
sys.modules[__name__] = sys.modules["sampo.mint"]
