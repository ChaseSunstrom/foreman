"""Old import path, kept for two releases (T-2742): the module is sampo.find."""
import sys
import sampo.find
sys.modules[__name__] = sys.modules["sampo.find"]
