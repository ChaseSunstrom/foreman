"""Old import path, kept for two releases (T-2742): the module is sampo.stack."""
import sys
import sampo.stack
sys.modules[__name__] = sys.modules["sampo.stack"]
