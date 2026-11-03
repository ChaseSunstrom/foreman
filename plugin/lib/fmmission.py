"""Old import path, kept for two releases (T-2742): the module is sampo.mission."""
import sys
import sampo.mission
sys.modules[__name__] = sys.modules["sampo.mission"]
