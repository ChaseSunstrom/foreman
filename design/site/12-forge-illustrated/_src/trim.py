"""Full-page captures report the layout overflow width; crop each to its viewport width (the page itself has no horizontal scroll)."""
import os
from PIL import Image
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for name, w in (('phone-320.png', 320), ('phone-390.png', 390), ('full-1440.png', 1440)):
    p = os.path.join(root, name); im = Image.open(p)
    if im.size[0] != w: im.crop((0, 0, w, im.size[1])).save(p)
    print(name, Image.open(p).size)
