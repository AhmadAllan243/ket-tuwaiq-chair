"""Trace the client's ket wordmark, TANASOUB line and smile mark into SVG paths."""
import sys, json
import numpy as np
from PIL import Image, ImageFilter
import potrace

S = sys.argv[1]
src = Image.open(f'{S}/logo_crop.png').convert('L')
UP = 8


def trace(box):
    im = src.crop(box)
    w, h = im.size
    im = im.resize((w * UP, h * UP), Image.BICUBIC).filter(ImageFilter.GaussianBlur(UP * 0.55))
    a = np.array(im) < 128
    bm = potrace.Bitmap(a)
    path = bm.trace(turdsize=40, alphamax=1.0, opticurve=True, opttolerance=0.25)
    out = []
    for curve in path:
        f = lambda p: f'{p.x / UP:.2f} {p.y / UP:.2f}'
        d = [f'M{f(curve.start_point)}']
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f'L{f(seg.c)}L{f(seg.end_point)}')
            else:
                d.append(f'C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}')
        d.append('Z')
        xs = [curve.start_point.x / UP] + [s.end_point.x / UP for s in curve.segments]
        ys = [curve.start_point.y / UP] + [s.end_point.y / UP for s in curve.segments]
        out.append({'d': ''.join(d), 'x0': min(xs), 'x1': max(xs), 'y0': min(ys), 'y1': max(ys)})
    return out, (w, h)


res = {}
for name, box in {'ket': (360, 20, 600, 165), 'lockup': (0, 10, 250, 200), 'smile': (755, 55, 870, 125)}.items():
    paths, size = trace(box)
    res[name] = {'paths': paths, 'size': size}
    print(name, size, len(paths), [(round(p['x0']), round(p['x1'])) for p in paths])
json.dump(res, open(f'{S}/logo_paths.json', 'w'))
