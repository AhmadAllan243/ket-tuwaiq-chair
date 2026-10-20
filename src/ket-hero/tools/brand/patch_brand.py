"""Client round 2 for ket-product.html:
purchase motivators, real logo + smile morph, real gazelle drawings in brand colours,
interactive gazelle peeks, decoration-inspiration chips, footer lockup + stamp.
Usage: python3 patch_brand.py src/ket-product.html brand_assets.js
"""
import sys, re

path, assets = sys.argv[1], sys.argv[2]
s = open(path, encoding='utf-8').read()
BRAND_JS = open(assets, encoding='utf-8').read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count}, found {n}: {old[:90]!r}'
    s = s.replace(old, new)


def rex(pattern, new, count=1):
    global s
    s, n = re.subn(pattern, new, s, flags=re.S)
    assert n == count, f'regex expected {count}, found {n}: {pattern[:90]!r}'


# =========================================================== DATA
rep("""    sold: '1,000+',
    rating: 4.8, reviewCount: 126,     // SAMPLE — from Zid reviews in production""",
"""    sold: '1,653+', soldCount: 1653,  // client figures (Oct 2026); in Zid: product sales count
    rating: 5.0, reviewCount: 326,     // client figures (Oct 2026); in Zid: live product rating""")
rep("""      distribution: [82, 12, 4, 1, 1],""", """      distribution: [96, 4, 0, 0, 0],""")

INSP = """
  // "Find more decoration inspiration" — rooms link to Zid collections in production
  inspiration: [
    { key: 'living', color: 'var(--lavender)', name: { ar: 'غرفة المعيشة', en: 'Living room' } },
    { key: 'bath', color: 'var(--g100)', name: { ar: 'الحمّام', en: 'Bath' } },
    { key: 'garden', color: 'var(--mint)', name: { ar: 'الحديقة', en: 'Garden' } },
    { key: 'bedroom', color: 'var(--peri)', name: { ar: 'غرفة النوم', en: 'Bedroom' } },
    { key: 'kitchen', color: 'var(--g100)', name: { ar: 'المطبخ', en: 'Kitchen' } },
    { key: 'office', color: 'var(--g100)', name: { ar: 'المكتب', en: 'Office' } }
  ],
"""
rep("""  // "Complete the majlis" — neutral placeholders where no image is given""",
    INSP.lstrip('\n') + """
  // "Complete the majlis" — neutral placeholders where no image is given""")

AR_KEYS = """g1: 'ضمان تسليم', g1s: 'نضمن وصول طلبك سالمًا.', g2: 'توصيل مجاني', g2s: 'لجميع مناطق المملكة.', g3: 'استبدال واسترجاع خلال 24 ساعة', g3s: 'راحتك أولويتنا.',
      proofBuy: 'تم شراؤه', proofRev: 'تقييم', proofRate: 'تقييم العملاء', proofLabel: 'أرقام المنتج',
      peekBuy: 'محتار؟ كلّمنا على واتساب ونساعدك تختار.', peekShip: 'التوصيل علينا، لكل مدن المملكة.', peekDims: 'قِس مكانك أول، وخلّ له مساحة يتنفّس فيها.', peekRev: '{n} عميل قيّموه قبلك.', peekIdle: 'خذ راحتك، إحنا هنا.', peekWa: 'كلّمنا',
      inspEyebrow: 'إلهام', inspTitle: 'اكتشف أفكار ديكور أكثر مع ket', inspBody: 'اختر الغرفة، ونوريك قطعًا تناسبها.',
      relEyebrow: 'أكمل الجلسة', relTitle: 'كمّل مجلسك',"""
EN_KEYS = """g1: 'Delivery guarantee', g1s: 'We guarantee your order arrives safely.', g2: 'Free delivery', g2s: 'Across all of Saudi Arabia.', g3: 'Exchange & return within 24 hours', g3s: 'Your peace of mind is our priority.',
      proofBuy: 'Purchases', proofRev: 'Reviews', proofRate: 'Customer rating', proofLabel: 'Product numbers',
      peekBuy: 'Still deciding? Message us and we will help you choose.', peekShip: 'Delivery is on us, anywhere in the Kingdom.', peekDims: 'Measure first, and give it room to breathe.', peekRev: '{n} customers rated it before you.', peekIdle: 'Take your time. We are here.', peekWa: 'Message us',
      inspEyebrow: 'Inspiration', inspTitle: 'Find more decoration inspiration with ket', inspBody: 'Pick a room and we will show you pieces made for it.',
      relEyebrow: 'Complete the look', relTitle: 'Complete the majlis',"""
rep("""relEyebrow: 'أكمل الجلسة', relTitle: 'كمّل مجلسك',""", AR_KEYS)
rep("""relEyebrow: 'Complete the look', relTitle: 'Complete the majlis',""", EN_KEYS)
rex(r"returnsBody: 'تقدر ترجع المنتج خلال 7 أيام[^']*'",
    "returnsBody: 'تقدر تستبدل المنتج أو ترجعه خلال 24 ساعة من الاستلام، بشرط يكون بحالته الأصلية ومعه تغليفه. تواصل معنا عبر واتساب ونرتّب الاستلام.'")
rex(r"returnsBody: 'Return any item within 7 days[^']*'",
    "returnsBody: 'Exchange or return any item within 24 hours of delivery, in its original condition and packaging. Message us on WhatsApp and we will arrange the pickup.'")

# =========================================================== CSS
rep(""".logo svg{ width:68px; height:auto; transition:width .4s var(--ease); }
.header.is-scrolled .logo svg{ width:56px; }""",
""".logo svg{ width:64px; height:auto; overflow:visible; transition:width .4s var(--ease); }
.header.is-scrolled .logo svg{ width:58px; }
/* logo morph: at the top the full ket wordmark; once scrolled the letters fold down into the smile */
.klogo .kl{ transform-box:fill-box; transform-origin:50% 100%; transition:transform .6s var(--ease), opacity .35s var(--ease); }
.klogo .kl:nth-child(2){ transition-delay:.05s; } .klogo .kl:nth-child(3){ transition-delay:.1s; }
.klogo__smile{ transform-box:fill-box; transform-origin:50% 50%; opacity:0; clip-path:inset(0 50% 0 50%); transform:translateY(-10%) scale(.7); transition:clip-path .55s var(--ease), opacity .25s, transform .6s var(--ease); }
.header.is-scrolled .klogo .kl{ transform:translateY(10%) scale(.2, .04); opacity:0; }
.header.is-scrolled .klogo .klogo__smile{ opacity:1; clip-path:inset(0 0 0 0); transform:translateY(-42%) scale(1.45); transition-delay:.18s; }
@media (hover:hover){
  .header.is-scrolled .logo:hover .kl{ transform:none; opacity:1; }
  .header.is-scrolled .logo:hover .klogo__smile{ opacity:0; clip-path:inset(0 50% 0 50%); transition-delay:0s; }
}""")

rex(r"\.trust\{ display:grid;.*?\.trust span\{[^}]*\}",
""".trust{ display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-top:10px; }
.trust li{ position:relative; padding:14px 12px 13px; border-radius:16px; background:color-mix(in srgb, var(--tint) 18%, #fff); display:flex; flex-direction:column; gap:10px; font-size:13px; line-height:1.35; }
.trust .shape{ height:34px; width:auto; display:block; transition:transform .5s var(--ease); }
.trust li:hover .shape{ transform:translateY(-3px) rotate(-4deg); }
.trust strong{ font-weight:700; display:block; font-size:13.5px; }
.trust span{ color:var(--ink-2); font-size:12px; display:block; margin-top:2px; }
@media (max-width:420px){ .trust li{ padding:12px 9px; } .trust strong{ font-size:12.5px; } }
/* social proof strip (client figures) */
.proof{ display:grid; grid-template-columns:repeat(3,1fr); margin-top:var(--s5); background:var(--g100); border-radius:20px; padding:16px 6px; }
.proof__item{ display:flex; flex-direction:column; align-items:center; text-align:center; gap:4px; padding-inline:6px; }
.proof__item + .proof__item{ border-inline-start:1px solid var(--g200); }
.proof__ic{ width:44px; height:44px; border-radius:50%; background:var(--white); display:grid; place-items:center; margin-bottom:4px; }
.proof__ic--stars{ width:auto; background:none; height:44px; }
.proof .star__fill{ color:var(--amber); }
.proof .star{ color:#F1E4C8; }
.proof__num{ font:700 clamp(20px,2.2vw,26px)/1.1 var(--f-latin); letter-spacing:-.02em; }
.proof__num small{ font-size:.62em; font-weight:600; color:var(--ink-2); }
.proof__lab{ font-size:12.5px; color:var(--ink-2); line-height:1.3; }""")

rex(r"\.gzbox\{ position:relative;.*?\.gzbox__logo svg\{[^}]*\}",
""".gzbox{ position:relative; display:block; width:110px; }
.gzbox img{ display:block; width:100%; height:auto; }
/* the smile sits on the box front panel (x 10–88%, y 67–97% of the drawing), like a printed stamp */
.gzbox__logo{ position:absolute; left:49%; top:82%; width:34%; transform:translate(-50%,-50%) rotate(-3deg); color:#111; line-height:0; }
.gzbox__logo svg{ width:100%; height:auto; display:block; }""")

rex(r"/\* Gazelle mascot \*/.*?@keyframes gz-nod\{[^\n]*\n",
"""/* Gazelle mascot (client drawings, recoloured) */
img.gz{ display:block; height:auto; }

/* Interactive gazelle: peeks in when the customer lingers on a section */
.peek{ position:fixed; inset:0; z-index:57; pointer-events:none; }
.peek__fig{ position:fixed; width:var(--pw,124px); pointer-events:auto; cursor:pointer; opacity:0; visibility:hidden; border:0; padding:0; background:none;
  transition:transform .95s cubic-bezier(.34,1.56,.64,1), opacity .3s, visibility 0s .95s; }
.peek__fig img{ width:100%; height:auto; display:block; transform:scaleX(var(--flip,1)); }
.peek.is-on .peek__fig{ opacity:1; visibility:visible; transition:transform .95s cubic-bezier(.34,1.56,.64,1), opacity .3s; }
.peek.is-on .peek__fig img{ animation:peek-bob 2.6s ease-in-out 1s infinite; }
@keyframes peek-bob{ 0%,100%{ transform:scaleX(var(--flip,1)) translateY(0) rotate(0); } 50%{ transform:scaleX(var(--flip,1)) translateY(-5px) rotate(-3deg); } }
.peek--side .peek__fig{ top:44vh; }
.peek--side.peek--l .peek__fig{ left:0; transform:translateX(-110%) rotate(30deg); }
.peek--side.peek--l.is-on .peek__fig{ transform:translateX(-26%) rotate(16deg); }
.peek--side.peek--r .peek__fig{ right:0; transform:translateX(110%) rotate(-30deg); }
.peek--side.peek--r.is-on .peek__fig{ transform:translateX(26%) rotate(-16deg); }
.peek--bottom .peek__fig{ bottom:0; transform:translateY(110%); }
.peek--bottom.peek--l .peek__fig{ left:max(16px, 7vw); }
.peek--bottom.peek--r .peek__fig{ right:max(16px, 7vw); }
.peek--bottom.is-on .peek__fig{ transform:translateY(14%); }
body.bar-on .peek--bottom .peek__fig{ bottom:calc(72px + env(safe-area-inset-bottom)); }
.peek__say{ position:fixed; max-width:min(240px, 62vw); background:var(--white); border:1.5px solid var(--black); border-radius:18px; padding:10px 14px; font-size:14px; font-weight:600; line-height:1.45;
  box-shadow:0 12px 30px -12px rgba(0,0,0,.3); pointer-events:auto; opacity:0; transform:scale(.6); transition:opacity .25s, transform .5s cubic-bezier(.34,1.56,.64,1); }
.peek.is-on .peek__say{ opacity:1; transform:scale(1); transition-delay:.55s; }
.peek--side .peek__say{ top:calc(44vh - 58px); }
.peek--side.peek--l .peek__say{ left:calc(var(--pw,124px) * .78); transform-origin:0 100%; }
.peek--side.peek--r .peek__say{ right:calc(var(--pw,124px) * .78); transform-origin:100% 100%; }
.peek--bottom .peek__say{ bottom:calc(var(--pw,124px) * 1.12); }
body.bar-on .peek--bottom .peek__say{ bottom:calc(var(--pw,124px) * 1.12 + 72px); }
.peek--bottom.peek--l .peek__say{ left:calc(max(16px, 7vw) + var(--pw,124px) * .55); transform-origin:0 100%; }
.peek--bottom.peek--r .peek__say{ right:calc(max(16px, 7vw) + var(--pw,124px) * .55); transform-origin:100% 100%; }
.peek__say a{ display:inline-flex; margin-top:8px; height:32px; align-items:center; padding-inline:14px; border-radius:var(--r-pill); background:var(--green); color:var(--white); text-decoration:none; font-size:13px; }

/* Decoration inspiration */
.insp__grid{ display:grid; gap:var(--s6); align-items:center; }
@media (min-width:1024px){ .insp__grid{ grid-template-columns:1fr 1.1fr; gap:clamp(40px,5vw,96px); } }
.insp__body{ font-size:var(--t-md); color:var(--ink-2); max-width:40ch; }
.insp__chips{ display:flex; flex-wrap:wrap; gap:10px; margin-top:var(--s5); }
.insp__chip{ height:54px; padding-inline:26px; border-radius:16px; background:var(--chip, var(--g100)); font-size:16px; font-weight:500; display:inline-flex; align-items:center; text-decoration:none; color:var(--black);
  transition:transform .45s var(--ease), background-color .3s, color .3s; }
.insp__chip:hover{ transform:translateY(-3px); background:var(--black); color:var(--white); }
.insp__art{ margin:0; }
.insp__art img{ width:100%; height:auto; }

/* Footer brand: full lockup + "from our hands to your home" stamp */
.footer__brand{ display:flex; align-items:center; justify-content:space-between; gap:24px; margin-bottom:var(--s7); }
.footer__logo svg{ width:clamp(118px,13vw,170px); height:auto; display:block; }
.stamp{ width:clamp(92px,9vw,118px); flex:none; color:#111; }
.stamp svg{ width:100%; height:auto; display:block; }
.stamp__ring{ transform-origin:60px 60px; animation:stamp-spin 24s linear infinite; }
@keyframes stamp-spin{ to{ transform:rotate(360deg); } }
""")

rep("""@media (prefers-reduced-motion: reduce){\n""", """@media (prefers-reduced-motion: reduce){
  .klogo .kl, .klogo__smile, .peek__fig, .peek__say{ transition:none!important; }
  .peek.is-on .peek__fig img, .stamp__ring{ animation:none!important; }
""")

# =========================================================== MARKUP
rep("""      <ul class="trust" id="trust"></ul>""",
"""      <div class="proof" id="proof" role="group" data-t-aria="proofLabel" aria-label="أرقام المنتج">
        <div class="proof__item"><span class="proof__ic" id="proofIcBuy"></span><strong class="proof__num" id="proofBuy">1,653+</strong><span class="proof__lab" data-t="proofBuy"></span></div>
        <div class="proof__item"><span class="proof__ic" id="proofIcRev"></span><strong class="proof__num" id="proofRev">326</strong><span class="proof__lab" data-t="proofRev"></span></div>
        <div class="proof__item"><span class="proof__ic proof__ic--stars" id="proofStars"></span><strong class="proof__num" id="proofRate">5.0</strong><span class="proof__lab" data-t="proofRate"></span></div>
      </div>

      <ul class="trust" id="trust"></ul>""")

rep("""</main>""", """
<!-- =====================================================================
     SECTION 12 · DECORATION INSPIRATION   → Vitrin: theme-settings list of rooms, each
     linking to a Zid collection
     ===================================================================== -->
<section class="section" id="inspire" aria-labelledby="inspTitle" style="padding-top:0">
  <div class="container">
    <div class="sec-head" data-reveal>
      <p class="eyebrow"><span class="idx">10</span><span data-t="inspEyebrow"></span></p>
      <h2 class="h-xl" id="inspTitle" data-t="inspTitle"></h2>
    </div>
    <div class="insp__grid">
      <div data-reveal>
        <p class="insp__body" data-t="inspBody"></p>
        <div class="insp__chips" id="inspChips"></div>
      </div>
      <figure class="insp__art" data-reveal><img id="inspImg" alt="" loading="lazy" decoding="async" width="900" height="517"></figure>
    </div>
  </div>
</section>
</main>""")
rep("""     SECTION 12 · FOOTER   →""", """     SECTION 13 · FOOTER   →""")
rep("""<footer class="footer">
  <div class="container">
""", """<footer class="footer">
  <div class="container">
    <div class="footer__brand"><span class="footer__logo" id="footerLogo"></span><span class="stamp" id="stamp" aria-hidden="true"></span></div>
""")
rep("""<div class="toast" id="toast" role="status" aria-live="polite"></div>""",
"""<div class="toast" id="toast" role="status" aria-live="polite"></div>

<!-- Interactive gazelle (client mascot): appears when the customer lingers on a section -->
<div class="peek" id="peek" aria-hidden="true">
  <button class="peek__fig" id="peekFig" type="button" tabindex="-1"><img id="peekImg" alt=""></button>
  <p class="peek__say" id="peekSay"></p>
</div>""")

# =========================================================== JS: brand assets + logo + gazelle
rep("""/* ---------------- BRAND SVG: logo, silhouettes, gazelle ---------------- */""",
    BRAND_JS + """
/* ---------------- BRAND SVG: logo, silhouettes, gazelle ---------------- */""")

rex(r"const logo = \(w = 72, cls = ''\) => `<svg[^\n]*\n",
"""const KT = BRAND.KET;
// the real ket wordmark (traced from the client's logo sheet) + the smile it folds into
const logo = (w = 64, cls = '') => `<svg class="klogo ${cls}" viewBox="0 0 ${KT.w} ${KT.h}" width="${w}" role="img" aria-label="ket" style="direction:ltr" fill="currentColor"><g class="klogo__word"><path class="kl" d="${KT.k}"/><path class="kl" fill-rule="evenodd" d="${KT.e}"/><path class="kl" d="${KT.t}"/></g><g transform="translate(${KT.smile.x} ${KT.smile.y})"><path class="klogo__smile" d="${KT.smile.d}"/></g></svg>`;
const smileMark = (w = 40) => `<svg viewBox="0 0 ${BRAND.SMILE.w} ${BRAND.SMILE.h}" width="${w}" aria-hidden="true" fill="currentColor"><path d="${BRAND.SMILE.d}"/></svg>`;
const lockup = () => `<svg viewBox="0 0 ${BRAND.LOCKUP.w} ${BRAND.LOCKUP.h}" role="img" aria-label="ket by Tanasoub" style="direction:ltr" fill="currentColor"><path fill-rule="evenodd" d="${BRAND.LOCKUP.d}"/></svg>`;
const shape = n => { const v = BRAND.SHAPES[n]; return `<svg class="shape" viewBox="0 0 ${v.w} ${v.h}" aria-hidden="true"><path fill="${v.c}" fill-rule="evenodd" d="${v.d}"/></svg>`; };
const stamp = () => {
  const sm = BRAND.SMILE, k = 38 / sm.w;
  return `<svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="60" fill="#FFAE15"/><defs><path id="stampArc" d="M60 60m-45 0a45 45 0 1 1 90 0a45 45 0 1 1-90 0"/></defs>
    <g class="stamp__ring"><text font-family="Inter Tight, sans-serif" font-size="10.4" font-weight="600" letter-spacing="1.1" fill="currentColor"><textPath href="#stampArc" textLength="276" lengthAdjust="spacing">FROM OUR HANDS TO YOUR HOME · FROM OUR HANDS ·</textPath></text></g>
    <g transform="translate(${60 - 19} ${60 - sm.h * k / 2}) scale(${k})" fill="currentColor"><path d="${sm.d}"/></g></svg>`;
};
""")

rex(r"// KET's own mascot: the gazelle in its delivery box.*?</svg>`;\n",
"""// KET's mascot: the client's gazelle drawings, grey wash recoloured in brand colours
const gz = (pose, cls = 'gz') => `<img class="${cls}" src="${BRAND.GZ[pose]}" alt="" width="${BRAND.GZSIZE[pose][0]}" height="${BRAND.GZSIZE[pose][1]}" decoding="async">`;
const gazelleBox = () => `<span class="gzbox">${gz('box', '')}<span class="gzbox__logo">${smileMark(64)}</span></span>`;
const gazelle = (pose = 'box') => gz(pose);
""")

# icons: chat bubble for the proof strip
rep("""  check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',""",
"""  check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
  chat: '<path d="M5 5h14a1.5 1.5 0 0 1 1.5 1.5v8.5A1.5 1.5 0 0 1 19 16.5h-8L6.5 20v-3.5H5a1.5 1.5 0 0 1-1.5-1.5V6.5A1.5 1.5 0 0 1 5 5Z"/><path d="M8 9.5h8M8 12.5h5"/>',""")

# build(): guarantees, proof icons, footer, inspiration
rex(r"  \$\('#trust'\)\.innerHTML = \[\['boxcart', 't1', 't1s'\].*?\.join\(''\);\n",
"""  // purchase motivators (client brief): guarantee, free delivery, 24h exchange & return
  $('#trust').innerHTML = [['lav', 'g1', 'g1s'], ['green', 'g2', 'g2s'], ['blue', 'g3', 'g3s']].map(([n, a, b]) => `<li style="--tint:${BRAND.SHAPES[n].c}">${shape(n)}<div><strong data-t="${a}"></strong><span data-t="${b}"></span></div></li>`).join('');
  $('#proofIcBuy').innerHTML = icon('bag', 22); $('#proofIcRev').innerHTML = icon('chat', 22);
""")
rep("""  // footer
  $('#social').innerHTML""", """  // inspiration
  $('#inspImg').src = BRAND.ILLUS;
  $('#inspChips').innerHTML = (STORE.inspiration || []).map((r, i) => `<a class="insp__chip" href="#" data-insp="${i}" style="--chip:${r.color}" data-l="inspiration.${i}.name"></a>`).join('');

  // footer
  $('#footerLogo').innerHTML = lockup();
  $('#stamp').innerHTML = stamp();
  $('#social').innerHTML""")
rep("""  $('#logo').innerHTML = logo(68);""", """  $('#logo').innerHTML = logo(64);""")

# applyLang: numbers
rep("""  $('#soldPill').innerHTML = t('sold', { n: cnum('sold', 1000) });""",
"""  $('#soldPill').innerHTML = t('sold', { n: cnum('sold', P.soldCount || 1000) });
  $('#proofBuy').innerHTML = `${cnum('pBuy', P.soldCount || 0)}+`;
  $('#proofRev').innerHTML = cnum('pRev', P.reviewCount);
  $('#proofRate').innerHTML = `${cnum('pRate', P.rating, 1)}<small>/5</small>`;
  $('#proofStars').innerHTML = stars(P.rating, 17, 'proof');""")

# cart gazelles: empty = asleep on its cloud, added = in its box
rep("""<div class="empty">${gazelle()}""", """<div class="empty">${gazelle('sleep')}""")
rep("""<div class="drawer__success">${gazelle()}""", """<div class="drawer__success">${gazelle('box')}""")

# =========================================================== JS: interactive gazelle
PEEK_JS = r"""
/* =================================================================
   INTERACTIVE GAZELLE — peeks in when the customer lingers on a section.
   Each moment shows once per visit (different pose, entrance and line),
   at most 3 per page view, 20 s apart, never over the cart or lightbox.
   ================================================================= */
// inspiration chips lead to Zid collections in the live store
document.addEventListener('click', e => { if (e.target.closest('[data-insp]')) { e.preventDefault(); toast(t('toastSoon')); } });

const PEEKS = [
  { id: 'buy', zone: '#buy', after: 9, pose: 'stand', mode: 'side', say: 'peekBuy', act: 'wa' },
  { id: 'ship', zone: '#info', after: 3, pose: 'box', mode: 'bottom', say: 'peekShip' },
  { id: 'dims', zone: '#dimensions', after: 3, pose: 'sit', mode: 'bottom', say: 'peekDims' },
  { id: 'rev', zone: '#reviews', after: 3, pose: 'hop', mode: 'side', say: 'peekRev' }
];
const PEEK_IDLE = { id: 'idle', pose: 'sleep', mode: 'bottom', say: 'peekIdle', idle: 25 };
const FACES_LEFT = { stand: 1, hop: 1, sleep: 1 };   // drawings that look to the left
const peekEl = $('#peek'), peekFig = $('#peekFig'), peekImg = $('#peekImg'), peekSay = $('#peekSay');
let peekSeen = new Set();
try { peekSeen = new Set(JSON.parse(sessionStorage.getItem('ket-peek') || '[]')); } catch (e) { /* storage blocked */ }
const peekSave = () => { try { sessionStorage.setItem('ket-peek', JSON.stringify([...peekSeen])); } catch (e) { /* storage blocked */ } };
let peekNow = null, peekCount = 0, peekLast = -1e9, peekHideT = 0, lastScroll = 0, lastInput = Date.now();
const dwell = {};
const peekBusy = () => drawer.classList.contains('is-open') || lb.classList.contains('is-open') || document.hidden;
function showPeek(p) {
  peekNow = p; peekCount++; peekLast = Date.now(); peekSeen.add(p.id); peekSave();
  const side = root.dir === 'rtl' ? 'l' : 'r';   // the inline-end edge, away from the WhatsApp button
  peekEl.className = `peek peek--${p.mode} peek--${side}`;
  peekEl.style.setProperty('--pw', (innerWidth < 640 ? (p.mode === 'side' ? 92 : 84) : (p.mode === 'side' ? 128 : 112)) + 'px');
  peekImg.src = BRAND.GZ[p.pose];
  peekImg.style.setProperty('--flip', side === 'l' && FACES_LEFT[p.pose] ? -1 : 1);
  peekSay.innerHTML = esc(t(p.say, { n: P.reviewCount })) + (p.act === 'wa' && STORE.whatsapp ? `<br><a href="${$('#wa').href}" target="_blank" rel="noopener">${esc(t('peekWa'))}</a>` : '');
  requestAnimationFrame(() => requestAnimationFrame(() => peekEl.classList.add('is-on')));
  clearTimeout(peekHideT); peekHideT = setTimeout(hidePeek, p.act ? 8000 : 6000);
}
function hidePeek() {
  if (!peekNow) return;
  peekEl.classList.remove('is-on'); clearTimeout(peekHideT);
  setTimeout(() => { if (!peekEl.classList.contains('is-on')) peekNow = null; }, 950);
}
peekFig.addEventListener('click', () => {
  // a little hop away when tapped
  peekFig.animate?.([{ transform: getComputedStyle(peekFig).transform }, { transform: getComputedStyle(peekFig).transform + ' translateY(-30px)' }], { duration: 220, easing: 'ease-out', direction: 'alternate', iterations: 2 });
  setTimeout(hidePeek, 300);
});
addEventListener('scroll', () => {
  lastScroll = lastInput = Date.now();
  if (peekNow && peekNow.zone) { const r = $(peekNow.zone).getBoundingClientRect(); if (r.bottom < innerHeight * .2 || r.top > innerHeight * .8) hidePeek(); }
}, { passive: true });
['pointermove', 'pointerdown', 'keydown', 'touchstart'].forEach(ev => addEventListener(ev, () => { lastInput = Date.now(); }, { passive: true }));
setInterval(() => {
  if (peekNow || peekBusy()) return;
  const now = Date.now();
  if (peekCount >= 3 || now - peekLast < 20000) return;
  const still = now - lastScroll > 600, mid = innerHeight * .5;
  for (const p of PEEKS) {
    if (peekSeen.has(p.id)) continue;
    const el = $(p.zone); if (!el) continue;
    const r = el.getBoundingClientRect(), focus = r.top < mid && r.bottom > mid;
    if (!focus) { dwell[p.id] = 0; continue; }
    if (still) dwell[p.id] = (dwell[p.id] || 0) + 250;
    if (dwell[p.id] >= p.after * 1000) { showPeek(p); return; }
  }
  if (!peekSeen.has(PEEK_IDLE.id) && now - lastInput > PEEK_IDLE.idle * 1000) showPeek(PEEK_IDLE);
}, 250);
"""
rep("""/* =================================================================
   MISC UI: header, sticky bar, accordions, sliders, toasts, AR, lang""",
    PEEK_JS + """
/* =================================================================
   MISC UI: header, sticky bar, accordions, sliders, toasts, AR, lang""")

# language switch: peek bubble follows the language; data-toast on inspiration chips is wired at load
# intro: the wordmark rises in (the old smile stroke no longer exists)
rep("""const smile = $('#logo .smile'); const sl = smile.getTotalLength();
intro.fromTo(smile, { strokeDasharray: sl, strokeDashoffset: sl }, { strokeDashoffset: 0, duration: 1.1, ease: 'power3.inOut' }, 0)
  .fromTo('.g-stage',""",
"""intro.fromTo('#logo .klogo__word', { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: 'back.out(1.7)' }, 0)
  .fromTo('.g-stage',""")
rep("""countUp(['rate2', 'reviews2'], '#revScore');""", """countUp(['rate2', 'reviews2'], '#revScore');
countUp(['pBuy', 'pRev', 'pRate'], '#proof');
popStars('[data-stars="proof"]', '#proof');""")

open(path, 'w', encoding='utf-8').write(s)
print('patched', path, len(s))
