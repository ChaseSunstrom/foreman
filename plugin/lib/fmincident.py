"""Old import path, kept for two releases (T-2742): the module is sampo.incident."""
import sys
import sampo.incident
sys.modules[__name__] = sys.modules["sampo.incident"]
