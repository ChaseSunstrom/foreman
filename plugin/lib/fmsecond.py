"""Old import path, kept for two releases (T-2742): the module is sampo.second."""
import sys
import sampo.second
sys.modules[__name__] = sys.modules["sampo.second"]
