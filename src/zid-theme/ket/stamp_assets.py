"""
Gives every KET asset address a fingerprint of its contents (…/ket-home.js?v=v1.0.10&k=3f2a9c1b), so a new
upload is never served from a browser's or the CDN's old copy (Zid keeps the same ?v= across uploads).
Run before zipping (ket/make-upload-zip.sh does).
"""
import hashlib, os, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ASSETS = ['ket.css', 'ket-site.js', 'ket-product.js', 'ket-hero.js', 'ket-brand.js', 'ket-home.css', 'ket-home.js', 'ket-category.css', 'ket-category.js', 'ket-cart.js']
H = {a: hashlib.sha1(open(os.path.join(ROOT, 'assets', a), 'rb').read()).hexdigest()[:8] for a in ASSETS if os.path.exists(os.path.join(ROOT, 'assets', a))}
n = 0
for d, _, files in os.walk(ROOT):
    if 'node_modules' in d or '/.' in d: continue
    for f in files:
        if not f.endswith('.jinja'): continue
        p = os.path.join(d, f); s = open(p).read(); o = s
        for a, h in H.items():
            # {{ 'ket-home.js' | asset_url }}  (optionally followed by an older &k=…)
            s = re.sub(r"(\{\{\s*'" + re.escape(a) + r"'\s*\|\s*asset_url\s*\}\})(&k=[0-9a-f]+)?", lambda m: m.group(1) + '&k=' + h, s)
        if s != o: open(p, 'w').write(s); n += 1
print('stamped', n, 'templates')
