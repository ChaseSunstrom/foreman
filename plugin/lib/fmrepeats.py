"""Old import path, kept for two releases (T-2742): the module is sampo.repeats."""
import sys
import sampo.repeats
sys.modules[__name__] = sys.modules["sampo.repeats"]
