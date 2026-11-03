"""Old import path, kept for two releases (T-2742): the module is sampo.relproof."""
import sys
import sampo.relproof
sys.modules[__name__] = sys.modules["sampo.relproof"]
