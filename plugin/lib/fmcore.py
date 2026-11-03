"""Old import path, kept for two releases (T-2742): the module is sampo.core."""
import sys
import sampo.core
sys.modules[__name__] = sys.modules["sampo.core"]
