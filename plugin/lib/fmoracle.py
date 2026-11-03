"""Old import path, kept for two releases (T-2742): the module is sampo.oracle."""
import sys
import sampo.oracle
sys.modules[__name__] = sys.modules["sampo.oracle"]
