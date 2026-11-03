"""Old import path, kept for two releases (T-2742): the module is sampo.smith."""
import sys
import sampo.smith
sys.modules[__name__] = sys.modules["sampo.smith"]
