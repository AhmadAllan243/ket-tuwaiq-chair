# Embeds the Zid product photos as JPEG data URIs (except tiny thumbnails).
import sys, re, base64, io, urllib.request, subprocess
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
s = open(src).read()
URL = r'https://media\.zid\.store/3d020177-292e-4bbd-8716-c86b494643f5/([0-9a-f-]+)\.png'
cache = {}
def data(uuid):
    if uuid not in cache:
        raw = subprocess.run(['curl', '-s', f'https://media.zid.store/3d020177-292e-4bbd-8716-c86b494643f5/{uuid}.png'], capture_output=True).stdout
        im = Image.open(io.BytesIO(raw)).convert('RGB'); im.thumbnail((1000, 1000))
        b = io.BytesIO(); im.save(b, 'JPEG', quality=78, optimize=True, progressive=True)
        cache[uuid] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    return cache[uuid]
seen = set()
def sub(m):
    # embed each photo once (its first use, e.g. the gallery); repeats keep the CDN URL so the page stays light
    tag = m.group(0)
    if 'width="64"' in tag or 'width="48"' in tag: return tag
    def one(mm):
        uuid = mm.group(1)
        if uuid in seen: return mm.group(0)
        seen.add(uuid); return f'src="{data(uuid)}"'
    return re.sub(r'src="' + URL + '"', one, tag)
s = re.sub(r'<img\b[^>]*>', sub, s)
open(out, 'w').write(s)
print(f'embedded {len(cache)} images, {len(s)/1e6:.2f} MB')
