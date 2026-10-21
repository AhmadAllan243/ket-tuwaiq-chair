"""Inlines the gazelle rig layers (assets-src/mascot/rigs) into ket-product.html as `const RIGS = {...}`,
between the /*RIGS*/ ... /*/RIGS*/ markers. Run after cut_rigs.py."""
import base64, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '..', 'assets-src', 'mascot', 'rigs')
PAGE = os.path.join(HERE, '..', '..', '..', 'ket-product.html')
meta = json.load(open(os.path.join(D, 'rigs.json')))
rigs = {}
for name, m in meta.items():
    layers = {l: 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(D, f'{name}-{l}.webp'), 'rb').read()).decode() for l in m['layers']}
    rigs[name] = {'w': m['w'], 'h': m['h'], 'pivots': m['pivots'], 'layers': layers}
block = '/*RIGS*/const RIGS = ' + json.dumps(rigs, separators=(',', ':')) + ';/*/RIGS*/'
s = open(PAGE).read()
if '/*RIGS*/' in s:
    s = re.sub(r'/\*RIGS\*/.*?/\*/RIGS\*/', lambda _: block, s, count=1, flags=re.S)
else:  # first run: place right after the BRAND block
    i = s.index('const BRAND = '); j = s.index('\n', i)
    s = s[:j + 1] + '// gazelle animation layers (tools/brand/cut_rigs.py + pack_rigs.py)\n' + block + '\n' + s[j + 1:]
open(PAGE, 'w').write(s)
print('packed', len(block) // 1024, 'KB into', os.path.basename(PAGE))
