"""Old import path, kept for two releases (T-2742): the module is sampo.integrations."""
import sys
import sampo.integrations
sys.modules[__name__] = sys.modules["sampo.integrations"]
