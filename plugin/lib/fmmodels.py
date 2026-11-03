"""Old import path, kept for two releases (T-2742): the module is sampo.models."""
import sys
import sampo.models
sys.modules[__name__] = sys.modules["sampo.models"]
