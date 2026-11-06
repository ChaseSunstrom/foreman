"""Old import path, kept for two releases (T-2742): the module is sampo.repro."""
import sys
import sampo.repro
sys.modules[__name__] = sys.modules["sampo.repro"]
