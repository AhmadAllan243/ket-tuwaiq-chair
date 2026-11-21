"""
Builds ket-lamps.html (the lighting department, for review) from ket-tables.html (the department design):
the lamps from the store, lavender (most) with lemon and orange as touches, and light everywhere:
  · the loader's ring of lamps switches on as it spins
  · the banner writes its words as the customer scrolls; when the words are done the lamp switches on,
    and it switches off again once the banner is scrolled half away
  · the "pick a type" photo starts off and switches on when it comes into view
  · a gallery of lamps on white: tap one and its white turns into the real room, then the light comes on
  · a light switch over the products turns every lamp on (and a hover lights one card)
  · under each product: an energy bar (efficiency class and a saving counter). PLACEHOLDER figures for review,
    to be replaced by each lamp's real data before it goes live.

usage: python3 make_lamps.py      (run from src)
"""
import re, json

s = open('ket-tables.html').read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, f'expected {n}x, found {c}: {a[:80]}'
    s = s.replace(a, b)

# ---------------------------------------------------------------- data: the lamps from the store
rows = {r[0]: r for r in (l.split('\t') for l in open('media/lamps/lamps.tsv', encoding='utf-8').read().strip().split('\n'))}
TYPE = {'floor': 'lp01 lp12 lp13 lp14 lp16 lp17 lp24', 'ceramic': 'lp05 lp06 lp07 lp08 lp09 lp10 lp11',
        'bedside': 'lp02 lp03 lp04 lp15 lp18 lp19', 'statement': 'lp20 lp21 lp22 lp23'}
COL = {'ceramic': 'lp05 lp06 lp07 lp08 lp09 lp10 lp11', 'metal': 'lp01 lp12 lp13 lp14 lp15 lp16 lp24',
       'gold': 'lp02 lp17 lp20 lp21', 'wood': 'lp03 lp04 lp22', 'glass': 'lp18 lp19 lp23'}
typ = {i: k for k, v in TYPE.items() for i in v.split()}
col = {i: k for k, v in COL.items() for i in v.split()}
ORDER = 'lp06 lp13 lp02 lp23 lp05 lp17 lp18 lp21 lp10 lp01 lp03 lp22 lp07 lp12 lp19 lp20 lp08 lp14 lp15 lp11 lp16 lp04 lp09 lp24'.split()
assert sorted(ORDER) == sorted(rows), 'every lamp once'
prods = []
for k, i in enumerate(ORDER):
    _, ar, en, price, was, _, slug = rows[i]
    eco = 72 + (k * 7) % 21          # PLACEHOLDER energy saving (%), for the review only
    prods.append("    { id: %s, type: %s, col: %s, ar: %s, en: %s, price: %s, was: %s, eco: %d, url: %s }" % (
        json.dumps(i), json.dumps(typ[i]), json.dumps(col[i]), json.dumps(ar, ensure_ascii=False), json.dumps(en),
        f'{float(price):g}', f'{float(was):g}', eco, json.dumps('https://ketfurniture.com/products/' + slug, ensure_ascii=False)))

i = s.index("const M = 'media/tables/';"); j = s.index('  ui: {')
s = s[:i] + """const M = 'media/lamps/';
const STORE = {
  currency: { ar: 'ر.س', en: 'SAR' },
  vat: '310803678600003', cr: '4030396963',
  category: { ar: 'الإضاءات', en: 'Lighting' },

  // shop by type. hero = the tile picture
  types: [
    { id: 'ceramic', ar: 'أبجورات سيراميك', en: 'Ceramic lamps', hero: 'lp06' },
    { id: 'floor', ar: 'أبجورات أرضية', en: 'Floor lamps', hero: 'lp13' },
    { id: 'bedside', ar: 'للكومودينو والمكتب', en: 'Bedside & desk', hero: 'lp02' },
    { id: 'statement', ar: 'قطع لافتة', en: 'Statement pieces', hero: 'lp23' }
  ],

  // every lamp in the department (names, prices and photos from ketfurniture.com, Nov 2026).
  // eco = energy saving % — PLACEHOLDER for the review; the live theme takes each lamp's real figure
  products: [
""" + ',\n'.join(prods) + """
  ],

  // lamp families
  collections: [
    { id: 'ceramic', ar: 'خزف بملمس الحجر', en: 'Stone-textured ceramic', img: 'lp10', note: { ar: 'قواعد يدوية الملمس وأغطية كتان', en: 'Hand-textured bases, linen shades' } },
    { id: 'metal', ar: 'معدن أسود وستيل', en: 'Black metal & steel', img: 'lp14', note: { ar: 'خطوط نحيلة للزوايا', en: 'Slim lines for corners' } },
    { id: 'gold', ar: 'لمسات ذهبية', en: 'Golden touches', img: 'lp17', note: { ar: 'نحاس ورخام', en: 'Brass and marble' } },
    { id: 'wood', ar: 'خشب دافئ', en: 'Warm wood', img: 'lp22', note: { ar: 'خشب طبيعي بألوان هادئة', en: 'Natural wood, calm tones' } },
    { id: 'glass', ar: 'زجاج وكهرمان', en: 'Glass & amber', img: 'lp19', note: { ar: 'ضوء يلمع من خلال الزجاج', en: 'Light that glows through glass' } }
  ],

  // the gallery: tap a lamp and its white turns into its room. x / y = where the lamp sits in the photo
  gallery: [
    // w/h = the photo's size; box = the lamp inside it (% left, top, right, bottom); pos = how the room photo is framed
    { id: 'rib', w: 1121, h: 1403, box: [31, 34.1, 68.8, 72.4], pos: [.5, .48], ar: 'ركن هادئ', en: 'A quiet corner', note: { ar: 'ضوء ناعم يدفّي الزاوية، ويصير المكان أهدأ.', en: 'A soft light that warms the corner and calms the room.' } },
    { id: 'mush', w: 1002, h: 1500, box: [36.6, 36.8, 82.7, 71.1], pos: [.58, .5], ar: 'ضوء القعدة', en: 'Living-room glow', note: { ar: 'قبّة زجاج تنشر ضوءًا ناعمًا على الجدار والرف.', en: 'A glass dome that spreads a soft light over the wall and shelf.' } },
    { id: 'spot', w: 1000, h: 1500, box: [44.5, 11.4, 99.9, 92.9], pos: [.62, .5], ar: 'على مكتبك', en: 'At your desk', note: { ar: 'ضوء مركّز تحرّكه بيدك، للقراءة والشغل.', en: 'A focused light you turn by hand, for reading and work.' } }
  ],

""" + s[j:]

# ---------------------------------------------------------------- wording
AR = dict(
  tables='الإضاءات', ann3='خصومات تصل إلى {n}٪ على الإضاءات', loadLine='نوّر بيتك',
  hShop='تسوّق الإضاءات', hStatL='تصميم إضاءة',
  shapeTx='من ركن القراءة إلى الكومودينو، ابدأ بالنوع الذي يناسب مساحتك.', shapeAll='كل الإضاءات', shapeSale='أعلى خصم', shapeStat='تصميم في {k} أنواع، تبدأ من {p}',
  whyEy='لماذا إضاءات ket', whyA='اكتشف', whyB='ضوء يناسب كل لحظة في البيت.',
  chip1='ركن القراءة', chip2='جلسة المساء', chip3='الكومودينو',
  acc1='ضوء دافئ ومريح', acc1b='أغطية كتان وزجاج تنشر الضوء بنعومة، فيصير المكان أهدأ وأدفأ في المساء.',
  acc2='توصيل مجاني', acc2b='توصيل مجاني لكل مدن المملكة، والأبجورة تصلك مغلّفة بعناية وجاهزة للاستخدام.',
  acc3='تصاميم تكمل بعضها', acc3b='خزف وخشب ومعدن وذهب، اختر قطعتين من نفس العائلة لركنين في نفس الغرفة.',
  cardEy='{n} تصميم', cardTx='إضاءات مختارة بعناية لتكمل بيتك وتعيش معك سنوات.', cardH='ضوء واحد،\nيغيّر المكان.', cardBtn='تسوّق الكل',
  typesEy='تسوّق حسب النوع', typesH='اختر ضوء مكانك.',
  colEy='العائلات', colH='عائلات ضوء تكمل بعضها.',
  gridEy='كل الإضاءات', gridH='الإضاءات',
  tileA='الضوء\nيصنع الجو.', tileAs='كل أبجورة هنا مختارة لتعطي مكانك دفئه.', tileB='من الخزف\nإلى الذهب.', tileBs='خامات هادئة بتفاصيل تلمع لما يشتغل الضوء.',
  helpH='محتار أي أبجورة تناسب مكانك؟', helpTx='أرسل لنا صورة المكان، ونقترح عليك الأبجورة والمقاس المناسبين.',
)
EN = dict(
  tables='Lighting', ann3='Up to {n}% off lighting', loadLine='Light up your home',
  hShop='Shop lighting', hStatL='Lighting designs',
  shapeTx='From the reading corner to the bedside, start with the type that suits your space.', shapeAll='All lighting', shapeSale='Biggest discount', shapeStat='designs in {k} types, from {p}',
  whyEy='Why ket lighting', whyA='Explore', whyB='light for every moment at home.',
  chip1='Reading corner', chip2='Evening sitting', chip3='Bedside',
  acc1='Warm, easy light', acc1b='Linen and glass shades spread the light softly, so the room feels calmer and warmer in the evening.',
  acc2='Free delivery', acc2b='Free delivery across the Kingdom; your lamp arrives carefully packed and ready to use.',
  acc3='Designs that go together', acc3b='Ceramic, wood, metal and gold: pick two from one family for two corners of the same room.',
  cardEy='{n} designs', cardTx='Lighting picked with care to complete your home and live with you for years.', cardH='One light\nchanges the room.', cardBtn='Shop all',
  typesEy='Shop by type', typesH='Pick the light for your space.',
  colEy='Families', colH='Families of light that go together.',
  gridEy='All lighting', gridH='Lighting',
  tileA='Light makes\nthe mood.', tileAs='Every lamp here is chosen to give your space its warmth.', tileB='From ceramic\nto gold.', tileBs='Calm materials with details that glow when the light is on.',
  helpH='Not sure which lamp suits your space?', helpTx='Send us a photo of the space and we will suggest the right lamp and size.',
)
def set_ui(lang_block_start, d):
    global s
    a = s.index(lang_block_start)
    b = s.index('\n    }', a)
    block = s[a:b]
    for k, v in d.items():
        m = re.search(r"\b" + k + r": '((?:[^'\\]|\\.)*)'", block)
        assert m, k
        block = block[:m.start()] + f"{k}: {json.dumps(v, ensure_ascii=False)}" + block[m.end():]
    s = s[:a] + block + s[b:]
set_ui('    ar: {', AR)
set_ui('    en: {', EN)

rep("      skip: 'تخطَّ إلى المنتجات',", """      hEy: 'قسم الإضاءات', hTitle: 'لمسة ضوء واحدة، تغيّر إحساس المكان كله.', hMarkW: 'ضوء', hSub2: 'أبجورات بتصاميم هادئة وضوء دافئ، تحوّل كل زاوية في بيتك إلى ركنك المفضل.',
      hHint: 'مرّر للأسفل… وشغّل الضوء', stOn: 'الضوء شغّال', stOff: 'الضوء مطفأ', tapLight: 'المس لتشغيل الضوء',
      lsw: 'شغّل الإضاءة', lswOn: 'الإضاءة شغّالة',
      galEy: 'المس الضوء', galH: 'المس أي أبجورة، وشوفها في مكانها.', galTx: 'اختر وحدة، وشوفها تدخل مكانها في البيت، ويشتغل ضوءها.', galBtn: 'تسوّق الإضاءات', galClose: 'رجوع', galTap: 'المس',
      eco: 'كفاءة الطاقة', ecoS: 'الطاقة', ecoSave: 'توفير {n}٪',
      skip: 'تخطَّ إلى المنتجات',""")
rep("      skip: 'Skip to products',", """      hEy: 'The lighting section', hTitle: 'One touch of light changes how the whole room feels.', hMarkW: 'light', hSub2: 'Lamps in calm designs with a warm light that turns every corner of your home into your favourite place.',
      hHint: 'Scroll down… and switch the light on', stOn: 'Light on', stOff: 'Light off', tapLight: 'Tap to switch the light',
      lsw: 'Lights on', lswOn: 'Lights are on',
      galEy: 'Touch the light', galH: 'Touch any lamp and see it in its place.', galTx: 'Pick one and watch it move into its place at home, and its light come on.', galBtn: 'Shop lighting', galClose: 'Back', galTap: 'Tap',
      eco: 'Energy efficiency', ecoS: 'Energy', ecoSave: '{n}% saving',
      skip: 'Skip to products',""")

# ---------------------------------------------------------------- colours: lavender (most), lemon and orange (touches)
rep("  --lime:#C6F7A6; --pink:#F4A7FC; --blush:var(--pink); --rose:var(--pink); --lime-l:#E9FCDD; --pink-l:#FCE6FE; --line:rgba(0,0,0,.08);",
    "  --lime:#F8FA75; --pink:#D4C5FF; --blush:var(--pink); --rose:var(--pink); --lime-l:#FDFDE3; --pink-l:#F0EBFF; --line:rgba(0,0,0,.08);\n"
    "  --lav:#D4C5FF; --lav-l:#F0EBFF; --lav-d:#7B61FF; --lemon:#F8FA75; --orange:#FF6417; --night:#17120E; --warm:#FFB867;   /* lighting: lavender most of the way; lemon and orange as touches */")
s = re.sub(r'<title>.*?</title>', '<title>ket · الإضاءات</title>', s, count=1)
rep('<link rel="preload" as="image" href="media/tables/hero-joy.webp">', '<link rel="preload" as="image" href="media/lamps/mush-off.webp">\n<link rel="preload" as="image" href="media/lamps/mush-on.webp">')

# ---------------------------------------------------------------- 1 · the banner: words written by the scroll, then the lamp switches on
i = s.index('<!-- 1 · HERO'); j = s.index('<!-- 2 · PICK THE SHAPE')
s = s[:i] + """<!-- 1 · BANNER: the words alone on top, written by the scroll; then the lamp below switches on (a smooth fade, no flicker) -->
<section class="lhero" id="lhero" aria-labelledby="hTitle">
  <div class="container lhero__in" id="heroCard">
    <h1 class="lhero__h" id="hTitle"></h1>
    <div class="lhero__media">
      <button class="lhero__ph" id="heroPh" type="button" data-t-aria="tapLight">
        <img class="is-off" src="media/lamps/mush-off.webp" alt="" width="1002" height="1500" fetchpriority="high">
        <img class="is-on" src="media/lamps/mush-on.webp" alt="" width="1002" height="1500">
        <span class="lhero__glow" aria-hidden="true"></span>
      </button>
      <span class="hero__stat" id="hStat"></span>
      <span class="lhero__state" id="hState" aria-live="polite"></span>
      <a class="hero__shop" href="#all"><span data-t="hShop"></span><i class="flip" id="hShopIco"></i></a>
    </div>
  </div>
</section>

""" + s[j:]

# ---------------------------------------------------------------- 2 · pick a type: the photo starts off and switches on in view
rep('<img src="media/tables/life2.webp" alt="" loading="lazy" width="1100" height="730">\n      <div><h2 id="shapeTitle" data-t="typesH"></h2>',
    '<img class="sb__off" src="media/lamps/globe-off.webp" alt="" loading="lazy" width="844" height="1500"><img class="sb__on" src="media/lamps/globe-on.webp" alt="" loading="lazy" width="844" height="1500">\n      <div><h2 id="shapeTitle"></h2>')
rep('<span class="sav"><img src="media/tables/t03.webp" alt="" loading="lazy"></span>', '<span class="sav"><img src="media/lamps/lp06.webp" alt="" loading="lazy"></span>')
rep("${tile('coffee', 'st--a', 'white')}", "${tile('ceramic', 'st--a', 'white')}")
rep("${tile('side', 'st--tall', 'white')}", "${tile('floor', 'st--tall', 'white')}")
rep("${tile('sets', 'st--short', 'white')}${col('tm', 'st--short', 'tm-side', 'white')}", "${tile('bedside', 'st--short', 'white')}${col('glass', 'st--short', 'lp18', 'white')}")
rep("${tile('console', 'st--sq', 'white')}", "${tile('statement', 'st--sq', 'white')}")
rep("${col('laxi', 'st--full', 't16', 'white', true)}", "${col('gold', 'st--full', 'lp17', 'white', true)}")
rep("  $('#shapeSeg').innerHTML =", "  $('#shapeTitle').innerHTML = WW(t('typesH'));\n  $('#shapeSeg').innerHTML =")

# ---------------------------------------------------------------- 3 · the gallery (before the products)
rep("<!-- 4 · ALL PRODUCTS   → Vitrin: category.products with Zid's filters / sort -->", """<!-- 3 · THE GALLERY: the lamps alone on a dark stage; tap one and it moves into its place in the real room, then the light comes on -->
<section class="gx" id="glow" aria-labelledby="galTitle">
  <div class="gx__stage" id="gx">
    <div class="gx__scene" id="gxScene"><img class="gx__boff" alt=""><img class="gx__bon" alt=""><img class="gx__off" alt=""><img class="gx__on" alt=""></div>
    <div class="gx__cap" id="gxCap"></div>
    <div class="gx__lamps" id="galRow"></div>
    <div class="container gx__head"><p class="eyebrow" data-t="galEy"></p><h2 id="galTitle" data-t="galH"></h2><p class="gx__tx" data-t="galTx"></p></div>
    <div class="gx__lbl" id="gxLbl" aria-hidden="true"></div>
    <div class="gx__nav" id="gxNav"></div>
  </div>
</section>

<!-- 4 · ALL PRODUCTS   → Vitrin: category.products with Zid's filters / sort -->""")

# the products: the light switch in the bar
rep('    <label class="sortw">', '    <button class="lsw" id="lsw" type="button" role="switch" aria-checked="false"><span class="lsw__k" aria-hidden="true"></span><span class="lsw__t" id="lswT"></span></button>\n    <label class="sortw">')

# the cards: the lamp switched on over it, and the energy bar
rep("""    <div class="card__media${p.photo ? ' is-photo' : ''}" ><img src="${img(p.id)}" alt="${L(p)}" loading="lazy" width="600" height="600">""",
    """    <div class="card__media${p.photo ? ' is-photo' : ''}" style="--i:${i % 8}"><img src="${img(p.id)}" alt="${L(p)}" loading="lazy" width="600" height="600"><img class="card__on" src="${img(p.id + '-on')}" alt="" loading="lazy" width="640" height="640">
      <span class="eco" style="--e:${p.eco}" title="${t('eco')}"><i class="eco__f"></i><span class="eco__z" aria-hidden="true">⚡</span><span class="eco__v">${t('ecoSave', { n: `<b class="eco__n" data-n="${p.eco}">0</b>` })}</span></span>""")
rep("`<div class=\"ttile ttile--photo\"><img src=\"${img('life1')}\" alt=\"\" loading=\"lazy\">", "`<div class=\"ttile ttile--photo\"><img src=\"${img('lady-on')}\" alt=\"\" loading=\"lazy\" style=\"object-position:30% 50%\">")

# intro, help
rep('<span class="ipill ipill--cut"><img src="media/tables/t08.webp" alt="" loading="lazy"></span>', '<span class="ipill ipill--cut"><img src="media/lamps/lp23.webp" alt="" loading="lazy"></span>')
rep('<img src="media/tables/life2.webp" alt="" loading="lazy" width="1100" height="730" data-par>', '<img src="media/lamps/bed-on.webp" alt="" loading="lazy" width="1200" height="1500" data-par>')
rep('<div class="help__img"><img src="media/tables/t11.webp" alt="" loading="lazy"></div>', '<div class="help__img"><img src="media/lamps/help-bed.webp" alt="" loading="lazy" style="object-fit:cover;mix-blend-mode:normal;padding:0;object-position:30% 40%"></div>')
rep("$('#sizeBtn').onclick = () => { setFilter({ type: 'coffee', col: null }); goGrid(); };", "")
rep('<!-- 7 · SIZE GUIDE -->\n<section class="section container" aria-labelledby="sizeTitle">', '<!-- 7 · SIZE GUIDE (not for lamps) -->\n<section class="section container" aria-labelledby="sizeTitle" hidden>')

# ---------------------------------------------------------------- script: the banner, the switch, the gallery, the energy bars
rep("const minPrice = Math.min(...P.map(p => p.price)), maxOff = Math.max(...P.map(off));", """const minPrice = Math.min(...P.map(p => p.price)), maxOff = Math.max(...P.map(off));
ICON.bolt = '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/>';
// words for "written by the scroll": a faint copy of each word, and the ink over it revealed by --wp (0 → 1)
const WW = (str, mark) => str.split(' ').map(w => `<span class="w${mark && w.replace(/[،,.]/g, '') === mark ? ' w--mark' : ''}"><span class="w__g">${w}</span><span class="w__i" aria-hidden="true">${w}</span></span>`).join(' ');""")

i = s.index('function renderBanner() {'); j = s.index('function renderIntro() {')
s = s[:i] + """let heroP = G ? 0 : 1, heroOn = !G, heroPaint = null;
function setHero(on) {
  heroOn = on; $('#heroCard').classList.toggle('is-lit', on);
  $('#hState').innerHTML = `<i></i>${t(on ? 'stOn' : 'stOff')}`; $('#hState').classList.toggle('is-on', on);
}
function renderBanner() {
  $('#hTitle').innerHTML = WW(t('hTitle'), t('hMarkW'));
  $('#hStat').innerHTML = `${icon('spark', 34, 1.5)}<span><b dir="ltr">+${P.length}</b><span>${t('hStatL')}</span></span>`;
  if (heroPaint) heroPaint(heroP); else $$('#hTitle .w').forEach(w => w.style.setProperty('--wp', heroP));
  setHero(heroOn);
}
""" + s[j:]

# the gallery and the light switch render with the language
rep("  renderBanner(); renderShape(); renderIntro(); renderCols(); renderControls(); renderGrid(false); renderSize();",
    "  renderBanner(); renderShape(); renderGal(); renderIntro(); renderCols(); renderControls(); renderGrid(false); renderSize(); renderSwitch();")
rep("function setFilter(s) {", """/* the light switch over the products: every lamp in the grid switches on, one after another */
let lightsOn = false;
function renderSwitch() { $('#lsw').setAttribute('aria-checked', String(lightsOn)); $('#lswT').textContent = t(lightsOn ? 'lswOn' : 'lsw'); $('#pgrid').classList.toggle('is-lit', lightsOn); document.body.classList.toggle('lights-on', lightsOn); }
$('#lsw').addEventListener('click', () => { lightsOn = !lightsOn; renderSwitch(); });

/* the gallery: the lamps alone in a row (the chosen one big in the middle); a tap carries it into its exact place in the room,
   the room fades in around it, then its light comes on. The cut-out has the same frame as the room photo, so it lands exactly. */
const GX = { i: 0, open: false, busy: false };
const gxEl = () => $('#gx');
const gxSize = () => ({ W: gxEl().clientWidth, H: gxEl().clientHeight });
function gxSlot(g, d) {          // d = place in the row: 0 the middle, ±1 the sides, further = out of view
  const { W, H } = gxSize(), ph = W < 768, [x0, y0, x1, y1] = g.box.map(v => v / 100);
  const lampH = H * (d === 0 ? (ph ? .36 : .42) : (ph ? .18 : .24));
  const fs = lampH / ((y1 - y0) * g.h), fw = g.w * fs, fh = g.h * fs;
  const step = W * (ph ? .42 : .34) * (lang === 'ar' ? -1 : 1);
  const cxT = W / 2 + d * step, cyT = H * (d === 0 ? (ph ? .5 : .52) : (ph ? .54 : .56));
  return { left: cxT - (x0 + x1) / 2 * fw, top: cyT - (y0 + y1) / 2 * fh, width: fw, height: fh, opacity: d === 0 ? 1 : Math.abs(d) === 1 ? .38 : 0 };
}
const gxBig = () => gxEl().classList.contains('gx--big');
function gxCover(g) {           // where the whole room photo sits inside the card (it is never cropped), in stage coordinates
  const st = gxEl().getBoundingClientRect(), b = $('#gxScene').getBoundingClientRect();
  const k = Math.min(b.width / g.w, b.height / g.h), dw = g.w * k, dh = g.h * k;
  return { left: b.left - st.left + (b.width - dw) / 2, top: b.top - st.top + (b.height - dh) / 2, width: dw, height: dh };
}
function gxFit(g) { if (!gxBig()) $('#gxScene').style.aspectRatio = `${g.w} / ${g.h}`; }   // the normal card takes the photo's own shape
function gxOff(j) { const n = STORE.gallery.length; let d = (j - GX.i + n) % n; if (d > n / 2) d -= n; if (n === 2 && d === -1) d = 1; return d; }
function gxLayout(anim) {
  $$('#galRow .gx__f').forEach((f, j) => { const t = gxSlot(STORE.gallery[j], gxOff(j)); f.classList.toggle('is-cur', j === GX.i);
    if (anim && G) gsap.to(f, { ...t, duration: 1, ease: 'expo.inOut' }); else gsap.set(f, t); });
  const g = STORE.gallery[GX.i];
  $('#gxLbl').innerHTML = `<b>${L(g)}</b><small><i></i>${t('galTap')}</small>`;
  $$('#gxNav .gx__dots i').forEach((x, k) => x.classList.toggle('is-on', k === GX.i));
}
function renderGal() {
  if (/[?&]big(?:[=&]|$)/.test(location.search)) $('#gx').classList.add('gx--big');   // the review option: the room opens as big as the banner photo
  const G2 = STORE.gallery;
  $('#galRow').innerHTML = G2.map((g, j) => `<button class="gx__f" type="button" data-j="${j}" aria-label="${L(g)}"><img src="${img(g.id + '-cut')}" alt="" loading="lazy" style="--d:${j * 1.3}s"></button>`).join('');
  $('#gxNav').innerHTML = `<button class="gx__arr" type="button" data-gx-go="-1" aria-label="${t('prev')}">${icon('arrow', 20, 2)}</button>
    <span class="gx__dots">${G2.map(() => '<i></i>').join('')}</span>
    <button class="gx__arr" type="button" data-gx-go="1" aria-label="${t('next')}">${icon('arrow', 20, 2)}</button>`;
  // arrows point the way the row moves: "next" toward the reading direction
  $('#gxNav [data-gx-go="1"] svg').style.transform = lang === 'ar' ? 'scaleX(-1)' : '';
  $('#gxNav [data-gx-go="-1"] svg').style.transform = lang === 'ar' ? '' : 'scaleX(-1)';
  gxCap();
  requestAnimationFrame(() => { gxLayout(false); if (GX.open) gsap.set($$('#galRow .gx__f')[GX.i], { ...gxCover(G2[GX.i]), opacity: 0 }); });
}
function gxCap() {
  const g = STORE.gallery[GX.i];
  $('#gxCap').innerHTML = `<b>${L(g)}</b><p>${L(g.note)}</p><div class="gal__btns"><a class="btn btn-primary" href="#all" data-gx-shop><span>${t('galBtn')}</span><span class="arr flip">${icon('arrow', 18, 1.8)}</span></a>
    <button class="gal__x" type="button" data-gx-close>${icon('close', 18, 2)}<span>${t('galClose')}</span></button></div>`;
}
function gxGo(d) { if (GX.open || GX.busy) return; const n = STORE.gallery.length; GX.i = (GX.i + d + n) % n; gxLayout(true); }
function gxOpen() {
  if (GX.open || GX.busy) return; GX.busy = true; GX.open = true;
  const g = STORE.gallery[GX.i], f = $$('#galRow .gx__f')[GX.i], st = gxEl();
  const off = $$('.gx__off, .gx__boff', st), on = $$('.gx__on, .gx__bon', st);
  off.forEach(x => x.src = img(g.id + '-off')); on.forEach(x => x.src = img(g.id + '-on'));
  gxFit(g); gxCap(); st.classList.add('is-open');
  // while it travels, the lamp stays inside the room card's edges
  { const r = st.getBoundingClientRect(), b = $('#gxScene').getBoundingClientRect(), rad = getComputedStyle($('#gxScene')).borderRadius;
    $('#galRow').style.clipPath = `inset(${b.top - r.top}px ${r.right - b.right}px ${r.bottom - b.bottom}px ${b.left - r.left}px round ${rad})`; }
  const others = $$('#galRow .gx__f').filter(x => x !== f);
  if (!G) { gsap.set(f, { opacity: 0 }); gsap.set([...off, ...on], { opacity: 1 }); GX.busy = false; return; }
  gsap.timeline({ onComplete: () => { GX.busy = false; } })
    .to(others, { opacity: 0, duration: .4 }, 0)
    .to(f, { ...gxCover(g), duration: 1.2, ease: 'power3.inOut' }, 0)
    .to(off, { opacity: 1, duration: .8, ease: 'power2.out' }, .55)
    .set(f, { opacity: 0 }, 1.25)
    .to(on, { opacity: 1, duration: 1.4, ease: 'power1.inOut' }, 1.55)
    .fromTo('#gxCap', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .8, ease: 'expo.out' }, 1.4);
}
function gxClose() {
  if (!GX.open || GX.busy) return; GX.busy = true;
  const g = STORE.gallery[GX.i], f = $$('#galRow .gx__f')[GX.i], st = gxEl(), off = $$('.gx__off, .gx__boff', st), on = $$('.gx__on, .gx__bon', st);
  const done = () => { st.classList.remove('is-open'); GX.open = false; GX.busy = false; gxLayout(false); $('#galRow').style.clipPath = ''; };
  if (!G) { gsap.set([...off, ...on], { opacity: 0 }); done(); return; }
  gsap.timeline({ onComplete: done })
    .to('#gxCap', { opacity: 0, duration: .3 }, 0)
    .to(on, { opacity: 0, duration: .6 }, 0)
    .set(f, { opacity: 1 }, .5)
    .to(off, { opacity: 0, duration: .6 }, .55)
    .add(() => { $('#galRow').style.clipPath = ''; }, .75)
    .to(f, { ...gxSlot(g, 0), duration: 1.1, ease: 'power3.inOut' }, .5)
    .add(() => $$('#galRow .gx__f').forEach((x, j) => { if (x !== f) gsap.to(x, { opacity: gxSlot(STORE.gallery[j], gxOff(j)).opacity, duration: .5 }); }), 1.1);
}
$('#gx').addEventListener('click', e => {
  const go = e.target.closest('[data-gx-go]'); if (go) { gxGo(+go.dataset.gxGo); return; }
  if (e.target.closest('[data-gx-close]')) { gxClose(); return; }
  if (e.target.closest('[data-gx-shop]')) { e.preventDefault(); gxClose(); goGrid(); return; }
  if (GX.open) { if (!e.target.closest('.gx__cap') && !GX.busy) { const on = $$('.gx__on, .gx__bon', gxEl()); gsap.to(on, { opacity: +getComputedStyle(on[0]).opacity > .5 ? 0 : 1, duration: .8 }); } return; }   // in the room: a tap switches the light
  const f = e.target.closest('.gx__f'); if (!f) return;
  const j = +f.dataset.j; if (j === GX.i) gxOpen(); else { GX.i = j; gxLayout(true); }
});
// a swipe moves the row
(() => { let x0 = null; const st = $('#gx');
  st.addEventListener('pointerdown', e => { x0 = e.clientX; });
  st.addEventListener('pointerup', e => { if (x0 == null) return; const dx = e.clientX - x0; x0 = null; if (Math.abs(dx) > 50) gxGo((dx < 0 ? 1 : -1) * (lang === 'ar' ? -1 : 1)); }); })();
addEventListener('resize', () => { if (GX.open) gxFit(STORE.gallery[GX.i]); if (GX.open) gsap.set($$('#galRow .gx__f')[GX.i], { ...gxCover(STORE.gallery[GX.i]), opacity: 0 }); gxLayout(false); });

function setFilter(s) {""")

# the banner motion (pinned while the words write), the type photo, the energy bars
i = s.index('/* ---------------- banner entrance (runs as the loader leaves) ---------------- */'); j = s.index('/* ---------------- loader ---------------- */')
s = s[:i] + """/* ---------------- the banner: pinned while the words write; done → the lamp on; scrolled half away → off ---------------- */
function heroMotion() {
  heroPaint = p => {
    heroP = p; const W = $$('#hTitle .w'), n = W.length, q = Math.min(1, p / .7) * n;
    W.forEach((w, k) => w.style.setProperty('--wp', Math.max(0, Math.min(1, q - k)).toFixed(3)));
  };
  $('#heroPh').onclick = () => setHero(!heroOn);   // the customer can switch it too
  if (!G) { heroPaint(1); setHero(true); return; }
  heroPaint(0); setHero(false);
  let auto = false;
  ScrollTrigger.create({
    trigger: '#lhero', start: () => `top ${$('#header').offsetHeight}px`, end: '+=120%', pin: true, anticipatePin: 1,
    onUpdate: st => { heroPaint(st.progress); const a = st.progress >= .78; if (a !== auto) { auto = a; setHero(a); } }
  });
  // once the banner is scrolled half away, the light goes off; coming back up, it comes on again
  ScrollTrigger.create({ trigger: '#heroCard', start: 'center 18%', onEnter: () => setHero(false), onLeaveBack: () => setHero(true) });
}
function bannerIn() {
  heroMotion();
  if (!G) return;
  gsap.timeline()
    .from('.lhero__media', { clipPath: 'inset(12% 8% 0% 8% round 60px)', duration: 1.5, ease: 'power3.out' }, 0)
    .from('#heroPh img', { scale: 1.18, duration: 2.1, ease: 'power3.out' }, 0)
    .from('.lhero .hero__shop, #hState', { y: 24, opacity: 0, duration: .9, stagger: .08, ease: 'expo.out' }, .7)
    .from('#hStat', { y: 30, opacity: 0, scale: .8, duration: .9, ease: 'back.out(1.8)' }, .9)
    .from('#logo .klogo__word', { y: 30, opacity: 0, duration: .9, ease: 'back.out(1.7)' }, .2);
}
function lampMotion() {
  // the type photo: its words write in, then its lamp switches on; scrolled back above, it goes off
  const sb = $('.shape__big');
  const sbOn = () => { if (G) gsap.fromTo('#shapeTitle .w', { '--wp': 0 }, { '--wp': 1, duration: .5, stagger: .14, ease: 'none', onComplete: () => sb.classList.add('is-lit') }); else sb.classList.add('is-lit'); };
  if (G) ScrollTrigger.create({ trigger: sb, start: 'top 62%', onEnter: sbOn, onLeaveBack: () => { sb.classList.remove('is-lit'); gsap.set('#shapeTitle .w', { '--wp': 0 }); } });
  else sbOn();
  if (G) gsap.set('#shapeTitle .w', { '--wp': 0 });
  if (G) gsap.fromTo('#galRow', { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 1.4, ease: 'expo.out', clearProps: 'transform,opacity', scrollTrigger: { trigger: '#gx', start: 'top 70%' } });
}
// the energy bars fill and count up as each card comes into view (and again after a filter)
function ecoGo(card) {
  card.classList.add('is-seen');
  const n = $('.eco__n', card); if (!n) return; const to = +n.dataset.n;
  if (!G) { n.textContent = to; return; }
  const o = { v: 0 }; gsap.to(o, { v: to, duration: 1.4, ease: 'power3.out', delay: .15, onUpdate: () => n.textContent = Math.round(o.v) });
}
function ecoWatch() {
  if (!('IntersectionObserver' in window)) { $$('#pgrid .card').forEach(ecoGo); return; }
  ecoWatch.io = ecoWatch.io || new IntersectionObserver(es => es.forEach(e => { if (!e.isIntersecting) return; ecoWatch.io.unobserve(e.target); ecoGo(e.target); }), { threshold: .4 });
  $$('#pgrid .card').forEach(c => ecoWatch.io.observe(c));
}

""" + s[j:]
rep("  const swap = () => { g.innerHTML = html.join(''); if (G)", "  const swap = () => { g.innerHTML = html.join(''); ecoWatch(); if (G)")
rep("onComplete: swap }); else g.innerHTML = html.join('');", "onComplete: swap }); else { g.innerHTML = html.join(''); ecoWatch(); }")
rep("  scrollMotion(); bannerIn();", "  bannerIn(); scrollMotion(); lampMotion();")

# ---------------------------------------------------------------- loader: the ring of lamps switches on as it spins
rep("try { seen = !!sessionStorage.getItem('ketCatSeen'); sessionStorage.setItem('ketCatSeen', '1'); } catch (e) {}",
    "try { seen = !!sessionStorage.getItem('ketLampsSeen'); sessionStorage.setItem('ketLampsSeen', '1'); } catch (e) {}")
i = s.index("  // ring of 8 tables in mixed shapes on pink and grey"); j = s.index("  let started = false;")
s = s[:i] + """  // just the three dots (lavender, lemon, orange), then the page opens
  let skipped = false;
  const tl = gsap.timeline({ onComplete: finish });
  tl.to({}, { duration: 1.2 })
    .addLabel('out')
    .to('#ldDots', { scale: .5, opacity: 0, duration: .4, ease: 'power2.in' }, 'out')
    .to(ldr, { opacity: 0, duration: .6, ease: 'power2.inOut' }, 'out+=.2')
    .add(() => { if (!skipped) bannerStart(); }, 'out+=.25');
""" + s[j:]
rep("  function finish() { gsap.ticker.remove(place); ldr.remove(); bannerStart(); }", "  function finish() { ldr.remove(); bannerStart(); }")
rep("  addEventListener('resize', () => ({ R, ts } = geo(), ring.style.setProperty('--ts', ts + 'px')));\n", "")
rep("""  // wait until the ring images are decoded (max 1.2s) so the tiles never pop in empty
  tl.pause();
  const ready = Promise.all($$('img', ring).map(i => i.decode().catch(() => {})));
  Promise.race([ready, new Promise(r => setTimeout(r, 1200))]).then(() => tl.play());""", "")

# ---------------------------------------------------------------- styles
rep("/* ===================== ANNOUNCEMENT + HEADER ===================== */", """/* ===================== LIGHTING: loader ===================== */
.loader__dots i{ background:var(--lav); } .loader__dots i:nth-child(2){ background:var(--lemon); } .loader__dots i:nth-child(3){ background:var(--orange); }
.ring__t img.ring__on{ position:absolute; inset:0; padding:0; object-fit:cover; mix-blend-mode:normal; opacity:0; transition:opacity .45s calc(var(--k) * 90ms) ease; }
.ring.is-lit .ring__t img.ring__on{ opacity:1; animation:flick .7s calc(var(--k) * 90ms) both; }
@keyframes flick{ 0%{ opacity:0; } 18%{ opacity:.85; } 26%{ opacity:.25; } 40%{ opacity:1; } 52%{ opacity:.7; } 100%{ opacity:1; } }

/* ===================== LIGHTING: the banner (the words alone on top, then the photo) ===================== */
.lhero{ padding-top:16px; }
.lhero__in{ display:flex; flex-direction:column; gap:clamp(14px, 2.4vh, 28px); height:calc(100svh - var(--header-h) - 32px); min-height:520px; max-height:900px; }
.lhero__h{ flex:none; margin:0 auto; text-align:center; font-size:clamp(30px, min(4.4vw, 7vh), 70px); font-weight:600; line-height:1.12; letter-spacing:-.035em; max-width:22ch; }
html[lang="ar"] .lhero__h{ font-weight:700; line-height:1.4; letter-spacing:0; max-width:20ch; }
/* a word "written by the scroll": the faint copy shows the shape, the ink wipes in over it */
.w{ position:relative; display:inline-block; }
.w__g{ color:rgba(0,0,0,.12); }
.w__i{ position:absolute; inset:0; white-space:nowrap; color:var(--black); clip-path:inset(-20% calc((1 - var(--wp, 1)) * 100%) -20% 0); }
html[dir="rtl"] .w__i{ clip-path:inset(-20% 0 -20% calc((1 - var(--wp, 1)) * 100%)); }
.w--mark{ isolation:isolate; padding-inline:.14em; }
.w--mark::before{ content:""; position:absolute; z-index:-1; inset:.16em 0 .1em; border-radius:.22em; background:var(--lemon); transform-origin:var(--mo, left) center; transform:scaleX(var(--wp, 1)); }
.w--mark .w__i{ inset-inline:.14em; }
html[dir="rtl"] .w--mark::before{ --mo:right; }
.lhero__media{ position:relative; flex:1 1 0; min-height:240px; width:100%; align-self:center; border-radius:clamp(26px, 3.6vw, 52px); box-shadow:0 0 0 rgba(255,184,103,0); transition:box-shadow 1.4s var(--ease); }
.is-lit .lhero__media{ box-shadow:0 30px 90px -30px rgba(255,170,90,.75); }
.lhero__ph{ position:absolute; inset:0; display:block; border-radius:inherit; overflow:hidden; background:#ece8e4; cursor:pointer; }
.lhero__ph > img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:58% 46%; }
.lhero__ph > img.is-on{ opacity:0; transition:opacity 1.4s ease; }
.is-lit .lhero__ph > img.is-on{ opacity:1; }
.lhero__glow{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(30% 46% at 57% 44%, rgba(255,205,140,.45), transparent 70%); mix-blend-mode:screen; opacity:0; transition:opacity 1.4s ease; }
.is-lit .lhero__glow{ opacity:1; }
.lhero .hero__stat{ top:14px; inset-inline-start:14px; padding:8px 18px 8px 10px; gap:10px; }
html[dir="rtl"] .lhero .hero__stat{ padding:8px 10px 8px 18px; }
.lhero .hero__stat svg{ color:var(--orange); }
.lhero__state{ position:absolute; z-index:3; top:14px; inset-inline-end:14px; display:inline-flex; align-items:center; gap:8px; height:40px; padding-inline:12px 16px; border-radius:var(--r-pill); background:rgba(255,255,255,.9); font-size:13px; font-weight:700; pointer-events:none; }
.lhero__state i{ width:9px; height:9px; border-radius:50%; background:#8d8d96; transition:background-color .6s, box-shadow .6s; }
.lhero__state.is-on i{ background:var(--orange); box-shadow:0 0 0 4px rgba(255,100,23,.22); }
.lhero .hero__shop{ background:var(--lemon); }
@media (max-width:767px){
  .lhero__in{ height:calc(100svh - var(--header-h) - 64px); min-height:480px; gap:14px; }
  .lhero__h{ font-size:clamp(28px, 8.2vw, 40px); }
  .lhero .hero__stat{ transform:scale(.82); transform-origin:top left; }
  html[dir="rtl"] .lhero .hero__stat{ transform-origin:top right; }
  .lhero__state{ height:34px; font-size:12px; }
  .lhero .hero__shop{ height:52px; font-size:15px; }
}

/* ===================== LIGHTING: the type photo, off → on ===================== */
.shape__big > img.sb__on{ opacity:0; transition:opacity .8s var(--ease); }
.shape__big.is-lit > img.sb__on{ opacity:1; animation:flick .9s both; }
.shape__big > img{ object-position:50% 32%; }
.shape__big h2 .w__g{ color:rgba(255,255,255,.25); }
.shape__big h2 .w__i{ color:var(--white); }
.shape__big::after{ background:linear-gradient(180deg, rgba(0,0,0,.62), rgba(0,0,0,.25) 46%, rgba(0,0,0,.08) 66%, rgba(0,0,0,.4)); }
.st{ background:var(--white); }

/* ===================== LIGHTING: the gallery (full width, as in the video) ===================== */
.gx{ padding-top:var(--section); }
.gx__stage{ --gh:clamp(600px, 90svh, 860px); position:relative; overflow:hidden; height:var(--gh); background:var(--white); color:var(--black); touch-action:pan-y; }
.gx__scene{ position:absolute; z-index:0; left:50%; top:50%; translate:-50% -50%; height:calc(100% - 150px); aspect-ratio:4 / 5; max-width:calc(100% - 32px); border-radius:clamp(22px, 2.6vw, 34px); overflow:hidden; pointer-events:none; }
.gx__stage.is-open .gx__scene{ pointer-events:auto; }
.gx__scene img{ position:absolute; inset:0; width:100%; height:100%; object-fit:contain; opacity:0; }
.gx__scene .gx__boff, .gx__scene .gx__bon{ display:none; object-fit:cover; filter:blur(30px) saturate(1.1); transform:scale(1.2); }
.gx--big .gx__scene .gx__boff, .gx--big .gx__scene .gx__bon{ display:block; }
.gx__lamps{ position:absolute; inset:0; z-index:1; }
.gx__f{ position:absolute; display:block; padding:0; transition:filter .4s; }
.gx__f img{ display:block; width:100%; height:100%; filter:drop-shadow(0 26px 26px rgba(0,0,0,.16)); animation:gxFloat 6s ease-in-out var(--d) infinite; }
@keyframes gxFloat{ 0%,100%{ transform:translateY(0); } 50%{ transform:translateY(-10px); } }
.gx__f.is-cur{ cursor:pointer; }
.gx__f:not(.is-cur):hover{ filter:brightness(1.25); }
.gx.is-open .gx__f img, .gx__stage.is-open .gx__f img{ animation:none; filter:none; }
.gx__head{ position:absolute; z-index:2; inset-inline:0; top:clamp(24px, 4vw, 56px); display:grid; gap:10px; pointer-events:none; transition:opacity .5s; }
.gx__head .eyebrow{ color:var(--black); }
.gx__head .eyebrow::before{ background:var(--orange); }
.gx__head h2{ font-size:clamp(28px, 3.6vw, 52px); font-weight:600; line-height:1.15; letter-spacing:-.03em; max-width:16ch; }
html[lang="ar"] .gx__head h2{ font-weight:700; line-height:1.45; letter-spacing:0; }
.gx__tx{ color:var(--ink-2); max-width:40ch; }
.gx__lbl{ position:absolute; z-index:2; left:50%; bottom:92px; translate:-50% 0; display:flex; flex-direction:column; align-items:center; gap:8px; text-align:center; pointer-events:none; transition:opacity .5s; }
.gx__lbl b{ font-size:clamp(18px, 1.8vw, 24px); font-weight:700; }
.gx__lbl small{ display:inline-flex; align-items:center; gap:6px; height:30px; padding-inline:10px 12px; border-radius:var(--r-pill); background:var(--lav-l); font-size:12px; font-weight:700; }
.gx__lbl small i{ width:7px; height:7px; border-radius:50%; background:var(--orange); animation:ping2 1.6s var(--ease) infinite; }
@keyframes ping2{ 0%,100%{ box-shadow:0 0 0 0 rgba(255,100,23,.6); } 70%{ box-shadow:0 0 0 8px rgba(255,100,23,0); } }
.gx__nav{ position:absolute; z-index:2; left:50%; bottom:28px; translate:-50% 0; display:flex; align-items:center; gap:16px; transition:opacity .5s; }
.gx__arr{ width:48px; height:48px; border-radius:50%; display:grid; place-items:center; background:var(--lav); color:var(--black); transition:transform .4s var(--ease), background-color .3s; }
.gx__arr:hover{ background:var(--lemon); transform:scale(1.06); }
.gx__dots{ display:flex; gap:6px; }
.gx__dots i{ width:8px; height:8px; border-radius:var(--r-pill); background:var(--g200); transition:width .5s var(--ease), background-color .4s; }
.gx__dots i.is-on{ width:26px; background:var(--orange); }
.gx__cap{ position:absolute; z-index:4; top:50%; translate:0 -50%; inset-inline-start:calc(50% + (var(--gh) - 150px) * .4 + 32px); width:min(340px, calc(50% - (var(--gh) - 150px) * .4 - 56px)); display:grid; gap:8px; justify-items:start; padding:clamp(16px, 2vw, 26px); border-radius:24px; background:rgba(255,255,255,.9); -webkit-backdrop-filter:blur(14px); backdrop-filter:blur(14px); color:var(--black); opacity:0; pointer-events:none; }
.gx__cap > b{ font-size:clamp(20px, 2vw, 28px); font-weight:700; line-height:1.25; }
.gx__cap p{ color:var(--ink-2); font-size:14px; }
.gal__btns{ display:flex; flex-wrap:wrap; align-items:center; gap:8px 14px; margin-top:4px; }
.gal__x{ display:inline-flex; align-items:center; gap:6px; height:44px; padding-inline:12px 16px; border-radius:var(--r-pill); background:var(--lav-l); font-size:14px; font-weight:700; }
.gx__stage.is-open .gx__head, .gx__stage.is-open .gx__lbl, .gx__stage.is-open .gx__nav{ opacity:0; pointer-events:none; }
.gx__stage.is-open .gx__cap{ pointer-events:auto; }
.gx__stage.is-open{ cursor:pointer; }
.gx--big .gx__scene{ left:max(var(--gutter), calc((100% - 1440px) / 2 + var(--gutter))); right:max(var(--gutter), calc((100% - 1440px) / 2 + var(--gutter))); top:64px; bottom:76px; height:auto; width:auto; aspect-ratio:auto; max-width:none; translate:none; border-radius:clamp(28px, 4vw, 60px); }
.gx__stage.gx--big .gx__cap{ top:auto; translate:none; left:auto; inset-inline-start:calc(max(var(--gutter), (100% - 1440px) / 2 + var(--gutter)) + clamp(16px, 2.4vw, 32px)); bottom:calc(76px + clamp(16px, 2.4vw, 32px)); width:min(400px, calc(100% - 2 * var(--gutter) - 32px)); padding:clamp(16px, 2vw, 24px); border-radius:22px; background:rgba(255,255,255,.92); -webkit-backdrop-filter:blur(14px); backdrop-filter:blur(14px); }
@media (max-width:767px){ .gx--big .gx__scene{ left:12px; right:12px; top:56px; bottom:70px; } .gx__stage.gx--big .gx__cap{ inset-inline:24px; bottom:86px; width:auto; padding:14px; } }
@media (min-width:768px) and (max-width:1199px){ .gx__cap{ top:auto; translate:-50% 0; inset-inline-start:auto; left:50%; bottom:28px; width:min(420px, 80%); } }
@media (max-width:767px){
  .gx__stage{ height:min(175vw, 92svh); min-height:600px; }
  .gx__scene{ height:auto; width:calc(100% - 24px); max-height:calc(100% - 130px); }
  .gx__cap{ top:auto; translate:none; bottom:20px; inset-inline:24px; width:auto; padding:14px; }
  .gx__cap p{ display:none; }
  .gx__lbl{ bottom:84px; }
}

/* ===================== LIGHTING: the light switch and the cards ===================== */
.lsw{ flex:none; display:inline-flex; align-items:center; gap:10px; height:40px; padding-inline:6px 14px; border-radius:var(--r-pill); background:var(--white); box-shadow:inset 0 0 0 1px var(--line); font-size:14px; font-weight:700; transition:background-color .5s, color .5s; }
.lsw__k{ position:relative; width:42px; height:26px; border-radius:var(--r-pill); background:var(--g200); transition:background-color .4s; }
.lsw__k::after{ content:""; position:absolute; top:3px; inset-inline-start:3px; width:20px; height:20px; border-radius:50%; background:var(--white); box-shadow:0 2px 6px rgba(0,0,0,.2); transition:inset-inline-start .45s var(--ease), background-color .4s, box-shadow .4s; }
.lsw[aria-checked="true"]{ background:var(--night); color:var(--lemon); box-shadow:none; }
.lsw[aria-checked="true"] .lsw__k{ background:#3a2f25; }
.lsw[aria-checked="true"] .lsw__k::after{ inset-inline-start:19px; background:var(--lemon); box-shadow:0 0 12px 3px rgba(248,250,117,.7); }
body.lights-on .bar{ background:var(--page); }
/* the light-on look: the same white card, the lamp glowing warm (a smooth fade, one after another) */
.card__media img.card__on{ opacity:0; transition:opacity 1s ease calc(var(--i) * 80ms); }
.pgrid.is-lit .card__media img.card__on{ opacity:1; }
@media (hover:hover) and (pointer:fine){ .card:hover .card__media img.card__on{ opacity:1; transition-delay:0s; } }
.card .card__off{ background:var(--orange); color:var(--white); box-shadow:none; }
/* the energy pill inside the photo, shaped like the quantity pill: green, a yellow ⚡, and a lighter green that fills as it counts
   (PLACEHOLDER figures for the review) */
.eco{ position:absolute; z-index:1; bottom:10px; inset-inline-start:10px; display:inline-flex; align-items:center; gap:6px; height:36px; padding-inline:6px 12px; border-radius:var(--r-pill); overflow:hidden; isolation:isolate; background:#066B36; color:var(--white); font-size:12.5px; font-weight:700; box-shadow:0 8px 18px -8px rgba(8,128,64,.6); }
.eco__f{ position:absolute; z-index:-1; inset-block:0; inset-inline-start:0; width:calc(var(--e) * 1%); background:linear-gradient(90deg, #02A27A, #3FCB86 45%, #02A27A 90%); background-size:200% 100%; transform:scaleX(0); transform-origin:var(--to, left) center; transition:transform 1.4s var(--ease); animation:ecoFlow 2s linear infinite; }
html[dir="rtl"] .eco__f{ --to:right; }
@keyframes ecoFlow{ to{ background-position:-200% 0; } }
.card.is-seen .eco__f{ transform:scaleX(1); }
.eco__z{ width:24px; height:24px; border-radius:50%; display:grid; place-items:center; background:rgba(0,0,0,.18); color:var(--lemon); font-size:14px; line-height:1; filter:drop-shadow(0 0 4px rgba(248,250,117,.8)); animation:zap 2.4s ease-in-out infinite; }
@keyframes zap{ 0%,100%{ transform:scale(1); } 50%{ transform:scale(1.15); } }
.eco__v{ white-space:nowrap; text-shadow:0 1px 2px rgba(0,0,0,.15); }
.eco__n{ font-family:var(--f-latin); font-variant-numeric:tabular-nums; }
@media (max-width:480px){ .eco{ height:30px; font-size:11px; gap:4px; padding-inline:4px 9px; bottom:8px; inset-inline-start:8px; } .eco__z{ width:20px; height:20px; font-size:12px; } }

/* the bar: room for the switch on phones */
@media (max-width:767px){ .bar{ flex-wrap:wrap; } .bar .filters{ flex:0 0 100%; order:1; } .bar .lsw{ order:2; } .bar .sortw{ order:3; margin-inline-start:auto; } }

/* the collections hover in lavender */
.crow:hover, .crow.is-on{ background:var(--lav); }
.hero__pill{ background:var(--lav); }

/* ===================== ANNOUNCEMENT + HEADER ===================== */""")

open('ket-lamps.html', 'w').write(s)
print('wrote ket-lamps.html', len(s))
