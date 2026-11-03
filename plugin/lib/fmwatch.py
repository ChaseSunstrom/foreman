"""Old import path, kept for two releases (T-2742): the module is sampo.watch."""
import sys
import sampo.watch
sys.modules[__name__] = sys.modules["sampo.watch"]
