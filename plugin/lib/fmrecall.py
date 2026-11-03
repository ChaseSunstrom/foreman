"""Old import path, kept for two releases (T-2742): the module is sampo.recall."""
import sys
import sampo.recall
sys.modules[__name__] = sys.modules["sampo.recall"]
