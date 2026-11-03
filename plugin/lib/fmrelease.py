"""Old import path, kept for two releases (T-2742): the module is sampo.release."""
import sys
import sampo.release
sys.modules[__name__] = sys.modules["sampo.release"]
