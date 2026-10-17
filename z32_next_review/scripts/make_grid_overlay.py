#!/usr/bin/env python3
"""Draw a pixel grid over the Fig.2 map so that label centres can be read. Output: images/fig2_grid_overlay_for_reading.png"""
from PIL import Image, ImageDraw
from common import IMAGES
im = Image.open(IMAGES / 'fig2_map_p9_native.png').convert('RGB')
W, H = im.size
d = ImageDraw.Draw(im)
for x in range(0, W, 50):
    d.line([(x, 0), (x, H)], fill=(255, 0, 0) if x % 100 == 0 else (0, 160, 255), width=1)
    d.text((x + 2, 2), str(x), fill=(255, 0, 0))
for y in range(0, H, 50):
    d.line([(0, y), (W, y)], fill=(255, 0, 0) if y % 100 == 0 else (0, 160, 255), width=1)
    d.text((2, y + 2), str(y), fill=(255, 0, 0))
im.save(IMAGES / 'fig2_grid_overlay_for_reading.png')
print("written images/fig2_grid_overlay_for_reading.png")
