"""Old import path, kept for two releases (T-2742): the module is sampo.marks."""
import sys
import sampo.marks
sys.modules[__name__] = sys.modules["sampo.marks"]
