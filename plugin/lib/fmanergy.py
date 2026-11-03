"""Old import path, kept for two releases (T-2742): the module is sampo.anergy."""
import sys
import sampo.anergy
sys.modules[__name__] = sys.modules["sampo.anergy"]
