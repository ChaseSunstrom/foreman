"""Old import path, kept for two releases (T-2742): the module is sampo.docs."""
import sys
import sampo.docs
sys.modules[__name__] = sys.modules["sampo.docs"]
