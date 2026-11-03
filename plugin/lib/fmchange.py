"""Old import path, kept for two releases (T-2742): the module is sampo.change."""
import sys
import sampo.change
sys.modules[__name__] = sys.modules["sampo.change"]
