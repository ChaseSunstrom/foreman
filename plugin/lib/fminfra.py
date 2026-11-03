"""Old import path, kept for two releases (T-2742): the module is sampo.infra."""
import sys
import sampo.infra
sys.modules[__name__] = sys.modules["sampo.infra"]
