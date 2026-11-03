"""Old import path, kept for two releases (T-2742): the module is sampo.smithbench."""
import sys
import sampo.smithbench
sys.modules[__name__] = sys.modules["sampo.smithbench"]
