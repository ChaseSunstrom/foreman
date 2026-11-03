"""Old import path, kept for two releases (T-2742): the module is sampo.new."""
import sys
import sampo.new
sys.modules[__name__] = sys.modules["sampo.new"]
