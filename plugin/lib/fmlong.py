"""Old import path, kept for two releases (T-2742): the module is sampo.long."""
import sys
import sampo.long
sys.modules[__name__] = sys.modules["sampo.long"]
