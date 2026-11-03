"""Old import path, kept for two releases (T-2742): the module is sampo.ledger."""
import sys
import sampo.ledger
sys.modules[__name__] = sys.modules["sampo.ledger"]
