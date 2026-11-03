"""Old import path, kept for two releases (T-2742): the module is sampo.dataproof."""
import sys
import sampo.dataproof
sys.modules[__name__] = sys.modules["sampo.dataproof"]
