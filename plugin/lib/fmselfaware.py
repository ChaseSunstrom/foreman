"""Old import path, kept for two releases (T-2742): the module is sampo.selfaware."""
import sys
import sampo.selfaware
sys.modules[__name__] = sys.modules["sampo.selfaware"]
