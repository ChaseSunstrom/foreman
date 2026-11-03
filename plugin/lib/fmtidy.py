"""Old import path, kept for two releases (T-2742): the module is sampo.tidy."""
import sys
import sampo.tidy
sys.modules[__name__] = sys.modules["sampo.tidy"]
