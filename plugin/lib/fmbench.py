"""Old import path, kept for two releases (T-2742): the module is sampo.bench."""
import sys
import sampo.bench
sys.modules[__name__] = sys.modules["sampo.bench"]
