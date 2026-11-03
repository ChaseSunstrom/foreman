"""Old import path, kept for two releases (T-2742): the module is sampo.agents."""
import sys
import sampo.agents
sys.modules[__name__] = sys.modules["sampo.agents"]
