"""Old import path, kept for two releases (T-2742): the module is sampo.trials."""
import sys
import sampo.trials
sys.modules[__name__] = sys.modules["sampo.trials"]
