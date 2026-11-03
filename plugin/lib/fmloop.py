"""Old import path, kept for two releases (T-2742): the module is sampo.loop."""
import sys
import sampo.loop
sys.modules[__name__] = sys.modules["sampo.loop"]
