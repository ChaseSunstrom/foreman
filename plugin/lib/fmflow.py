"""Old import path, kept for two releases (T-2742): the module is sampo.flow."""
import sys
import sampo.flow
sys.modules[__name__] = sys.modules["sampo.flow"]
