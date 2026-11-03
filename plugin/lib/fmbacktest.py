"""Old import path, kept for two releases (T-2742): the module is sampo.backtest."""
import sys
import sampo.backtest
sys.modules[__name__] = sys.modules["sampo.backtest"]
