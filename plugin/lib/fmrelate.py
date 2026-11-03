"""Old import path, kept for two releases (T-2742): the module is sampo.relate."""
import sys
import sampo.relate
sys.modules[__name__] = sys.modules["sampo.relate"]
