"""Old import path, kept for two releases (T-2742): the module is sampo.prove."""
import sys
import sampo.prove
sys.modules[__name__] = sys.modules["sampo.prove"]
