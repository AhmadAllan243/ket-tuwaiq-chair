/* KET, every page: the header logo folds into the smile once the page scrolls, and the mobile
   menu opens just below the header + announcement bar. */

/* EN / ع button: Zid's locale switch (/locales/<lang[-country]>?redirect_to=…), keeping the
   country from the address (/en-kw/… → ar-kw; no prefix = the store's default country). */
window.ketSwitchLang = (lang) => {
  const parts = location.pathname.split('/');
  const m = /^(ar|en)(-[a-z]{2})?$/i.exec(parts[1] || '');
  const locale = lang + (m && m[2] ? m[2].toLowerCase() : '');
  if (m) parts[1] = locale; else parts.splice(1, 0, locale);
  location.href = '/locales/' + locale + '?redirect_to=' + encodeURIComponent(parts.join('/') + location.search);
};

/* night mode: the moon in the header; the choice is kept for the next visit (layout.jinja applies it before paint) */
window.ketToggleTheme = () => {
  const dark = document.documentElement.dataset.theme !== 'dark';
  if (dark) document.documentElement.dataset.theme = 'dark'; else delete document.documentElement.dataset.theme;
  try { localStorage.setItem('ketTheme', dark ? 'dark' : 'light'); } catch (e) {}
  document.querySelectorAll('.ket-theme-btn').forEach(b => b.setAttribute('aria-pressed', dark));
};
document.querySelectorAll('.ket-theme-btn').forEach(b => b.setAttribute('aria-pressed', document.documentElement.dataset.theme === 'dark'));

(() => {
  const top = document.getElementById('ket-top'), header = document.getElementById('header');
  if (!top || !header) return;
  const setH = () => document.documentElement.style.setProperty('--ket-top-h', top.getBoundingClientRect().height + 'px');
  const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); addEventListener('resize', setH);
  onScroll(); setH(); setTimeout(setH, 400);
})();
