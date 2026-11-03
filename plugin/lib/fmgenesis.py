"""Old import path, kept for two releases (T-2742): the module is sampo.rune."""
import sys
import sampo.rune
sys.modules[__name__] = sys.modules["sampo.rune"]
