"""Old import path, kept for two releases (T-2742): the module is sampo.selfcheck."""
import sys
import sampo.selfcheck
sys.modules[__name__] = sys.modules["sampo.selfcheck"]
