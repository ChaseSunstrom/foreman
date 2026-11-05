"""Old import path, kept for two releases (T-2742): the module is sampo.kalevala."""
import sys
import sampo.kalevala
sys.modules[__name__] = sys.modules["sampo.kalevala"]
