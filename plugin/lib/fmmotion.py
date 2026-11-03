"""Old import path, kept for two releases (T-2742): the module is sampo.motion."""
import sys
import sampo.motion
sys.modules[__name__] = sys.modules["sampo.motion"]
