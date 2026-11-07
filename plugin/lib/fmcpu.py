"""Old import path, kept for two releases (T-2742): the module is sampo.cpu."""
import sys
import sampo.cpu
sys.modules[__name__] = sys.modules["sampo.cpu"]
