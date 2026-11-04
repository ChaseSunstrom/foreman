"""Old import path, kept for two releases (T-2742): the module is sampo.mint (T-2978)."""
import sys
import sampo.mint
sys.modules[__name__] = sys.modules["sampo.mint"]
