"""Delivery gazelle: the client's black-and-white box drawing with a coloured sticker outline around
the box only (like the "Hey" gazelles). Outside = transparent, inside = white, lines = black.
Usage: python3 box_bw.py <box-bw.jpg> <out.webp> [halo #hex]"""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
src, out = sys.argv[1], sys.argv[2]
halo_rgb = tuple(int(sys.argv[3].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)) if len(sys.argv) > 3 else (252, 152, 211)
L = np.array(Image.open(src).convert('L')).astype(float)
H, W = L.shape
ink = L < 128
barrier = ndimage.binary_dilation(ink, iterations=2)
lab, _ = ndimage.label(~barrier)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
outside = np.isin(lab, list(border)) & ~ink
shape = ~outside
ys, xs = np.nonzero(ink)
# the box: everything of the figure from the top of the box flaps down
rows = np.nonzero(ink.sum(1) > W * .35)[0]            # long horizontal lines = box rim / edges
rim = rows.min() - 40
box = shape.copy(); box[:rim] = False
yy, xx = np.mgrid[:H, :W]
r = 26
dist = ndimage.distance_transform_edt(~box)
halo = (dist > 0) & (dist <= r)
alpha_halo = np.clip(r + 1 - dist, 0, 1) * halo
ink_a = np.clip((150 - L) / 70, 0, 1)
rgb = np.zeros((H, W, 3)); a = np.zeros((H, W))
rgb[:] = 255
fill = shape & ~ink
a = np.maximum(a, fill * 1.0)
rgb[halo] = halo_rgb; a = np.maximum(a, alpha_halo)
rgb = rgb * (1 - ink_a[..., None]) + 17 * ink_a[..., None]
a = np.maximum(a, ink_a * shape + ink_a * 0)
img = Image.fromarray(np.dstack([rgb, a * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
bb = img.getbbox(); img = img.crop((bb[0] - 4, bb[1] - 4, bb[2] + 4, bb[3] + 4))
# box front panel (for the smile stamp): the biggest white region below the rim
fl, n = ndimage.label(fill & (yy > rim + 60))
big = np.argmax(ndimage.sum(fill, fl, range(1, n + 1))) + 1
fy, fx = np.nonzero(fl == big)
ox, oy = bb[0] - 4, bb[1] - 4
panel = [(fx.min() - ox) / img.width * 100, (fx.max() - ox) / img.width * 100, (fy.min() - oy) / img.height * 100, (fy.max() - oy) / img.height * 100]
img.thumbnail((440, 440), Image.LANCZOS)
img.save(out, 'WEBP', quality=88, method=6)
print(json.dumps({'size': img.size, 'rim': int(rim), 'panel_pct': [round(v, 1) for v in panel]}))
