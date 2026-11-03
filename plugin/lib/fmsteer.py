"""Old import path, kept for two releases (T-2742): the module is sampo.steer."""
import sys
import sampo.steer
sys.modules[__name__] = sys.modules["sampo.steer"]
