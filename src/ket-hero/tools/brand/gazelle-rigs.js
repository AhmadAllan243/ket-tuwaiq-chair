/* ket gazelle rigs — the client's "ارحبوووو" drawing cut into vector parts (rig_arhab.py), animated
   with a tiny requestAnimationFrame animator (no libraries).

   KetGazelle(ARHAB, { t, onDone }) returns:
     welcome()            paws grip the left edge, the head slides out, looks, blinks, says ارحبوووو
     walk(kind, text)     kind: 'walk' | 'hop' | 'sit' — a full gazelle walks / hops in along the bottom,
                          stops, talks (text above it, no bubble), then leaves
     busy()               true while one is on screen
     stop()               remove whatever is showing

   The page owns when these play; this file only draws and animates. All gazelles are black and white. */
function KetGazelle(A, opts = {}) {
  const t = opts.t || (k => k);
  const NS = 'http://www.w3.org/2000/svg';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const P = A.parts;
  const el = (tag, attrs = {}, kids = '') => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (kids) e.innerHTML = kids; return e; };
  const part = (name, cls = '') => `<g class="${cls}"><path fill="#fff" d="${P[name].fill}"/><path fill="#111" fill-rule="evenodd" d="${P[name].ink}"/></g>`;
  const inkOnly = name => `<path fill="#111" fill-rule="evenodd" d="${P[name].ink}"/>`;

  // ---- easing + tiny tween helpers ---------------------------------------------------------
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, k) => a + (b - a) * k;
  const E = {
    out: k => 1 - Math.pow(1 - k, 3),
    in: k => k * k * k,
    io: k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2,
    back: k => { const c = 1.7, c3 = c + 1; return 1 + c3 * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); },
    elastic: k => k === 0 || k === 1 ? k : Math.pow(2, -9 * k) * Math.sin((k * 10 - .75) * (2 * Math.PI) / 3.2) + 1,
  };
  // seg(time, start, dur, ease) -> 0..1 progress of a segment
  const seg = (tm, s, d, e = E.io) => e(clamp((tm - s) / d));
  const tf = (node, x = 0, y = 0, r = 0, ox = 0, oy = 0, sx = 1, sy = 1) =>
    node.setAttribute('transform', `translate(${x.toFixed(2)} ${y.toFixed(2)}) rotate(${r.toFixed(2)} ${ox} ${oy}) translate(${ox} ${oy}) scale(${sx.toFixed(3)} ${sy.toFixed(3)}) translate(${-ox} ${-oy})`);

  // ---- shared styles -------------------------------------------------------------------------
  if (!document.getElementById('kg-css')) document.head.insertAdjacentHTML('beforeend', `<style id="kg-css">
    .kg{ position:fixed; z-index:57; pointer-events:none; bottom:0; }
    .kg svg{ display:block; width:100%; height:auto; overflow:visible; }
    .kg__say{ position:absolute; white-space:nowrap; width:max-content; font:700 var(--kg-fs,30px)/1.1 'Marhey','IBM Plex Sans Arabic',sans-serif; color:#111;
      text-shadow:0 0 3px #fff,0 0 6px #fff,0 0 10px #fff; opacity:0; transform-origin:50% 100%; pointer-events:auto; }
    .kg__say small{ display:block; font:600 calc(var(--kg-fs,30px) * .5)/1.35 'IBM Plex Sans Arabic',sans-serif; white-space:normal; width:max-content; max-width:min(270px,72vw); margin-top:4px; }
    .kg__say a{ display:inline-flex; margin-top:8px; height:32px; align-items:center; padding-inline:14px; border-radius:99px; background:#111; color:#fff; text-decoration:none; font:600 13px 'IBM Plex Sans Arabic',sans-serif; text-shadow:none; }
    .kg__pole{ position:fixed; top:0; bottom:0; z-index:56; width:var(--kg-pw,3px); background:#111; transform-origin:50% 0; transform:scaleY(0); pointer-events:none; }
    body.bar-on .kg--walk{ bottom:calc(66px + env(safe-area-inset-bottom)); }
  </style>`);

  let live = null;   // the one rig on screen
  const busy = () => !!live;
  function stop() { if (!live) return; cancelAnimationFrame(live.raf); live.nodes.forEach(n => n.remove()); const d = live.done; live = null; d && d(); }
  function run(nodes, dur, frame, done) {
    const t0 = performance.now();
    live = { nodes, raf: 0, done };
    const tick = now => {
      if (!live || live.nodes !== nodes) return;
      const tm = (now - t0) / 1000;
      frame(tm);
      if (tm < dur) live.raf = requestAnimationFrame(tick); else stop();
    };
    live.raf = requestAnimationFrame(tick);
  }
  const sayHTML = (big, small, link) => `${big ? `<b>${big}</b>` : ''}${small ? `<small>${small}</small>` : ''}${link ? `<a href="${link.href}" target="_blank" rel="noopener">${link.label}</a>` : ''}`;

  // ---- face parts (shared by both rigs): eyes = lid arcs + pupils, mouth squashes to talk ----
  const PUP = [[355, 533, 25], [574, 664, 26]];   // pupil centres under the lid arcs (image px)
  const face = id => `
    <g class="kg-mouth">${inkOnly('mouth')}</g>
    <g class="kg-eyes">${inkOnly('eyeL')}${inkOnly('eyeR')}
      ${PUP.map(([x, y, r], i) => `<g class="kg-pup" data-i="${i}"><circle cx="${x}" cy="${y}" r="${r}" fill="#111"/><circle cx="${x + r * .38}" cy="${y - r * .34}" r="${r * .3}" fill="#fff"/><circle cx="${x - r * .3}" cy="${y + r * .38}" r="${r * .13}" fill="#fff"/></g>`).join('')}
    </g>`;
  // eyes: open 1 = pupils shown; blink squashes them; look shifts them
  function setFace(svg, { open = 1, blink = 0, look = 0, mouth = .38 } = {}) {
    svg.querySelectorAll('.kg-pup').forEach((g, i) => {
      const [x, y] = PUP[i];
      g.style.opacity = open;
      tf(g, look * 9, 0, 0, x, y - 6, 1, Math.max(.06, 1 - blink));
    });
    tf(svg.querySelector('.kg-mouth'), 0, 0, 0, 440, 612, 1, mouth);
  }
  // natural blinks: every ~2.8 s, a 0.16 s blink
  const blinkAt = tm => { const p = (tm % 2.8) / 2.8; return p > .94 ? Math.sin((p - .94) / .06 * Math.PI) : 0; };
  // talking: the mouth opens and closes while the line is being "said"
  const talkAt = (tm, s, d) => (tm < s || tm > s + d) ? null : .45 + .55 * Math.abs(Math.sin((tm - s) * 9.5));

  /* =============================================================================================
     WELCOME — the ارحبوووو peek from the left edge (hands first, then the head, then the line)
     ============================================================================================= */
  function welcome() {
    stop();
    const small = innerWidth < 640, W = small ? 176 : 230;
    const VB = { x: 190, y: 80, w: 750, h: 1093 };
    const s = W / VB.w, poleX = (A.pole_x - VB.x) * s;
    const box = document.createElement('div'); box.className = 'kg kg--hi';
    box.style.cssText = `left:0; width:${W}px; --kg-fs:${small ? 28 : 34}px`;
    const svg = el('svg', { viewBox: `${VB.x} ${VB.y} ${VB.w} ${VB.h}`, 'aria-hidden': 'true' });
    svg.innerHTML = `
      <defs><clipPath id="kgBehind"><rect x="${A.pole_x + 4}" y="-400" width="2000" height="3000"/></clipPath></defs>
      <g clip-path="url(#kgBehind)"><g class="kg-slide">
        ${part('body')}
        <g class="kg-head">
          ${part('earL', 'kg-earL')}${part('earR', 'kg-earR')}${part('head')}${face()}
        </g>
      </g></g>
      ${part('pawT', 'kg-pawT')}${part('pawB', 'kg-pawB')}`;
    box.appendChild(svg);
    const say = document.createElement('div'); say.className = 'kg__say'; say.setAttribute('role', 'status');
    say.innerHTML = sayHTML(t('arhab'));
    say.style.cssText = `left:${W * .3}px; bottom:${(VB.h - 40) * s}px`;
    box.appendChild(say);
    const pole = document.createElement('div'); pole.className = 'kg__pole';
    pole.style.cssText = `left:${poleX - 1.5}px; --kg-pw:${Math.max(2.5, A.pole_w * s)}px`;
    document.body.append(pole, box);

    const q = c => svg.querySelector(c);
    const slide = q('.kg-slide'), head = q('.kg-head'), earL = q('.kg-earL'), earR = q('.kg-earR'), pawT = q('.kg-pawT'), pawB = q('.kg-pawB');
    const NECK = [420, 785], EARL = [430, 362], EARR = [700, 566];
    const END = 8.2;
    if (reduce) {   // still frame, then fade away
      pole.style.transform = 'none'; setFace(svg, { open: 0, mouth: 1 }); say.style.opacity = 1;
      run([pole, box], 6, () => {}); return;
    }
    run([pole, box], END, tm => {
      // 0 · the edge line draws down
      pole.style.transform = `scaleY(${tm < 7.4 ? seg(tm, 0, .45, E.io) : 1 - seg(tm, 7.6, .45, E.io)})`;
      pole.style.transformOrigin = tm < 7.4 ? '50% 0' : '50% 100%';
      // 1 · hands grab the edge (top first, then bottom)
      const out = seg(tm, 7.05, .45, E.in);
      tf(pawT, lerp(-170, 0, seg(tm, .35, .5, E.back)) - 170 * out, 0);
      tf(pawB, lerp(-170, 0, seg(tm, .5, .5, E.back)) - 170 * out, 0);
      // 2 · head and body slide out from behind the edge, with a tilt that settles
      const inK = seg(tm, 1.05, .95, E.back), outK = seg(tm, 6.55, .6, E.in);
      const sx = lerp(-640, 0, inK) - 640 * outK;
      tf(slide, sx, 0);
      // head: tilt in, curious tilt while looking, happy bob while talking, idle sway
      let hr = lerp(-16, 0, seg(tm, 1.05, 1.3, E.elastic));
      hr += -6 * Math.sin(clamp((tm - 2.3) / 1.2) * Math.PI);                 // curious tilt
      hr += tm > 3.6 && tm < 6.5 ? 3.2 * Math.sin((tm - 3.6) * 7) * Math.exp(-(tm - 3.6) * .9) : 0;  // excited bob
      hr += tm > 4.2 ? 1.8 * Math.sin((tm - 4.2) * 2.4) : 0;                  // idle sway
      tf(head, 0, 0, hr, NECK[0], NECK[1]);
      // ears flop with a little lag after every head move, and twitch now and then
      const flop = k => Math.sin(k * 14) * Math.exp(-k * 4);
      const eL = 14 * flop(Math.max(0, tm - 1.7)) + 10 * flop(Math.max(0, tm - 3.6)) + (tm > 5 ? 7 * flop(Math.max(0, (tm - 5) % 2.3)) : 0);
      const eR = -12 * flop(Math.max(0, tm - 1.75)) - 12 * flop(Math.max(0, tm - 3.65)) - (tm > 5.6 ? 8 * flop(Math.max(0, (tm - 5.6) % 2.1)) : 0);
      tf(earL, 0, 0, eL, ...EARL); tf(earR, 0, 0, eR, ...EARR);
      // face: open eyes look around and blink, then the happy face says ارحبوووو
      const happy = tm > 3.55 && tm < 5.6;
      const look = tm < 3.5 ? Math.sin(clamp((tm - 1.9) / 1.4) * Math.PI * 2) * .9 : 0;
      const blink = (tm > 3.05 && tm < 3.25) ? Math.sin((tm - 3.05) / .2 * Math.PI) : (!happy && tm > 5.6 ? blinkAt(tm - 5.6 + 2.4) : 0);
      const talk = talkAt(tm, 3.6, 1.6);
      setFace(svg, { open: happy ? 0 : 1, blink, look, mouth: talk ?? (happy ? 1 : .38) });
      // 3 · the line pops above the head, floats, then fades as it leaves
      const sk = seg(tm, 3.55, .55, E.back), so = seg(tm, 6.4, .3);
      say.style.opacity = clamp(sk * 1.6) * (1 - so);
      say.style.transform = `translateY(${lerp(14, 0, sk) + (tm > 4.1 ? Math.sin((tm - 4.1) * 2.6) * 3 : 0)}px) rotate(${lerp(-14, -4, sk)}deg) scale(${lerp(.4, 1, sk)})`;
    }, opts.onDone);
  }

  /* =============================================================================================
     WALKER — the same head on a body with four legs; walks, hops or sits along the bottom
     ============================================================================================= */
  // body + neck as one outline so the joint is seamless; legs hang from hips inside the body
  const BODY = 'M452 742C466 818 474 864 474 904C474 994 544 1060 646 1060L842 1060C922 1060 968 1000 962 938C956 878 912 846 842 846L652 850C598 850 566 818 548 750Z';
  const SPOTS = [[700, 892, 14, 20, -20], [748, 882, 12, 18, -25], [792, 896, 13, 19, -15], [728, 930, 10, 15, -20], [838, 884, 11, 16, -30], [664, 918, 9, 14, -10]];
  const TAIL = 'M944 900C980 878 1004 840 994 806C984 790 966 796 960 812C952 840 938 864 922 880Z';
  const HIPS = { fn: [560, 1000], ff: [612, 990], bf: [826, 990], bn: [880, 1000] };   // front-near, front-far, back-far, back-near
  const LEG_LEN = 232;
  const leg = (k, far) => `<g class="kg-leg" data-leg="${k}"><path d="M-27 0L-22 ${LEG_LEN - 24}C-22 ${LEG_LEN + 6} 22 ${LEG_LEN + 6} 22 ${LEG_LEN - 24}L27 0Z" fill="${far ? '#f2f2f2' : '#fff'}" stroke="#111" stroke-width="16" stroke-linejoin="round"/>
    <path d="M-22 ${LEG_LEN - 30}C-22 ${LEG_LEN + 6} 22 ${LEG_LEN + 6} 22 ${LEG_LEN - 30}Z" fill="#111"/></g>`;
  const GROUND = 1000 + LEG_LEN + 6;
  // in the drawing the left of the face hides behind the pole and the paw; close it for the walker
  const HEAD_PATCH_FILL = '<path fill="#fff" d="M280 470C248 516 240 602 258 654C270 690 292 716 322 736L344 600L330 470Z"/>';
  const HEAD_PATCH_LINE = '<path fill="none" stroke="#111" stroke-width="17" stroke-linecap="round" d="M281 478C252 520 244 600 262 652C274 688 296 714 324 734"/>';

  function walk(kind = 'walk', line = '', small = '', link = null) {
    stop();
    const mobile = innerWidth < 640, W = mobile ? 150 : 196;
    const VB = { x: 250, y: 60, w: 780, h: GROUND - 60 + 12 };
    const s = W / VB.w;
    // walk in from the side away from the WhatsApp button (inline-start): left in Arabic, right in English
    const fromLeft = document.documentElement.dir === 'rtl';
    const box = document.createElement('div'); box.className = 'kg kg--walk';
    box.style.cssText = `width:${W}px; ${fromLeft ? 'left' : 'right'}:0; --kg-fs:${mobile ? 24 : 28}px`;
    const svg = el('svg', { viewBox: `${VB.x} ${VB.y} ${VB.w} ${VB.h}`, 'aria-hidden': 'true' });
    svg.innerHTML = `<g class="kg-flip"><g class="kg-all">
      <ellipse class="kg-shadow" cx="720" cy="${GROUND - 4}" rx="250" ry="16" fill="#111" opacity=".08"/>
      ${leg('ff', 1)}${leg('bf', 1)}
      <g class="kg-torso"><path d="${TAIL}" class="kg-tail" fill="#fff" stroke="#111" stroke-width="16" stroke-linejoin="round"/>
        <path d="${BODY}" fill="#fff" stroke="#111" stroke-width="16" stroke-linejoin="round"/>
        ${SPOTS.map(([x, y, rx, ry, r]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" transform="rotate(${r} ${x} ${y})" fill="#111"/>`).join('')}
        <g class="kg-head">${part('earL', 'kg-earL')}${part('earR', 'kg-earR')}${HEAD_PATCH_FILL}${part('head')}${HEAD_PATCH_LINE}${face()}</g>
      </g>
      ${leg('fn')}${leg('bn')}
    </g></g>`;
    box.appendChild(svg);
    const say = document.createElement('div'); say.className = 'kg__say'; say.setAttribute('role', 'status');
    say.innerHTML = sayHTML(line, small, link);
    box.appendChild(say);
    document.body.appendChild(box);

    const q = c => svg.querySelector(c);
    const all = q('.kg-all'), flip = q('.kg-flip'), torso = q('.kg-torso'), head = q('.kg-head'), tail = q('.kg-tail'),
      earL = q('.kg-earL'), earR = q('.kg-earR'), legs = [...svg.querySelectorAll('.kg-leg')].reduce((o, g) => (o[g.dataset.leg] = g, o), {});
    // the drawing faces left; mirror it when it walks in from the left so it faces where it goes
    flip.setAttribute('transform', fromLeft ? `translate(${VB.x * 2 + VB.w} 0) scale(-1 1)` : '');
    const dir = fromLeft ? 1 : -1;                 // screen direction of travel
    const travel = (W + 40) / s;                  // off-screen distance in drawing units
    const NECK = [500, 790], EARL = [430, 362], EARR = [700, 566];
    const setLeg = (k, a, lift = 0) => { const [x, y] = HIPS[k]; legs[k].setAttribute('transform', `translate(${x} ${y - lift}) rotate(${a.toFixed(2)})`); };
    // text sits above the head; mirror-aware horizontal position
    say.style.cssText = `bottom:${(GROUND - 95) * s}px; ${fromLeft ? 'left' : 'right'}:${W * .12}px; transform-origin:${fromLeft ? '20%' : '80%'} 100%`;

    const T = { walk: { inEnd: 1.9, talk: [2.4, 2.2], leave: 6.4, end: 8.4 }, hop: { inEnd: 2.1, talk: [2.6, 2.2], leave: 6.6, end: 8.6 }, sit: { inEnd: 1.9, talk: [3.1, 2.2], leave: 7.0, end: 9.0 } }[kind];
    if (reduce) {
      setFace(svg, { open: 1, mouth: .38 }); Object.keys(HIPS).forEach(k => setLeg(k, 0));
      say.style.opacity = 1; run([box], 6, () => {}); return;
    }
    run([box], T.end, tm => {
      // where it is: comes in, stands, goes back out the way it came (turning round first)
      const inK = kind === 'hop' ? seg(tm, 0, T.inEnd, k => k) : seg(tm, 0, T.inEnd, E.out);
      const outK = seg(tm, T.leave + .35, T.end - T.leave - .35, E.in);
      const x = -travel * (1 - inK) - travel * outK * 1.05;
      const turned = tm > T.leave;                    // faces back the way it came
      const moving = (tm < T.inEnd) || (tm > T.leave + .35);
      // gait phase follows distance so feet do not slide
      const speed = moving ? 1 : 0;
      const ph = tm * (kind === 'hop' ? 9 : 11);
      let bodyY = 0, bodyR = 0, a = { fn: 0, ff: 0, bf: 0, bn: 0 }, lift = { fn: 0, ff: 0, bf: 0, bn: 0 };
      if (kind === 'hop' && moving) {
        // bouncy hops: up with legs tucked, down with legs reaching
        const h = Math.abs(Math.sin(ph / 2));
        bodyY = -150 * h; bodyR = -8 * Math.cos(ph / 2) * h;
        const tuck = h;
        a = { fn: 28 * tuck, ff: 22 * tuck, bf: -26 * tuck, bn: -32 * tuck };
        lift = { fn: 0, ff: 0, bf: 0, bn: 0 };
      } else if (moving) {
        const sw = Math.sin(ph), sw2 = Math.sin(ph + Math.PI);
        a = { fn: 22 * sw, bf: 22 * sw, ff: 22 * sw2, bn: 22 * sw2 };
        lift = { fn: Math.max(0, Math.cos(ph)) * 18, bf: Math.max(0, Math.cos(ph)) * 18, ff: Math.max(0, -Math.cos(ph)) * 18, bn: Math.max(0, -Math.cos(ph)) * 18 };
        bodyY = -10 * Math.abs(Math.cos(ph)); bodyR = 1.6 * Math.sin(ph);
      } else {
        // standing: a soft breath; for "sit" the rear folds down and the back legs tuck under
        bodyY = 3 * Math.sin(tm * 2.6);
        const sitK = kind === 'sit' ? seg(tm, T.inEnd + .25, .55, E.back) * (1 - seg(tm, T.leave - .5, .45, E.io)) : 0;
        if (sitK) {
          bodyR = 14 * sitK; bodyY += 62 * sitK;
          a.bn = 80 * sitK; a.bf = 74 * sitK; lift.bn = 24 * sitK; lift.bf = 24 * sitK;   // fold forward under the body
          a.fn = -6 * sitK; a.ff = -4 * sitK;
          // a front hoof taps while it talks
          if (tm > T.talk[0] && tm < T.talk[0] + T.talk[1]) { const tap = Math.max(0, Math.sin((tm - T.talk[0]) * 8)); a.fn -= 18 * tap; lift.fn = 14 * tap; }
        }
        // a little settle when it stops walking
        if (tm > T.inEnd && tm < T.inEnd + .5) bodyY += 10 * Math.sin((tm - T.inEnd) / .5 * Math.PI);
      }
      Object.keys(HIPS).forEach(k => setLeg(k, a[k], lift[k]));
      const piv = kind === 'sit' ? [600, 1000] : [720, 1000];
      torso.setAttribute('transform', `translate(0 ${bodyY.toFixed(2)}) rotate(${bodyR.toFixed(2)} ${piv[0]} ${piv[1]})`);
      // the front legs belong to the torso's front, so they ride up with it
      ['fn', 'ff'].forEach(k => { const [hx, hy] = HIPS[k]; legs[k].setAttribute('transform', `translate(0 ${bodyY.toFixed(2)}) rotate(${bodyR.toFixed(2)} ${piv[0]} ${piv[1]}) translate(${hx} ${hy - lift[k]}) rotate(${a[k].toFixed(2)})`); });
      if (kind !== 'sit') ['bn', 'bf'].forEach(k => { const [hx, hy] = HIPS[k]; legs[k].setAttribute('transform', `translate(0 ${bodyY.toFixed(2)}) rotate(${bodyR.toFixed(2)} ${piv[0]} ${piv[1]}) translate(${hx} ${hy - lift[k]}) rotate(${a[k].toFixed(2)})`); });
      else ['bn', 'bf'].forEach(k => { const [hx, hy] = HIPS[k]; legs[k].setAttribute('transform', `translate(0 ${bodyY.toFixed(2)}) rotate(${bodyR.toFixed(2)} ${piv[0]} ${piv[1]}) translate(${hx} ${hy - lift[k]}) rotate(${a[k].toFixed(2)})`); });
      // head: nods with the steps, looks up at you to talk, happy bob while talking
      const talking = tm > T.talk[0] && tm < T.talk[0] + T.talk[1];
      let hr = moving ? 3 * Math.sin(ph * 2) : -7 * seg(tm, T.inEnd, .5, E.back) * (1 - seg(tm, T.leave - .2, .4));
      if (talking) hr += 3 * Math.sin((tm - T.talk[0]) * 6);
      tf(head, 0, 0, hr - bodyR * .6, ...NECK);
      // ears flop with the bounce and flick while it listens
      const ek = moving ? Math.sin(ph * 2 - .8) : Math.sin(tm * 9) * Math.exp(-((tm - T.inEnd) % 2.4) * 2.5);
      tf(earL, 0, 0, 9 * ek, ...EARL); tf(earR, 0, 0, -9 * ek, ...EARR);
      // tail wags faster when it is happy
      tf(tail, 0, 0, (talking ? 16 : 8) * Math.sin(tm * (talking ? 16 : 7)), 944, 900);
      // face
      const happy = talking && ((tm - T.talk[0]) % 1.6) < 1;
      setFace(svg, { open: happy ? 0 : 1, blink: blinkAt(tm + .7), look: moving ? 0 : .5 * Math.sin(tm * 1.3), mouth: talkAt(tm, T.talk[0], T.talk[1] - .5) ?? .38 });
      // position + turning round to leave
      const flipBack = turned ? -1 : 1;
      all.setAttribute('transform', `translate(${(x * dir * (fromLeft ? -1 : 1)).toFixed(1)} 0) ${turned ? `translate(${(VB.x * 2 + VB.w)} 0) scale(-1 1)` : ''}`);
      // the line
      const sk = seg(tm, T.talk[0] - .15, .5, E.back), so = seg(tm, T.leave - .3, .3);
      say.style.opacity = clamp(sk * 1.6) * (1 - so);
      say.style.transform = `translateY(${lerp(12, 0, sk) + (tm > T.talk[0] + .4 ? Math.sin((tm - T.talk[0]) * 2.6) * 2.5 : 0)}px) scale(${lerp(.5, 1, sk)}) rotate(${lerp(fromLeft ? 8 : -8, fromLeft ? 2 : -2, sk)}deg)`;
    }, opts.onDone);
  }

  return { welcome, walk, busy, stop };
}
