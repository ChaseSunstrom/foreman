"""Old import path, kept for two releases (T-2742): the module is sampo.mandate."""
import sys
import sampo.mandate
sys.modules[__name__] = sys.modules["sampo.mandate"]
