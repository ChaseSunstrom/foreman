"""Old import path, kept for two releases (T-2742): the module is sampo.auditrun."""
import sys
import sampo.auditrun
sys.modules[__name__] = sys.modules["sampo.auditrun"]
