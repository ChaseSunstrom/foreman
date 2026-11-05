"""Old import path, kept for two releases (T-2742): the module is sampo.works."""
import sys
import sampo.works
sys.modules[__name__] = sys.modules["sampo.works"]
