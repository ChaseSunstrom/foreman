"""Old import path, kept for two releases (T-2742): the module is sampo.deps."""
import sys
import sampo.deps
sys.modules[__name__] = sys.modules["sampo.deps"]
