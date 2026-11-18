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
    let n = $$('.g-slide', track).length, gi = 0;
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

    // a colour / option with its own photos (Zid's "product:variant-changed"): the gallery, thumbs and zoom show that option's photos
    const sized = (u, w) => u ? u.replace(/(width=)\d+/, '$1' + w).replace(/(height=)\d+/, '$1' + w) : '';
    let shownMedia = '';
    addEventListener('product:variant-changed', e => {
      const p = e.detail && e.detail.selectedProduct;
      const pics = ((p && p.media) || []).filter(m => m.image && !(m.provider && m.link)).map(m => m.image.large || m.image.full_size || m.image.medium).filter(Boolean);
      const key = pics.join('|'); if (!pics.length || key === shownMedia) return; shownMedia = key;
      const alt = (p.name || '').replace(/"/g, '&quot;');
      track.innerHTML = pics.map((u, i) => `<div class="g-slide" role="group" aria-roledescription="slide" data-i="${i}"><img src="${sized(u, 1200)}" alt="${alt}" width="1254" height="1254" data-lightbox-trigger="${i}" draggable="false" decoding="async"${i ? ' loading="lazy"' : ' fetchpriority="high"'}></div>`).join('');
      const th = $('#gThumbs'); if (th) th.innerHTML = pics.map((u, i) => `<button class="g-thumb${i ? '' : ' is-active'}" type="button" data-i="${i}" aria-label="${i + 1}"><img src="${sized(u, 160)}" alt="" loading="lazy" width="64" height="64"></button>`).join('');
      const lb = $('#product-gallery-lightbox'); if (lb) lb.innerHTML = pics.map(u => `<a href="${sized(u, 1600)}" data-pswp-width="1600" data-pswp-height="1600"><img src="${sized(u, 1600)}" alt="${alt}" data-lightbox-item data-lightbox-src="${sized(u, 1600)}" data-lightbox-width="1600" data-lightbox-height="1600"></a>`).join('');
      const many = pics.length > 1;
      ['#gThumbs', '#gProg', '#gCount', '#gPrev', '#gNext'].forEach(sel => { const el = $(sel); if (el) el.hidden = !many; });
      $('#gProg')?.style.setProperty('--n', pics.length);
      n = pics.length; gi = 0; track.scrollTo({ left: 0, behavior: 'auto' }); onScroll();
      if (zoom) zoom.dataset.lightboxTrigger = 0;
    });
  }

  /* ---------- Colour swatches: each shows its own photo (the colour codes set in Zid are often all black) ---------- */
  (async () => {
    const items = $$('.product-options__item--color'); if (!items.length) return;
    for (let i = 0; i < 60 && !(window.zid && window.zid.products); i++) await new Promise(r => setTimeout(r, 200));
    const id = document.getElementById('product-parent-id')?.value; if (!id || !window.zid?.products) return;
    try {
      const p = await window.zid.products.get(id), pic = {};
      (p.variants || []).forEach(v => {
        const im = (v.images || [])[0]?.image, src = im && (im.small || im.thumbnail || im.medium); if (!src) return;
        (v.attributes || []).forEach(a => { if (a.type === 'color' && !pic[a.value]) pic[a.value] = src; });
      });
      const srcs = items.map(li => pic[li.getAttribute('value')]);
      if (srcs.some(s => !s) || new Set(srcs).size < srcs.length) return;   // only when every colour has a photo of its own
      items.forEach((li, k) => { const sw = li.querySelector('.product-options__swatch'); if (sw) { sw.style.backgroundImage = `url("${srcs[k]}")`; sw.classList.add('has-photo'); } });
    } catch (e) {}
  })();

  /* ---------- Sticky add-to-cart bar: a green button with a shine, a pulse and a wiggle, the saving as a tag on its corner,
     and a chip of true reasons to buy that slides from one to the next (the saving, free delivery, the offer ending within
     48 h, few pieces left), from the product's own Zid data ---------- */
  (async () => {
    const bar = $('#sticky-cta'), btn = bar && bar.querySelector('[data-sticky-cta-add-to-cart]'); if (!btn) return;
    btn.classList.add('ket-cta-go'); btn.parentElement.classList.add('ket-cta-wrap');
    const fit = () => { btn.parentElement.style.setProperty('--bw', btn.offsetWidth + 'px'); btn.parentElement.style.setProperty('--bh', btn.offsetHeight + 'px'); };   // the pulse ring hugs the button
    // while the bar is up, the floating chat button (BusinessChat) rides above it instead of hiding behind it
    const lift = () => { const on = bar.getAttribute('aria-hidden') === 'false' && !document.body.classList.contains('ket-before-buy');
      document.body.classList.toggle('ket-cta-on', on); if (on && bar.offsetHeight) document.documentElement.style.setProperty('--ket-cta-h', (bar.offsetHeight + 14) + 'px'); };
    const fitAll = () => { fit(); lift(); };
    fitAll(); addEventListener('resize', fitAll); new MutationObserver(fitAll).observe(bar, { attributes: true, attributeFilter: ['class', 'aria-hidden'] });
    new MutationObserver(lift).observe(document.body, { attributes: true, attributeFilter: ['class'] });
    // a variant with its own prices: the struck old price follows it
    const wasEl = bar.querySelector('[data-ket-cta-was]'), priceBox = bar.querySelector('[data-ket-cta-price]');
    window.addEventListener('product:variant-changed', e => { const v = e.detail?.selectedProduct; if (!v || !wasEl) return;
      const on = !!(v.formatted_sale_price && v.formatted_price && v.formatted_sale_price !== v.formatted_price);
      wasEl.textContent = on ? v.formatted_price : ''; priceBox?.classList.toggle('is-sale', on); });
    const nameEl = bar.querySelector('[data-sticky-cta-name]'); if (!nameEl) return;
    const tick = document.createElement('div'); tick.className = 'ket-perk'; tick.setAttribute('aria-live', 'polite');
    nameEl.insertAdjacentElement('afterend', tick);
    for (let i = 0; i < 60 && !(window.zid && window.zid.products); i++) await new Promise(r => setTimeout(r, 200));
    const id = document.getElementById('product-parent-id')?.value || document.getElementById('product-id')?.value; if (!id || !window.zid?.products) return;   // the parent id exists only on products with options
    let p; try { p = await window.zid.products.get(id); } catch (e) { return; }
    const ar = (document.documentElement.lang || 'ar').startsWith('ar'), perks = [];
    const svg = d => `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
    const ICO = {
      tag: svg('<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8Z"/><circle cx="7.5" cy="7.5" r="1.5"/>'),
      truck: svg('<path d="M2 6h11v10H2zM13 9h4l4 4v3h-8"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>'),
      clock: svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
      flame: svg('<path d="M12 3c1 3 4 4.5 4 8.5a4 4 0 0 1-8 0c0-1.6.7-2.7 1.6-3.6.2 1.4 1 2.1 1.9 2.1C11 7.5 11 5 12 3Z"/>')
    };
    const num = s => +String(s || '').replace(/[^\d.]/g, '') || 0;
    const price = num(p.formatted_price), sale = num(p.formatted_sale_price);
    let off = 0;
    if (sale && price > sale) {
      off = Math.round((1 - sale / price) * 100); const save = price - sale;
      const saveTxt = String(p.formatted_price).replace(/[\d.,]+/, save.toLocaleString('en-US', { minimumFractionDigits: save % 1 ? 2 : 0, maximumFractionDigits: 2 })).trim();
      perks.push({ i: 'tag', t: ar ? `خصم ${off}% · وفّر ${saveTxt}` : `${off}% off · save ${saveTxt}`, s: ar ? `وفّر ${saveTxt}` : `Save ${saveTxt}` });
    }
    perks.push({ i: 'truck', t: ar ? 'توصيل مجاني لكل مدن المملكة' : 'Free delivery across the Kingdom', s: ar ? 'توصيل مجاني' : 'Free delivery' });
    const end = Date.parse(p.purchase_restrictions?.sale_price_period_end || '');
    if (sale && end && end > Date.now() && end - Date.now() < 48 * 3600e3) perks.push({ i: 'clock', t: ar ? 'العرض ينتهي خلال أقل من 48 ساعة' : 'Offer ends in under 48 hours', s: ar ? 'ينتهي خلال 48 ساعة' : 'Ends within 48 h', hot: true });
    const qty = +p.quantity || 0;
    if (!p.is_infinite && qty > 0 && qty <= 10) perks.push({ i: 'flame', t: ar ? `باقي ${qty} ${qty === 1 ? 'قطعة' : qty === 2 ? 'قطعتان' : 'قطع'} فقط` : `Only ${qty} left`, hot: true });
    if (off) { const tag = document.createElement('span'); tag.className = 'ket-cta-badge'; tag.setAttribute('aria-hidden', 'true'); tag.innerHTML = `<b dir="ltr">−${off}%</b>`; btn.parentElement.appendChild(tag); }
    let k = 0;
    const show = () => {
      const x = perks[k++ % perks.length], el = document.createElement('span');
      el.className = 'ket-perk__i' + (x.hot ? ' is-hot' : ''); el.innerHTML = `${ICO[x.i]}<span>${(matchMedia('(max-width: 767px)').matches && x.s) || x.t}</span>`;   // short words on a phone
      tick.querySelectorAll('.ket-perk__i:not(.is-out)').forEach(o => { o.classList.add('is-out'); setTimeout(() => o.remove(), 700); });
      tick.appendChild(el); requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('is-in')));
    };
    show(); if (perks.length > 1) setInterval(show, 3400);
  })();

  /* ---------- Delivery estimate (today + N days, from theme settings) ---------- */
  const del = $('[data-ket-delivery]');
  if (del) {
    const d = new Date(); d.setDate(d.getDate() + (+del.dataset.days || 3));
    const ar = (root.lang || 'ar').startsWith('ar');
    const ds = d.toLocaleDateString(ar ? 'ar-SA-u-ca-gregory-nu-latn' : 'en-GB', { weekday: 'long', day: 'numeric', month: 'long' });
    $('span', del).innerHTML = ar ? `اطلبه اليوم، ويوصلك <strong>${ds}</strong>` : `Order today, delivered by <strong>${ds}</strong>`;
    del.hidden = false;
  }

  /* ---------- Numbers: 1,653 style (Zid prints 1653); animated below ---------- */
  const fmtN = (v, dec) => (+v).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const counters = $$('[data-count]', page);
  counters.forEach(el => { el.textContent = fmtN(el.dataset.count, +el.dataset.dec || 0); });

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

  /* ---------- Suggested bundle: Zid bundle offers are not in the page data, so ask Zid's API.
     The offer says what to add in its description; the related product named there gives the
     picture and the add-to-cart button. ---------- */
  const relTrack = $('#relTrack');
  const pid = $('#product-id')?.value;
  if (relTrack && pid && !$('.ket .bundle')) {
    fetch('/api/v1/products/bundle-offers?product_ids=' + encodeURIComponent(pid), { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(r => r.ok ? r.json() : null).then(d => {
        const bo = d?.payload?.[0]; if (!bo) return;
        const esc = v => String(v ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
        const desc = (bo.description || '').toLowerCase();
        const match = $$('.prod', relTrack).find(p => { const n = p.querySelector('h3')?.textContent.trim().toLowerCase(); return n && desc.includes(n); });
        const own = $('.g-slide img')?.currentSrc || $('.g-slide img')?.src;
        const media = match?.querySelector('.prod__link img, .prod__link svg');
        const add = match?.querySelector('[data-add-to-cart]');
        const box = document.createElement('div'); box.className = 'bundle';
        box.innerHTML = `<div class="bundle__thumbs"><div>${own ? `<img src="${esc(own)}" alt="" loading="lazy">` : ''}</div>${media ? `<div style="display:grid;place-items:center">${media.outerHTML}</div>` : ''}</div>
          <div class="bundle__text"><strong>${esc(bo.name)}</strong>${bo.description ? `<p>${esc(bo.description)}</p>` : ''}</div>
          ${add ? `<button class="btn btn-primary" type="button" data-add-to-cart="${esc(add.dataset.addToCart)}"><span class="btn-label">${esc(page.dataset.bundleAdd || '')} ${esc(match.querySelector('h3')?.textContent.trim())}</span></button>` : ''}`;
        relTrack.before(box);
        if (add) box.querySelector('[data-add-to-cart]').addEventListener('click', e => { e.preventDefault(); add.click(); });
        if (G) gsap.from(box, { y: 30, opacity: 0, duration: .9, ease: 'power3.out' });
      }).catch(() => {});
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

  /* ---------- Count-ups: every number runs from 0 (or from its data-from) to its value, like a speedometer ---------- */
  counters.forEach(el => {
    const to = +el.dataset.count, dec = +el.dataset.dec || 0, o = { v: +el.dataset.from || 0 };
    el.textContent = fmtN(o.v, dec);
    gsap.to(o, { v: to, duration: 1.8, ease: 'power3.out', scrollTrigger: { trigger: el.closest('.pill, .rating, .stock, .proof, .rev, .prod, .price') || el, start: 'top 92%', once: true },
      onUpdate: () => { el.textContent = fmtN(dec ? o.v : Math.round(o.v), dec); } });
  });
  // stars pop in one after the other
  [['.ket .rating', '.ket .rating .star'], ['.ket .proof', '.ket .proof .star'], ['.ket .rev__meta', '.ket .rev__meta .star']].forEach(([trig, sel]) => {
    if ($(sel)) gsap.fromTo(sel, { scale: .2, opacity: 0, rotate: -35 }, { scale: 1, opacity: 1, rotate: 0, duration: .55, stagger: .16, ease: 'back.out(2.4)', scrollTrigger: { trigger: trig, start: 'top 90%', once: true } });
  });
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
