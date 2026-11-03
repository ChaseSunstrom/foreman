"""Old import path, kept for two releases (T-2742): the module is sampo.bus."""
import sys
import sampo.bus
sys.modules[__name__] = sys.modules["sampo.bus"]
