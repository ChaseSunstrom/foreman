"""Old import path, kept for two releases (T-2742): the module is sampo.sync."""
import sys
import sampo.sync
sys.modules[__name__] = sys.modules["sampo.sync"]
