"""Old import path, kept for two releases (T-2742): the module is sampo.draft."""
import sys
import sampo.draft
sys.modules[__name__] = sys.modules["sampo.draft"]
