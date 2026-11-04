"""Old import path, kept for two releases (T-2742): the module is sampo.smallcards."""
import sys
import sampo.smallcards
sys.modules[__name__] = sys.modules["sampo.smallcards"]
