#!/usr/bin/env python3
"""Compare two PNG files pixel by pixel (ignores PNG encoding/metadata differences).
usage: python3 compare_pixels.py <fresh.png> <bundled.png>   exit 0 if identical pixels, 1 otherwise."""
import sys
import numpy as np
from PIL import Image
a = Image.open(sys.argv[1]).convert('RGBA'); b = Image.open(sys.argv[2]).convert('RGBA')
same = a.size == b.size and np.array_equal(np.array(a), np.array(b))
print(f"{sys.argv[2]}: pixel-identical = {same}  (size {a.size})")
sys.exit(0 if same else 1)
