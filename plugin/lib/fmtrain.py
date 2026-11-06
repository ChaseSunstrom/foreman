"""Old import path, kept for two releases (T-2742): the module is sampo.train."""
import sys
import sampo.train
sys.modules[__name__] = sys.modules["sampo.train"]
