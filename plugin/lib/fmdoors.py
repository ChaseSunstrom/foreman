"""Old import path, kept for two releases (T-2742): the module is sampo.doors."""
import sys
import sampo.doors
sys.modules[__name__] = sys.modules["sampo.doors"]
