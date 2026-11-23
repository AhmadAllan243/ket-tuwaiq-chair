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
    // w/h = the photo's size; box = the lamp inside it (% left, top, right, bottom). price / was: PLACEHOLDER until these lamps are in the store
    { id: 'rib', w: 1121, h: 1403, box: [31, 34.1, 68.8, 72.4], price: 249, was: 499, ar: 'ركن هادئ', en: 'A quiet corner', note: { ar: 'ضوء ناعم يدفّي الزاوية، ويصير المكان أهدأ.', en: 'A soft light that warms the corner and calms the room.' } },
    { id: 'mush', w: 1002, h: 1500, box: [36.6, 36.8, 82.7, 71.1], price: 329, was: 650, ar: 'ضوء القعدة', en: 'Living-room glow', note: { ar: 'قبّة زجاج تنشر ضوءًا ناعمًا على الجدار والرف.', en: 'A glass dome that spreads a soft light over the wall and shelf.' } },
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
      band: ['ضوء دافئ', 'تصاميم هادئة', 'توصيل مجاني', 'خصم يصل إلى {n}٪', 'لكل زاوية في البيت'], gxHint: 'المس الصورة وشغّل الضوء',
      eco: 'كفاءة الطاقة', ecoS: 'الطاقة', ecoSave: 'توفير {n}٪', pdEco: 'موفّرة للطاقة', pdSave: 'توفير {n}٪ من الكهرباء', pdLight: 'شغّل الضوء', pdLightOn: 'الضوء شغّال', pdClose: 'إغلاق', pdPage: 'صفحة المنتج في المتجر', pdQty: 'الكمية', gxRoomOn: 'شغّل الضوء', gxRoomOff: 'طفّ الضوء', gxBack: 'كل الأبجورات',
      skip: 'تخطَّ إلى المنتجات',""")
rep("      skip: 'Skip to products',", """      hEy: 'The lighting section', hTitle: 'One touch of light changes how the whole room feels.', hMarkW: 'light', hSub2: 'Lamps in calm designs with a warm light that turns every corner of your home into your favourite place.',
      hHint: 'Scroll down… and switch the light on', stOn: 'Light on', stOff: 'Light off', tapLight: 'Tap to switch the light',
      lsw: 'Lights on', lswOn: 'Lights are on',
      galEy: 'Touch the light', galH: 'Touch any lamp and see it in its place.', galTx: 'Pick one and watch it move into its place at home, and its light come on.', galBtn: 'Shop lighting', galClose: 'Back', galTap: 'Tap',
      band: ['Warm light', 'Calm designs', 'Free delivery', 'Up to {n}% off', 'For every corner of home'], gxHint: 'Tap the photo to switch the light on',
      eco: 'Energy efficiency', ecoS: 'Energy', ecoSave: '{n}% saving', pdEco: 'Energy saving', pdSave: '{n}% less electricity', pdLight: 'Switch the light on', pdLightOn: 'Light on', pdClose: 'Close', pdPage: 'Product page on the store', pdQty: 'Quantity', gxRoomOn: 'Switch it on', gxRoomOff: 'Switch it off', gxBack: 'All lamps',
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

# shop by type: the tiles show the lamps switched on
rep("<img src=\"${img(ty(id).hero)}\" alt=\"\" loading=\"lazy\">${lbl(", "<img src=\"${img(ty(id).hero + '-on')}\" alt=\"\" loading=\"lazy\">${lbl(")
rep("data-col=\"${id}\" aria-label=\"${L(c)}\" style=\"--tint:var(--${tint})\"><img src=\"${img(im)}\" alt=\"\" loading=\"lazy\">", "data-col=\"${id}\" aria-label=\"${L(c)}\" style=\"--tint:var(--${tint})\"><img src=\"${img(im + '-on')}\" alt=\"\" loading=\"lazy\">")

# ---------------------------------------------------------------- 3 · the gallery (before the products)
rep("<!-- 4 · ALL PRODUCTS   → Vitrin: category.products with Zid's filters / sort -->", """<!-- 3 · THE GALLERY: the lamps in a row; a tap carries the lamp into its exact spot in its room, the room fades in around it,
     then the room dims and the lamp glows. Arrows move straight to the next room; price and add to cart sit beside it -->
<section class="gx" id="glow" aria-labelledby="galTitle">
  <div class="gx__stage" id="gx">
    <div class="gx__scene" id="gxScene"><img class="gx__boff" alt=""><img class="gx__bon" alt=""><img class="gx__off" alt=""><img class="gx__on" alt="">
      <button class="gx__x" type="button" data-gx-close></button></div>
    <div class="gx__lamps" id="galRow"></div>
    <div class="gx__names" id="gxNames" aria-hidden="true"></div>
    <div class="container gx__head"><p class="eyebrow" data-t="galEy"></p><h2 id="galTitle" data-t="galH"></h2><p class="gx__tx" data-t="galTx"></p></div>
    <div class="gx__cap" id="gxCap"></div>
    <div class="gx__nav" id="gxNav"></div>
  </div>
</section>

<!-- 4 · ALL PRODUCTS   → Vitrin: category.products with Zid's filters / sort -->""")

# the products: the light switch in the bar
rep('    <label class="sortw">', '    <button class="lsw" id="lsw" type="button" role="switch" aria-checked="false"><span class="lsw__k" aria-hidden="true"></span><span class="lsw__t" id="lswT"></span></button>\n    <label class="sortw">')

# the cards: the lamp switched on over it, and the energy bar
rep("""    <div class="card__media${p.photo ? ' is-photo' : ''}" ><img src="${img(p.id)}" alt="${L(p)}" loading="lazy" width="600" height="600">""",
    """    <div class="card__media${p.photo ? ' is-photo' : ''}" style="--i:${i % 8}"><img src="${img(p.id)}" alt="${L(p)}" loading="lazy" width="600" height="600"><img class="card__on" src="${img(p.id + '-on')}" alt="" loading="lazy" width="640" height="640">""")
rep("`<div class=\"ttile ttile--photo\"><img src=\"${img('life1')}\" alt=\"\" loading=\"lazy\">", "`<div class=\"ttile ttile--photo\"><img src=\"${img('lady-on')}\" alt=\"\" loading=\"lazy\" style=\"object-position:30% 50%\">")

rep('<div class="card__body"><h3 class="card__name"><a href="#" data-toast="soon">${L(p)}</a></h3>', '<div class="card__body"><h3 class="card__name"><a href="${p.url}">${L(p)}</a></h3>')

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
    "  renderBanner(); renderShape(); renderGal(); renderBand(); renderIntro(); renderCols(); renderControls(); renderGrid(false); renderSize(); renderSwitch();")
rep("function setFilter(s) {", """/* the light switch over the products: every lamp in the grid switches on, one after another */
let lightsOn = false;
function renderSwitch() { $('#lsw').setAttribute('aria-checked', String(lightsOn)); $('#lswT').textContent = t(lightsOn ? 'lswOn' : 'lsw'); $('#pgrid').classList.toggle('is-lit', lightsOn); document.body.classList.toggle('lights-on', lightsOn); }
$('#lsw').addEventListener('click', () => { lightsOn = !lightsOn; renderSwitch(); });

/* the gallery: the lamps in a row (all at full strength, the chosen one big); a tap carries it into its exact spot in its room
   (the cut-out has the same frame as the room photo), the room fades in around it, then the room dims and the lamp glows.
   Arrows and swipes move straight to the next room; the price and add to cart sit beside the room. */
const GX = { i: 0, open: true, busy: false, lit: false };   // it opens straight on the first room
const gxEl = () => $('#gx');
const gxSize = () => ({ W: gxEl().clientWidth, H: gxEl().clientHeight });
const gxBox = g => g.box.map(v => v / 100);
function gxSlot(g, d) {          // d = place in the row: 0 the middle, ±1 the sides, further = out of view
  const { W, H } = gxSize(), ph = W < 768, [x0, y0, x1, y1] = gxBox(g);
  const lampH = H * (d === 0 ? (ph ? .34 : .4) : (ph ? .17 : .22));
  const fs = lampH / ((y1 - y0) * g.h), fw = g.w * fs, fh = g.h * fs;
  const step = W * (ph ? .36 : .3) * (lang === 'ar' ? -1 : 1);
  const cxT = W / 2 + d * step, cyT = H * (d === 0 ? (ph ? .5 : .5) : (ph ? .55 : .56));
  return { left: cxT - (x0 + x1) / 2 * fw, top: cyT - (y0 + y1) / 2 * fh, width: fw, height: fh, opacity: Math.abs(d) <= 1 ? 1 : 0 };
}
function gxRoom(g) {             // the room photo inside the room box: framed around the lamp, never cropping it
  const b = $('#gxScene').getBoundingClientRect(), st = gxEl().getBoundingClientRect(), bw = b.width, bh = b.height, [x0, y0, x1, y1] = gxBox(g);
  const cover = Math.max(bw / g.w, bh / g.h), contain = Math.min(bw / g.w, bh / g.h);
  const fit = Math.min(bh / ((y1 - y0) * g.h * 1.5), bw / ((x1 - x0) * g.w * 1.6));
  const k = Math.max(contain, Math.min(cover, fit)), dw = g.w * k, dh = g.h * k;
  let l = bw / 2 - (x0 + x1) / 2 * dw, tp = bh * .52 - (y0 + y1) / 2 * dh;
  l = dw >= bw ? Math.min(0, Math.max(bw - dw, l)) : (bw - dw) / 2;
  tp = dh >= bh ? Math.min(0, Math.max(bh - dh, tp)) : (bh - dh) / 2;
  return { box: { left: l, top: tp, width: dw, height: dh }, stage: { left: b.left - st.left + l, top: b.top - st.top + tp, width: dw, height: dh } };
}
function gxOff(j) { const n = STORE.gallery.length; let d = (j - GX.i + n) % n; if (d > n / 2) d -= n; if (n === 2 && d === -1) d = 1; return d; }
function gxLayout(anim) {
  $$('#galRow .gx__f').forEach((f, j) => {
    const g = STORE.gallery[j], d = gxOff(j), r = gxSlot(g, d), [x0, , x1, y1] = gxBox(g), nm = $$('#gxNames span')[j];
    if (GX.open) r.opacity = 0;   // a room is open: the row stays hidden (phones fire a resize as the address bar moves)
    f.classList.toggle('is-cur', j === GX.i); nm.classList.toggle('is-cur', j === GX.i);
    const n = { left: r.left + (x0 + x1) / 2 * r.width, top: r.top + y1 * r.height + 14, opacity: r.opacity };
    if (anim && G) { gsap.to(f, { ...r, duration: 1, ease: 'expo.inOut' }); gsap.to(nm, { ...n, duration: 1, ease: 'expo.inOut' }); }
    else { gsap.set(f, r); gsap.set(nm, n); }
  });
  $$('#gxNav .gx__dots i').forEach((x, k) => x.classList.toggle('is-on', k === GX.i));
}
function gxRoomImgs(g) {          // the room photo, its lit twin and their blurred fill
  const st = gxEl(), r = gxRoom(g);
  $$('.gx__off, .gx__boff', st).forEach(x => x.src = img(g.id + '-off'));
  $$('.gx__on, .gx__bon', st).forEach(x => x.src = img(g.id + '-on'));
  $$('.gx__off, .gx__on', st).forEach(x => Object.assign(x.style, { left: r.box.left + 'px', top: r.box.top + 'px', width: r.box.width + 'px', height: r.box.height + 'px' }));
  return r;
}
function gxCap() {
  const g = STORE.gallery[GX.i];
  $('#gxCap').innerHTML = `<p class="eyebrow" data-t="galEy">${t('galEy')}</p><b>${L(g)}</b><p>${L(g.note)}</p>
    <p class="card__price gx__price"><b>${money(g.price)}</b><s>${fmt(g.was)}</s></p>
    <p class="gx__hint"><i></i>${t('gxHint')}</p>
    <div class="gx__btns"><button class="gx__add" type="button" data-gx-add>${icon('bag', 18, 1.8)}<span>${t('add')}</span></button>
      <button class="lsw gx__sw" type="button" role="switch" aria-checked="${GX.lit}" data-gx-light><span class="lsw__k" aria-hidden="true"></span><span>${t(GX.lit ? 'gxRoomOff' : 'gxRoomOn')}</span></button></div>`;
}
function gxSetLit(on, dur) {
  GX.lit = on; const sw = $('[data-gx-light]');
  if (sw) { sw.setAttribute('aria-checked', String(on)); sw.lastElementChild.textContent = t(on ? 'gxRoomOff' : 'gxRoomOn'); }
  const els = $$('.gx__on, .gx__bon', gxEl());
  if (G) gsap.to(els, { opacity: on ? 1 : 0, duration: dur ?? 1.4, ease: 'power1.inOut' }); else gsap.set(els, { opacity: on ? 1 : 0 });
}
function renderBand() {
  const words = STORE.ui[lang].band.map(w => w.replace('{n}', maxOff));
  const one = words.map(w => `<span>${w}</span><i>✦</i>`).join('');
  $('#lband').innerHTML = `<div class="lband__g">${one}</div><div class="lband__g">${one}</div>`;
}
function renderGal() {
  const G2 = STORE.gallery;
  $('#galRow').innerHTML = G2.map((g, j) => `<button class="gx__f" type="button" data-j="${j}" aria-label="${L(g)}"><img src="${img(g.id + '-cut')}" alt="" loading="lazy" style="--d:${j * 1.3}s"></button>`).join('');
  $('#gxNames').innerHTML = G2.map(g => `<span><b>${L(g)}</b><small><i></i>${t('galTap')}</small></span>`).join('');
  $('#gxNav').innerHTML = `<button class="gx__arr" type="button" data-gx-go="-1" aria-label="${t('prev')}">${icon('arrow', 20, 2)}</button>
    <span class="gx__dots">${G2.map(() => '<i></i>').join('')}</span>
    <button class="gx__arr" type="button" data-gx-go="1" aria-label="${t('next')}">${icon('arrow', 20, 2)}</button>`;
  $('#gxNav [data-gx-go="1"] svg').style.transform = lang === 'ar' ? 'scaleX(-1)' : '';
  $('#gxNav [data-gx-go="-1"] svg').style.transform = lang === 'ar' ? '' : 'scaleX(-1)';
  $('[data-gx-close]').innerHTML = icon('close', 18, 2); $('[data-gx-close]').setAttribute('aria-label', t('gxBack'));
  gxEl().classList.toggle('is-open', GX.open); gxCap();
  requestAnimationFrame(() => { gxLayout(false); if (GX.open) { const st = gxEl(); gxRoomImgs(STORE.gallery[GX.i]); gsap.set($$('#galRow .gx__f'), { opacity: 0 }); gsap.set('#gxCap > *', { opacity: 1 });
    gsap.set($$('.gx__off, .gx__boff', st), { opacity: 1 }); gsap.set($$('.gx__on, .gx__bon', st), { opacity: GX.lit ? 1 : 0 }); } });
}
function gxGo(d) {
  if (GX.busy) return; const n = STORE.gallery.length;
  if (!GX.open) { GX.i = (GX.i + d + n) % n; gxLayout(true); return; }
  // in a room: straight to the next room — the light goes off, the next room fades in, then its lamp glows
  GX.busy = true; const st = gxEl(), all = $$('.gx__off, .gx__on, .gx__boff, .gx__bon', st);
  const swap = () => { GX.i = (GX.i + d + n) % n; gxLayout(false); $$('#galRow .gx__f').forEach(f => gsap.set(f, { opacity: 0 })); gxRoomImgs(STORE.gallery[GX.i]); GX.lit = false; gxCap();
    if (!G) { gsap.set($$('.gx__off, .gx__boff', st), { opacity: 1 }); GX.busy = false; return; }
    gsap.fromTo($$('.gx__off, .gx__boff', st), { opacity: 0, x: 40 * d * (lang === 'ar' ? -1 : 1) }, { opacity: 1, x: 0, duration: .7, ease: 'expo.out' });
    gsap.fromTo('#gxCap > *', { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: .6, stagger: .05, ease: 'expo.out' });
    gsap.delayedCall(.5, () => { GX.busy = false; }); };
  if (G) gsap.to(all, { opacity: 0, duration: .4, onComplete: swap }); else swap();
}
function gxOpen() {
  if (GX.open || GX.busy) return; GX.busy = true; GX.open = true;
  const g = STORE.gallery[GX.i], f = $$('#galRow .gx__f')[GX.i], st = gxEl();
  st.classList.add('is-open'); GX.lit = false; gxCap();
  const r = gxRoomImgs(g);
  // while it travels, the lamp stays inside the room's edges
  { const sr = st.getBoundingClientRect(), b = $('#gxScene').getBoundingClientRect(), rad = getComputedStyle($('#gxScene')).borderRadius;
    $('#galRow').style.clipPath = `inset(${b.top - sr.top}px ${sr.right - b.right}px ${sr.bottom - b.bottom}px ${b.left - sr.left}px round ${rad})`; }
  const others = $$('#galRow .gx__f').filter(x => x !== f), off = $$('.gx__off, .gx__boff', st);
  if (!G) { gsap.set(f, { opacity: 0 }); gsap.set(off, { opacity: 1 }); gxSetLit(true); GX.busy = false; return; }
  gsap.timeline({ onComplete: () => { GX.busy = false; } })
    .to([...others, '#gxNames'], { opacity: 0, duration: .4 }, 0)
    .to(f, { ...r.stage, duration: 1.2, ease: 'power3.inOut' }, 0)
    .to(off, { opacity: 1, duration: .8, ease: 'power2.out' }, .55)
    .set(f, { opacity: 0 }, 1.25)
    .add(() => gxSetLit(true), 1.45)
    .fromTo('#gxCap > *', { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: .8, stagger: .06, ease: 'expo.out' }, .9);
}
function gxClose() {
  if (!GX.open || GX.busy) return; GX.busy = true;
  const g = STORE.gallery[GX.i], f = $$('#galRow .gx__f')[GX.i], st = gxEl(), all = $$('.gx__off, .gx__on, .gx__boff, .gx__bon', st);
  const done = () => { st.classList.remove('is-open'); GX.open = false; GX.busy = false; GX.lit = false; $('#galRow').style.clipPath = ''; gxLayout(false); gsap.set('#gxNames', { opacity: 1 }); };
  if (!G) { gsap.set(all, { opacity: 0 }); done(); return; }
  gsap.set(f, { ...gxRoom(g).stage, opacity: 1 });
  gsap.timeline({ onComplete: done })
    .to('#gxCap > *', { opacity: 0, duration: .3 }, 0)
    .to(all, { opacity: 0, duration: .6 }, .1)
    .add(() => { $('#galRow').style.clipPath = ''; }, .35)
    .to(f, { ...gxSlot(g, 0), duration: 1.1, ease: 'power3.inOut' }, .3)
    .add(() => { $$('#galRow .gx__f').forEach((x, j) => { if (x !== f) gsap.to(x, { opacity: gxSlot(STORE.gallery[j], gxOff(j)).opacity, duration: .5 }); }); gxLayout(true); gsap.to('#gxNames', { opacity: 1, duration: .5 }); }, 1);
}
$('#gx').addEventListener('click', e => {
  const go = e.target.closest('[data-gx-go]'); if (go) { gxGo(+go.dataset.gxGo); return; }
  if (e.target.closest('[data-gx-close]')) { gxClose(); return; }
  if (e.target.closest('[data-gx-light]')) { if (!GX.busy) { gxSetLit(!GX.lit, .9); } return; }
  if (e.target.closest('[data-gx-add]')) { const g = STORE.gallery[GX.i]; cart++; const c = $('#cartCount'); c.textContent = cart; c.classList.add('has-items'); c.classList.remove('bump'); void c.offsetWidth; c.classList.add('bump'); toast(t('added', { n: L(g) })); return; }
  if (GX.open) { if (e.target.closest('.gx__scene') && !GX.busy) gxSetLit(!GX.lit, .9); return; }   // in the room: a tap on the photo switches the light
  const f = e.target.closest('.gx__f'); if (!f) return;
  const j = +f.dataset.j; if (j === GX.i) gxOpen(); else { GX.i = j; gxLayout(true); }
});
// a swipe moves to the next lamp (or the next room)
(() => { let x0 = null; const st = $('#gx');
  st.addEventListener('pointerdown', e => { x0 = e.clientX; });
  st.addEventListener('pointerup', e => { if (x0 == null) return; const dx = e.clientX - x0; x0 = null; if (Math.abs(dx) > 50) gxGo((dx < 0 ? 1 : -1) * (lang === 'ar' ? -1 : 1)); }); })();
addEventListener('resize', () => { if (GX.busy) return; gxLayout(false); if (GX.open) gxRoomImgs(STORE.gallery[GX.i]); });

/* the product view (the live store's product page): photo with its own light switch, price, and the green energy bar */
let pdP = null, pdN = 1;
function pdOpen(id) {
  const p = byId[id]; if (!p) return; pdP = p; pdN = 1;
  $('.pd__off').src = img(p.id); $('.pd__on').src = img(p.id + '-on'); $('#pdMedia').classList.remove('is-lit');
  $('#pdName').textContent = L(p); $('#pdPrice').innerHTML = `<b>${money(p.price)}</b><s>${fmt(p.was)}</s>`; $('#pdQ').textContent = 1;
  $('#pdSw').setAttribute('aria-checked', 'false'); $('#pdSwT').textContent = t('pdLight');
  $('#pdEco').innerHTML = `<div class="ebar__row"><span class="ebar__l"><i aria-hidden="true">⚡</i>${t('pdEco')}</span><b class="ebar__v">${t('pdSave', { n: `<span class="ebar__n">0</span>` })}</b></div><div class="ebar__t"><i style="--e:${p.eco}"></i></div>`;
  $('#pdAdd').innerHTML = `${icon('bag', 18, 1.8)}<span>${t('add')}</span>`;
  $('#pdPage').href = p.url; $('#pdPage').innerHTML = `<span>${t('pdPage')}</span>${icon('ne', 16, 2)}`;
  $('#pd').showModal(); if (lenis) lenis.stop();
  requestAnimationFrame(() => requestAnimationFrame(() => $('#pdEco').classList.add('is-in')));
  const n = $('.ebar__n'), o = { v: 0 };
  if (G) { gsap.fromTo('.pd__in', { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: .6, ease: 'expo.out' }); gsap.to(o, { v: p.eco, duration: 1.4, delay: .25, ease: 'power3.out', onUpdate: () => n.textContent = Math.round(o.v) }); } else n.textContent = p.eco;
}
function pdClose() { $('#pd').close(); $('#pdEco').classList.remove('is-in'); if (lenis) lenis.start(); }
$('#pgrid').addEventListener('click', e => { const a = e.target.closest('[data-pd]'); if (!a) return; e.preventDefault(); pdOpen(a.dataset.pd); });
$('#pdX').innerHTML = icon('close', 22); $('#pdX').onclick = pdClose;
$('#pd').addEventListener('click', e => { if (e.target === $('#pd')) pdClose(); });
$('#pd').addEventListener('cancel', () => { $('#pdEco').classList.remove('is-in'); if (lenis) lenis.start(); });
$('#pdSw').onclick = () => { const on = !$('#pdMedia').classList.contains('is-lit'); $('#pdMedia').classList.toggle('is-lit', on); $('#pdSw').setAttribute('aria-checked', String(on)); $('#pdSwT').textContent = t(on ? 'pdLightOn' : 'pdLight'); };
$('.pd__qty').addEventListener('click', e => { const b = e.target.closest('[data-q]'); if (!b) return; pdN = Math.max(1, pdN + +b.dataset.q); $('#pdQ').textContent = pdN; });
$('#pdAdd').onclick = () => { cart += pdN; const c = $('#cartCount'); c.textContent = cart; c.classList.add('has-items'); c.classList.remove('bump'); void c.offsetWidth; c.classList.add('bump'); toast(t('added', { n: L(pdP) })); pdClose(); };

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
  if (G) gsap.fromTo(['#gxScene', '#gxCap'], { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 1.3, stagger: .12, ease: 'expo.out', clearProps: 'transform,opacity', scrollTrigger: { trigger: '#gx', start: 'top 75%' } });
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
# the department loader as on the other departments: dots → line → logo → a ring of lamps spins around it (the lamps as they are, no lighting)
rep("  // ring of 8 tables in mixed shapes on pink and grey\n  const pick = [['t03', 'circle', '#C6F7A6'], ['t12', 'arch', '#F4F4F4'], ['life1', 'sq', '#e9e7e4'], ['t01', 'pill', '#F4A7FC'], ['t08', 'circle', '#F4F4F4'], ['t17', 'sq', '#C6F7A6'], ['t15', 'arch', '#F4F4F4'], ['t02', 'circle', '#F4F4F4']];",
    "  // ring of 8 lamps in mixed shapes on lavender, lemon and grey\n  const pick = [['lp06', 'circle', '#D4C5FF'], ['lp13', 'arch', '#F4F4F4'], ['lp02', 'sq', '#F8FA75'], ['lp07', 'pill', '#D4C5FF'], ['lp05', 'circle', '#F4F4F4'], ['lp17', 'sq', '#F0EBFF'], ['lp15', 'arch', '#F4F4F4'], ['lp10', 'circle', '#FDFDE3']];")

# the product view: in this preview a tap on a card opens it; on the live store this is the product page
rep('<div class="toast" id="toast" role="status" aria-live="polite"></div>', '''<div class="toast" id="toast" role="status" aria-live="polite"></div>

<!-- THE PRODUCT (on the live store: the product page). The energy bar sits under the price, like the "pieces left" bar, in green -->
<dialog class="pd" id="pd" aria-labelledby="pdName">
  <div class="pd__in" data-lenis-prevent>
    <button class="icon-btn pd__x" type="button" id="pdX" data-t-aria="pdClose"></button>
    <div class="pd__media" id="pdMedia"><img class="pd__off" alt=""><img class="pd__on" alt="">
      <button class="lsw pd__sw" id="pdSw" type="button" role="switch" aria-checked="false"><span class="lsw__k" aria-hidden="true"></span><span id="pdSwT"></span></button></div>
    <div class="pd__copy">
      <p class="eyebrow" data-t="tables"></p>
      <h2 id="pdName"></h2>
      <p class="card__price pd__price" id="pdPrice"></p>
      <div class="ebar" id="pdEco"></div>
      <div class="pd__buy"><div class="pd__qty"><button type="button" data-q="-1" aria-label="-">−</button><b id="pdQ">1</b><button type="button" data-q="1" aria-label="+">+</button></div>
        <button class="pd__add" type="button" id="pdAdd"></button></div>
      <a class="pd__page" id="pdPage" href="#" target="_blank" rel="noopener"></a>
    </div>
  </div>
</dialog>''')

# a band of words between the "why" card and the help card, so their two pictures never meet
rep('<!-- 8 · HELP -->', '<!-- a band of words between two pictures -->\n<section class="lband" aria-hidden="true"><div class="lband__track" id="lband"></div></section>\n\n<!-- 8 · HELP -->')

# ---------------------------------------------------------------- styles
rep("/* ===================== ANNOUNCEMENT + HEADER ===================== */", """/* ===================== LIGHTING: loader ===================== */
.loader__dots i{ background:var(--lav); } .loader__dots i:nth-child(2){ background:var(--lemon); } .loader__dots i:nth-child(3){ background:var(--orange); }
.ring__t img.ring__on{ position:absolute; inset:0; padding:0; object-fit:cover; mix-blend-mode:normal; opacity:0; transition:opacity .45s calc(var(--k) * 90ms) ease; }
.ring.is-lit .ring__t img.ring__on{ opacity:1; }

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
.shape__big > img.sb__on{ opacity:0; transition:opacity 1.4s ease; }
.shape__big.is-lit > img.sb__on{ opacity:1; }
.shape__big > img{ object-position:50% 32%; }
.shape__big h2 .w__g{ color:rgba(255,255,255,.25); }
.shape__big h2 .w__i{ color:var(--white); }
.shape__big::after{ background:linear-gradient(180deg, rgba(0,0,0,.62), rgba(0,0,0,.25) 46%, rgba(0,0,0,.08) 66%, rgba(0,0,0,.4)); }
.st{ background:var(--white); }

/* ===================== LIGHTING: the gallery (the lamp travels into its room; one brand colour for the controls) ===================== */
.gx{ padding-top:var(--section); }
.gx__stage{ --acc:var(--forest); --pad:max(var(--gutter), calc((100% - 1440px) / 2 + var(--gutter))); position:relative; overflow:hidden; height:clamp(640px, 92svh, 880px); background:var(--white); color:var(--black); touch-action:pan-y; }
/* the room: about two thirds of the width, the words in a column beside it */
.gx__scene{ position:absolute; z-index:0; top:28px; bottom:28px; inset-inline-end:var(--pad); width:min(64%, 1000px); border-radius:clamp(24px, 3vw, 44px); overflow:hidden; pointer-events:none; }
.gx__stage.is-open .gx__scene{ pointer-events:auto; cursor:pointer; }
.gx__scene img{ position:absolute; opacity:0; }
.gx__scene .gx__boff, .gx__scene .gx__bon{ inset:0; width:100%; height:100%; object-fit:cover; filter:blur(30px) saturate(1.05); transform:scale(1.2); }
.gx__x{ display:none!important; position:absolute; z-index:3; top:14px; inset-inline-end:14px; width:42px; height:42px; border-radius:50%; display:grid; place-items:center; background:rgba(255,255,255,.9); opacity:0; transition:opacity .4s; }
.gx__stage.is-open .gx__x{ opacity:1; transition-delay:1s; }
.gx__lamps, .gx__names{ position:absolute; inset:0; }
.gx__lamps{ z-index:1; }
.gx__names{ z-index:2; pointer-events:none; }
.gx__f{ position:absolute; display:block; padding:0; }
.gx__f img{ display:block; width:100%; height:100%; filter:drop-shadow(0 24px 24px rgba(0,0,0,.14)); animation:gxFloat 6s ease-in-out var(--d) infinite; }
@keyframes gxFloat{ 0%,100%{ transform:translateY(0); } 50%{ transform:translateY(-10px); } }
.gx__stage.is-open .gx__f img{ animation:none; filter:none; }
.gx__names span{ position:absolute; display:flex; flex-direction:column; align-items:center; gap:6px; translate:-50% 0; white-space:nowrap; }
.gx__names b{ font-size:14px; font-weight:700; }
.gx__names span.is-cur b{ font-size:clamp(18px, 1.8vw, 22px); }
.gx__names small{ display:none; align-items:center; gap:6px; height:30px; padding-inline:10px 12px; border-radius:var(--r-pill); background:var(--g100); font-size:12px; font-weight:700; }
.gx__names span.is-cur small{ display:inline-flex; }
.gx__names small i{ width:7px; height:7px; border-radius:50%; background:var(--acc); animation:ping3 1.6s var(--ease) infinite; }
@keyframes ping3{ 0%,100%{ box-shadow:0 0 0 0 rgba(8,128,64,.5); } 70%{ box-shadow:0 0 0 8px rgba(8,128,64,0); } }
.gx__head{ position:absolute; z-index:2; inset-inline:0; top:clamp(24px, 4vw, 56px); display:grid; gap:10px; pointer-events:none; transition:opacity .5s; }
.gx__head .eyebrow::before, .gx__cap .eyebrow::before{ background:var(--acc); }
.gx__head h2{ font-size:clamp(28px, 3.6vw, 52px); font-weight:600; line-height:1.15; letter-spacing:-.03em; max-width:16ch; }
html[lang="ar"] .gx__head h2{ font-weight:700; line-height:1.45; letter-spacing:0; }
.gx__tx{ color:var(--ink-2); max-width:40ch; }
.gx__nav{ position:absolute; z-index:3; left:50%; bottom:26px; translate:-50% 0; display:flex; align-items:center; gap:16px; transition:left .8s var(--ease), translate .8s var(--ease); }
.gx__arr{ width:48px; height:48px; border-radius:50%; display:grid; place-items:center; background:var(--acc); color:var(--white); transition:transform .4s var(--ease), background-color .3s; }
.gx__arr:hover{ background:#066B36; transform:scale(1.06); }
.gx__dots{ display:flex; gap:6px; }
.gx__dots i{ width:8px; height:8px; border-radius:var(--r-pill); background:var(--g200); transition:width .5s var(--ease), background-color .4s; }
.gx__dots i.is-on{ width:26px; background:var(--acc); }
/* the words beside the room: name, a line, price, add to cart and the light switch */
.gx__cap{ position:absolute; z-index:3; inset-inline-start:var(--pad); top:50%; translate:0 -50%; width:calc(100% - min(64%, 1000px) - 2 * var(--pad) - 40px); max-width:380px; display:grid; gap:12px; justify-items:start; pointer-events:none; }
.gx__cap > *{ opacity:0; }
.gx__cap > b{ font-size:clamp(26px, 2.8vw, 40px); font-weight:700; line-height:1.25; }
.gx__cap > p:not(.eyebrow):not(.gx__price){ color:var(--ink-2); font-size:15px; line-height:1.7; }
.gx__price b{ font-size:22px; }
.gx__btns{ display:flex; flex-wrap:wrap; align-items:center; gap:10px; }
.gx__hint{ display:inline-flex; align-items:center; gap:8px; font-size:13px; font-weight:700; color:var(--ink-2); }
.gx__hint i{ width:8px; height:8px; border-radius:50%; background:var(--acc); animation:ping3 1.6s var(--ease) infinite; }
.gx__stage:has(.gx__sw[aria-checked="true"]) .gx__hint{ opacity:.0!important; }
/* the band of words between the last two sections */
.lband{ margin-top:var(--section); overflow:hidden; background:var(--lav); padding-block:clamp(18px, 2.6vw, 30px); }
.lband__track{ display:flex; width:max-content; animation:marquee 34s linear infinite; }
.lband__g{ display:flex; align-items:center; gap:clamp(18px, 2.6vw, 36px); padding-inline-end:clamp(18px, 2.6vw, 36px); white-space:nowrap; }
.lband__g span{ font-size:clamp(24px, 3.4vw, 46px); font-weight:700; letter-spacing:-.02em; }
html[lang="ar"] .lband__g span{ letter-spacing:0; }
.lband__g i{ font-style:normal; font-size:clamp(18px, 2.4vw, 30px); color:var(--orange); }
.lband + .help{ padding-top:var(--section); }
.gx__add{ display:inline-flex; align-items:center; gap:8px; height:50px; padding-inline:20px 22px; border-radius:var(--r-pill); background:var(--acc); color:var(--white); font-size:15px; font-weight:700; transition:background-color .3s; }
.gx__add:hover{ background:#066B36; }
.gx__sw{ height:50px; }
.gx__sw[aria-checked="true"]{ background:var(--night); color:#FFE7B8; }
.gx__sw[aria-checked="true"] .lsw__k::after{ background:#FFD27A; box-shadow:0 0 12px 3px rgba(255,200,110,.7); }
.gx__stage.is-open .gx__head, .gx__stage.is-open .gx__names{ opacity:0; pointer-events:none; }
.gx__stage.is-open .gx__lamps{ pointer-events:none; }   /* the cut-outs no longer cover the room, so its ✕ and light taps work */
.gx__stage.is-open .gx__cap{ pointer-events:auto; }
.gx__stage.is-open .gx__nav{ left:calc(var(--pad) + min(190px, (100% - min(64%, 1000px) - 2 * var(--pad) - 40px) / 2)); }
html[dir="rtl"] .gx__stage.is-open .gx__nav{ left:auto; right:calc(var(--pad) + min(190px, (100% - min(64%, 1000px) - 2 * var(--pad) - 40px) / 2)); translate:50% 0; }
@media (max-width:899px){
  .gx__stage{ height:auto; min-height:min(190vw, 820px); }
  .gx__scene{ top:12px; bottom:auto; inset-inline:12px; width:auto; height:min(62vh, 120vw); }
  .gx__cap{ top:auto; translate:none; inset-inline:20px; bottom:84px; width:auto; max-width:none; gap:8px; }
  .gx__cap > p:not(.eyebrow):not(.gx__price){ display:none; }
  .gx__cap .eyebrow{ display:none; }
  .gx__cap > b{ font-size:24px; }
  .gx__add, .gx__sw{ height:46px; }
  .gx__stage.is-open .gx__nav, html[dir="rtl"] .gx__stage.is-open .gx__nav{ left:50%; right:auto; translate:-50% 0; }
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
.pgrid .ttile--dark{ background:var(--orange); color:var(--white); }
.pgrid .ttile--dark p{ color:rgba(255,255,255,.88); }
/* the product view (on the live store: the product page) */
.pd{ width:min(100%, 980px); max-width:none; max-height:none; margin:auto; padding:0; border:0; background:none; overflow:visible; }
.pd::backdrop{ background:rgba(15,12,20,.45); -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px); }
.pd__in{ position:relative; display:grid; max-height:calc(100svh - 32px); overflow:auto; margin:16px; border-radius:28px; background:var(--white); }
@media (min-width:820px){ .pd__in{ grid-template-columns:1fr 1fr; } }
.pd__x{ position:absolute; z-index:3; top:12px; inset-inline-end:12px; background:var(--g100); }
.pd__media{ position:relative; aspect-ratio:1; background:var(--white); }
.pd__media img{ position:absolute; inset:0; width:100%; height:100%; object-fit:contain; padding:6%; mix-blend-mode:multiply; }
.pd__media .pd__on{ opacity:0; transition:opacity 1.2s ease; }
.pd__media.is-lit .pd__on{ opacity:1; }
.pd__sw{ position:absolute; z-index:2; bottom:14px; inset-inline-start:14px; }
.pd__sw[aria-checked="true"]{ background:var(--night); color:#FFE7B8; }
.pd__sw[aria-checked="true"] .lsw__k::after{ inset-inline-start:19px; background:#FFD27A; box-shadow:0 0 12px 3px rgba(255,200,110,.7); }
.pd__copy{ display:grid; gap:14px; align-content:center; padding:clamp(20px, 3.4vw, 44px); }
.pd__copy h2{ font-size:clamp(24px, 2.6vw, 34px); font-weight:700; line-height:1.3; }
.pd__price b{ font-size:22px; }
.pd__buy{ display:flex; gap:10px; margin-top:6px; }
.pd__qty{ display:inline-flex; align-items:center; gap:14px; height:52px; padding-inline:14px; border-radius:var(--r-pill); box-shadow:inset 0 0 0 1px var(--g200); font:600 16px/1 var(--f-latin); }
.pd__qty button{ width:26px; height:26px; font-size:20px; line-height:1; }
.pd__page{ display:inline-flex; align-items:center; gap:6px; justify-self:start; font-size:14px; font-weight:700; text-decoration:underline; text-underline-offset:4px; }
.pd__add{ flex:1; display:inline-flex; align-items:center; justify-content:center; gap:8px; height:52px; border-radius:var(--r-pill); background:var(--black); color:var(--white); font-size:15px; font-weight:700; }
/* the energy bar: like the store's "pieces left" bar (a line of words over a thin bar), in green, with a yellow ⚡ and a moving shine.
   The figure is a PLACEHOLDER for the review; on the live store it comes from each lamp's real data */
.ebar{ display:grid; gap:8px; }
.ebar__row{ display:flex; justify-content:space-between; align-items:center; gap:10px; font-size:14px; }
.ebar__l{ display:inline-flex; align-items:center; gap:8px; font-weight:700; color:#0B5E30; }
.ebar__l i{ width:24px; height:24px; border-radius:50%; display:grid; place-items:center; background:#088040; color:var(--lemon); font-style:normal; font-size:13px; animation:zap 2.4s ease-in-out infinite; }
@keyframes zap{ 0%,100%{ transform:scale(1); box-shadow:0 0 0 0 rgba(8,128,64,.35); } 50%{ transform:scale(1.1); box-shadow:0 0 0 6px rgba(8,128,64,0); } }
.ebar__v{ color:#0B5E30; font-weight:700; }
.ebar__n{ font-family:var(--f-latin); font-variant-numeric:tabular-nums; }
.ebar__t{ position:relative; height:6px; border-radius:6px; background:#E2F3E9; overflow:hidden; }
.ebar__t i{ position:absolute; inset-block:0; inset-inline-start:0; width:calc(var(--e) * 1%); border-radius:inherit; background:linear-gradient(90deg, #02A27A, #3FCB86 40%, #088040 80%); background-size:200% 100%; transform:scaleX(0); transform-origin:var(--to, left) center; transition:transform 1.4s var(--ease) .2s; animation:ecoFlow 1.8s linear infinite; }
html[dir="rtl"] .ebar__t i{ --to:right; }
@keyframes ecoFlow{ to{ background-position:-200% 0; } }
.ebar.is-in .ebar__t i{ transform:scaleX(1); }

/* the bar: room for the switch on phones */
@media (max-width:767px){ .bar{ flex-wrap:wrap; } .bar .filters{ flex:0 0 100%; order:1; } .bar .lsw{ order:2; } .bar .sortw{ order:3; margin-inline-start:auto; } }

/* phones: the help card's words come before its picture, so it never sits right under the photo above it */
@media (max-width:639px){ .help__copy{ order:-1; } }

/* the collections hover in lavender */
.crow:hover, .crow.is-on{ background:var(--lav); }
.hero__pill{ background:var(--lav); }

/* ===================== ANNOUNCEMENT + HEADER ===================== */""")

open('ket-lamps.html', 'w').write(s)
print('wrote ket-lamps.html', len(s))
