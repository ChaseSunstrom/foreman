"""Old import path, kept for two releases (T-2742): the module is sampo.scout."""
import sys
import sampo.scout
sys.modules[__name__] = sys.modules["sampo.scout"]
