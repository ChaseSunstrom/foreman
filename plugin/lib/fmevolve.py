"""Old import path, kept for two releases (T-2742): the module is sampo.evolve."""
import sys
import sampo.evolve
sys.modules[__name__] = sys.modules["sampo.evolve"]
