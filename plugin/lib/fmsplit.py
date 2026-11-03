"""Old import path, kept for two releases (T-2742): the module is sampo.split."""
import sys
import sampo.split
sys.modules[__name__] = sys.modules["sampo.split"]
