"""Old import path, kept for two releases (T-2742): the module is sampo.toolproof."""
import sys
import sampo.toolproof
sys.modules[__name__] = sys.modules["sampo.toolproof"]
