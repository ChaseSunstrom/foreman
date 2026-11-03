"""Old import path, kept for two releases (T-2742): the module is sampo.migrate."""
import sys
import sampo.migrate
sys.modules[__name__] = sys.modules["sampo.migrate"]
