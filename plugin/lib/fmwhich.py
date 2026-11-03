"""Old import path, kept for two releases (T-2742): the module is sampo.which."""
import sys
import sampo.which
sys.modules[__name__] = sys.modules["sampo.which"]
