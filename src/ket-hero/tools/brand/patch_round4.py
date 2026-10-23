"""Round 4 clean-up for ket-product.html (one-off patch, kept for reference):
 - gazelle: drop the hand-built walkers and the traced rig; the peeking gazelle is now the client's own
   animation (their "hello" video, trimmed before the speech bubble, media/gazelle-peek.mp4)
 - header smile no longer clipped when scrolled
 - inspiration section laid out properly; footer payment marks tidied; stray green blob removed
Usage: python3 patch_round4.py <ket-product.html>
"""
import sys, re

path = sys.argv[1]
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


# ============================================================ gazelle: client's animation replaces the walkers
a = s.index('/*ARHAB*/const ARHAB = ')
b = s.index('\n', s.index('const KG = KetGazelle(')) + 1
s = s[:a] + r"""/* ---------------------------------------------------------------------------------------------
   PEEKING GAZELLE — the client's own animation (their "hello" video, trimmed before the speech
   bubble): it slides out from behind a screen edge, looks around, blinks, then smiles and talks.
   Muted + inline so it can autoplay; mix-blend multiply makes its white background disappear.
   --------------------------------------------------------------------------------------------- */
function gazellePeek() {
  const SRC = 'media/gazelle-peek.mp4', STILL = 'media/gazelle-peek-end.webp';
  const box = document.createElement('div'); box.className = 'gzv'; box.setAttribute('aria-hidden', 'true');
  box.innerHTML = '<video class="gzv__v" muted playsinline preload="none" disablepictureinpicture></video><img class="gzv__still" alt="" hidden><div class="gzv__say" role="status"></div>';
  document.body.appendChild(box);
  const v = $('video', box), still = $('img', box), say = $('.gzv__say', box);
  v.muted = true;
  let on = false, loaded = false, timers = [], done = null;
  const load = () => { if (loaded) return; loaded = true; v.src = SRC; v.preload = 'auto'; v.load(); };
  if (document.readyState === 'complete') setTimeout(load, 2500); else addEventListener('load', () => setTimeout(load, 2500), { once: true });
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  function stop() {
    timers.forEach(clearTimeout); timers = [];
    box.className = 'gzv'; document.body.classList.remove('kg-hi'); v.pause(); on = false;
    const d = done; done = null; d && d();
  }
  function showStill() {
    v.hidden = true; still.src = STILL; still.hidden = false;
    requestAnimationFrame(() => box.classList.add('is-on', 'is-talk'));
    at(6500, () => box.classList.add('is-out')); at(7200, stop);
  }
  function play({ side = 'l', line = '', small = '', link = null, onDone = null } = {}) {
    if (on) stop();
    on = true; done = onDone; load();
    box.style.setProperty('--gw', (innerWidth < 640 ? 186 : 236) + 'px');
    say.innerHTML = `${line ? `<b>${line}</b>` : ''}${small ? `<small>${small}</small>` : ''}${link ? `<a href="${link.href}" target="_blank" rel="noopener">${link.label}</a>` : ''}`;
    box.className = `gzv gzv--${side}`;
    document.body.classList.add('kg-hi');            // the WhatsApp button steps aside while it plays
    if (reduce) { showStill(); return; }
    still.hidden = true; v.hidden = false;
    const go = () => {
      if (!on) return;
      try { v.currentTime = 0; } catch (e) { /* not seekable yet */ }
      const p = v.play();
      const started = () => {
        requestAnimationFrame(() => box.classList.add('is-on'));
        at(4100, () => box.classList.add('is-talk'));   // the happy face: time to say the line
        at(7700, () => box.classList.remove('is-talk'));
        at(8000, () => box.classList.add('is-out'));
        at(8700, stop);
      };
      if (p && p.then) p.then(started).catch(showStill); else started();
    };
    if (v.readyState >= 3) go();
    else { const t0 = Date.now(); const wait = () => (v.readyState >= 3 || Date.now() - t0 > 5000) ? (v.readyState >= 2 ? go() : showStill()) : setTimeout(wait, 120); wait(); }
  }
  return { play, stop, busy: () => on };
}
const GV = gazellePeek();
""" + s[b:]

rex(r"const PEEKS = \[\n.*?\n\];\n",
    """const PEEKS = [
  { id: 'buy', zone: '#buy', after: 6, video: 'end', say: ['peekBuyT', 'peekBuyS'], act: 'wa' },
  { id: 'ship', zone: '#info', after: 2.5, rig: 'hey-pink-paws', mode: 'bottom', say: 'peekShip' },
  { id: 'dims', zone: '#dimensions', after: 2.5, rig: 'hey-yellow', mode: 'bottom', say: 'peekDims' },
  { id: 'rev', zone: '#reviews', after: 2.5, video: 'start', say: ['peekRevT', 'peekRevS'] }
];
""")
rep("""const PEEK_HI = { id: 'hi' };                                                                     // a bit later: the ارحبوووو peek (KG.welcome)""",
    """const PEEK_HI = { id: 'hi' };                                                                     // a bit later: the ارحبوووو peek from the left edge""")
rep("""const peekBusy = () => drawer.classList.contains('is-open') || lb.classList.contains('is-open') || document.hidden || KG.busy();""",
    """const peekBusy = () => drawer.classList.contains('is-open') || lb.classList.contains('is-open') || document.hidden || GV.busy();""")
rex(r"  if \(p\.walker\) \{   // a whole gazelle walks / hops in, says its line above itself, then leaves\n.*?\n    return;\n  \}\n",
    """  if (p.video) {   // the client's peeking gazelle; 'end' = the edge away from the WhatsApp button, 'start' = the other one
    const n = P.reviewCount, rtl = root.dir === 'rtl';
    const side = p.video === 'end' ? (rtl ? 'l' : 'r') : (rtl ? 'r' : 'l');
    GV.play({ side, line: esc(t(p.say[0], { n })), small: esc(t(p.say[1], { n })),
      link: p.act === 'wa' && STORE.whatsapp ? { href: $('#wa').href, label: esc(t('peekWa')) } : null,
      onDone: () => { if (peekNow === p) peekNow = null; } });
    return;
  }
""")
rep("""  if (peekNow && peekNow.zone && !peekNow.walker) {""", """  if (peekNow && peekNow.zone && !peekNow.video) {""")
rex(r"peekNow = PEEK_HI; peekLast = Date\.now\(\); KG\.welcome\(\); \};",
    "peekNow = PEEK_HI; peekLast = Date.now(); GV.play({ side: 'l', line: esc(t('arhab')), onDone: () => { if (peekNow === PEEK_HI) peekNow = null; } }); };")
assert 'KG.' not in s and 'KetGazelle' not in s, 'old engine still referenced'

# styles for the peek (the old engine injected its own; this replaces them)
rep("""/* Decoration inspiration */""", """/* Peeking gazelle (client's animation) */
.gzv{ position:fixed; bottom:0; z-index:57; width:var(--gw,186px); pointer-events:none; opacity:0; visibility:hidden;
  transition:opacity .25s, transform .7s cubic-bezier(.55,0,.75,.2), visibility 0s .7s; }
.gzv.is-on{ opacity:1; visibility:visible; transition:opacity .25s, transform .7s cubic-bezier(.55,0,.75,.2); }
.gzv--l{ left:0; } .gzv--r{ right:0; }
.gzv--r .gzv__v, .gzv--r .gzv__still{ transform:scaleX(-1); }
.gzv--l.is-out{ transform:translateX(-106%); } .gzv--r.is-out{ transform:translateX(106%); }
.gzv__v, .gzv__still{ display:block; width:100%; height:auto; mix-blend-mode:multiply; background:#fff; }
body.bar-on .gzv{ bottom:calc(66px + env(safe-area-inset-bottom)); }
.gzv__say{ position:absolute; bottom:95%; width:max-content; max-width:min(250px, 66vw); font:700 26px/1.15 'Marhey', var(--f-ar); color:#111;
  text-shadow:0 0 3px #fff, 0 0 6px #fff, 0 0 10px #fff; opacity:0; transform:translateY(12px) scale(.55); transition:opacity .25s, transform .55s cubic-bezier(.34,1.56,.64,1); pointer-events:auto; }
.gzv--l .gzv__say{ left:10%; transform-origin:25% 100%; } .gzv--r .gzv__say{ right:10%; transform-origin:75% 100%; }
.gzv.is-talk .gzv__say{ opacity:1; transform:none; }
.gzv__say b{ display:block; font-weight:700; }
.gzv__say small{ display:block; font:600 14px/1.45 var(--f-ar); margin-top:4px; white-space:normal; }
.gzv__say a{ display:inline-flex; margin-top:8px; height:32px; align-items:center; padding-inline:14px; border-radius:var(--r-pill); background:#111; color:#fff; text-decoration:none; text-shadow:none; font:600 13px var(--f-ar); }
.wa{ transition:opacity .3s; } body.kg-hi .wa{ opacity:0; pointer-events:none; }
@media (prefers-reduced-motion: reduce){ .gzv, .gzv__say{ transition:opacity .2s!important; } .gzv--l.is-out, .gzv--r.is-out{ transform:none; opacity:0; } }

/* Decoration inspiration */""")

# ============================================================ header: the smile stays inside the bar
rep(""".header.is-scrolled .klogo .klogo__smile{ opacity:1; clip-path:inset(0 0 0 0); transform:translateY(-42%) scale(1.45); transition-delay:.18s; }""",
    """.header.is-scrolled .klogo .klogo__smile{ opacity:1; clip-path:inset(0 0 0 0); transform:translateY(-34%) scale(1.18); transition-delay:.18s; }""")

# ============================================================ inspiration: tidy grid
rex(r"\.insp__grid\{ display:grid; gap:var\(--s6\); align-items:center; \}\n@media \(min-width:1024px\)\{ \.insp__grid\{[^\n]*\n",
    """.insp__grid{ display:grid; gap:var(--s6); align-items:center; }
@media (min-width:1024px){ .insp__grid{ grid-template-columns:1fr 1fr; gap:clamp(40px,5vw,96px); } }
#inspTitle{ text-transform:none; }
""")
rep(""".insp__chips{ display:flex; flex-wrap:wrap; gap:10px; margin-top:var(--s5); }""",
    """.insp__chips{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:10px; margin-top:var(--s5); max-width:520px; }
@media (min-width:640px){ .insp__chips{ grid-template-columns:repeat(3, minmax(0,1fr)); } }""")
rex(r"\.insp__chip\{ height:54px; padding-inline:26px;", ".insp__chip{ justify-content:center; height:56px; padding-inline:16px;")
rep(""".insp__art{ margin:0; }""", """.insp__art{ margin:0; max-width:560px; justify-self:center; width:100%; }""")

# ============================================================ footer: proper mastercard mark, tidy grid on phones
rep("""<span class="pay pay--mc" aria-label="Mastercard"><b></b><b></b></span>""",
    """<span class="pay pay--mc" aria-label="Mastercard"><svg width="38" height="24" viewBox="0 0 38 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#111"/><circle cx="26" cy="12" r="11" fill="#111" fill-opacity=".55"/></svg></span>""")
rex(r"\.pay--mc\{ gap:0; \} \.pay--mc b\{[^\n]*\n", ".pay--mc svg{ display:block; }\n")
rep(""".pays{ direction:ltr; display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:14px 26px; max-width:520px; }""",
    """.pays{ direction:ltr; display:grid; grid-template-columns:repeat(4, auto); justify-content:center; justify-items:center; align-items:center; gap:16px 26px; }
@media (min-width:640px){ .pays{ display:flex; flex-wrap:wrap; gap:14px 30px; } }""")

# ============================================================ dimensions: drop the stray green arch
rep("""  $('#decoDims').innerHTML = SIL.arch('#02A27A');\n""", "")

open(path, 'w', encoding='utf-8').write(s)
print('patched', round(len(s) / 1e6, 3), 'MB')
