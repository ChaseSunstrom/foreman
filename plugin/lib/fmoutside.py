"""Old import path, kept for two releases (T-2742): the module is sampo.outside."""
import sys
import sampo.outside
sys.modules[__name__] = sys.modules["sampo.outside"]
