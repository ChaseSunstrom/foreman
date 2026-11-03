"""Old import path, kept for two releases (T-2742): the module is sampo.contract."""
import sys
import sampo.contract
sys.modules[__name__] = sys.modules["sampo.contract"]
