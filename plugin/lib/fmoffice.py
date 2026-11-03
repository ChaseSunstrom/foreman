"""Old import path, kept for two releases (T-2742): the module is sampo.office."""
import sys
import sampo.office
sys.modules[__name__] = sys.modules["sampo.office"]
