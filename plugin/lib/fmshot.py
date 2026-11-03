"""Old import path, kept for two releases (T-2742): the module is sampo.shot."""
import sys
import sampo.shot
sys.modules[__name__] = sys.modules["sampo.shot"]
