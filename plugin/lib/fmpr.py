"""Old import path, kept for two releases (T-2742): the module is sampo.pr."""
import sys
import sampo.pr
sys.modules[__name__] = sys.modules["sampo.pr"]
