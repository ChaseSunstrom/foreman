"""Old import path, kept for two releases (T-2742): the module is sampo.settings."""
import sys
import sampo.settings
sys.modules[__name__] = sys.modules["sampo.settings"]
