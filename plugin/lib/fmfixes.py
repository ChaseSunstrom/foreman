"""Old import path, kept for two releases (T-2742): the module is sampo.fixes."""
import sys
import sampo.fixes
sys.modules[__name__] = sys.modules["sampo.fixes"]
