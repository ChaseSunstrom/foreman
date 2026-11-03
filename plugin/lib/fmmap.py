"""Old import path, kept for two releases (T-2742): the module is sampo.map."""
import sys
import sampo.map
sys.modules[__name__] = sys.modules["sampo.map"]
