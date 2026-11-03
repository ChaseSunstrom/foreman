"""Old import path, kept for two releases (T-2742): the module is sampo.ideas."""
import sys
import sampo.ideas
sys.modules[__name__] = sys.modules["sampo.ideas"]
