"""Old import path, kept for two releases (T-2742): the module is sampo.stories."""
import sys
import sampo.stories
sys.modules[__name__] = sys.modules["sampo.stories"]
