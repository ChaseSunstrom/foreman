"""Old import path, kept for two releases (T-2742): the module is sampo.landlock."""
import sys
import sampo.landlock
sys.modules[__name__] = sys.modules["sampo.landlock"]
