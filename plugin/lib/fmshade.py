"""Old import path, kept for two releases (T-2742): the module is sampo.shade."""
import sys
import sampo.shade
sys.modules[__name__] = sys.modules["sampo.shade"]
