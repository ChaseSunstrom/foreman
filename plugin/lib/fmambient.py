"""Old import path, kept for two releases (T-2742): the module is sampo.ambient."""
import sys
import sampo.ambient
sys.modules[__name__] = sys.modules["sampo.ambient"]
