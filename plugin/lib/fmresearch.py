"""Old import path, kept for two releases (T-2742): the module is sampo.research."""
import sys
import sampo.research
sys.modules[__name__] = sys.modules["sampo.research"]
