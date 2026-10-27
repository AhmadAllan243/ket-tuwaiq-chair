/* KET, every page: the header logo folds into the smile once the page scrolls, and the mobile
   menu opens just below the header + announcement bar. */
(() => {
  const top = document.getElementById('ket-top'), header = document.getElementById('header');
  if (!top || !header) return;
  const setH = () => document.documentElement.style.setProperty('--ket-top-h', top.getBoundingClientRect().height + 'px');
  const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); addEventListener('resize', setH);
  onScroll(); setH(); setTimeout(setH, 400);
})();
