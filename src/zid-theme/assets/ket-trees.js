/* KET trees department (design: ket-trees.html): the planting banner's headline, the initiative page, and their motion.
   The markup is components/ket/trees-banner.jinja and trees-page.jinja; the watering loader is in ket-category.js. */
(() => {
  const KC = document.querySelector('.kc--trees'); if (!KC) return;
  const $ = (s, c = document) => c.querySelector(s);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const G = !!(window.gsap && window.ScrollTrigger) && !reduce;
  const ic = (n, s, w) => (typeof icon === 'function' && typeof ICON !== 'undefined' && ICON[n] ? icon(n, s, w) : '');   // ket-brand.js (arrow added by ket-category.js)

  // the headline: words, two picture pills and the green highlight, as on the rest of the store
  const h = $('#ptTitle');
  if (h) {
    const W = str => str.split(' ').map(w => `<span class="w">${w}</span>`).join(' ');
    const pill = (src, cls) => `<span class="w hero__pill ${cls}"><img src="${src}" alt=""></span>`;
    const sprout = $('.plant__sprout')?.getAttribute('src') || '', leaf = (window.KET_CAT && KET_CAT.tilePhoto) || $('.wp__p--ph img')?.getAttribute('src') || '';
    h.innerHTML = `${W(h.dataset.l1)} ${pill(sprout, 'is-cut')} <span class="hero__pink">${W(h.dataset.l2)}</span> <span class="w hero__mark">${h.dataset.mark}</span> ${pill(leaf, 'hero__pill--p')} ${W(h.dataset.l3)} <span class="w">🇸🇦</span>`;
  }
  const arr = ic('arrow', 18, 2); ['#pMoreArr', '#gArr'].forEach(s => { const el = $(s); if (el) el.innerHTML = arr; });
  const wa = $('#wpArr'); if (wa) wa.innerHTML = ic('arrow', 40, 1.6);
  const gx = $('#gClose'); if (gx) gx.innerHTML = ic('close', 22);

  // the initiative page
  const green = $('#green');
  if (green) {
    const open = () => {
      green.showModal(); document.documentElement.style.overflow = 'hidden';
      if (G) {
        gsap.fromTo('.green__in', { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: .7, ease: 'expo.out' });
        gsap.fromTo('.green__copy > *', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .7, stagger: .06, delay: .15, ease: 'expo.out' });
        gsap.fromTo('.green__sprout', { scaleY: 0 }, { scaleY: 1, duration: 1.1, delay: .35, ease: 'elastic.out(1,.6)' });
      }
    };
    const close = () => { green.close(); };
    green.addEventListener('close', () => { document.documentElement.style.overflow = ''; });
    $('#pMore')?.addEventListener('click', open);
    $('#gClose')?.addEventListener('click', close);
    green.addEventListener('click', e => { if (e.target === green) close(); });
    $('#gGo')?.addEventListener('click', () => { close(); setTimeout(() => { const all = $('#all'); if (all) scrollTo({ top: all.getBoundingClientRect().top + scrollY - 70, behavior: 'smooth' }); }, 60); });
  }

  // the banner comes in as it scrolls into view; the strip's pills pop
  if (G && $('.plant')) {
    gsap.registerPlugin(ScrollTrigger);
    gsap.timeline({ scrollTrigger: { trigger: '.plant', start: 'top 78%' } })
      .from('.plant__card', { clipPath: 'inset(10% 6% 0% 6% round 60px)', duration: 1.4, ease: 'expo.out' }, 0)
      .from('#ptTitle .w:not(.hero__pill)', { y: 26, opacity: 0, duration: .9, stagger: .05, ease: 'expo.out' }, .45)
      .from('#ptTitle .hero__pill', { scale: 0, duration: .9, stagger: .15, ease: 'back.out(1.8)' }, .8)
      .from('#ptTitle .hero__mark', { '--ms': 0, duration: .8, ease: 'expo.out' }, 1)
      .from('.plant__ey, .plant__sub, .plant__btns', { y: 24, opacity: 0, duration: .9, stagger: .08, ease: 'expo.out' }, .55)
      .from('.plant__woman', { y: 60, opacity: 0, duration: 1.1, ease: 'expo.out' }, .3)
      .from('.plant__soil', { scaleX: .2, opacity: 0, duration: .7, ease: 'back.out(2)' }, .7)
      .from('.plant__sprout', { scaleY: 0, duration: 1.4, ease: 'elastic.out(1,.55)' }, .95)
      .from('.plant__sun', { scale: 0, duration: 1.2, ease: 'expo.out' }, .4);
    gsap.from('.wp__p', { y: 50, opacity: 0, scale: .9, duration: .9, stagger: .09, ease: 'back.out(1.6)', scrollTrigger: { trigger: '#wp', start: 'top 88%' } });
  }
})();
