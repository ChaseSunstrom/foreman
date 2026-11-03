"""Old import path, kept for two releases (T-2742): the module is sampo.mutate."""
import sys
import sampo.mutate
sys.modules[__name__] = sys.modules["sampo.mutate"]
