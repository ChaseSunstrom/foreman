"""Old import path, kept for two releases (T-2742): the module is sampo.dojo."""
import sys
import sampo.dojo
sys.modules[__name__] = sys.modules["sampo.dojo"]
