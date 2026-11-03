"""Old import path, kept for two releases (T-2742): the module is sampo.triggers."""
import sys
import sampo.triggers
sys.modules[__name__] = sys.modules["sampo.triggers"]
