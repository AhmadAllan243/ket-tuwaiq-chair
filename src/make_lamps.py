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
    { id: 'globe', x: '50%', y: '36%', ar: 'ضوء السهرة', en: 'Evening glow', note: { ar: 'ضوء ناعم يملأ الجلسة دفئًا.', en: 'A soft light that fills the room with warmth.' } },
    { id: 'rib', x: '50%', y: '54%', ar: 'ركن هادئ', en: 'A quiet corner', note: { ar: 'زاوية تصير مكانك المفضل.', en: 'A corner that becomes your favourite place.' } },
    { id: 'spot', x: '62%', y: '50%', ar: 'على مكتبك', en: 'At your desk', note: { ar: 'ضوء مركّز للقراءة والشغل.', en: 'Focused light for reading and work.' } }
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
      galEy: 'المس الضوء', galH: 'المس أي أبجورة، وشوفها في مكانها.', galTx: 'اختر وحدة، وشوف كيف يتحوّل البياض إلى بيت، ويشتغل الضوء.', galBtn: 'تسوّق الإضاءات', galClose: 'رجوع', galTap: 'المس',
      eco: 'كفاءة الطاقة', ecoS: 'الطاقة', ecoSave: 'توفير {n}٪',
      skip: 'تخطَّ إلى المنتجات',""")
rep("      skip: 'Skip to products',", """      hEy: 'The lighting section', hTitle: 'One touch of light changes how the whole room feels.', hMarkW: 'light', hSub2: 'Lamps in calm designs with a warm light that turns every corner of your home into your favourite place.',
      hHint: 'Scroll down… and switch the light on', stOn: 'Light on', stOff: 'Light off', tapLight: 'Tap to switch the light',
      lsw: 'Lights on', lswOn: 'Lights are on',
      galEy: 'Touch the light', galH: 'Touch any lamp and see it in its place.', galTx: 'Pick one and watch the white turn into a home, and the light come on.', galBtn: 'Shop lighting', galClose: 'Back', galTap: 'Tap',
      eco: 'Energy efficiency', ecoS: 'Energy', ecoSave: '{n}% saving',
      skip: 'Skip to products',""")

# ---------------------------------------------------------------- colours: lavender (most), lemon and orange (touches)
rep("  --lime:#C6F7A6; --pink:#F4A7FC; --blush:var(--pink); --rose:var(--pink); --lime-l:#E9FCDD; --pink-l:#FCE6FE; --line:rgba(0,0,0,.08);",
    "  --lime:#F8FA75; --pink:#D4C5FF; --blush:var(--pink); --rose:var(--pink); --lime-l:#FDFDE3; --pink-l:#F0EBFF; --line:rgba(0,0,0,.08);\n"
    "  --lav:#D4C5FF; --lav-l:#F0EBFF; --lav-d:#7B61FF; --lemon:#F8FA75; --orange:#FF6417; --night:#17120E; --warm:#FFB867;   /* lighting: lavender most of the way; lemon and orange as touches */")
s = re.sub(r'<title>.*?</title>', '<title>ket · الإضاءات</title>', s, count=1)
rep('<link rel="preload" as="image" href="media/tables/hero-joy.webp">', '<link rel="preload" as="image" href="media/lamps/globe-off.webp">\n<link rel="preload" as="image" href="media/lamps/globe-on.webp">')

# ---------------------------------------------------------------- 1 · the banner: words written by the scroll, then the lamp switches on
i = s.index('<!-- 1 · HERO'); j = s.index('<!-- 2 · PICK THE SHAPE')
s = s[:i] + """<!-- 1 · BANNER: the words write themselves as the customer scrolls; when they are done the lamp switches on -->
<section class="lhero" id="lhero" aria-labelledby="hTitle">
  <div class="container">
    <div class="lhero__card" id="heroCard">
      <div class="lhero__copy">
        <p class="lhero__ey"><i class="lhero__bulb" aria-hidden="true"></i><span data-t="hEy"></span></p>
        <h1 class="lhero__h" id="hTitle"></h1>
        <p class="lhero__sub" data-t="hSub2"></p>
        <div class="lhero__btns">
          <a class="hero__shop" href="#all"><span data-t="hShop"></span><i class="flip" id="hShopIco"></i></a>
          <span class="lhero__state" id="hState" aria-live="polite"></span>
        </div>
        <p class="lhero__hint" id="hHint"><span data-t="hHint"></span><i aria-hidden="true"></i></p>
      </div>
      <button class="lhero__ph" id="heroPh" type="button" data-t-aria="tapLight">
        <img class="is-off" src="media/lamps/globe-off.webp" alt="" width="941" height="1500" fetchpriority="high">
        <img class="is-on" src="media/lamps/globe-on.webp" alt="" width="941" height="1500">
        <span class="lhero__glow" aria-hidden="true"></span>
        <span class="hero__stat" id="hStat"></span>
      </button>
    </div>
  </div>
</section>

""" + s[j:]

# ---------------------------------------------------------------- 2 · pick a type: the photo starts off and switches on in view
rep('<img src="media/tables/life2.webp" alt="" loading="lazy" width="1100" height="730">\n      <div><h2 id="shapeTitle" data-t="typesH"></h2>',
    '<img class="sb__off" src="media/lamps/rib-off.webp" alt="" loading="lazy" width="1121" height="1403"><img class="sb__on" src="media/lamps/rib-on.webp" alt="" loading="lazy" width="1121" height="1403">\n      <div><h2 id="shapeTitle"></h2>')
rep('<span class="sav"><img src="media/tables/t03.webp" alt="" loading="lazy"></span>', '<span class="sav"><img src="media/lamps/lp06.webp" alt="" loading="lazy"></span>')
rep("${tile('coffee', 'st--a', 'white')}", "${tile('ceramic', 'st--a', 'white')}")
rep("${tile('side', 'st--tall', 'white')}", "${tile('floor', 'st--tall', 'white')}")
rep("${tile('sets', 'st--short', 'white')}${col('tm', 'st--short', 'tm-side', 'white')}", "${tile('bedside', 'st--short', 'white')}${col('glass', 'st--short', 'lp18', 'white')}")
rep("${tile('console', 'st--sq', 'white')}", "${tile('statement', 'st--sq', 'white')}")
rep("${col('laxi', 'st--full', 't16', 'white', true)}", "${col('gold', 'st--full', 'lp17', 'white', true)}")
rep("  $('#shapeSeg').innerHTML =", "  $('#shapeTitle').innerHTML = WW(t('typesH'));\n  $('#shapeSeg').innerHTML =")

# ---------------------------------------------------------------- 3 · the gallery (before the products)
rep("<!-- 4 · ALL PRODUCTS   → Vitrin: category.products with Zid's filters / sort -->", """<!-- 3 · THE GALLERY: lamps on white; tap one and its white becomes the real room, then the light comes on -->
<section class="section container" id="glow" aria-labelledby="galTitle">
  <div class="gal" id="gal">
    <div class="gal__head"><p class="eyebrow" data-t="galEy"></p><h2 id="galTitle" data-t="galH"></h2><p class="gal__tx" data-t="galTx"></p></div>
    <div class="gal__row" id="galRow"></div>
  </div>
</section>

<!-- 4 · ALL PRODUCTS   → Vitrin: category.products with Zid's filters / sort -->""")

# the products: the light switch in the bar
rep('    <label class="sortw">', '    <button class="lsw" id="lsw" type="button" role="switch" aria-checked="false"><span class="lsw__k" aria-hidden="true"></span><span class="lsw__t" id="lswT"></span></button>\n    <label class="sortw">')

# the cards: the lamp switched on over it, and the energy bar
rep("""    <div class="card__media${p.photo ? ' is-photo' : ''}" ><img src="${img(p.id)}" alt="${L(p)}" loading="lazy" width="600" height="600">""",
    """    <div class="card__media${p.photo ? ' is-photo' : ''}" style="--i:${i % 8}"><img src="${img(p.id)}" alt="${L(p)}" loading="lazy" width="600" height="600"><img class="card__on" src="${img(p.id + '-on')}" alt="" loading="lazy" width="640" height="640">""")
rep("""<p class="card__price"><b>${money(p.price)}</b><s>${fmt(p.was)}</s></p></div>""",
    """<p class="card__price"><b>${money(p.price)}</b><s>${fmt(p.was)}</s></p>
      <div class="eco" style="--e:${p.eco}"><span class="eco__ic">${icon('bolt', 12, 2.2)}</span><span class="eco__t"><span class="eco__l">${t('eco')}</span><span class="eco__s">${t('ecoS')}</span></span><b class="eco__r" dir="ltr">${p.eco >= 85 ? 'A++' : 'A+'}</b>
        <span class="eco__m"><i></i></span><span class="eco__v">${t('ecoSave', { n: `<b class="eco__n" data-n="${p.eco}">0</b>` })}</span></div></div>""")
rep("`<div class=\"ttile ttile--photo\"><img src=\"${img('life1')}\" alt=\"\" loading=\"lazy\">", "`<div class=\"ttile ttile--photo\"><img src=\"${img('rib-on')}\" alt=\"\" loading=\"lazy\">")

# intro, help
rep('<span class="ipill ipill--cut"><img src="media/tables/t08.webp" alt="" loading="lazy"></span>', '<span class="ipill ipill--cut"><img src="media/lamps/lp23.webp" alt="" loading="lazy"></span>')
rep('<img src="media/tables/life2.webp" alt="" loading="lazy" width="1100" height="730" data-par>', '<img src="media/lamps/spot-on.webp" alt="" loading="lazy" width="1024" height="1500" data-par>')
rep('<div class="help__img"><img src="media/tables/t11.webp" alt="" loading="lazy"></div>', '<div class="help__img"><img src="media/lamps/lp21.webp" alt="" loading="lazy"></div>')
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

/* the gallery: lamps on white; a tap opens one into its room, then its light comes on */
function renderGal() {
  const open = $('#galRow .gal__it.is-open')?.dataset.i;
  $('#galRow').innerHTML = STORE.gallery.map((g, k) => `<div class="gal__it" data-i="${k}" style="--x:${g.x};--y:${g.y}">
      <button class="gal__hit" type="button" aria-label="${L(g)}"></button>
      <span class="gal__ph" aria-hidden="true"><img src="${img(g.id + '-off')}" alt="" loading="lazy"><img class="gal__on" src="${img(g.id + '-on')}" alt="" loading="lazy"></span>
      <span class="gal__lbl"><b>${L(g)}</b><small><i></i>${t('galTap')}</small></span>
      <div class="gal__cap"><b>${L(g)}</b><p>${L(g.note)}</p>
        <div class="gal__btns"><a class="btn btn-primary" href="#all" data-gal-shop><span>${t('galBtn')}</span><span class="arr flip">${icon('arrow', 18, 1.8)}</span></a>
        <button class="gal__x" type="button" data-gal-close>${icon('close', 18, 2)}<span>${t('galClose')}</span></button></div></div>
    </div>`).join('');
  if (open != null) galOpen($(`#galRow .gal__it[data-i="${open}"]`), true);
}
let galT;
function galOpen(it, now) {
  clearTimeout(galT); $('#gal').classList.add('has-open');
  $$('#galRow .gal__it').forEach(x => x.classList.toggle('is-open', x === it));
  if (now) it.classList.add('is-lit'); else galT = setTimeout(() => it.classList.add('is-lit'), 950);
}
function galClose() { clearTimeout(galT); $('#gal').classList.remove('has-open'); $$('#galRow .gal__it').forEach(x => x.classList.remove('is-open', 'is-lit')); }
$('#galRow').addEventListener('click', e => {
  if (e.target.closest('[data-gal-close]')) { galClose(); return; }
  if (e.target.closest('[data-gal-shop]')) { e.preventDefault(); galClose(); goGrid(); return; }
  const it = e.target.closest('.gal__it'); if (!it) return;
  if (it.classList.contains('is-open')) { it.classList.toggle('is-lit'); return; }   // in the room: a tap switches the light
  galOpen(it);
});

function setFilter(s) {""")

# the banner motion (pinned while the words write), the type photo, the energy bars
i = s.index('/* ---------------- banner entrance (runs as the loader leaves) ---------------- */'); j = s.index('/* ---------------- loader ---------------- */')
s = s[:i] + """/* ---------------- the banner: pinned while the words write; done → the lamp on; scrolled half away → off ---------------- */
function heroMotion() {
  heroPaint = p => {
    heroP = p; const W = $$('#hTitle .w'), n = W.length, q = Math.min(1, p / .7) * n;
    W.forEach((w, k) => w.style.setProperty('--wp', Math.max(0, Math.min(1, q - k)).toFixed(3)));
    $('#hHint').classList.toggle('is-gone', p > .08);
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
    .from('#heroCard', { clipPath: 'inset(10% 8% 0% 8% round 60px)', duration: 1.5, ease: 'power3.out' }, 0)
    .from('#heroPh img', { scale: 1.18, duration: 2.1, ease: 'power3.out' }, 0)
    .from('.lhero__ey, .lhero__sub, .lhero__btns, .lhero__hint', { y: 24, opacity: 0, duration: .9, stagger: .08, ease: 'expo.out' }, .45)
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
  if (G) gsap.fromTo('#galRow .gal__it', { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 1, stagger: .1, ease: 'expo.out', clearProps: 'transform,opacity', scrollTrigger: { trigger: '#galRow', start: 'top 85%' } });
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
rep("  // ring of 8 tables in mixed shapes on pink and grey\n  const pick = [['t03', 'circle', '#C6F7A6'], ['t12', 'arch', '#F4F4F4'], ['life1', 'sq', '#e9e7e4'], ['t01', 'pill', '#F4A7FC'], ['t08', 'circle', '#F4F4F4'], ['t17', 'sq', '#C6F7A6'], ['t15', 'arch', '#F4F4F4'], ['t02', 'circle', '#F4F4F4']];",
    "  // ring of 8 lamps in mixed shapes on lavender, lemon and grey; they switch on as the ring turns\n  const pick = [['lp06', 'circle', '#D4C5FF'], ['lp13', 'arch', '#F4F4F4'], ['lp02', 'sq', '#F8FA75'], ['lp23', 'pill', '#D4C5FF'], ['lp05', 'circle', '#F4F4F4'], ['lp17', 'sq', '#F0EBFF'], ['lp18', 'arch', '#F4F4F4'], ['lp21', 'circle', '#FFE3D3']];")
rep("""  ring.innerHTML = pick.map(([id, sh, bg]) => `<span class="ring__t sh-${sh}${byId[id]?.photo ? ' is-photo' : ''}" style="--bg:${bg}"><img src="${img(id)}" alt=""></span>`).join('');""",
    """  ring.innerHTML = pick.map(([id, sh, bg], k) => `<span class="ring__t sh-${sh}" style="--bg:${bg};--k:${k}"><img src="${img(id)}" alt=""><img class="ring__on" src="${img(id + '-on')}" alt=""></span>`).join('');""")
rep("    .addLabel('out', '-=.55')", "    .add(() => ring.classList.add('is-lit'), 'ring+=1.05')\n    .addLabel('out', '-=.55')")

# ---------------------------------------------------------------- styles
rep("/* ===================== ANNOUNCEMENT + HEADER ===================== */", """/* ===================== LIGHTING: loader ===================== */
.loader__dots i{ background:var(--lav); } .loader__dots i:nth-child(2){ background:var(--lemon); } .loader__dots i:nth-child(3){ background:var(--orange); }
.ring__t img.ring__on{ position:absolute; inset:0; padding:0; object-fit:cover; mix-blend-mode:normal; opacity:0; transition:opacity .45s calc(var(--k) * 90ms) ease; }
.ring.is-lit .ring__t img.ring__on{ opacity:1; animation:flick .7s calc(var(--k) * 90ms) both; }
@keyframes flick{ 0%{ opacity:0; } 18%{ opacity:.85; } 26%{ opacity:.25; } 40%{ opacity:1; } 52%{ opacity:.7; } 100%{ opacity:1; } }

/* ===================== LIGHTING: the banner ===================== */
.lhero{ padding-top:16px; }
.lhero__card{ position:relative; display:grid; overflow:hidden; isolation:isolate; height:calc(100svh - var(--header-h) - 40px); min-height:520px; max-height:860px; border-radius:clamp(28px, 4vw, 56px); background:var(--lav); transition:background-color 1.2s var(--ease); }
.lhero__card::after{ content:""; position:absolute; z-index:0; inset:0; pointer-events:none; background:radial-gradient(60% 70% at var(--gx, 78%) 40%, rgba(255,184,103,.55), transparent 70%); opacity:0; transition:opacity 1.2s var(--ease); }
html[dir="rtl"] .lhero__card::after{ --gx:22%; }
.lhero__card.is-lit{ background:#CDB9FF; }
.lhero__card.is-lit::after{ opacity:1; }
@media (min-width:900px){ .lhero__card{ grid-template-columns:1.05fr .95fr; } }
.lhero__copy{ position:relative; z-index:2; display:flex; flex-direction:column; justify-content:center; align-items:flex-start; gap:clamp(10px, 2vh, 20px); padding:clamp(22px, 4vw, 64px); }
.lhero__ey{ display:inline-flex; align-items:center; gap:8px; height:34px; padding-inline:10px 14px; border-radius:var(--r-pill); background:var(--white); font-size:13px; font-weight:700; }
.lhero__bulb{ width:12px; height:12px; border-radius:50%; background:#cfcfd6; box-shadow:0 0 0 0 rgba(248,250,117,0); transition:background-color .5s, box-shadow .5s; }
.is-lit .lhero__bulb{ background:var(--lemon); box-shadow:0 0 0 5px rgba(248,250,117,.45), 0 0 18px 4px rgba(255,184,103,.8); }
.lhero__h{ margin:0; font-size:clamp(32px, min(4.2vw, 7.4vh), 68px); font-weight:600; line-height:1.12; letter-spacing:-.035em; max-width:15ch; }
html[lang="ar"] .lhero__h{ font-weight:700; line-height:1.4; letter-spacing:0; max-width:15ch; }
/* a word "written by the scroll": the faint copy shows the shape, the ink wipes in over it */
.w{ position:relative; display:inline-block; }
.w__g{ color:rgba(0,0,0,.13); }
.w__i{ position:absolute; inset:0; white-space:nowrap; color:var(--black); clip-path:inset(-20% calc((1 - var(--wp, 1)) * 100%) -20% 0); }
html[dir="rtl"] .w__i{ clip-path:inset(-20% 0 -20% calc((1 - var(--wp, 1)) * 100%)); }
.w--mark{ isolation:isolate; padding-inline:.14em; }
.w--mark::before{ content:""; position:absolute; z-index:-1; inset:.16em 0 .1em; border-radius:.22em; background:var(--lemon); transform-origin:var(--mo, left) center; transform:scaleX(var(--wp, 1)); }
.w--mark .w__i{ inset-inline:.14em; }
html[dir="rtl"] .w--mark::before{ --mo:right; }
.lhero__sub{ font-size:clamp(15px, 1.4vw, 19px); font-weight:500; line-height:1.75; max-width:36ch; color:rgba(0,0,0,.72); }
.lhero__btns{ display:flex; flex-wrap:wrap; align-items:center; gap:12px; }
.lhero .hero__shop{ position:relative; inset:auto; height:58px; font-size:17px; background:var(--black); color:var(--white); box-shadow:none; }
.lhero .hero__shop i{ background:var(--lemon); color:var(--black); width:44px; height:44px; }
.lhero__state{ display:inline-flex; align-items:center; gap:8px; height:40px; padding-inline:12px 16px; border-radius:var(--r-pill); background:rgba(255,255,255,.6); font-size:13px; font-weight:700; }
.lhero__state i{ width:9px; height:9px; border-radius:50%; background:#8d8d96; transition:background-color .4s, box-shadow .4s; }
.lhero__state.is-on i{ background:var(--orange); box-shadow:0 0 0 4px rgba(255,100,23,.22); }
.lhero__hint{ display:inline-flex; align-items:center; gap:10px; font-size:13px; font-weight:600; color:rgba(0,0,0,.6); transition:opacity .4s, transform .4s var(--ease); }
.lhero__hint i{ position:relative; width:22px; height:34px; border-radius:12px; border:2px solid currentColor; }
.lhero__hint i::after{ content:""; position:absolute; left:50%; top:6px; width:4px; height:7px; margin-left:-2px; border-radius:2px; background:currentColor; animation:wheel 1.6s var(--ease) infinite; }
@keyframes wheel{ 0%{ transform:translateY(0); opacity:1; } 70%{ transform:translateY(10px); opacity:0; } 100%{ opacity:0; } }
.lhero__hint.is-gone{ opacity:0; transform:translateY(8px); }
.lhero__ph{ position:relative; z-index:1; display:block; margin:10px; border-radius:clamp(22px, 3.2vw, 46px); overflow:hidden; background:#e9e4f4; cursor:pointer; }
.lhero__ph > img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:50% 30%; }
.lhero__ph > img.is-on{ opacity:0; transition:opacity .8s var(--ease); }
.is-lit .lhero__ph > img.is-on{ opacity:1; animation:flick .9s both; }
.lhero__glow{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(38% 30% at 50% 30%, rgba(255,200,130,.7), transparent 70%); mix-blend-mode:screen; opacity:0; transition:opacity 1s var(--ease); }
.is-lit .lhero__glow{ opacity:1; animation:breath 3.2s ease-in-out 1s infinite; }
@keyframes breath{ 0%,100%{ opacity:.75; } 50%{ opacity:1; } }
.lhero .hero__stat{ top:14px; inset-inline-start:14px; padding:8px 18px 8px 10px; gap:10px; }
html[dir="rtl"] .lhero .hero__stat{ padding:8px 10px 8px 18px; }
.lhero .hero__stat svg{ color:var(--orange); }
@media (max-width:899px){
  .lhero__card{ display:flex; flex-direction:column; min-height:0; }
  .lhero__copy{ padding:22px 20px 8px; gap:12px; flex:none; }
  .lhero__h{ font-size:clamp(30px, 8.6vw, 44px); }
  .lhero__sub{ font-size:14.5px; line-height:1.65; }
  .lhero .hero__shop{ height:50px; font-size:15px; }
  .lhero .hero__shop i{ width:38px; height:38px; }
  .lhero__hint{ display:none; }
  .lhero__ph{ flex:1; min-height:200px; margin:6px 8px 8px; }
  .lhero .hero__stat{ transform:scale(.85); transform-origin:top left; }
  html[dir="rtl"] .lhero .hero__stat{ transform-origin:top right; }
}

/* ===================== LIGHTING: the type photo, off → on ===================== */
.shape__big > img.sb__on{ opacity:0; transition:opacity .8s var(--ease); }
.shape__big.is-lit > img.sb__on{ opacity:1; animation:flick .9s both; }
.shape__big > img{ object-position:50% 55%; }
.shape__big h2 .w__g{ color:rgba(255,255,255,.25); }
.shape__big h2 .w__i{ color:var(--white); }
.shape__big::after{ background:linear-gradient(180deg, rgba(0,0,0,.62), rgba(0,0,0,.25) 46%, rgba(0,0,0,.08) 66%, rgba(0,0,0,.4)); }
.st{ background:var(--white); }

/* ===================== LIGHTING: the gallery ===================== */
.gal{ background:var(--white); border-radius:var(--r-card); padding:clamp(18px, 3vw, 40px); box-shadow:inset 0 0 0 1px var(--line); }
.gal__head{ display:grid; gap:10px; margin-bottom:clamp(18px, 2.6vw, 32px); }
.gal__head .eyebrow::before{ background:var(--orange); }
.gal__head h2{ font-size:clamp(26px, 3.2vw, 44px); font-weight:600; line-height:1.2; letter-spacing:-.03em; max-width:22ch; }
html[lang="ar"] .gal__head h2{ font-weight:700; line-height:1.45; letter-spacing:0; }
.gal__tx{ color:var(--ink-2); max-width:46ch; }
@property --r{ syntax:'<length>'; inherits:true; initial-value:0px; }
.gal__row{ display:flex; height:clamp(440px, 52vw, 680px); }
.gal__it{ --r:clamp(110px, 17vw, 250px); --z:.6; position:relative; flex:1 1 0; min-width:0; margin-inline:6px; border-radius:clamp(20px, 2.6vw, 34px); overflow:hidden; background:var(--white); transition:flex-grow 1s var(--ease), margin .8s var(--ease), opacity .5s, --r 1.2s var(--ease); }
.gal__it:first-child{ margin-inline-start:0; } .gal__it:last-child{ margin-inline-end:0; }
.gal__hit{ position:absolute; inset:0; z-index:3; border-radius:inherit; }
.gal__ph{ position:absolute; inset:0; -webkit-mask-image:radial-gradient(circle at var(--x) var(--y), #000 var(--r), transparent calc(var(--r) * 1.3)); mask-image:radial-gradient(circle at var(--x) var(--y), #000 var(--r), transparent calc(var(--r) * 1.3)); transform:scale(var(--z)); transform-origin:var(--x) var(--y); transition:transform 1.2s var(--ease); }
.gal__ph img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:var(--x) var(--y); }
.gal__ph .gal__on{ opacity:0; transition:opacity .8s var(--ease); }
.gal__it:not(.is-open):hover{ --z:.66; }
.gal__lbl{ position:absolute; z-index:2; inset-inline:12px; bottom:12px; display:flex; flex-direction:column; align-items:center; gap:6px; text-align:center; pointer-events:none; transition:opacity .4s, transform .5s var(--ease); }
.gal__lbl b{ font-size:clamp(14px, 1.4vw, 18px); font-weight:700; }
.gal__lbl small{ display:inline-flex; align-items:center; gap:6px; height:28px; padding-inline:10px 12px; border-radius:var(--r-pill); background:var(--lav-l); font-size:12px; font-weight:700; }
.gal__lbl small i{ width:7px; height:7px; border-radius:50%; background:var(--orange); animation:ping2 1.6s var(--ease) infinite; }
@keyframes ping2{ 0%,100%{ box-shadow:0 0 0 0 rgba(255,100,23,.5); } 70%{ box-shadow:0 0 0 7px rgba(255,100,23,0); } }
.gal__cap{ position:absolute; z-index:4; inset-inline:clamp(14px, 2.4vw, 32px); bottom:clamp(14px, 2.4vw, 32px); display:grid; gap:8px; justify-items:start; max-width:430px; padding:clamp(16px, 2vw, 24px); border-radius:22px; background:rgba(255,255,255,.9); -webkit-backdrop-filter:blur(14px); backdrop-filter:blur(14px); opacity:0; transform:translateY(20px); pointer-events:none; transition:opacity .5s .25s, transform .7s .25s var(--ease); }
.gal__cap > b{ font-size:clamp(22px, 2.4vw, 32px); font-weight:700; line-height:1.3; }
.gal__cap p{ color:var(--ink-2); font-size:15px; }
.gal__btns{ display:flex; flex-wrap:wrap; align-items:center; gap:8px 14px; margin-top:4px; }
.gal__x{ display:inline-flex; align-items:center; gap:6px; height:44px; padding-inline:12px 16px; border-radius:var(--r-pill); background:var(--lav-l); font-size:14px; font-weight:700; }
.gal.has-open .gal__it{ flex-grow:.0001; margin-inline:0; opacity:0; pointer-events:none; }
.gal.has-open .gal__it.is-open{ --r:170vmax; --z:1; flex-grow:1; opacity:1; pointer-events:auto; }
.gal__it.is-open .gal__lbl{ opacity:0; transform:translateY(10px); }
.gal__it.is-open .gal__hit{ z-index:1; }
.gal__it.is-open .gal__cap{ opacity:1; transform:none; pointer-events:auto; }
.gal__it.is-lit .gal__on{ opacity:1; animation:flick .9s both; }
@media (max-width:767px){
  /* phones: the lamps stacked; the one tapped grows into its room and the others fold away */
  .gal__row{ flex-direction:column; height:auto; }
  .gal__it{ --r:clamp(110px, 34vw, 170px); --z:.56; flex:none; height:min(68vw, 330px); margin:0 0 10px; transition:height 1s var(--ease), margin .8s var(--ease), opacity .5s, --r 1.2s var(--ease); }
  .gal__it:last-child{ margin-bottom:0; }
  .gal.has-open .gal__it{ height:0; margin:0; }
  .gal.has-open .gal__it.is-open{ height:min(132vw, 620px); }
  .gal__lbl small{ height:24px; font-size:11px; }
  .gal__cap{ inset-inline:10px; bottom:10px; }
}

/* ===================== LIGHTING: the light switch and the cards ===================== */
.lsw{ flex:none; display:inline-flex; align-items:center; gap:10px; height:40px; padding-inline:6px 14px; border-radius:var(--r-pill); background:var(--white); box-shadow:inset 0 0 0 1px var(--line); font-size:14px; font-weight:700; transition:background-color .5s, color .5s; }
.lsw__k{ position:relative; width:42px; height:26px; border-radius:var(--r-pill); background:var(--g200); transition:background-color .4s; }
.lsw__k::after{ content:""; position:absolute; top:3px; inset-inline-start:3px; width:20px; height:20px; border-radius:50%; background:var(--white); box-shadow:0 2px 6px rgba(0,0,0,.2); transition:inset-inline-start .45s var(--ease), background-color .4s, box-shadow .4s; }
.lsw[aria-checked="true"]{ background:var(--night); color:var(--lemon); box-shadow:none; }
.lsw[aria-checked="true"] .lsw__k{ background:#3a2f25; }
.lsw[aria-checked="true"] .lsw__k::after{ inset-inline-start:19px; background:var(--lemon); box-shadow:0 0 12px 3px rgba(248,250,117,.7); }
body.lights-on .bar{ background:var(--page); }
.card__media img.card__on{ padding:0; object-fit:cover; mix-blend-mode:normal; opacity:0; transition:opacity .6s var(--ease), transform .9s var(--ease); }
.pgrid.is-lit .card__media img.card__on{ opacity:1; animation:flick .8s calc(var(--i) * 70ms) both; }
@media (hover:hover) and (pointer:fine){ .card:hover .card__media img.card__on{ opacity:1; } }
.card{ transition:background-color .6s var(--ease), color .6s; }
.pgrid.is-lit .card{ background:var(--night); color:var(--white); }
.pgrid.is-lit .card__price s{ color:#8f857b; }
.pgrid.is-lit .ttile--dark{ background:var(--lav); }
.card .card__off{ background:var(--orange); color:var(--white); box-shadow:none; }
/* the energy bar under every product (PLACEHOLDER figures for the review) */
.eco{ display:grid; grid-template-columns:auto 1fr auto; align-items:center; gap:6px 8px; margin-top:6px; padding:8px 10px; border-radius:14px; background:#E6F6EE; color:#0B5E30; font-size:12px; font-weight:700; }
.eco__ic{ width:22px; height:22px; border-radius:50%; display:grid; place-items:center; background:#02A27A; color:var(--white); animation:ecoP 2.4s ease-in-out infinite; }
@keyframes ecoP{ 0%,100%{ box-shadow:0 0 0 0 rgba(2,162,122,.45); } 60%{ box-shadow:0 0 0 7px rgba(2,162,122,0); } }
.eco__t{ white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.eco__r{ justify-self:end; padding:3px 7px; border-radius:7px; background:#088040; color:var(--white); font:800 11px/1.1 var(--f-latin); }
.eco__m{ grid-column:1 / 3; position:relative; height:7px; border-radius:7px; background:rgba(8,128,64,.15); overflow:hidden; }
.eco__m i{ position:absolute; inset-block:0; inset-inline-start:0; width:calc(var(--e) * 1%); border-radius:inherit; background:linear-gradient(90deg, #02A27A, #5FDB9A 40%, #02A27A 80%); background-size:200% 100%; transform:scaleX(0); transform-origin:var(--to, left) center; transition:transform 1.4s var(--ease); animation:ecoFlow 1.8s linear infinite; }
html[dir="rtl"] .eco__m i{ --to:right; }
@keyframes ecoFlow{ to{ background-position:-200% 0; } }
.card.is-seen .eco__m i{ transform:scaleX(1); }
.eco__v{ white-space:nowrap; font-size:11.5px; }
.eco__n{ font-family:var(--f-latin); font-variant-numeric:tabular-nums; }
.pgrid.is-lit .eco{ background:#14261C; color:#9EF0C0; }
.pgrid.is-lit .eco__m{ background:rgba(158,240,192,.15); }
.eco__s{ display:none; }
@media (max-width:480px){ .eco{ padding:7px 8px; font-size:11px; gap:5px 6px; } .eco__l{ display:none; } .eco__s{ display:inline; } }

/* the bar: room for the switch on phones */
@media (max-width:767px){ .bar{ flex-wrap:wrap; } .bar .filters{ flex:0 0 100%; order:1; } .bar .lsw{ order:2; } .bar .sortw{ order:3; margin-inline-start:auto; } }

/* the collections hover in lavender */
.crow:hover, .crow.is-on{ background:var(--lav); }
.hero__pill{ background:var(--lav); }

/* ===================== ANNOUNCEMENT + HEADER ===================== */""")

open('ket-lamps.html', 'w').write(s)
print('wrote ket-lamps.html', len(s))
