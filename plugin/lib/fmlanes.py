"""Old import path, kept for two releases (T-2742): the module is sampo.lanes."""
import sys
import sampo.lanes
sys.modules[__name__] = sys.modules["sampo.lanes"]
