"""Old import path, kept for two releases (T-2742): the module is sampo.smoke."""
import sys
import sampo.smoke
sys.modules[__name__] = sys.modules["sampo.smoke"]
