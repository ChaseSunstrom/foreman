"""Old import path, kept for two releases (T-2742): the module is sampo.headroom."""
import sys
import sampo.headroom
sys.modules[__name__] = sys.modules["sampo.headroom"]
