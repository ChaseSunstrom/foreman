"""Old import path, kept for two releases (T-2742): the module is sampo.taste."""
import sys
import sampo.taste
sys.modules[__name__] = sys.modules["sampo.taste"]
