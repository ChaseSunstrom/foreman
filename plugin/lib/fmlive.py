"""Old import path, kept for two releases (T-2742): the module is sampo.live."""
import sys
import sampo.live
sys.modules[__name__] = sys.modules["sampo.live"]
