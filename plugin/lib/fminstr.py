"""Old import path, kept for two releases (T-2742): the module is sampo.instr."""
import sys
import sampo.instr
sys.modules[__name__] = sys.modules["sampo.instr"]
