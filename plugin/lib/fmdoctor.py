"""Old import path, kept for two releases (T-2742): the module is sampo.doctor."""
import sys
import sampo.doctor
sys.modules[__name__] = sys.modules["sampo.doctor"]
