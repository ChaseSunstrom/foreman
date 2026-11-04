"""Old import path style shim (T-2742): the module is sampo.traces."""
import sys
import sampo.traces
sys.modules[__name__] = sys.modules["sampo.traces"]
