"""Old import path, kept for two releases (T-2742): the module is sampo.night."""
import sys
import sampo.night
sys.modules[__name__] = sys.modules["sampo.night"]
