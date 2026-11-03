"""Old import path, kept for two releases (T-2742): the module is sampo.playbooks."""
import sys
import sampo.playbooks
sys.modules[__name__] = sys.modules["sampo.playbooks"]
