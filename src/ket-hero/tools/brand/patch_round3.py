"""Client round 3 for ket-product.html (one-off patch, kept for reference):
 - all gazelles black and white (colour only as an outline around the box / cloud)
 - no cloud or bubble behind what a gazelle says: the words sit above it
 - the welcome is the "ارحبوووو" gazelle: paws grip the left edge, the head slides out, then it talks
 - the side moments are full cartoon gazelles that walk, hop or sit (legs, ears, blinks, talking)
 - story: blur crossfade instead of the circle; mobile story photo no longer cropped
 - footer as in the client's reference; accordion as rounded grey cards; sticky bar price on one line
Usage: python3 patch_round3.py <ket-product.html> <assets-src dir>
"""
import sys, re, json, base64, io
import numpy as np
from PIL import Image

path, A = sys.argv[1], sys.argv[2]
s = open(path, encoding='utf-8').read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count}, found {n}: {old[:100]!r}'
    s = s.replace(old, new)


def rex(pattern, new, count=1):
    global s
    s, n = re.subn(pattern, new, s, flags=re.S)
    assert n == count, f'regex expected {count}, found {n}: {pattern[:100]!r}'


def webp_uri(im, q=88):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=6)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


# ============================================================ 1. rigs: colour marks -> black
i = s.index('/*RIGS*/const RIGS = ') + len('/*RIGS*/const RIGS = ')
R, end = json.JSONDecoder().raw_decode(s[i:])
for name, r in R.items():
    for layer in ('spark', 'zzz'):
        if layer not in r['layers']: continue
        im = Image.open(io.BytesIO(base64.b64decode(r['layers'][layer].split(',')[1]))).convert('RGBA')
        a = np.array(im)
        a[..., :3] = 17                           # every mark becomes ink black, alpha kept
        out = Image.fromarray(a, 'RGBA')
        out.save(f'{A}/mascot/rigs/{name}-{layer}.webp', 'WEBP', quality=88, method=6)
        r['layers'][layer] = webp_uri(out)
s = s[:i] + json.dumps(R, separators=(',', ':')) + s[i + end:]

# ============================================================ 2. data: i18n
rep("""      hey: 'هلا', peekHi: 'هلا والله! حيّاك في ket، خذ راحتك وتفرّج.',""",
    """      hey: 'هلا', peekHi: 'هلا والله! حيّاك في ket، خذ راحتك وتفرّج.', arhab: 'ارحبوووو!',
      peekBuyT: 'محتار؟', peekBuyS: 'كلّمنا على واتساب ونساعدك تختار.', peekRevT: '{n} عميل', peekRevS: 'قيّموه قبلك، شوف وش قالوا.', peekDimsT: 'قِس مكانك أول', peekDimsS: 'وخلّ له مساحة يتنفّس فيها.',
      touch: 'تواصل معنا:', vatNo: 'الرقم الضريبي: {n}', crNo: 'رقم السجل التجاري: {n}', allRights: 'جميع الحقوق محفوظة', sbc: 'موثّق في المركز السعودي للأعمال',""")
rep("""      hey: 'Hey', peekHi: 'Hi there! Welcome to ket. Take your time and look around.',""",
    """      hey: 'Hey', peekHi: 'Hi there! Welcome to ket. Take your time and look around.', arhab: 'Hello!',
      peekBuyT: 'Still deciding?', peekBuyS: 'Message us and we will help you choose.', peekRevT: '{n} customers', peekRevS: 'rated it before you. See what they said.', peekDimsT: 'Measure first', peekDimsS: 'and give it room to breathe.',
      touch: 'Get in touch:', vatNo: 'The VAT number: {n}', crNo: 'The commercial register number: {n}', allRights: 'All Rights Reserved', sbc: 'Verified by the Saudi Business Center',""")
rep("""  whatsapp: '',                       // e.g. '9665XXXXXXXX' from Zid settings""",
    """  whatsapp: '',                       // e.g. '9665XXXXXXXX' from Zid settings
  vat: '310803678600003', cr: '4030396963',   // from the client's footer design""")

# ============================================================ 3. CSS
# what a gazelle says: plain words above it, no cloud behind
rex(r"\.peek__say\{ position:fixed; max-width:min\(240px, 62vw\);[^}]*\}\n",
    """.peek__say{ position:fixed; width:max-content; max-width:min(250px, 66vw); font:700 17px/1.35 'Marhey', var(--f-ar); color:#111; text-align:center;
  text-shadow:0 0 3px #fff, 0 0 6px #fff, 0 0 10px #fff; pointer-events:auto; opacity:0; transform:scale(.6); transition:opacity .25s, transform .5s cubic-bezier(.34,1.56,.64,1); }
""")
rep(""".peek__say a{ display:inline-flex; margin-top:8px; height:32px; align-items:center; padding-inline:14px; border-radius:var(--r-pill); background:var(--green); color:var(--white); text-decoration:n""",
    """.peek__say a{ display:inline-flex; margin-top:8px; height:32px; align-items:center; padding-inline:14px; border-radius:var(--r-pill); background:#111; color:var(--white); text-shadow:none; text-decoration:n""")
rex(r"\.rig__hey\{ position:absolute; left:50%; top:-4%; transform:translateX\(-50%\) rotate\(-7deg\); padding:[^;]*; border-radius:[^;]*;\n  background:var\(--hl, var\(--yellow\)\); color:#000;",
    """.rig__hey{ position:absolute; left:50%; top:-4%; transform:translateX(-50%) rotate(-7deg); padding:0;
  background:none; color:#111; text-shadow:0 0 3px #fff, 0 0 6px #fff;""")
# shipping gazelle (black and white, coloured outline around the box)
rex(r"\.gzbox\{ position:relative; display:block; width:110px; \}",
    """.gzbox{ position:relative; display:block; width:112px; }""")
rex(r"\.gzbox__logo\{ position:absolute; left:49%; top:82%; width:34%;",
    """.gzbox__logo{ position:absolute; left:49%; top:79.5%; width:33%;""")
# story: blur crossfade instead of the circle reveal; mobile photo square so the chair is never cropped
rep(""".story__detail{ position:absolute; inset:0; clip-path:circle(0% at 50% 50%); }""",
    """.story__detail{ position:absolute; inset:0; opacity:0; will-change:opacity, filter; }""")
rep("""@media (max-width:1023px){ .story__card{ aspect-ratio:auto; height:100%; max-height:46svh; } }""",
    """@media (max-width:1023px){ .story__card{ aspect-ratio:1 / 1; height:auto; width:min(100%, 46svh); } }""")
rep("""html:not(.motion) .story__detail{ clip-path:none; position:relative;""", """html:not(.motion) .story__detail{ opacity:1; position:relative;""")
# accordion: rounded grey cards (client's reference for the bottom of the store)
rex(r"\.acc\{ border-top:1px solid var\(--black\); \}\n\.acc__item\{ border-bottom:1px solid var\(--g200\); \}\n\.acc__btn\{([^}]*)padding:22px 0;",
    """.acc{ display:grid; gap:10px; }
.acc__item{ background:var(--g100); border-radius:22px; }
.acc__btn{\\1padding:18px 22px;""")
rep(""".acc__content{ padding-bottom:26px;""", """.acc__content{ padding:0 22px 22px;""")
rep(""".acc__icon{ position:relative; width:32px; height:32px; flex:none; border-radius:50%; border:1px solid var(--black);""",
    """.acc__icon{ position:relative; width:32px; height:32px; flex:none; border-radius:50%; border:0;""")
rep(""".acc__btn:hover .acc__icon{ background:var(--black); color:var(--white); }""", """.acc__btn:hover .acc__icon{ background:var(--white); }""")
rep(""".acc__btn[aria-expanded="true"] .acc__icon{ transform:rotate(135deg); background:var(--black); color:var(--white); }""",
    """.acc__btn[aria-expanded="true"] .acc__icon{ transform:rotate(135deg); }""")
# sticky bar: keep the price on one line
rep(""".sticky-bar__price{ font:600 15px var(--f-latin); }""", """.sticky-bar__price{ font:600 15px var(--f-latin); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }""")
rep(""".sticky-bar__price s{ font-weight:400; font-size:12px; color:var(--ink-2); margin-inline-start:6px; }""",
    """.sticky-bar__price s{ font-weight:400; font-size:11.5px; color:var(--ink-2); margin-inline-start:6px; }""")
# footer: the client's layout
rex(r"\.footer\{ background:var\(--blush\);.*?\.footer__legal\{[^}]*\}\n",
    """.footer{ background:var(--blush); padding-top:var(--s7); padding-bottom:calc(var(--s7) + 72px); overflow:hidden; position:relative; }
.footer__grid{ display:grid; gap:var(--s5); justify-items:center; text-align:center; }
.footer__mark{ display:grid; justify-items:center; gap:10px; }
.footer__mark svg{ width:64px; height:auto; display:block; }
.footer__copy{ font-size:13px; color:var(--ink-2); }
.footer__touch{ display:grid; justify-items:center; gap:12px; }
.footer__touch p{ font-size:15px; font-weight:500; }
.social{ display:flex; gap:4px; }
.social a{ width:40px; height:40px; border-radius:50%; display:grid; place-items:center; color:#111; transition:background-color .25s; }
.social a:hover{ background:rgba(0,0,0,.07); }
.pays{ display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:14px 26px; max-width:520px; }
.pay{ display:inline-flex; align-items:center; gap:5px; color:#111; font:700 19px/1 var(--f-latin); letter-spacing:-.02em; }
.pay--visa{ font-style:italic; font-weight:800; font-size:21px; letter-spacing:.01em; }
.pay--mada{ font-size:15px; flex-direction:column; gap:1px; align-items:flex-start; }
.pay--mada i{ display:block; width:32px; height:4px; background:#111; border-radius:1px; }
.pay--flow{ font-weight:800; letter-spacing:-.04em; }
.pay--mc{ gap:0; } .pay--mc b{ width:20px; height:20px; border-radius:50%; background:#111; display:block; } .pay--mc b + b{ margin-inline-start:-8px; background:transparent; border:3px solid #111; }
.pay--amex{ font-size:9.5px; font-weight:800; background:#111; color:var(--blush); padding:6px 5px; border-radius:3px; letter-spacing:.02em; }
.footer__legal{ display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:10px 18px; font-size:12px; color:#111; }
.footer__legal .sbc{ display:inline-flex; align-items:center; gap:6px; padding:6px 10px; border:1px solid rgba(0,0,0,.25); border-radius:8px; font-size:11px; }
.footer__legal .ids{ display:grid; gap:2px; text-align:start; }
html[dir="rtl"] .footer__legal .ids{ text-align:right; }
@media (min-width:1024px){
  .footer__grid{ grid-template-columns:1fr 1fr; justify-items:stretch; text-align:start; row-gap:var(--s6); }
  .footer__mark{ grid-column:1; grid-row:1; justify-items:start; }
  .footer__touch{ grid-column:2; grid-row:1; justify-items:end; }
  .pays, .footer__legal{ grid-column:1 / -1; justify-self:center; }
}
""")
rex(r"\.footer__brand\{[^}]*\}\n\.footer__logo svg\{[^}]*\}\n\.stamp\{[^}]*\}\n\.stamp svg\{[^}]*\}\n\.stamp__ring\{[^}]*\}\n", "")
rex(r"@keyframes stamp-spin\{[^\n]*\n", "")

# ============================================================ 4. markup: footer
rex(r'<footer class="footer">\n  <div class="container">\n.*?\n  </div>\n</footer>',
    """<footer class="footer">
  <div class="container footer__grid">
    <div class="footer__mark"><span id="footerSmile"></span><p class="footer__copy">© <span data-t="allRights"></span></p></div>
    <div class="footer__touch"><p data-t="touch"></p><div class="social" id="social"></div></div>
    <div class="pays" aria-label="Payment methods">
      <span class="pay pay--visa">VISA</span>
      <span class="pay pay--apple" id="payApple">Pay</span>
      <span class="pay pay--tabby">tabby</span>
      <span class="pay pay--mada"><i></i>mada</span>
      <span class="pay pay--flow">Flow</span>
      <span class="pay pay--mc" aria-label="Mastercard"><b></b><b></b></span>
      <span class="pay pay--amex">AMERICAN<br>EXPRESS</span>
    </div>
    <div class="footer__legal">
      <span class="sbc" data-t="sbc"></span>
      <span class="ids"><span id="vatNo"></span><span id="crNo"></span></span>
    </div>
  </div>
</footer>""")

# ============================================================ 5. JS: brand bits, footer build
rep("""  ig: '<rect x="4" y="4" width="16" height="16" rx="5"/>""",
    """  wa: '<path d="M5.2 18.8l1-3.6A7.8 7.8 0 1 1 9 18.2Z"/><path d="M9.6 9.2c.3 2 1.7 3.6 3.9 4.4l1-1 1.8.8c-.2 1-1 1.6-2 1.6-3 0-6.2-3-6.2-6 0-1 .6-1.8 1.6-2l.8 1.8Z"/>',
  mail: '<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/>',
  globe: '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.4 3.6 5.2 3.6 8.5S14.4 18.1 12 20.5M12 3.5C9.6 5.9 8.4 8.7 8.4 12s1.2 6.1 3.6 8.5"/>',
  ig: '<rect x="4" y="4" width="16" height="16" rx="5"/>""")
rex(r"  \$\('#footerLogo'\)\.innerHTML = lockup\(\);\n  \$\('#stamp'\)\.innerHTML = stamp\(\);\n  \$\('#social'\)\.innerHTML = \[\['ig', 'Instagram'\], \['tiktok', 'TikTok'\], \['snap', 'Snapchat'\], \['x', 'X'\]\]",
    """  $('#footerSmile').innerHTML = smileMark(64);
  $('#payApple').insertAdjacentHTML('afterbegin', '<svg width="17" height="20" viewBox="0 0 17 20" aria-hidden="true"><path fill="#111" d="M14 10.6c0-2.3 1.9-3.4 2-3.5a4.3 4.3 0 0 0-3.4-1.8c-1.4-.2-2.8.8-3.5.8s-1.8-.8-3-.8A4.5 4.5 0 0 0 2.4 7.6c-1.6 2.8-.4 6.9 1.1 9.2.8 1.1 1.7 2.3 2.9 2.3s1.6-.8 3-.8 1.8.8 3 .7 2-1.1 2.8-2.2a9.8 9.8 0 0 0 1.3-2.6A3.9 3.9 0 0 1 14 10.6ZM11.7 3.8A4 4 0 0 0 12.6.9a4.1 4.1 0 0 0-2.7 1.4 3.8 3.8 0 0 0-.9 2.8 3.4 3.4 0 0 0 2.7-1.3Z"/></svg>');
  $('#social').innerHTML = [['snap', 'Snapchat'], ['ig', 'Instagram'], ['tiktok', 'TikTok'], ['wa', 'WhatsApp'], ['mail', 'Email'], ['globe', 'Website']]""")
rep("""  $('#wa').href = `https://wa.me/${STORE.whatsapp}?text=${encodeURIComponent(L(P.name) + ' — ' + P.sku)}`;""",
    """  $('#wa').href = `https://wa.me/${STORE.whatsapp}?text=${encodeURIComponent(L(P.name) + ' — ' + P.sku)}`;
  $('#vatNo').textContent = t('vatNo', { n: STORE.vat }); $('#crNo').textContent = t('crNo', { n: STORE.cr });""")

# shipping gazelle: the client's black-and-white box drawing with the coloured box outline
box_uri = 'data:image/webp;base64,' + base64.b64encode(open(f'{A}/mascot/rigs/box-bw.webp', 'rb').read()).decode()
rex(r"const gazelleBox = \(\) => `<span class=\"gzbox\">\$\{gz\('box', ''\)\}",
    f"const GZ_BOX_BW = '{box_uri}';\nconst gazelleBox = () => `<span class=\"gzbox\"><img src=\"${{GZ_BOX_BW}}\" alt=\"\" width=\"340\" height=\"440\" decoding=\"async\">")

# ============================================================ 6. JS: the new gazelle engine + welcome + walkers
arhab = json.load(open(f'{A}/mascot/rigs/arhab.json'))
engine = open(f'{A}/../tools/brand/gazelle-rigs.js', encoding='utf-8').read()
engine = engine.replace("  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;\n", "")
rep("""/* =================================================================
   INTERACTIVE GAZELLE — peeks in when the customer lingers on a section.""",
    "/*ARHAB*/const ARHAB = " + json.dumps(arhab, separators=(',', ':')) + ";\n" + engine + """
const KG = KetGazelle(ARHAB, { t: (k, v) => t(k, v), onDone: () => { if (peekNow && (peekNow.walker || peekNow.id === 'hi')) peekNow = null; } });

/* =================================================================
   INTERACTIVE GAZELLE — peeks in when the customer lingers on a section.""")
# the walkers say a short line (big) and a longer one (small) above themselves
rex(r"const PEEKS = \[\n.*?\n\];\n",
    """const PEEKS = [
  { id: 'buy', zone: '#buy', after: 6, walker: 'walk', say: ['peekBuyT', 'peekBuyS'], act: 'wa' },
  { id: 'ship', zone: '#info', after: 2.5, rig: 'hey-pink-paws', mode: 'bottom', say: 'peekShip' },
  { id: 'dims', zone: '#dimensions', after: 2.5, walker: 'sit', say: ['peekDimsT', 'peekDimsS'] },
  { id: 'rev', zone: '#reviews', after: 2.5, walker: 'hop', say: ['peekRevT', 'peekRevS'] }
];
""")
rep("""const PEEK_HI = { id: 'hi', rig: 'hey-green', hey: true, mode: 'bottom', say: 'peekHi' };""",
    """const PEEK_HI = { id: 'hi' };   // the ارحبوووو welcome (KG.welcome)""")
rep("""const peekBusy = () => drawer.classList.contains('is-open') || lb.classList.contains('is-open') || document.hidden;""",
    """const peekBusy = () => drawer.classList.contains('is-open') || lb.classList.contains('is-open') || document.hidden || KG.busy();""")
rep("""function showPeek(p) {
  peekNow = p; peekCount++; peekLast = Date.now(); peekSeen.add(p.id); peekSave();""",
    """function showPeek(p) {
  peekNow = p; peekCount++; peekLast = Date.now(); peekSeen.add(p.id); peekSave();
  if (p.walker) {   // a whole gazelle walks / hops in, says its line above itself, then leaves
    const n = P.reviewCount;
    KG.walk(p.walker, esc(t(p.say[0], { n })), esc(t(p.say[1], { n })), p.act === 'wa' && STORE.whatsapp ? { href: $('#wa').href, label: esc(t('peekWa')) } : null);
    return;
  }""")
rep("""  showPeek(PEEK_HI); peekCount--;   // the welcome does not use up one of the five moments
  clearTimeout(peekHideT); peekHideT = setTimeout(hidePeek, 7000);""",
    """  peekNow = PEEK_HI; KG.welcome();   // the welcome does not use up one of the five moments""")
rep("""  if (peekNow && peekNow.zone) { const r = $(peekNow.zone).getBoundingClientRect(); if (r.bottom < innerHeight * .2 || r.top > innerHeight * .8) hidePeek(); }""",
    """  if (peekNow && peekNow.zone && !peekNow.walker) { const r = $(peekNow.zone).getBoundingClientRect(); if (r.bottom < innerHeight * .2 || r.top > innerHeight * .8) hidePeek(); }""")
rep("""// first visit ever: the gazelle pops out of its box and waves هلا / Hey""",
    """// first visit ever: paws grip the left edge, the head slides out and says ارحبوووو""")

# ============================================================ 7. JS: story blur crossfade
rep(""".fromTo('#storyDetail', { clipPath: 'circle(0% at 50% 50%)' }, { clipPath: 'circle(75% at 50% 50%)', duration: 1.1, ease: 'power2.inOut' }, '<')""",
    """.fromTo('#storyDetail', { opacity: 0, filter: 'blur(22px)' }, { opacity: 1, filter: 'blur(0px)', duration: 1.1, ease: 'power2.inOut' }, '<')
    .fromTo('#storyProduct', { filter: 'blur(0px)' }, { filter: 'blur(16px)', duration: 1.1, ease: 'power2.inOut' }, '<')""")
rep("""mm.add('(max-height: 559px)', () => { gsap.set('#storyDetail', { clipPath: 'none' }); });""",
    """mm.add('(max-height: 559px)', () => { gsap.set('#storyDetail', { opacity: 1, filter: 'none' }); });""")

open(path, 'w', encoding='utf-8').write(s)
print('patched', path, round(len(s) / 1e6, 2), 'MB')
