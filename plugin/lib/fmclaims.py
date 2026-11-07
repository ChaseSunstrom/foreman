"""Old import path, kept for two releases (T-2742): the module is sampo.claims."""
import sys
import sampo.claims
sys.modules[__name__] = sys.modules["sampo.claims"]
