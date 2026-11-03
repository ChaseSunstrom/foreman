"""Old import path, kept for two releases (T-2742): the module is sampo.serve."""
import sys
import sampo.serve
sys.modules[__name__] = sys.modules["sampo.serve"]
