"""
Cuts the client's gazelle drawings into animation layers ("rigs").

Each drawing becomes a few transparent WebP layers of the same size, so the page can stack them
and animate each one: the body hides inside the box and pops up, the arm waves, paws land on the
rim, sparkles flash, the Zzz float. The baked-in "Hey" is removed (the page renders هلا / Hey as
live text), and the box rim hidden under each paw is redrawn so the box is whole while the
gazelle is still inside.

usage: python3 tools/brand/cut_rigs.py      (reads assets-src/mascot/new, writes assets-src/mascot/rigs)
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_fill_holes, label

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', 'assets-src', 'mascot', 'new')
OUT = os.path.join(HERE, '..', '..', 'assets-src', 'mascot', 'rigs')
os.makedirs(OUT, exist_ok=True)
OUT_W = 520  # layer width in px (shown at ~110-200 css px, sharp on 3x screens)


def poly_mask(shape, pts):
    m = Image.new('L', (shape[1], shape[0]), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return np.asarray(m) > 0


def rect(shape, x0, y0, x1, y1):
    m = np.zeros(shape, bool); m[y0:y1, x0:x1] = True; return m


def cut(name, crop, hey, layers, rim_fixes=(), pivots=None):
    im = np.asarray(Image.open(os.path.join(SRC, name + '.jpg')).convert('RGB')).astype(int)
    H, W = im.shape[:2]
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    mx, mn = im.max(2), im.min(2)
    lum = im.mean(2)
    # background = near-white connected to the image border
    whiteish = (lum > 236) & (mx - mn < 18)
    lab, _ = label(whiteish)
    border = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
    bg = np.isin(lab, list(border))
    alpha = (~bg).astype(float)
    # soften the outer edge a little (anti-aliased pixels next to the background)
    from scipy.ndimage import binary_dilation
    near_bg = binary_dilation(bg, iterations=2)          # only the outline, not white fills inside
    edge = (~bg) & near_bg & (lum > 200) & (mx - mn < 25)
    alpha[edge] = np.clip((255 - lum[edge]) / 55, 0.25, 1)

    # remove the baked-in "Hey" (its glow + lettering) so the page can render it as text
    hey_mask = np.zeros((H, W), bool)
    sat = mx - mn
    for kind, *args in hey:
        if kind == 'glow':
            hey_mask |= rect((H, W), *args) & (sat > 40)
        else:
            hey_mask |= rect((H, W), *args) if kind == 'rect' else poly_mask((H, W), args[0])
    alpha[hey_mask] = 0

    rgba = np.dstack([im, (alpha * 255).astype(int)]).astype(np.uint8)
    assigned = np.zeros((H, W), bool)
    out = {}
    for lname, rule in layers:
        if rule == 'rest':
            m = ~assigned
        else:
            m = np.zeros((H, W), bool)
            for kind, *args in rule:
                m |= rect((H, W), *args) if kind == 'rect' else poly_mask((H, W), args[0])
            m &= ~assigned
        assigned |= m
        out[lname] = m

    x0, y0, x1, y1 = crop
    meta = {'w': x1 - x0, 'h': y1 - y0, 'layers': [], 'pivots': {}}
    for lname, m in out.items():
        layer = rgba.copy(); layer[~m, 3] = 0
        if lname == 'box':
            layer = Image.fromarray(layer, 'RGBA')
            d = ImageDraw.Draw(layer)
            for (fx0, fy0, fx1, fy1, line_y0, line_y1) in rim_fixes:   # redraw the rim under a paw
                d.rectangle([fx0, fy0, fx1, fy1], fill=(255, 255, 255, 255))
                d.rectangle([fx0, line_y0, fx1, line_y1], fill=(10, 10, 10, 255))
            layer = np.asarray(layer)
        img = Image.fromarray(np.asarray(layer)[y0:y1, x0:x1], 'RGBA')
        img = img.resize((OUT_W, round(OUT_W * img.height / img.width)), Image.LANCZOS)
        fn = f'{name}-{lname}.webp'
        img.save(os.path.join(OUT, fn), quality=88, method=6)
        meta['layers'].append(lname)
    for k, (px, py) in (pivots or {}).items():   # rotation origins, as % of the cropped canvas
        meta['pivots'][k] = [round((px - x0) / (x1 - x0) * 100, 1), round((py - y0) / (y1 - y0) * 100, 1)]
    print(name, meta)
    return meta


RIM = 712  # top of the box rim in both "Hey" drawings
meta = {}

# --- waving gazelle in a box (green: welcome · yellow: added to cart) ---
wave_layers = [
    ('spark', [('rect', 322, 420, 426, 524), ('rect', 840, 575, 922, 672), ('rect', 380, 205, 455, 310), ('rect', 820, 170, 905, 275)]),
    ('wave',  [('rect', 315, 535, 388, 636)]),
    ('arm',   [('poly', [(382, 508), (484, 504), (522, 585), (524, RIM), (474, RIM), (386, 616)])]),
    ('paw',   [('rect', 770, 660, 880, 800)]),
    ('box',   [('rect', 300, RIM, 1010, 1100), ('rect', 300, 660, 470, RIM), ('rect', 880, 660, 1010, RIM)]),
    ('body',  'rest'),
]
hey_wave = [('rect', 430, 100, 850, 300), ('rect', 650, 300, 830, 362), ('glow', 430, 100, 850, 370)]
for n in ('hey-green', 'hey-yellow'):
    meta[n] = cut(n, (300, 150, 1010, 1095), hey_wave, wave_layers,
                  rim_fixes=[(772, RIM + 10, 878, 796, RIM, RIM + 12)],
                  pivots={'arm': (498, RIM), 'pop': (650, RIM)})

# --- gazelle with both paws on the rim (pink: shipping) ---
meta['hey-pink-paws'] = cut('hey-pink-paws', (300, 150, 1010, 1095),
    [('rect', 470, 100, 840, 305), ('rect', 640, 300, 830, 352), ('glow', 460, 100, 850, 360)],
    [('spark', [('rect', 390, 540, 455, 630), ('rect', 855, 580, 920, 665), ('rect', 410, 215, 480, 300), ('rect', 840, 190, 905, 280)]),
     ('paw',   [('rect', 438, 662, 536, 798), ('rect', 786, 662, 876, 798)]),
     ('box',   [('rect', 300, 698, 1010, 1100), ('rect', 300, 655, 438, 698), ('rect', 876, 655, 1010, 698)]),
     ('body',  'rest')],
    rim_fixes=[(440, 712, 534, 796, 700, 712), (788, 712, 874, 796, 700, 712)],
    pivots={'pop': (650, RIM)})

# --- sleeping on a cloud (idle) ---
meta['sleep-cloud'] = cut('sleep-cloud', (150, 170, 1250, 1080), [],
    [('zzz',  [('rect', 735, 190, 1170, 456), ('rect', 1095, 456, 1170, 500)]),
     ('body', 'rest')],
    pivots={'breathe': (700, 1040)})

json.dump(meta, open(os.path.join(OUT, 'rigs.json'), 'w'), indent=1)
print('wrote', OUT)
