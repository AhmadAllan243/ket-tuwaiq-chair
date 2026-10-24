"""
Layers for the sofa illustration (decoration inspiration) so two things can move:
the coffee steam (rises and sways) and the sleeping gazelle (breathes).

  base  = the illustration with the steam painted out
  steam = the steam strokes alone (transparent)
  gz    = the gazelle above the cloud, alone (transparent; taken out of the base); the page
          scales it up a touch from its belly line, so it never parts from the cloud

usage: python3 tools/brand/illus_fx.py      (run from src/ket-hero; reads assets-src/brand/illus.webp)
writes assets-src/brand/illus-{base,steam,gz}.webp and packs them into ../ket-product.html
between /*ILLUSFX*/ … /*/ILLUSFX*/ (inserted after the BRAND line the first time)
"""
import base64, io, json, os, re
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, '..', '..', 'assets-src', 'brand')
PAGE = os.path.join(HERE, '..', '..', '..', 'ket-product.html')
BELLY = 445                      # gazelle above this line breathes; the cloud below stays

im = np.asarray(Image.open(os.path.join(BRAND, 'illus.webp')).convert('RGB')).astype(np.uint8)
H, W = im.shape[:2]
lum = im.mean(2)
yy, xx = np.mgrid[:H, :W]

# steam: dark strokes above the mug
sbox = (xx >= 238) & (xx <= 298) & (yy >= 20) & (yy < 100)
steam_a = np.clip((235 - lum) / 150, 0, 1) * sbox
steam = np.zeros((H, W, 4), np.uint8); steam[..., 3] = (steam_a * 255).astype(np.uint8)
base = im.copy(); base[sbox] = 255           # the sky behind the steam is plain white

# gazelle: everything inside its outline, above the belly line
gbox = (xx >= 35) & (xx <= 255) & (yy >= 305) & (yy <= 500)
ink = (lum < 110) & gbox
fig = ndimage.binary_fill_holes(ndimage.binary_dilation(ink, iterations=2)) & gbox
fig = ndimage.binary_erosion(fig, iterations=1) & (yy < BELLY)   # keep 1px of anti-aliasing, not the sofa around it
gz = np.dstack([im, fig.astype(np.uint8) * 255])
# take the still gazelle out of the base (sofa purple above the sofa's bottom edge, white below), so
# thin parts like the antlers leave no ghost line behind when the layer breathes
hole = ndimage.binary_dilation(fig, iterations=2) & (yy < BELLY)
sofa_edge = 421 + (xx - 35) * 3 / 215
base[hole & (yy < sofa_edge)] = (211, 194, 255)
base[hole & (yy >= sofa_edge)] = 255

out = {}
for name, arr, mode in (('base', base, 'RGB'), ('steam', steam, 'RGBA'), ('gz', gz, 'RGBA')):
    img = Image.fromarray(arr, mode)
    if mode == 'RGBA':                       # keep the canvas size so layers line up with inset:0
        img.save(os.path.join(BRAND, f'illus-{name}.webp'), quality=90, method=6)
    else:
        img.save(os.path.join(BRAND, f'illus-{name}.webp'), quality=88, method=6)
    b = io.BytesIO(); img.save(b, 'WEBP', quality=88 if mode == 'RGB' else 90, method=6)
    out[name] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    print(name, len(b.getvalue()))
out['belly'] = round(BELLY / H * 100, 2)
ys, xs = np.nonzero(fig); out['gzx'] = round(xs.mean() / W * 100, 2)

s = open(PAGE).read()
block = '/*ILLUSFX*/const ILLUS_FX = ' + json.dumps(out, separators=(',', ':')) + ';/*/ILLUSFX*/'
if '/*ILLUSFX*/' in s:
    s = re.sub(r'/\*ILLUSFX\*/.*?/\*/ILLUSFX\*/', lambda m: block, s, flags=re.S)
else:
    i = s.index('\n', s.index('const BRAND = ')) + 1
    s = s[:i] + block + '\n' + s[i:]
open(PAGE, 'w').write(s)
print('packed', len(block))
