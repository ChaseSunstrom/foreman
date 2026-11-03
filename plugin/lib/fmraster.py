"""Old import path, kept for two releases (T-2742): the module is sampo.raster."""
import sys
import sampo.raster
sys.modules[__name__] = sys.modules["sampo.raster"]
