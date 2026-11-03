"""Old import path, kept for two releases (T-2742): the module is sampo.moons."""
import sys
import sampo.moons
sys.modules[__name__] = sys.modules["sampo.moons"]
