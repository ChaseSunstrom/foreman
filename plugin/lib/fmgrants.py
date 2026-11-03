"""Old import path, kept for two releases (T-2742): the module is sampo.grants."""
import sys
import sampo.grants
sys.modules[__name__] = sys.modules["sampo.grants"]
