"""Old import path, kept for two releases (T-2742): the module is sampo.sandbox."""
import sys
import sampo.sandbox
sys.modules[__name__] = sys.modules["sampo.sandbox"]
