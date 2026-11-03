"""Old import path, kept for two releases (T-2742): the module is sampo.setup."""
import sys
import sampo.setup
sys.modules[__name__] = sys.modules["sampo.setup"]
