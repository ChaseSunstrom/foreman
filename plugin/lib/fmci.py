"""Old import path, kept for two releases (T-2742): the module is sampo.ci."""
import sys
import sampo.ci
sys.modules[__name__] = sys.modules["sampo.ci"]
