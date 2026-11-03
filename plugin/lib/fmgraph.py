"""Old import path, kept for two releases (T-2742): the module is sampo.graph."""
import sys
import sampo.graph
sys.modules[__name__] = sys.modules["sampo.graph"]
