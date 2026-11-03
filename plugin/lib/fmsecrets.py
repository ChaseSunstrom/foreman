"""Old import path, kept for two releases (T-2742): the module is sampo.secrets."""
import sys
import sampo.secrets
sys.modules[__name__] = sys.modules["sampo.secrets"]
