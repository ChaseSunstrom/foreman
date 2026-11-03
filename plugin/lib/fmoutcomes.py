"""Old import path, kept for two releases (T-2742): the module is sampo.outcomes."""
import sys
import sampo.outcomes
sys.modules[__name__] = sys.modules["sampo.outcomes"]
