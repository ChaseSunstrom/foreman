"""Old import path, kept for two releases (T-2742): the module is sampo.page."""
import sys
import sampo.page
sys.modules[__name__] = sys.modules["sampo.page"]
