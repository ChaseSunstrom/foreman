"""Old import path, kept for two releases (T-2742): the module is sampo.critique."""
import sys
import sampo.critique
sys.modules[__name__] = sys.modules["sampo.critique"]
