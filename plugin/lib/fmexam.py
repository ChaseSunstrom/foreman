"""Old import path, kept for two releases (T-2742): the module is sampo.louhi."""
import sys
import sampo.louhi
sys.modules[__name__] = sys.modules["sampo.louhi"]
