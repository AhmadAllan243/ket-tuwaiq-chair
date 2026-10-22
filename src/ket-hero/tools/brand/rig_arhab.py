"""Cuts the client's "ارحبوووو" gazelle drawing into vector parts for the animated welcome.

The drawing (assets-src/mascot/new/arhab.jpg) is bold black line art: a gazelle peeking from behind a
pole, both paws gripping it. We drop the pole (the page draws its own line), the purple bubble and
the purple speech marks, then cut the rest into layers with hand-placed polygons and trace each layer
twice with potrace: once for the black ink, once for its white fill (so layers hide what is behind
them when they move).

Output: assets-src/mascot/rigs/arhab.json  {w, h, parts: {name: {ink, fill}}, pole_x, eyes: [...]}
Usage:  python3 rig_arhab.py <arhab.jpg> <out.json> [preview.png]
"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
import potrace

SRC, OUT = sys.argv[1], sys.argv[2]
PREVIEW = sys.argv[3] if len(sys.argv) > 3 else None

im = np.array(Image.open(SRC).convert('RGB')).astype(int)
H, W = im.shape[:2]
sat = im.max(2) - im.min(2)
L = im.mean(2)
purple = ndimage.binary_dilation(sat > 25, iterations=3)
ink = (L < 128) & ~purple

POLE = (252, 273)          # pole columns (drawn by the page instead)
POLE_X = 262.5

def poly(pts):
    m = Image.new('1', (W, H), 0)
    ImageDraw.Draw(m).polygon(pts, fill=1)
    return np.array(m, bool)

# ---- part polygons (image px) -------------------------------------------------------------
PAW_T = poly([(195, 612), (306, 612), (306, 760), (195, 760)])
PAW_B = poly([(195, 826), (304, 826), (304, 958), (195, 958)])
PAWS = PAW_T | PAW_B
# head / body cut runs through the white of the neck, between the jaw line and the collar
NECK_CUT = [(273, 738), (330, 754), (400, 796), (447, 794), (482, 770), (720, 748), (W, 748)]
ABOVE = poly([(273, 0), (W, 0)] + NECK_CUT[::-1])
BELOW = poly([(273, H)] + NECK_CUT + [(W, H)])
EAR_L = poly([(268, 150), (322, 150), (396, 258), (438, 336), (446, 372), (380, 398), (300, 404), (268, 404)])
EAR_R = poly([(684, 503), (905, 515), (935, 548), (905, 610), (835, 678), (700, 678), (684, 610)])
MOUTH = poly([(379, 618), (424, 610), (452, 618), (500, 640), (498, 698), (379, 698)])
EYE_L = poly([(300, 455), (410, 455), (410, 565), (300, 565)])
EYE_R = poly([(510, 605), (645, 605), (645, 700), (510, 700)])

pole_cols = np.zeros((H, W), bool); pole_cols[:, POLE[0]:POLE[1]] = True
right_of_pole = np.zeros((H, W), bool); right_of_pole[:, POLE[1]:] = True

# "inside" = white enclosed by the drawing. Close the pole gap and the bottom edge (the torso runs
# off the bottom of the drawing) so those regions do not leak to the outside.
barrier = ndimage.binary_dilation(ink | pole_cols, iterations=2)
barrier[H - 3:, POLE[0]:520] = True
lab, _ = ndimage.label(~barrier)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
outside = np.isin(lab, list(border))

# Ears touch the head outline and the antlers, so a straight polygon cut leaves slivers of the ear
# outline in the head layer (a doubled line when the ear moves). Split the touching strokes by
# growing labels from seed points along the ink (multi-source geodesic flood), inside a search zone.
def geo_split(zone, seeds):
    lab = np.zeros((H, W), np.int8)
    for i, pts in enumerate(seeds, 1):
        for x, y in pts:
            ys, xs = np.nonzero(ink[y - 6:y + 7, x - 6:x + 7])
            lab[ys + y - 6, xs + x - 6] = i
    allowed = ink & zone
    for _ in range(900):
        grown = False
        for i in range(1, len(seeds) + 1):
            nb = ndimage.binary_dilation(lab == i) & allowed & (lab == 0)
            if nb.any(): lab[nb] = i; grown = True
        if not grown: break
    return lab
zoneL = poly([(262, 120), (470, 120), (470, 420), (262, 420)])
labL = geo_split(zoneL, [
    [(275, 240), (280, 300), (305, 350), (340, 372), (310, 180), (350, 220), (390, 265), (425, 322), (318, 215), (335, 280), (368, 330)],   # ear
    [(470, 108), (395, 175), (408, 250), (540, 200), (525, 320), (500, 330)],                                                         # antler
    [(452, 346), (520, 350), (300, 410), (286, 440)]])                                                                               # head
zoneR = poly([(660, 430), (940, 430), (940, 690), (660, 690)])
labR = geo_split(zoneR, [
    [(905, 545), (880, 600), (830, 650), (770, 660), (722, 640), (722, 515), (800, 518), (878, 530), (722, 560), (800, 576), (870, 566)],   # ear
    [(880, 380), (800, 410), (735, 470), (700, 488)],                                                                                 # antler
    [(688, 600), (678, 652), (690, 455)]])                                                                                           # head
EAR_L_INK = labL == 1
EAR_R_INK = labR == 1

parts = {
    'body':  BELOW & right_of_pole & ~PAWS,
    'earL':  EAR_L & right_of_pole,
    'earR':  EAR_R,
    'head':  ABOVE & right_of_pole & ~PAWS & ~EAR_L & ~EAR_R & ~MOUTH & ~EYE_L & ~EYE_R,
    'mouth': MOUTH,
    'eyeL':  EYE_L,
    'eyeR':  EYE_R,
    'pawT':  PAW_T,
    'pawB':  PAW_B,
}
# fills: each enclosed white region goes to the part that holds most of it (the eyes and mouth
# sit on the head's fill, so their regions count as head)
owner = {'body': BELOW & right_of_pole & ~PAWS, 'earL': EAR_L & right_of_pole, 'earR': EAR_R,
         'head': ABOVE & right_of_pole & ~PAWS & ~EAR_L & ~EAR_R, 'pawT': PAW_T, 'pawB': PAW_B}
fills = {k: np.zeros((H, W), bool) for k in parts}
wl, wn = ndimage.label(~outside & ~ink & ~barrier | (~outside & ~ink))
for i in range(1, wn + 1):
    comp = wl == i
    if comp.sum() < 30: continue
    best = max(owner, key=lambda k: (comp & owner[k]).sum())
    fills[best] |= comp
for k in fills:
    if fills[k].any():   # grow under the ink so no hairline gaps show between fill and outline
        fills[k] = ndimage.binary_dilation(fills[k], iterations=6) & (~outside | ink) & ~(pole_cols & ~PAWS)
inside = ~outside | ink

UP = 2
def trace(mask, turd=30, tol=0.3):
    if not mask.any(): return ''
    m = Image.fromarray((mask * 255).astype(np.uint8)).resize((W * UP, H * UP), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.1))
    bm = potrace.Bitmap(~(np.array(m) > 127))   # potracer traces the False pixels
    path = bm.trace(turdsize=turd, alphamax=1.0, opticurve=True, opttolerance=tol)
    f = lambda p: f'{round(p.x / UP)} {round(p.y / UP)}'   # whole pixels: 1 px here is ~0.25 px on screen
    d = []
    for c in path:
        xs = [c.start_point.x] + [s.end_point.x for s in c.segments]
        ys = [c.start_point.y] + [s.end_point.y for s in c.segments]
        if min(xs) < 2 and max(xs) > W * UP - 2 and min(ys) < 2 and max(ys) > H * UP - 2: continue
        d.append(f'M{f(c.start_point)}')
        for s in c.segments:
            d.append(f'L{f(s.c)}L{f(s.end_point)}' if s.is_corner else f'C{f(s.c1)} {f(s.c2)} {f(s.end_point)}')
        d.append('Z')
    return ''.join(d)

out = {'w': W, 'h': H, 'pole_x': POLE_X, 'pole_w': POLE[1] - POLE[0] - 1, 'parts': {}}
for name, m in parts.items():
    ink_m = ink & m & ~(pole_cols & ~PAWS)
    if name == 'earL': ink_m = EAR_L_INK & right_of_pole
    if name == 'earR': ink_m = EAR_R_INK
    if name == 'head': ink_m = ink_m | (ink & (EAR_L | EAR_R) & ~EAR_L_INK & ~EAR_R_INK & ABOVE & right_of_pole); ink_m &= ~EAR_L_INK & ~EAR_R_INK
    fill_m = fills[name]
    if name.startswith('paw'): fill_m = ndimage.binary_fill_holes(ink & m) & m
    out['parts'][name] = {'ink': trace(ink_m), 'fill': trace(ndimage.binary_opening(fill_m, iterations=2), 60, 1.2)}
    print(name, len(out['parts'][name]['ink']), len(out['parts'][name]['fill']))
json.dump(out, open(OUT, 'w'))

if PREVIEW:   # colour each part's fill so the cuts can be checked
    cols = {'body': (255, 220, 220), 'earL': (220, 255, 220), 'earR': (220, 255, 220), 'head': (220, 230, 255),
            'mouth': (255, 240, 180), 'eyeL': (255, 200, 255), 'eyeR': (255, 200, 255), 'pawT': (200, 255, 255), 'pawB': (200, 255, 255)}
    pv = np.full((H, W, 3), 255, np.uint8)
    for name in parts:
        pv[fills[name]] = cols[name]
    pv[ink] = (0, 0, 0)
    pv[pole_cols & ~PAWS] = (255, 0, 0)
    for x, y in NECK_CUT: pv[max(0, y - 3):y + 3, max(0, x - 3):x + 3] = (255, 0, 0)
    Image.fromarray(pv).resize((W // 2, H // 2)).save(PREVIEW)
