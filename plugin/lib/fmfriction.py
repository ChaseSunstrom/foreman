"""Old import path, kept for two releases (T-2742): the module is sampo.friction."""
import sys
import sampo.friction
sys.modules[__name__] = sys.modules["sampo.friction"]
