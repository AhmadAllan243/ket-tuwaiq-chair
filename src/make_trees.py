"""
Builds ket-trees.html (the trees department, for review) from ket-tables.html (the department design):
the trees from the store, yellow (most) and light green (a touch), the watering loader, the planting
initiative banner and its page, the store's own plant photos.

usage: python3 make_trees.py      (run from src)
"""
import re, json

s = open('ket-tables.html').read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, f'expected {n}x, found {c}: {a[:80]}'
    s = s.replace(a, b)

# ---------------------------------------------------------------- data: the trees from the store
rows = [l.split('\t') for l in open('media/trees/trees.tsv').read().strip().split('\n')]
def budget(p): return 'coffee' if p < 300 else 'side' if p < 400 else 'sets' if p < 500 else 'console'
FAM = {'laxi': 'tr08 tr13 tr29 tr30', 'tm': 'tr01 tr03 tr04 tr09 tr10 tr11 tr18 tr19 tr28', 'wood': 'tr02 tr05 tr06 tr07',
       'teras': 'tr20 tr21 tr22 tr23 tr24 tr25', 'golden': 'tr14 tr26 tr27', 'tropic': 'tr12 tr15 tr16 tr17'}
fam = {i: k for k, v in FAM.items() for i in v.split()}
ORDER = 'tr01 tr15 tr30 tr22 tr03 tr02 tr11 tr17 tr05 tr21 tr09 tr12 tr08 tr23 tr04 tr16 tr24 tr10 tr06 tr25 tr19 tr18 tr13 tr20 tr28 tr07 tr14 tr26 tr27 tr29'.split()
by = {r[0]: r for r in rows}
prods = []
for i in ORDER:
    _, ar, en, price, was, _, slug = by[i]
    pr = float(price); w = float(was)
    prods.append("    { id: %s, type: %s, col: %s, ar: %s, en: %s, price: %s, was: %s, url: %s }" % (
        json.dumps(i), json.dumps(budget(pr)), json.dumps(fam[i]), json.dumps(ar, ensure_ascii=False), json.dumps(en),
        f'{pr:g}', f'{w:g}', json.dumps('https://ketfurniture.com/products/' + slug, ensure_ascii=False)))

i = s.index("const M = 'media/tables/';"); j = s.index('  ui: {')
s = s[:i] + """const M = 'media/trees/';
const STORE = {
  currency: { ar: 'ر.س', en: 'SAR' },
  vat: '310803678600003', cr: '4030396963',
  category: { ar: 'الأشجار', en: 'Trees' },

  // shop by budget (on the live store: price ranges). hero = the tile picture
  types: [
    { id: 'coffee', ar: 'أقل من 300', en: 'Under 300', hero: 'tr21' },
    { id: 'side', ar: '300 – 400', en: '300 – 400', hero: 'tr11' },
    { id: 'sets', ar: '400 – 500', en: '400 – 500', hero: 'tr03' },
    { id: 'console', ar: '500 وأكثر', en: '500 and up', hero: 'tr30' }
  ],

  // every tree in the department (names, prices and photos from ketfurniture.com, Nov 2026)
  products: [
""" + ',\n'.join(prods) + """
  ],

  // tree families
  collections: [
    { id: 'tm', ar: 'فيكس وليراتا', en: 'Ficus & lyrata', img: 'tr03', note: { ar: 'أوراق عريضة لامعة', en: 'Broad, glossy leaves' } },
    { id: 'laxi', ar: 'أشجار الزيتون', en: 'Olive trees', img: 'tr30', note: { ar: 'أغصان فضية بروح المكان', en: 'Silver branches, local spirit' } },
    { id: 'teras', ar: 'أشجار بأسماء', en: 'Named trees', img: 'tr22', note: { ar: 'نسيم، سنا، روين، ليوان', en: 'Naseem, Sana, Rawin, Liwan' } },
    { id: 'tropic', ar: 'استوائية', en: 'Tropical', img: 'tr15', note: { ar: 'موز وستريليتزيا وبامبو', en: 'Banana, strelitzia, bamboo' } },
    { id: 'wood', ar: 'دراسينا ومارجيناتا', en: 'Dracaena & marginata', img: 'tr02', note: { ar: 'أوراق رفيعة وجذوع نحيلة', en: 'Slim leaves, slender trunks' } },
    { id: 'golden', ar: 'نباتات صغيرة', en: 'Small plants', img: 'tr14', note: { ar: 'للطاولة والرف', en: 'For tables and shelves' } }
  ],

""" + s[j:]

# ---------------------------------------------------------------- wording
AR = dict(
  tables='الأشجار', ann3='خصومات تصل إلى {n}٪ على الأشجار', loadLine='قسم الأشجار',
  hLine1='من شجرتك', hPink='يبدأ أثر', hMark='أخضر', hSub='في وطننا', hStatL='تصميم شجرة',
  shapeTx='من ركن الصالة إلى المدخل، ابدأ بالميزانية التي تناسبك.', shapeAll='كل الأشجار', shapeSale='أعلى خصم', shapeStat='تصميم في {k} فئات سعرية، تبدأ من {p}',
  whyEy='لماذا أشجار ket', whyA='اكتشف', whyB='خضرة تدوم بلا سقاية.',
  chip1='ركن الصالة', chip2='المدخل', chip3='المكتب',
  acc1='تبدو حقيقية', acc1b='أوراق بملمس ولون طبيعي، وجذوع حقيقية الشكل، تثبت جمالها سنة بعد سنة.',
  acc2='بلا سقاية ولا عناية', acc2b='لا تحتاج ماء ولا شمس ولا تقليم. تمسح الغبار مرة بالشهر وتبقى كأنها اليوم.',
  acc3='مع كل شجرة نغرس نبتة', acc3b='مع كل شجرة صناعية تختارها، نغرس نبتة طبيعية في أرض وطننا، دعمًا لمبادرة السعودية الخضراء.',
  cardEy='{n} تصميم', cardTx='أشجار مختارة بعناية لتكمّل بيتك وتعيش معك سنوات.', cardH='خضرة تبقى،\nبلا سقاية.', cardBtn='تسوّق الكل',
  typesEy='تسوّق حسب ميزانيتك', typesH='اختر اللي يناسب ميزانيتك.',
  colEy='العائلات', colH='عائلات خضراء تكمّل بعضها.',
  gridEy='كل الأشجار', gridH='الأشجار',
  tileA='خضرة\nبلا عناية.', tileAs='كل شجرة هنا مختارة لتعيش معك بلا سقاية.', tileB='من الورقة\nإلى الجذع.', tileBs='تفاصيل طبيعية تقرّبها من الحقيقة.',
  helpH='محتار وين تحطها؟', helpTx='أرسل لنا صورة المكان، ونقترح عليك الشجرة والمقاس المناسبين.',
)
EN = dict(
  tables='Trees', ann3='Up to {n}% off trees', loadLine='The trees section',
  hLine1='From your tree', hPink='grows a', hMark='green', hSub='mark on our homeland', hStatL='Tree designs',
  shapeTx='From the living-room corner to the entrance, start with the budget that suits you.', shapeAll='All trees', shapeSale='Biggest discount', shapeStat='designs in {k} price ranges, from {p}',
  whyEy='Why ket trees', whyA='Explore', whyB='green that lasts, no watering.',
  chip1='Living-room corner', chip2='Entrance', chip3='Office',
  acc1='They look real', acc1b='Leaves with a natural feel and colour, and real-looking trunks that stay beautiful year after year.',
  acc2='No watering, no care', acc2b='No water, no sun, no pruning. Dust them once a month and they look like the first day.',
  acc3='With every tree, we plant one', acc3b='For every artificial tree you choose, we plant a natural one in our homeland, in support of the Saudi Green Initiative.',
  cardEy='{n} designs', cardTx='Trees picked with care to complete your home and live with you for years.', cardH='Green that stays,\nno watering.', cardBtn='Shop all',
  typesEy='Shop by budget', typesH='Pick what suits your budget.',
  colEy='Families', colH='Green families that go together.',
  gridEy='All trees', gridH='Trees',
  tileA='Green,\nno care.', tileAs='Every tree here is chosen to live with you, no watering.', tileB='From leaf\nto trunk.', tileBs='Natural details that bring them close to the real thing.',
  helpH='Not sure where it goes?', helpTx='Send us a photo of the space and we will suggest the right tree and size.',
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

# the banner and its page (new keys)
rep("      skip: 'تخطَّ إلى المنتجات',", """      pEy: 'مبادرة ket الخضراء', pSub: 'مع كل شجرة صناعية تشتريها منا، نغرس نبتة طبيعية في أرض وطننا 🇸🇦🌱', pMore: 'اعرف عن المبادرة', pShop: 'تسوّق الأشجار',
      ldH: 'قسم الأشجار', ldTx: 'من أهم اللمسات التي تكمّل ديكور بيتك وتزيد المكان جمالًا',
      gH: '🌱 من شجرتك يبدأ أثر أخضر في وطننا', gP1: 'مع كل شجرة صناعية تختارها من متجرنا، نغرس نبتة طبيعية في أرض وطننا الغالي 🇸🇦💚',
      gP2: 'مبادرة نعتز بها، نساهم من خلالها في زيادة الغطاء النباتي في مناطق مملكتنا، لنترك أثرًا ينمو مع الأيام، ويمنح أرضنا مزيدًا من الخضرة، وهواءنا مزيدًا من النقاء، وظلًا يستظل به عابر، ومأوى تحتضن فيه الطيور حياتها.',
      gP3: 'نغرس اليوم خيرًا، ليبقى غدًا ظلًا وأجرًا وعطاءً.', gP4: 'معًا نحو مستقبل أكثر خضرة، تماشيًا مع مستهدفات مبادرة السعودية الخضراء.', gBtn: 'ازرع أثرًا معنا 🌱', gClose: 'إغلاق',
      w1: 'نغرس', w2: 'أثرًا', w3: 'في وطننا',
      skip: 'تخطَّ إلى المنتجات',""")
rep("      skip: 'Skip to products',", """      pEy: 'The ket green initiative', pSub: 'For every artificial tree you buy from us, we plant a natural one in our homeland 🇸🇦🌱', pMore: 'About the initiative', pShop: 'Shop trees',
      ldH: 'The trees section', ldTx: 'One of the touches that completes your home and makes the space even more beautiful',
      gH: '🌱 From your tree, a green mark grows in our homeland', gP1: 'For every artificial tree you choose from our store, we plant a natural one in the land of our dear homeland 🇸🇦💚',
      gP2: 'An initiative we are proud of: we add to the green cover across the regions of our Kingdom, leaving a mark that grows with the days, giving our land more green and our air more freshness, shade for a passer-by and a home for the birds.',
      gP3: 'We plant good today, so tomorrow it stays shade, reward and giving.', gP4: 'Together towards a greener future, in line with the goals of the Saudi Green Initiative.', gBtn: 'Plant a mark with us 🌱', gClose: 'Close',
      w1: 'We plant', w2: 'a mark', w3: 'in our homeland',
      skip: 'Skip to products',""")

# ---------------------------------------------------------------- colours: yellow (most), light green (a touch)
rep("  --lime:#C6F7A6; --pink:#F4A7FC; --blush:var(--pink); --rose:var(--pink); --lime-l:#E9FCDD; --pink-l:#FCE6FE; --line:rgba(0,0,0,.08);",
    "  --lime:#C4F5A4; --pink:#F8FA75; --blush:var(--pink); --rose:var(--pink); --lime-l:#E9FCDD; --pink-l:#FCFDD9; --line:rgba(0,0,0,.08);\n  --yellow:#F8FA75; --yellow-l:#FCFDD9; --yellow-d:#E6E85A;   /* the trees section: yellow most of the way, the light green as a touch */")
rep(".hero__pink{ color:var(--pink); }", ".hero__pink{ color:var(--forest); }")
rep(".hero__stat svg{ color:var(--pink); }", ".hero__stat svg{ color:var(--forest); }")
rep("place-items:center; color:var(--pink); }", "place-items:center; color:var(--forest); }")
rep("<link rel=\"preload\" as=\"image\" href=\"media/tables/hero-joy.webp\">", "<link rel=\"preload\" as=\"image\" href=\"media/trees/ill-water.webp\">\n<link rel=\"preload\" as=\"image\" href=\"media/trees/ill-woman.webp\">")
rep('<title>', '<title>', s.count('<title>'))
s = re.sub(r'<title>.*?</title>', '<title>ket · الأشجار</title>', s, count=1)

# ---------------------------------------------------------------- pictures in the page
rep('<img src="media/tables/hero-joy.webp" alt="" width="838" height="474" fetchpriority="high" id="heroImg">',
    '<img src="media/trees/life-sofa.webp" alt="" width="1145" height="1374" fetchpriority="high" id="heroImg">')
rep('<img src="media/tables/life2.webp" alt="" loading="lazy" width="1100" height="730">\n      <div><h2 id="shapeTitle"',
    '<img src="media/trees/life-lily.webp" alt="" loading="lazy" width="736" height="1104">\n      <div><h2 id="shapeTitle"')
rep('<span class="sav"><img src="media/tables/t03.webp" alt="" loading="lazy"></span>', '<span class="sav"><img src="media/trees/tr03.webp" alt="" loading="lazy"></span>')
rep('<span class="ipill ipill--cut"><img src="media/tables/t08.webp" alt="" loading="lazy"></span>', '<span class="ipill ipill--cut"><img src="media/trees/tr05.webp" alt="" loading="lazy"></span>')
rep('<img src="media/tables/life2.webp" alt="" loading="lazy" width="1100" height="730" data-par>', '<img src="media/trees/life-walk.webp" alt="" loading="lazy" width="1024" height="1280" data-par>')
rep('<div class="help__img"><img src="media/tables/t11.webp" alt="" loading="lazy"></div>', '<div class="help__img"><img src="media/trees/leaf-lily.webp" alt="" loading="lazy"></div>')
rep("`<div class=\"ttile ttile--photo\"><img src=\"${img('life1')}\" alt=\"\" loading=\"lazy\">", "`<div class=\"ttile ttile--photo\"><img src=\"${img('leaf-fig')}\" alt=\"\" loading=\"lazy\">")
rep("${col('tm', 'st--short', 'tm-side', 'white')}", "${col('tm', 'st--short', 'tr09', 'yellow-l')}")
rep("${col('laxi', 'st--full', 't16', 'white', true)}", "${col('laxi', 'st--full', 'tr29', 'yellow-l', true)}")
rep("${tile('coffee', 'st--a', 'white')}", "${tile('coffee', 'st--a', 'yellow-l')}")
rep("${tile('console', 'st--sq', 'white')}", "${tile('console', 'st--sq', 'lime-l')}")
rep("$('#sizeBtn').onclick = () => { setFilter({ type: 'coffee', col: null }); goGrid(); };", "")
rep('<!-- 7 · SIZE GUIDE -->\n<section class="section container" aria-labelledby="sizeTitle">', '<!-- 7 · SIZE GUIDE (not for trees) -->\n<section class="section container" aria-labelledby="sizeTitle" hidden>')

# ---------------------------------------------------------------- 1 · the initiative banner (replaces the headline above the photo)
rep("""<section class="hero container" aria-labelledby="hTitle">
  <h1 class="hero__h" id="hTitle"></h1>
  <div class="hero__media">""", """<section class="plant container" aria-labelledby="hTitle">
  <div class="plant__card">
    <div class="plant__copy">
      <p class="plant__ey"><span data-t="pEy"></span></p>
      <h1 class="hero__h plant__h" id="hTitle"></h1>
      <p class="plant__sub" data-t="pSub"></p>
      <div class="plant__btns">
        <button class="btn btn-primary" type="button" id="pMore"><span data-t="pMore"></span><span class="arr flip" id="pMoreArr"></span></button>
        <a class="plant__shop" href="#all" data-t="pShop"></a>
      </div>
    </div>
    <div class="plant__art" aria-hidden="true">
      <span class="plant__sun"></span>
      <img class="plant__woman" src="media/trees/ill-woman.webp" alt="" width="452" height="1050">
      <span class="plant__soil"><img class="plant__sprout" src="media/trees/ill-sprout.webp" alt="" width="383" height="372"></span>
      <i class="plant__leaf"></i><i class="plant__leaf"></i><i class="plant__leaf"></i>
    </div>
  </div>
</section>

<!-- the "we plant" strip: words and photos in pills -->
<section class="container weplant" aria-hidden="true">
  <div class="wp" id="wp">
    <span class="wp__p wp__p--w" data-t="w1"></span>
    <span class="wp__p wp__p--ph"><img src="media/trees/leaf-bamboo.webp" alt=""><b data-t="w2"></b></span>
    <span class="wp__p wp__p--y"><i class="flip" id="wpArr"></i></span>
    <span class="wp__p wp__p--ph"><img src="media/trees/diriyah.webp" alt=""><b data-t="w3"></b></span>
  </div>
</section>

<section class="hero container" aria-label="ket">
  <div class="hero__media">""")

# the headline: words rise and the pills pop, as on the live store
s = re.sub(r"  \$\('#hTitle'\)\.innerHTML = `.*?`;\n",
           "  $('#hTitle').innerHTML = `${W(t('hLine1'))} <span class=\"w hero__pill is-cut\"><img src=\"${img('ill-sprout')}\" alt=\"\"></span> <span class=\"hero__pink\">${W(t('hPink'))}</span> <span class=\"w hero__mark\">${t('hMark')}</span> <span class=\"w hero__pill hero__pill--p\"><img src=\"${img('leaf-fig')}\" alt=\"\"></span> ${W(t('hSub'))} <span class=\"w\">🇸🇦</span>`;\n",
           s, count=1, flags=re.S)

# ---------------------------------------------------------------- the initiative page (opens from the banner)
rep('<div class="toast" id="toast" role="status" aria-live="polite"></div>', """<div class="toast" id="toast" role="status" aria-live="polite"></div>

<!-- THE INITIATIVE: opens from the banner; the button takes the customer down to the trees -->
<dialog class="green" id="green" aria-labelledby="gH">
  <div class="green__in" data-lenis-prevent>
    <button class="icon-btn green__x" type="button" id="gClose" data-t-aria="gClose"></button>
    <div class="green__ph"><img src="media/trees/diriyah.webp" alt="" loading="lazy"><span class="green__sprout"><img src="media/trees/ill-sprout.webp" alt=""></span></div>
    <div class="green__copy">
      <p class="plant__ey"><span data-t="pEy"></span></p>
      <h2 id="gH" data-t="gH"></h2>
      <p class="green__lead" data-t="gP1"></p>
      <p data-t="gP2"></p>
      <p class="green__quote" data-t="gP3"></p>
      <p data-t="gP4"></p>
      <button class="btn btn-green" type="button" id="gGo"><span data-t="gBtn"></span><span class="arr flip" id="gArr"></span></button>
    </div>
  </div>
</dialog>""")

# ---------------------------------------------------------------- loader: the dots, then the watering card, then the section
rep("""  <p class="loader__line" id="ldLine" data-t="loadLine"></p>
  <div class="ring" id="ring"></div>
  <div class="loader__logo" id="ldLogo"></div>""", """  <div class="wcard" id="wcard">
    <img src="media/trees/ill-water.webp" alt="" width="820" height="1278">
    <div class="wcard__copy"><h2 id="ldH" data-t="ldH"></h2><p id="ldTx" data-t="ldTx"></p></div>
    <span class="wcard__drops" id="wDrops"></span>
    <span class="wcard__spark"></span><span class="wcard__spark"></span><span class="wcard__spark"></span>
  </div>""")
i = s.index("  // ring of 8 tables in mixed shapes on pink and grey")
j = s.index("  let started = false;")
s = s[:i] + """  // the watering card: it rises in, the words come up, the water falls on the plant, then it opens onto the section
  $('#wDrops').innerHTML = Array.from({ length: 14 }, (_, k) => `<i style="--x:${(6 + (k * 37) % 30)}%;--y:${(52 + (k * 13) % 22)}%;--d:${(k * .17).toFixed(2)}s"></i>`).join('');
  let skipped = false;
  const tl = gsap.timeline({ onComplete: finish });
  tl.to('#ldDots', { opacity: 0, scale: .6, duration: .35, delay: .6 })
    .fromTo('#wcard', { opacity: 0, y: 60, scale: .86, rotate: -3 }, { opacity: 1, y: 0, scale: 1, rotate: 0, duration: 1, ease: 'expo.out' }, '-=.05')
    .from('#ldH', { y: 30, opacity: 0, duration: .7, ease: 'expo.out' }, '-=.55')
    .from('#ldTx', { y: 20, opacity: 0, duration: .7, ease: 'expo.out' }, '-=.5')
    .add(() => $('#wcard').classList.add('is-on'), '-=.6')
    .to('#wcard', { y: -6, duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 1 })
    .addLabel('out')
    .to('#wcard', { scale: 1.12, opacity: 0, y: -40, duration: .7, ease: 'power3.in' }, 'out')
    .to(ldr, { opacity: 0, duration: .45 }, 'out+=.45')
    .add(() => { if (!skipped) bannerStart(); }, 'out+=.2');
""" + s[j:]
rep("$('#ldLogo').innerHTML = logo(140);\n", "")
rep("  function finish() { gsap.ticker.remove(place); ldr.remove(); bannerStart(); }", "  function finish() { ldr.remove(); bannerStart(); }")
rep("  addEventListener('resize', () => ({ R, ts } = geo(), ring.style.setProperty('--ts', ts + 'px')));\n", "")
rep("""  // wait until the ring images are decoded (max 1.2s) so the tiles never pop in empty
  tl.pause();
  const ready = Promise.all($$('img', ring).map(i => i.decode().catch(() => {})));""", """  // wait until the card is decoded (max 1.2s) so it never pops in empty
  tl.pause();
  const ready = Promise.all($$('img', $('#wcard')).map(i => i.decode().catch(() => {})));""")
rep("try { seen = !!sessionStorage.getItem('ketCatSeen'); sessionStorage.setItem('ketCatSeen', '1'); } catch (e) {}",
    "try { seen = !!sessionStorage.getItem('ketTreesSeen'); sessionStorage.setItem('ketTreesSeen', '1'); } catch (e) {}")

# ---------------------------------------------------------------- banner, strip and page motion + wiring
rep("/* ---------------- loader ---------------- */", """/* ---------------- the initiative: banner art, the strip, the page ---------------- */
$('#pMoreArr').innerHTML = icon('arrow', 18, 2); $('#gArr').innerHTML = icon('arrow', 18, 2); $('#wpArr').innerHTML = icon('arrow', 40, 1.6); $('#gClose').innerHTML = icon('close', 22);
const green = $('#green');
const openGreen = () => { green.showModal(); if (lenis) lenis.stop(); if (G) { gsap.fromTo('.green__in', { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: .7, ease: 'expo.out' }); gsap.fromTo('.green__copy > *', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .7, stagger: .06, delay: .15, ease: 'expo.out' }); gsap.fromTo('.green__sprout', { scaleY: 0 }, { scaleY: 1, duration: 1.1, delay: .35, ease: 'elastic.out(1,.6)' }); } };
const closeGreen = () => { green.close(); if (lenis) lenis.start(); };
$('#pMore').onclick = openGreen;
$('#gClose').onclick = closeGreen;
green.addEventListener('click', e => { if (e.target === green) closeGreen(); });
green.addEventListener('cancel', () => { if (lenis) lenis.start(); });
$('#gGo').onclick = () => { closeGreen(); setFilter({ type: 'all', col: null }); setTimeout(goGrid, 60); };
function plantIn() {
  if (!G) return;
  gsap.timeline()
    .from('.plant__card', { clipPath: 'inset(10% 6% 0% 6% round 60px)', duration: 1.4, ease: 'expo.out' }, 0)
    .from('.plant__ey, .plant__sub, .plant__btns', { y: 24, opacity: 0, duration: .9, stagger: .08, ease: 'expo.out' }, .55)
    .from('.plant__woman', { y: 60, opacity: 0, duration: 1.1, ease: 'expo.out' }, .3)
    .from('.plant__soil', { scaleX: .2, opacity: 0, duration: .7, ease: 'back.out(2)' }, .7)
    .from('.plant__sprout', { scaleY: 0, duration: 1.4, ease: 'elastic.out(1,.55)' }, .95)
    .from('.plant__sun', { scale: 0, duration: 1.2, ease: 'expo.out' }, .4);
  gsap.from('.wp__p', { y: 50, opacity: 0, scale: .9, duration: .9, stagger: .09, ease: 'back.out(1.6)', scrollTrigger: { trigger: '#wp', start: 'top 88%' } });
}

/* ---------------- loader ---------------- */""")
rep("  scrollMotion(); bannerIn();", "  scrollMotion(); bannerIn(); plantIn();")
rep(".from('#hTitle .w:not(.hero__pill)', { y: 26, opacity: 0, duration: .9, stagger: .035, ease: 'expo.out' }, 0)",
    ".from('#hTitle .w:not(.hero__pill)', { y: 26, opacity: 0, duration: .9, stagger: .05, ease: 'expo.out' }, .45)")
rep(".from('#hTitle .hero__pill', { scale: 0, duration: .9, stagger: .15, ease: 'back.out(1.8)' }, .3)",
    ".from('#hTitle .hero__pill', { scale: 0, duration: .9, stagger: .15, ease: 'back.out(1.8)' }, .8)\n    .from('#hTitle .hero__mark', { '--ms': 0, duration: .8, ease: 'expo.out' }, 1)")

# ---------------------------------------------------------------- styles for the new parts
rep("/* ===================== ANNOUNCEMENT + HEADER ===================== */", """/* ===================== TREES: watering loader ===================== */
.loader{ background:var(--white); }
.wcard{ position:relative; width:min(78vw, 400px); aspect-ratio:820 / 1278; border-radius:34px; overflow:hidden; background:#FDFBA4; box-shadow:0 40px 80px -30px rgba(80,80,0,.35); opacity:0; }
.wcard > img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
.wcard__copy{ position:absolute; inset-inline:8%; top:7%; display:grid; gap:8px; text-align:start; }
.wcard__copy h2{ font-size:clamp(26px, 7vw, 38px); font-weight:700; line-height:1.2; letter-spacing:-.02em; }
.wcard__copy p{ font-size:clamp(12.5px, 3.3vw, 15px); font-weight:600; line-height:1.5; max-width:30ch; }
html[dir="rtl"] .wcard__copy{ text-align:right; }
.wcard__drops i{ position:absolute; left:var(--x); top:var(--y); width:6px; height:9px; border-radius:50% 50% 50% 50% / 60% 60% 40% 40%; background:#2F6BFF; opacity:0; }
.wcard.is-on .wcard__drops i{ animation:drop 1.1s var(--d) ease-in infinite; }
@keyframes drop{ 0%{ opacity:0; transform:translateY(-10px) scale(.6); } 25%{ opacity:.9; } 100%{ opacity:0; transform:translateY(60px) scale(1); } }
.wcard__spark{ position:absolute; width:10px; height:10px; border-radius:50%; background:var(--lime); box-shadow:0 0 0 6px rgba(196,245,164,.35); opacity:0; }
.wcard__spark:nth-of-type(1){ left:24%; bottom:22%; } .wcard__spark:nth-of-type(2){ left:42%; bottom:30%; } .wcard__spark:nth-of-type(3){ left:14%; bottom:34%; }
.wcard.is-on .wcard__spark{ animation:spark 1.6s ease-in-out infinite; } .wcard.is-on .wcard__spark:nth-of-type(2){ animation-delay:.5s; } .wcard.is-on .wcard__spark:nth-of-type(3){ animation-delay:1s; }
@keyframes spark{ 0%,100%{ opacity:0; transform:scale(.4); } 50%{ opacity:1; transform:scale(1); } }

/* ===================== TREES: the initiative banner ===================== */
.plant{ padding-top:clamp(16px, 2.4vw, 32px); }
.plant__card{ position:relative; display:grid; overflow:hidden; isolation:isolate; border-radius:clamp(30px, 4vw, 60px); background:var(--yellow); min-height:min(78svh, 720px); }
@media (min-width:900px){ .plant__card{ grid-template-columns:1.1fr .9fr; align-items:center; } }
.plant__copy{ position:relative; z-index:2; display:grid; justify-items:start; gap:clamp(14px, 1.8vw, 22px); padding:clamp(26px, 5vw, 72px); }
.plant__ey{ display:inline-flex; align-items:center; gap:8px; height:34px; padding-inline:8px 14px; border-radius:var(--r-pill); background:var(--white); font-size:13px; font-weight:700; }
.plant__ey::before{ content:"🇸🇦"; font-size:16px; }
.plant__h.hero__h{ max-width:14ch; margin:0; text-align:start; font-size:clamp(36px, 5.4vw, 80px); line-height:1.15; }
html[lang="ar"] .plant__h.hero__h{ line-height:1.5; max-width:13ch; }
.plant__h .hero__pill{ background:var(--white); }
.plant__h .hero__pill--p{ background:var(--lime); }
.plant__h .hero__mark{ --ms:1; }
.plant__h .hero__mark::before{ background:var(--lime); transform:scaleX(var(--ms)); }
.plant__sub{ font-size:clamp(16px, 1.5vw, 20px); font-weight:500; line-height:1.7; max-width:34ch; }
.plant__btns{ display:flex; flex-wrap:wrap; align-items:center; gap:10px 18px; }
.plant__shop{ font-weight:700; font-size:15px; text-decoration:underline; text-underline-offset:5px; text-decoration-thickness:2px; }
.plant__art{ position:relative; height:100%; min-height:clamp(380px, 52vw, 640px); }
.plant__sun{ position:absolute; z-index:-1; width:72%; aspect-ratio:1; border-radius:50%; background:var(--lime); left:50%; top:46%; translate:-50% -50%; opacity:.9; }
.plant__woman{ position:absolute; bottom:4%; inset-inline-start:14%; height:92%; width:auto; max-width:none; animation:sway 6s ease-in-out infinite; transform-origin:50% 100%; }
html[dir="rtl"] .plant__woman{ inset-inline-start:auto; inset-inline-end:34%; }
.plant__soil{ position:absolute; bottom:5%; inset-inline-end:8%; width:34%; transform-origin:50% 100%; }
html[dir="rtl"] .plant__soil{ inset-inline-end:auto; inset-inline-start:6%; }
.plant__sprout{ display:block; width:100%; height:auto; transform-origin:50% 92%; animation:breeze 4.5s ease-in-out infinite; }
@keyframes sway{ 0%,100%{ transform:rotate(0); } 50%{ transform:rotate(-1.2deg); } }
@keyframes breeze{ 0%,100%{ rotate:0deg; } 50%{ rotate:3deg; } }
.plant__leaf{ position:absolute; width:16px; height:10px; border-radius:100% 0; background:#2E9F4D; opacity:0; animation:leaf 7s linear infinite; }
.plant__leaf:nth-of-type(1){ left:60%; top:10%; } .plant__leaf:nth-of-type(2){ left:78%; top:4%; animation-delay:2.3s; } .plant__leaf:nth-of-type(3){ left:40%; top:0; animation-delay:4.6s; }
@keyframes leaf{ 0%{ opacity:0; transform:translate(0, 0) rotate(0); } 10%{ opacity:.9; } 100%{ opacity:0; transform:translate(-60px, 360px) rotate(320deg); } }
@media (max-width:899px){
  .plant__card{ min-height:0; }
  .plant__copy{ padding-bottom:0; }
  .plant__art{ min-height:340px; }
  .plant__woman{ height:96%; }
}

/* the "we plant" strip */
.weplant{ padding-top:clamp(28px, 4vw, 56px); }
.wp{ display:grid; grid-template-columns:1fr 1.25fr .9fr 1.25fr; gap:clamp(6px, 1vw, 14px); }
.wp__p{ position:relative; display:grid; place-items:center; height:clamp(74px, 12vw, 170px); border-radius:999px; overflow:hidden; font-size:clamp(20px, 3.6vw, 52px); font-weight:700; letter-spacing:-.02em; }
.wp__p--w{ background:var(--g100); }
.wp__p--y{ background:var(--yellow); }
.wp__p--y svg{ width:clamp(26px, 4vw, 52px); height:auto; }
.wp__p--ph img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
.wp__p--ph b{ position:relative; color:var(--white); text-shadow:0 2px 16px rgba(0,0,0,.35); }
@media (max-width:640px){ .wp{ grid-template-columns:1fr 1fr; } .wp__p{ height:86px; font-size:24px; } }

/* the hero photo: the sofa (portrait): her face stays in view on wide screens */
.hero__card > img{ object-position:60% 22%; }
@media (max-width:767px){ .hero__card > img{ object-position:50% 40%; } }

/* ===================== TREES: the initiative page ===================== */
.green{ width:min(100%, 980px); max-width:none; max-height:none; height:auto; margin:auto; padding:0; border:0; background:none; overflow:visible; }
.green::backdrop{ background:rgba(20,22,0,.45); -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px); }
.green__in{ position:relative; display:grid; max-height:calc(100svh - 32px); overflow:auto; margin:16px; border-radius:32px; background:var(--yellow-l); color:var(--black); }
@media (min-width:860px){ .green__in{ grid-template-columns:.9fr 1.1fr; } }
.green__x{ position:absolute; z-index:3; top:12px; inset-inline-end:12px; background:var(--white); }
.green__ph{ position:relative; min-height:260px; }
.green__ph > img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
.green__sprout{ position:absolute; bottom:-6px; inset-inline-start:8%; width:34%; transform-origin:50% 100%; }
.green__sprout img{ width:100%; height:auto; display:block; }
.green__copy{ display:grid; gap:14px; align-content:start; padding:clamp(22px, 4vw, 48px); }
.green__copy .plant__ey{ justify-self:start; background:var(--yellow); }
.green__copy h2{ font-size:clamp(26px, 3.2vw, 40px); font-weight:700; line-height:1.35; }
.green__copy p{ font-size:15.5px; line-height:1.85; }
.green__lead{ font-weight:700; font-size:17px!important; }
.green__quote{ padding:12px 16px; border-radius:16px; background:var(--lime); font-weight:700; }
.btn-green{ justify-self:start; background:var(--forest); color:var(--white); margin-top:6px; }
.btn-green .arr{ background:var(--yellow); }

/* ===================== ANNOUNCEMENT + HEADER ===================== */""")

open('ket-trees.html', 'w').write(s)
print('wrote ket-trees.html', len(s))
