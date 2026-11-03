"""Old import path, kept for two releases (T-2742): the module is sampo.reverify."""
import sys
import sampo.reverify
sys.modules[__name__] = sys.modules["sampo.reverify"]
