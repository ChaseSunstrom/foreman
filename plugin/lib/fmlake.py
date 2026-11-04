"""Old import path, kept for two releases (T-2742): the module is sampo.lake."""
import sys
import sampo.lake
sys.modules[__name__] = sys.modules["sampo.lake"]
