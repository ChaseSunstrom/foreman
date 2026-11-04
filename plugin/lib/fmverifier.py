"""Old import path, kept for two releases (T-2742): the module is sampo.verifier."""
import sys
import sampo.verifier
sys.modules[__name__] = sys.modules["sampo.verifier"]
