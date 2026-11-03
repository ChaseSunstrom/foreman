"""Old import path, kept for two releases (T-2742): the module is sampo.mcp."""
import sys
import sampo.mcp
sys.modules[__name__] = sys.modules["sampo.mcp"]
