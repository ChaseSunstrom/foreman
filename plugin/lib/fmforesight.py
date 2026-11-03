"""Old import path, kept for two releases (T-2742): the module is sampo.foresight."""
import sys
import sampo.foresight
sys.modules[__name__] = sys.modules["sampo.foresight"]
