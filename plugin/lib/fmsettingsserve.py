"""Old import path, kept for two releases (T-2742): the module is sampo.settingsserve."""
import sys
import sampo.settingsserve
sys.modules[__name__] = sys.modules["sampo.settingsserve"]
