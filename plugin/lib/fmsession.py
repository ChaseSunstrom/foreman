"""Old import path, kept for two releases (T-2742): the module is sampo.session."""
import sys
import sampo.session
sys.modules[__name__] = sys.modules["sampo.session"]
