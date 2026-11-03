"""Old import path, kept for two releases (T-2742): the module is sampo.smithterm."""
import sys
import sampo.smithterm
sys.modules[__name__] = sys.modules["sampo.smithterm"]
