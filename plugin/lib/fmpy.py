"""Old import path, kept for two releases (T-2742): the module is sampo.py."""
import sys
import sampo.py
sys.modules[__name__] = sys.modules["sampo.py"]
