"""Old import path, kept for two releases (T-2742): the module is sampo.hooks."""
import sys
import sampo.hooks
sys.modules[__name__] = sys.modules["sampo.hooks"]
