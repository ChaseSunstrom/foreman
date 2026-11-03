"""Old import path, kept for two releases (T-2742): the module is sampo.eco."""
import sys
import sampo.eco
sys.modules[__name__] = sys.modules["sampo.eco"]
