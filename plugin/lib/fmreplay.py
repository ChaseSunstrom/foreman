"""Old import path, kept for two releases (T-2742): the module is sampo.replay."""
import sys
import sampo.replay
sys.modules[__name__] = sys.modules["sampo.replay"]
