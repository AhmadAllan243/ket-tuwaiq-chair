/* KET product page behaviour (templates/product.jinja). Ported from ket-product.html.
   Shop logic (cart, options, buy now, lightbox, sticky bar) stays in the Growth theme bundle;
   this file only adds the KET look and motion: gallery count/progress/thumbs, delivery date,
   accordions, review slider, count-ups, reveals, the dimension drawings, the story pin and the
   3D hero (loaded only when the product has a 3D model). */
(() => {
  const page = document.querySelector('[data-ket-product]');
  if (!page) return;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const root = document.documentElement;
  const rtl = () => root.dir === 'rtl';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const G = !!(window.gsap && window.ScrollTrigger) && !reduce;
  root.classList.add(G ? 'motion' : 'no-motion');   // without motion the story shows its two photos stacked (ket.css)

  /* ---------- 3D hero: load the bundle only when the product has a model ---------- */
  const hero = $('#ket-hero');
  const heroSrc = document.currentScript?.dataset.hero || $('script[data-hero]')?.dataset.hero;
  // the theme header is sticky; the hero keeps its 3D scene below it
  const zh = document.querySelector('body > .sticky, header');
  const setHeaderH = () => root.style.setProperty('--ket-header-h', (zh ? zh.getBoundingClientRect().height : 0) + 'px');
  setHeaderH(); addEventListener('resize', setHeaderH);
  if (hero && heroSrc) {
    const s = document.createElement('script'); s.src = heroSrc; s.defer = true;
    // the hero adds its own pinned section after the page's pins exist: re-measure them all once it is in
    s.onload = () => [300, 1500].forEach(t => setTimeout(() => { if (window.ScrollTrigger) { ScrollTrigger.sort?.(); ScrollTrigger.refresh(); } }, t));
    document.body.append(s);
  }

  /* ---------- Zid's sticky add-to-cart bar: only once the customer has scrolled past the buy box ---------- */
  const actions = $('[data-product-actions]');
  if (actions) {
    const before = () => document.body.classList.toggle('ket-before-buy', actions.getBoundingClientRect().top > innerHeight);
    before(); addEventListener('scroll', before, { passive: true });
  }

  /* ---------- Gallery: count, progress bar, thumbs, arrows ---------- */
  const track = $('#gTrack');
  if (track) {
    const n = $$('.g-slide', track).length;
    let gi = 0;
    const onScroll = () => {
      const max = track.scrollWidth - track.clientWidth;
      const p = max > 0 ? Math.min(1, Math.abs(track.scrollLeft) / max) : 0;
      $('#gProg')?.style.setProperty('--p', p);
      gi = Math.round(p * (n - 1));
      const c = $('#gCount'); if (c) c.textContent = `${String(gi + 1).padStart(2, '0')} / ${String(n).padStart(2, '0')}`;
      $$('.g-thumb').forEach((b, k) => { b.classList.toggle('is-active', k === gi); b.setAttribute('aria-current', k === gi); });
    };
    const go = (i, smooth = true) => { i = (i + n) % n; track.scrollTo({ left: (rtl() ? -1 : 1) * i * track.clientWidth, behavior: smooth && !reduce ? 'smooth' : 'auto' }); };
    track.addEventListener('scroll', onScroll, { passive: true });
    $('#gPrev')?.addEventListener('click', () => go(gi - 1));
    $('#gNext')?.addEventListener('click', () => go(gi + 1));
    $('#gThumbs')?.addEventListener('click', e => { const b = e.target.closest('.g-thumb'); if (b) go(+b.dataset.i); });
    track.addEventListener('keydown', e => {
      const fwd = rtl() ? 'ArrowLeft' : 'ArrowRight', back = rtl() ? 'ArrowRight' : 'ArrowLeft';
      if (e.key === fwd) { e.preventDefault(); go(gi + 1); } else if (e.key === back) { e.preventDefault(); go(gi - 1); }
    });
    // the zoom button opens the lightbox at the current slide
    const zoom = $('.g-zoom'); if (zoom) track.addEventListener('scroll', () => { zoom.dataset.lightboxTrigger = gi; }, { passive: true });
  }

  /* ---------- Delivery estimate (today + N days, from theme settings) ---------- */
  const del = $('[data-ket-delivery]');
  if (del) {
    const d = new Date(); d.setDate(d.getDate() + (+del.dataset.days || 3));
    const ar = (root.lang || 'ar').startsWith('ar');
    const ds = d.toLocaleDateString(ar ? 'ar-SA-u-ca-gregory-nu-latn' : 'en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
    $('span', del).innerHTML = ar ? `اطلبه اليوم، ويوصلك <strong>${ds}</strong>` : `Order today, delivered by <strong>${ds}</strong>`;
    del.hidden = false;
  }

  /* ---------- Numbers read 1,653 (Zid prints 1653) ---------- */
  $$('[data-count]').forEach(el => { const plus = el.textContent.trim().endsWith('+') ? '+' : ''; el.textContent = (+el.dataset.count).toLocaleString('en-US') + plus; });
  $$('[data-sold-count-text]').forEach(el => { el.textContent = el.textContent.replace(/\d{4,}/g, n => (+n).toLocaleString('en-US')); });

  /* ---------- Story title: as large as the column allows ---------- */
  const fitStoryTitle = () => {
    const h = $('#storyWord'), txt = $('#storyTitle')?.firstChild;
    if (!h || !txt) return;
    h.style.fontSize = '';
    const range = document.createRange(); range.selectNodeContents(txt);
    const textW = range.getBoundingClientRect().width, avail = h.clientWidth;
    if (textW > avail && textW > 0) h.style.fontSize = Math.max(36, parseFloat(getComputedStyle(h).fontSize) * (avail / textW) * 0.97) + 'px';
  };
  fitStoryTitle(); document.fonts?.ready.then(fitStoryTitle);
  let fitT; addEventListener('resize', () => { clearTimeout(fitT); fitT = setTimeout(fitStoryTitle, 120); });

  /* ---------- Customer moments: a fanned deck of cards ---------- */
  const deck = $('#momDeck');
  if (deck) {
    const cards = $$('.mcard', deck), n = cards.length; let ma = 0;
    const layout = () => {
      const wide = matchMedia('(min-width:900px)').matches;
      cards.forEach((c, i) => {
        let o = i - ma; if (o > n / 2) o -= n; if (o < -n / 2) o += n;   // circular: the fan always has both sides
        const ao = Math.abs(o);
        c.style.setProperty('--o', o); c.style.setProperty('--ao', ao); c.style.zIndex = 20 - ao;
        c.classList.toggle('is-active', o === 0); c.classList.toggle('is-hidden', ao > (wide ? 2 : 1));
        c.setAttribute('aria-hidden', o !== 0); $$('button', c).forEach(b => { b.tabIndex = o === 0 ? 0 : -1; });
      });
      const cnt = $('#momCount'); if (cnt) cnt.textContent = `${String(ma + 1).padStart(2, '0')} / ${String(n).padStart(2, '0')}`;
      $('#momPrev').hidden = $('#momNext').hidden = n < 2;
    };
    const go = i => { ma = (i + n) % n; layout(); };
    $('#momPrev')?.addEventListener('click', () => go(ma - 1));
    $('#momNext')?.addEventListener('click', () => go(ma + 1));
    deck.addEventListener('click', e => { const c = e.target.closest('.mcard'); if (c && !c.classList.contains('is-active') && !e.target.closest('button')) go(+c.dataset.mi); });
    deck.addEventListener('keydown', e => {
      const fwd = rtl() ? 'ArrowLeft' : 'ArrowRight', back = rtl() ? 'ArrowRight' : 'ArrowLeft';
      if (e.key === fwd) { e.preventDefault(); go(ma + 1); } else if (e.key === back) { e.preventDefault(); go(ma - 1); }
    });
    let down = null;   // swipe: the next card sits on the reading-forward side
    deck.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY }; });
    deck.addEventListener('pointerup', e => {
      if (!down) return; const dx = e.clientX - down.x, dy = e.clientY - down.y; down = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) go(ma + (dx < 0 ? 1 : -1) * (rtl() ? -1 : 1));
    });
    addEventListener('resize', layout); layout();
    if (G) { deck.classList.add('is-stacked'); }
  }

  /* ---------- Accordions + review slider ---------- */
  page.addEventListener('click', e => {
    const b = e.target.closest('.acc__btn');
    if (b) {
      const it = b.closest('.acc__item'), open = !it.classList.contains('is-open');
      it.classList.toggle('is-open', open); b.setAttribute('aria-expanded', open);
      if (G) setTimeout(() => ScrollTrigger.refresh(), 650);
      return;
    }
    const s = e.target.closest('[data-slide]');
    if (s) {
      const tr = document.getElementById(s.dataset.slide), card = tr?.firstElementChild; if (!card) return;
      tr.scrollBy({ left: +s.dataset.step * (card.getBoundingClientRect().width + 12) * (rtl() ? -1 : 1), behavior: reduce ? 'auto' : 'smooth' });
    }
  });

  if (!G) return;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- Intro ---------- */
  gsap.timeline({ defaults: { ease: 'expo.out' } })
    .fromTo('.ket .g-stage', { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.3, ease: 'expo.inOut' }, .05)
    .fromTo('.ket .g-slide:first-child img', { scale: 1.18 }, { scale: 1, duration: 1.8 }, .1)
    .fromTo('.ket .intro-line > span', { yPercent: 110 }, { yPercent: 0, duration: 1.1, stagger: .09 }, .3)
    .fromTo('.ket .intro-fade', { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: .9, stagger: .06 }, .45);

  /* ---------- Count-ups (proof numbers, review bars) and stars ---------- */
  $$('[data-count]').forEach(el => {
    const to = +el.dataset.count, suffix = el.textContent.trim().endsWith('+') ? '+' : '', o = { v: 0 };
    gsap.to(o, { v: to, duration: 1.8, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      onUpdate: () => { el.textContent = Math.round(o.v).toLocaleString('en-US') + suffix; } });
  });
  $$('.ket .rating .star, .ket .proof .star').length && gsap.fromTo('.ket .rating .star, .ket .proof .star', { scale: .2, opacity: 0, rotate: -35 },
    { scale: 1, opacity: 1, rotate: 0, duration: .55, stagger: .08, ease: 'back.out(2.4)', scrollTrigger: { trigger: '.ket .rating, .ket .proof', start: 'top 90%', once: true } });
  const bar = $('.ket .stock__bar span');
  if (bar) gsap.fromTo(bar, { width: '100%', backgroundColor: '#02A27A' },
    { width: () => getComputedStyle(bar).getPropertyValue('--w'), backgroundColor: '#FF6517', duration: 1.8, ease: 'power3.out', scrollTrigger: { trigger: bar, start: 'top 92%', once: true } });

  /* ---------- Reveals ---------- */
  $$('.ket [data-reveal]').forEach(el => gsap.from(el, { y: 40, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true } }));
  $$('.ket .sec-head .h-xl').forEach(h => gsap.from(h, { clipPath: 'inset(0 0 100% 0)', y: 30, duration: 1.1, ease: 'expo.out', scrollTrigger: { trigger: h, start: 'top 90%', once: true } }));
  ['#features', '#relTrack'].forEach(sel => { if ($(sel)) gsap.from(`${sel} [data-reveal-item]`, { y: 50, opacity: 0, duration: 1, stagger: .08, ease: 'power3.out', scrollTrigger: { trigger: sel, start: 'top 85%', once: true } }); });
  if (deck) ScrollTrigger.create({ trigger: deck, start: 'top 80%', once: true, onEnter: () => deck.classList.remove('is-stacked') });

  /* ---------- Feature crops: zoom out as they scroll in ---------- */
  $$('.ket .feature img').forEach(img => {
    const z = +img.dataset.z || 1.4;
    gsap.fromTo(img, { scale: z * 1.25 }, { scale: z, ease: 'none', scrollTrigger: { trigger: img.closest('.feature'), start: 'top bottom', end: 'center 45%', scrub: true } });
    gsap.from(img.closest('.feature__media'), { clipPath: 'inset(100% 0 0 0 round 16px)', duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: img, start: 'top 88%', once: true } });
  });

  if ($('#revTrack')) gsap.from('.ket .rcard', { x: () => 60 * (rtl() ? -1 : 1), opacity: 0, duration: 1, stagger: .08, ease: 'power3.out', scrollTrigger: { trigger: '#revTrack', start: 'top 85%', once: true } });
  if ($('.ket .rev__bars')) gsap.from('.ket .rev__bar b', { scaleX: 0, transformOrigin: () => rtl() ? 'right' : 'left', duration: 1.2, stagger: .07, ease: 'expo.out', scrollTrigger: { trigger: '.ket .rev__bars', start: 'top 85%', once: true } });

  /* ---------- Dimensions: the drawings draw themselves ---------- */
  $$('.ket .dims__fig').forEach(fig => {
    gsap.timeline({ scrollTrigger: { trigger: fig, start: 'top 75%', once: true } })
      .fromTo($$('.chair .dl', fig), { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.4, stagger: .12, ease: 'power2.inOut' })
      .fromTo($$('.dims .dm', fig), { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: .8, stagger: .15, ease: 'power3.out' }, '-=.4')
      .from($$('.dm-t', fig), { opacity: 0, y: 6, duration: .5, stagger: .1 }, '-=.4');
  });

  /* ---------- Story: pinned; the product comes forward, then a closer look ---------- */
  if ($('#storyStage')) {
    gsap.timeline({ scrollTrigger: { trigger: '#story', start: 'top 70%', once: true } })
      .from('#storyWord .line-mask > span', { yPercent: 110, duration: 1.2, ease: 'expo.out' })
      .from('#storyLines .line-mask > span', { yPercent: 110, duration: 1, stagger: .12, ease: 'expo.out' }, '-=.9');
    gsap.matchMedia().add('(min-height: 560px)', () => {
      const tl = gsap.timeline({ scrollTrigger: { trigger: '#storyStage', start: 'top top', end: () => '+=' + innerHeight * 1.8, pin: true, scrub: .35, anticipatePin: 1, invalidateOnRefresh: true } });
      tl.fromTo('#storyCard', { y: () => innerHeight * .28, scale: .55, rotate: -6, opacity: 0 }, { y: 0, scale: 1, rotate: 0, opacity: 1, duration: 1.1, ease: 'back.out(1.3)' })
        .fromTo('#storyProduct', { scale: 1.3 }, { scale: 1, duration: 1.3, ease: 'power2.out' }, '<');
      if ($('.story__chip')) tl.fromTo('.story__chip', { scale: .3, opacity: 0, y: 24 }, { scale: 1, opacity: 1, y: 0, duration: .45, stagger: .22, ease: 'back.out(2.2)' }, '-=.35')
        .to({}, { duration: .35 })
        .to('.story__chip', { opacity: 0, y: -12, duration: .35, stagger: .06 });
      if ($('#storyDetail')) tl.to({}, { duration: .3 })
        .fromTo('#storyDetail', { opacity: 0, filter: 'blur(22px)' }, { opacity: 1, filter: 'blur(0px)', duration: 1.1, ease: 'power2.inOut' })
        .fromTo('#storyProduct', { filter: 'blur(0px)' }, { filter: 'blur(16px)', duration: 1.1, ease: 'power2.inOut' }, '<')
        .fromTo('#storyImgEl', { scale: 1.35 }, { scale: 1, duration: 1.3, ease: 'power2.out' }, '<');
      if ($('#storyBody')) tl.fromTo('#storyBody', { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: .6 }, '-=.5');
      tl.to({}, { duration: .4 });
    });
  }

  addEventListener('load', () => ScrollTrigger.refresh());
  document.fonts?.ready.then(() => ScrollTrigger.refresh());
})();
