"""Old import path, kept for two releases (T-2742): the module is sampo.moonscale."""
import sys
import sampo.moonscale
sys.modules[__name__] = sys.modules["sampo.moonscale"]
