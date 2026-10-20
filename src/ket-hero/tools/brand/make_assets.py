"""Builds the JS asset block (logo paths, brand icons, gazelle + illustration data URIs)."""
import sys, json, base64, re

S = sys.argv[1]
L = json.load(open(f'{S}/logo_paths.json'))
I = json.load(open(f'{S}/icons.json'))


def real(entry):
    w, h = entry['size']
    return [p for p in entry['paths'] if not (p['x0'] < 1 and p['x1'] > w - 1)]


def shift(d, dx, dy, k=1.0):
    nums = re.findall(r'-?\d+\.?\d*', d)
    out, i = [], 0
    def rep(m):
        nonlocal i
        v = float(m.group(0)); r = (v - (dx if i % 2 == 0 else dy)) * k; i += 1
        return f'{r:.1f}'.rstrip('0').rstrip('.')
    return re.sub(r'-?\d+\.?\d*', rep, d)


# ---- ket wordmark: k, e (outer + counter), t
kp = real(L['ket'])
x0 = min(p['x0'] for p in kp); x1 = max(p['x1'] for p in kp)
y0 = min(p['y0'] for p in kp); y1 = max(p['y1'] for p in kp)
letters = {'k': [], 'e': [], 't': []}
for p in kp:
    cx = (p['x0'] + p['x1']) / 2
    key = 'k' if p['x1'] < 92 else ('t' if p['x0'] > 175 else 'e')
    letters[key].append(shift(p['d'], x0, y0))
W, H = x1 - x0, y1 - y0
# x-height zone (top of e to baseline) for placing the smile
e_top = min(p['y0'] for p in kp if 92 <= (p['x0'] + p['x1']) / 2 <= 175) - y0

# ---- smile
sp = real(L['smile'])[0]
sw, sh = sp['x1'] - sp['x0'], sp['y1'] - sp['y0']
k = (W * 0.42) / sw
smile_d = shift(sp['d'], sp['x0'], sp['y0'], k)
smile_w, smile_h = sw * k, sh * k
sx = (W - smile_w) / 2
sy = e_top + ((H - e_top) - smile_h) / 2 + smile_h * 0.12

# standalone smile viewBox
smile_alone = shift(sp['d'], sp['x0'], sp['y0'])

# ---- lockup (ket + TANASOUB) for the footer
lp = real(L['lockup'])
lx0 = min(p['x0'] for p in lp); lx1 = max(p['x1'] for p in lp)
ly0 = min(p['y0'] for p in lp); ly1 = max(p['y1'] for p in lp)
lock_d = ''.join(shift(p['d'], lx0, ly0) for p in lp)

def uri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()

gz = {n: uri(f'{S}/gz/gazelle-{n}.webp', 'image/webp') for n in ['box', 'sleep', 'sit', 'hop', 'stand']}
gzmeta = json.load(open(f'{S}/gz/meta.json'))

out = {
    'KET': {'w': round(W, 1), 'h': round(H, 1), 'k': ''.join(letters['k']), 'e': ''.join(letters['e']), 't': ''.join(letters['t']),
            'smile': {'d': smile_d, 'x': round(sx, 1), 'y': round(sy, 1)}},
    'SMILE': {'w': round(sw, 1), 'h': round(sh, 1), 'd': smile_alone},
    'LOCKUP': {'w': round(lx1 - lx0, 1), 'h': round(ly1 - ly0, 1), 'd': lock_d},
    'SHAPES': {n: {'w': v['w'], 'h': v['h'], 'c': v['col'], 'd': v['d']} for n, v in I.items()},
    'GZ': gz,
    'GZSIZE': {n: [m['w'], m['h']] for n, m in gzmeta.items()},
    'ILLUS': uri(f'{S}/illus.webp', 'image/webp'),
}
js = '/* ket brand assets — traced from the client\'s logo sheet, trust graphic and mascot drawings */\nconst BRAND = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(f'{S}/brand_assets.js', 'w').write(js)
print('KET', out['KET']['w'], out['KET']['h'], 'smile at', sx, sy, 'e_top', e_top, 'bytes', len(js))
