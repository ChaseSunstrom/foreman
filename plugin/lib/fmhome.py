"""Old import path, kept for two releases (T-2742): the module is sampo.home."""
import sys
import sampo.home
sys.modules[__name__] = sys.modules["sampo.home"]
