"""Old import path, kept for two releases (T-2742): the module is sampo.demo."""
import sys
import sampo.demo
sys.modules[__name__] = sys.modules["sampo.demo"]
