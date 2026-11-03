"""Old import path, kept for two releases (T-2742): the module is sampo.edit."""
import sys
import sampo.edit
sys.modules[__name__] = sys.modules["sampo.edit"]
