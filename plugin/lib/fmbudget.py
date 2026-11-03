"""Old import path, kept for two releases (T-2742): the module is sampo.budget."""
import sys
import sampo.budget
sys.modules[__name__] = sys.modules["sampo.budget"]
