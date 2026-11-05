"""Old import path, kept for two releases (T-2742): the module is sampo.callcards."""
import sys

import sampo.callcards

sys.modules[__name__] = sys.modules["sampo.callcards"]
