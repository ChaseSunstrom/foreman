"""Old import path, kept for two releases (T-2742): the module is sampo.away."""
import sys
import sampo.away
sys.modules[__name__] = sys.modules["sampo.away"]
