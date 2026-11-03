"""Old import path, kept for two releases (T-2742): the module is sampo.smithmod."""
import sys
import sampo.smithmod
sys.modules[__name__] = sys.modules["sampo.smithmod"]
