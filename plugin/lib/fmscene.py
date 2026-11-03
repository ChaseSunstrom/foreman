"""Old import path, kept for two releases (T-2742): the module is sampo.scene."""
import sys
import sampo.scene
sys.modules[__name__] = sys.modules["sampo.scene"]
