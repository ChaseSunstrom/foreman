"""Old import path, kept for two releases (T-2742): the module is sampo.claude."""
import sys
import sampo.claude
sys.modules[__name__] = sys.modules["sampo.claude"]
