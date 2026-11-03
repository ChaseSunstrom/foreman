"""Old import path, kept for two releases (T-2742): the module is sampo.risk."""
import sys
import sampo.risk
sys.modules[__name__] = sys.modules["sampo.risk"]
