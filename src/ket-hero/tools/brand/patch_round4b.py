"""Round 4b: the walking gazelle (built and animated in Blender, see README) for the buy box and the
dimensions; text above the gazelles gets a white letter outline instead of a soft cloud (client: no cloud)."""
import sys
path = sys.argv[1]; s = open(path, encoding='utf-8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:90]); s = s.replace(old, new)

rep("""padding:22px 26px; margin:-22px -26px; background:radial-gradient(closest-side, rgba(255,255,255,.96) 55%, rgba(255,255,255,.75) 75%, rgba(255,255,255,0)); width:max-content;""",
    """width:max-content;""")
rep("""text-shadow:0 0 2px #fff, 0 0 4px #fff, 0 0 8px #fff, 0 0 12px #fff, 0 0 18px #fff, 0 0 26px #fff, 0 0 34px #fff, 0 0 44px #fff; opacity:0; transform:translateY(12px) scale(.55);""",
    """-webkit-text-stroke:7px #fff; paint-order:stroke fill; text-shadow:0 0 6px #fff, 0 0 12px #fff; opacity:0; transform:translateY(12px) scale(.55);""")
rep(""".gzv--l .gzv__say{ left:10%; transform-origin:25% 100%; } .gzv--r .gzv__say{ right:10%; transform-origin:75% 100%; }
.gzv.is-talk .gzv__say{ opacity:1; transform:none; }""",
""".gzv--l .gzv__say{ left:10%; transform-origin:25% 100%; } .gzv--r .gzv__say{ right:10%; transform-origin:75% 100%; }
.gzv.is-talk .gzv__say, .gzw.is-talk .gzv__say{ opacity:1; transform:none; }
.gzv__say small{ -webkit-text-stroke-width:5px; }
/* Walking gazelle (Blender: walk + idle loops on white; multiply removes the white) */
.gzw{ position:fixed; bottom:0; z-index:57; width:var(--gw,150px); pointer-events:none; visibility:hidden; mix-blend-mode:multiply; will-change:transform; }
.gzw.is-on{ visibility:visible; }
.gzw--l{ left:0; } .gzw--r{ right:0; }
.gzw--txt{ mix-blend-mode:normal; height:calc(var(--gw,150px) * 1.222); }
body.bar-on .gzw{ bottom:calc(66px + env(safe-area-inset-bottom)); }
.gzw__m{ position:relative; aspect-ratio:360/440; }
.gzw__m video, .gzw__m img{ position:absolute; inset:0; width:100%; height:100%; display:block; background:#fff; }
.gzw__walk{ opacity:0; } .gzw.is-walk .gzw__walk{ opacity:1; } .gzw.is-walk .gzw__idle{ opacity:0; }
.gzw--r .gzw__m, .gzw--l.is-back .gzw__m{ transform:scaleX(-1); } .gzw--r.is-back .gzw__m{ transform:none; }
.gzw--l .gzv__say{ left:18%; transform-origin:25% 100%; } .gzw--r .gzv__say{ right:18%; transform-origin:75% 100%; }""")
rep("""@media (max-width:639px){ .gzv .gzv__say small{ display:none; } }""", """@media (max-width:639px){ .gzv .gzv__say small, .gzw .gzv__say small{ display:none; } }""")

rep("""const GV = gazellePeek();
""", r"""const GV = gazellePeek();

/* WALKING GAZELLE — modelled and animated in Blender (src/ket-hero/assets-src/mascot/3d): a 2 s walk loop and a
   2 s idle loop (head tilt, ear flick, tail wag, blink). It walks in from a screen edge, stops, says its line,
   then turns round and walks back out. The CSS move matches the stride so the hooves don't skate. */
function gazelleWalk() {
  const mk = c => { const e = document.createElement('div'); e.className = c; e.setAttribute('aria-hidden', 'true'); return e; };
  const box = mk('gzw'), tb = mk('gzw gzw--txt'), els = [box, tb];
  box.innerHTML = '<div class="gzw__m"><video class="gzw__idle" muted playsinline loop preload="none" disablepictureinpicture></video><video class="gzw__walk" muted playsinline loop preload="none" disablepictureinpicture></video><img class="gzw__still" alt="" hidden></div>';
  tb.innerHTML = '<div class="gzv__say" role="status"></div>';
  document.body.append(box, tb);
  const walk = $('.gzw__walk', box), idle = $('.gzw__idle', box), still = $('img', box), say = $('.gzv__say', tb);
  walk.muted = idle.muted = true;
  const ext = walk.canPlayType('video/mp4; codecs="avc1.42E01E"') ? 'mp4' : 'webm';
  let loaded = false, on = false, timers = [], done = null;
  const load = () => { if (loaded) return; loaded = true; walk.src = `media/gazelle-walk.${ext}`; idle.src = `media/gazelle-idle.${ext}`; walk.preload = idle.preload = 'auto'; };
  if (document.readyState === 'complete') setTimeout(load, 3000); else addEventListener('load', () => setTimeout(load, 3000), { once: true });
  const at = (ms, fn) => timers.push(setTimeout(fn, ms));
  const cls = (fn, ...c) => els.forEach(e => e.classList[fn](...c));
  const move = (x, ms) => els.forEach(e => { e.style.transition = ms ? `transform ${ms}ms linear` : 'none'; e.style.transform = `translateX(${x}px)`; });
  const pl = v => { try { v.currentTime = 0; } catch (e) { /* not seekable yet */ } const p = v.play(); p && p.catch && p.catch(() => {}); };
  function stop() {
    timers.forEach(clearTimeout); timers = [];
    cls('remove', 'is-on', 'is-talk', 'is-back', 'is-walk'); move(0, 0);
    walk.pause(); idle.pause(); document.body.classList.remove('kg-hi'); on = false;
    const d = done; done = null; d && d();
  }
  function play({ side = 'l', line = '', small = '', link = null, onDone = null } = {}) {
    if (on) stop();
    on = true; done = onDone; load();
    const W = innerWidth < 640 ? 140 : 190, dir = side === 'l' ? 1 : -1;
    els.forEach((e, i) => { e.style.setProperty('--gw', W + 'px'); e.className = `gzw gzw--${side}${i ? ' gzw--txt' : ''}`; });
    say.innerHTML = `${line ? `<b>${line}</b>` : ''}${small ? `<small>${small}</small>` : ''}${link ? `<a href="${link.href}" target="_blank" rel="noopener">${link.label}</a>` : ''}`;
    document.body.classList.add('kg-hi');
    const off = -dir * (W + 24), inX = dir * 6;
    const speed = 160 * W / 360;                              // px/s: one stride of the rendered walk, at this size
    const tIn = Math.round(Math.abs(inX - off) / speed * 1000);
    move(off, 0);
    if (reduce) {
      still.src = 'media/gazelle-idle.webp'; still.hidden = false; move(inX, 0); cls('add', 'is-on', 'is-talk');
      at(6000, () => cls('remove', 'is-on')); at(6300, stop); return;
    }
    still.hidden = true;
    const go = () => {
      if (!on) return;
      pl(walk); box.classList.add('is-walk');
      requestAnimationFrame(() => requestAnimationFrame(() => { cls('add', 'is-on'); move(inX, tIn); }));
      at(tIn, () => { pl(idle); box.classList.remove('is-walk'); walk.pause(); cls('add', 'is-talk'); });
      const back = tIn + 5400;
      at(back, () => { cls('remove', 'is-talk'); cls('add', 'is-back'); box.classList.add('is-walk'); pl(walk); idle.pause(); move(off, tIn); });
      at(back + tIn + 80, stop);
    };
    const t0 = Date.now();
    const wait = () => (walk.readyState >= 3 && idle.readyState >= 2) ? go()
      : Date.now() - t0 > 6000 ? stop() : setTimeout(wait, 120);
    wait();
  }
  return { play, stop, busy: () => on };
}
const GW = gazelleWalk();
""")
rep("""  { id: 'buy', zone: '#buy', after: 6, video: 'end', say: ['peekBuyT', 'peekBuyS'], act: 'wa' },""",
    """  { id: 'buy', zone: '#buy', after: 6, walk: 'end', say: ['peekBuyT', 'peekBuyS'], act: 'wa' },""")
rep("""  { id: 'dims', zone: '#dimensions', after: 2.5, rig: 'hey-yellow', mode: 'bottom', say: 'peekDims' },""",
    """  { id: 'dims', zone: '#dimensions', after: 2.5, walk: 'start', say: ['peekDimsT', 'peekDimsS'] },""")
rep("""document.hidden || GV.busy();""", """document.hidden || GV.busy() || GW.busy();""")
rep("""  if (p.video) {   // the client's peeking gazelle""", """  if (p.walk) {    // the Blender gazelle walks in from 'end' (away from WhatsApp) or 'start'
    const n = P.reviewCount, rtl = root.dir === 'rtl';
    const side = p.walk === 'end' ? (rtl ? 'l' : 'r') : (rtl ? 'r' : 'l');
    GW.play({ side, line: esc(t(p.say[0], { n })), small: esc(t(p.say[1], { n })),
      link: p.act === 'wa' && STORE.whatsapp ? { href: $('#wa').href, label: esc(t('peekWa')) } : null,
      onDone: () => { if (peekNow === p) peekNow = null; } });
    return;
  }
  if (p.video) {   // the client's peeking gazelle""")
rep("""if (peekNow && peekNow.zone && !peekNow.video) {""", """if (peekNow && peekNow.zone && !peekNow.video && !peekNow.walk) {""")
open(path, 'w', encoding='utf-8').write(s); print('ok')
