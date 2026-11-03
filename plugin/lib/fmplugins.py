"""Old import path, kept for two releases (T-2742): the module is sampo.plugins."""
import sys
import sampo.plugins
sys.modules[__name__] = sys.modules["sampo.plugins"]
