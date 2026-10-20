"""Turns the client's grey-wash gazelle drawings into line art + one brand colour.
Black ink lines stay, the grey watercolour wash becomes the brand colour (texture kept),
white inside the drawing stays white, the outside becomes transparent.
Usage: python3 gazelles.py <mascot-src-dir> <out-dir>
"""
import sys, os, io, base64, json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

strip = Image.open(f'{SRC}/gazelle-poses-original.jpg').convert('L')
box = Image.open(f'{SRC}/gazelle-box-original.jpg').convert('L')


def split_strip(im):
    a = np.array(im) < 200
    cols = a.any(axis=0)
    runs, x = [], 0
    while x < len(cols):
        if cols[x]:
            s = x
            while x < len(cols) and (cols[x] or cols[x:x + 12].any()):
                x += 1
            runs.append((s, x))
        x += 1
    return [r for r in runs if r[1] - r[0] > 40]


def crop_tight(im, pad=6):
    a = np.array(im) < 215
    ys, xs = np.where(a)
    return im.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + pad), min(im.height, ys.max() + pad)))


def colourise(im, colour, target_h):
    scale = target_h / im.height
    im = im.resize((round(im.width * scale), target_h), Image.LANCZOS)
    L = np.array(im).astype(float)
    # ink: soft ramp so the lines stay anti-aliased
    ink = np.clip((105 - L) / 55, 0, 1)
    # wash: mid greys, strength keeps the watercolour texture
    wash = np.clip((238 - L) / 120, 0, 1) * (1 - ink)
    # outside = white region connected to the border (not enclosed by the drawing)
    barrier = ndimage.binary_dilation(L < 225, iterations=1)
    lab, _ = ndimage.label(~barrier)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(border))
    outside = ndimage.binary_erosion(outside, iterations=1, border_value=1)
    c = np.array(colour, float)
    w = np.array([255, 255, 255], float)
    base = w[None, None, :] * (1 - wash[..., None]) + c[None, None, :] * wash[..., None]
    rgb = base * (1 - ink[..., None]) + np.array([17, 17, 17])[None, None, :] * ink[..., None]
    alpha = np.where(outside, np.maximum(ink, wash * 1.4), 1.0)
    ring = ndimage.binary_dilation(outside, iterations=3) & ~outside & (L > 222)
    alpha = np.where(ring, ink, alpha)
    alpha = np.clip(alpha, 0, 1)
    rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')


def line_only(im, target_h):
    scale = target_h / im.height
    im = im.resize((round(im.width * scale), target_h), Image.LANCZOS)
    L = np.array(im).astype(float)
    ink = np.clip((105 - L) / 55, 0, 1)
    rgba = np.dstack([np.full_like(L, 17)] * 3 + [ink * 255]).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')


runs = split_strip(strip)
names = ['box', 'sleep', 'sit', 'hop', 'stand']
print('poses found', runs)
poses = {n: crop_tight(strip.crop((a - 4, 0, b + 4, strip.height))) for n, (a, b) in zip(names, runs)}
poses['box'] = crop_tight(box)  # the big drawing is much sharper

# brand colours (ket packaging / social): lavender, periwinkle, pink, amber, orange
COL = {'box': (127, 148, 255), 'sleep': (190, 170, 255), 'sit': (244, 140, 240), 'hop': (255, 174, 21), 'stand': (255, 120, 60)}
H = {'box': 360, 'sleep': 300, 'sit': 300, 'hop': 360, 'stand': 360}
meta = {}
for n, im in poses.items():
    out = colourise(im, COL[n], H[n])
    out.save(f'{OUT}/gazelle-{n}.webp', 'WEBP', quality=86, method=6)
    sz = os.path.getsize(f'{OUT}/gazelle-{n}.webp')
    meta[n] = {'w': out.width, 'h': out.height, 'bytes': sz}
lo = line_only(poses['box'], 360); lo.save(f'{OUT}/gazelle-box-line.webp', 'WEBP', quality=86, method=6)
json.dump(meta, open(f'{OUT}/meta.json', 'w'), indent=1)
print(json.dumps(meta))
