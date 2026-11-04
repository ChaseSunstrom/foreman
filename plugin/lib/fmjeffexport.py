"""Old import path, kept for two releases (T-2742): the module is sampo.jeffexport."""
import sys
import sampo.jeffexport
sys.modules[__name__] = sys.modules["sampo.jeffexport"]
