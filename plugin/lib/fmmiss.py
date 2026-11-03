"""Old import path, kept for two releases (T-2742): the module is sampo.miss."""
import sys
import sampo.miss
sys.modules[__name__] = sys.modules["sampo.miss"]
