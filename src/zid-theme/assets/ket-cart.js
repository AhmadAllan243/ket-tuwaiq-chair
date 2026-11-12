/* KET cart drawer, every page (components/ket/cart-drawer.jinja, design: ket-product.html).
   The bag in the header opens it; it also slides in by itself whenever something is added (the theme's
   "cart:updated" event). Lines, quantities, removal and the total are Zid's cart; checkout is Zid's own. */
(() => {
  const root = document.getElementById('ket-cart'); if (!root) return;
  const drawer = root.querySelector('.drawer'), scrim = root.querySelector('.scrim');
  const body = root.querySelector('[data-cart-body]'), foot = root.querySelector('[data-cart-foot]'), count = root.querySelector('[data-cart-count]');
  const T = k => root.dataset['t' + k[0].toUpperCase() + k.slice(1)] || '';
  const ico = n => root.querySelector(`template[data-icon="${n}"]`).innerHTML;
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const zid = async () => { for (let i = 0; i < 60 && !(window.zid && window.zid.cart); i++) await new Promise(r => setTimeout(r, 200)); return window.zid && window.zid.cart; };
  let cart = null, busy = false, justAdded = false, lastFocus = null;

  const qtyOf = c => (c && (c.cart_items_quantity ?? (c.products || []).reduce((a, p) => a + (+p.quantity || 0), 0))) || 0;
  const badge = c => document.querySelectorAll('[data-cart-badge]').forEach(el => { const n = qtyOf(c); el.textContent = n; el.hidden = !n; });
  const thumb = p => { const im = (p.images || [])[0]; return im ? (im.thumbs && (im.thumbs.small || im.thumbs.thumbnail)) || im.origin || '' : ''; };

  function render() {
    const items = (cart && cart.products) || [], n = qtyOf(cart);
    count.textContent = n ? `(${n})` : '';
    if (!items.length) {
      body.innerHTML = `<div class="empty"><img class="gz" src="${root.dataset.gz}" alt="" width="150" height="150"><h3>${esc(T('emptyTitle'))}</h3><p>${esc(T('emptyBody'))}</p><button class="btn btn-outline" type="button" data-cart-close><span class="btn-label">${esc(T('continue'))}</span></button></div>`;
      foot.innerHTML = ''; return;
    }
    body.innerHTML = (justAdded ? `<div class="drawer__success"><img class="gz" src="${root.dataset.gz}" alt="" width="56" height="56"><span>${esc(T('added'))}</span></div>` : '') +
      items.map(p => {
        const was = +p.price_before > +p.price + .009 ? p.price_before_string : '';
        return `<div class="citem" data-line="${esc(p.id)}">
          <a class="citem__img" href="${esc(p.url || '#')}">${thumb(p) ? `<img src="${esc(thumb(p))}" alt="" loading="lazy">` : ''}</a>
          <div><h3><a href="${esc(p.url || '#')}">${esc(p.name)}</a></h3><p class="citem__price">${esc(p.total_string || p.price_string)}${was ? `<s>${esc(p.total_before_string || was)}</s>` : ''}</p>
            <div class="stepper" role="group" aria-label="${esc(T('qty'))}"><button type="button" data-d="-1" aria-label="${esc(T('dec'))}"${+p.quantity <= 1 ? ' disabled' : ''}>${ico('minus')}</button><span class="stepper__val"><span>${+p.quantity || 1}</span></span><button type="button" data-d="1" aria-label="${esc(T('inc'))}">${ico('plus')}</button></div>
          </div>
          <button class="citem__rm" type="button" data-rm>${esc(T('remove'))}</button>
        </div>`; }).join('');
    const total = (cart.total && cart.total.value_string) || '';
    foot.innerHTML = `<div class="drawer__total"><span>${esc(T('total'))}</span><span class="num">${esc(total)}</span></div><small>${esc(T('tax'))}</small>
      ${T('closed') ? `<button class="btn btn-primary btn-block" type="button" disabled><span class="btn-label">${esc(T('closed'))}</span></button>` : `<a class="btn btn-primary btn-block" href="/checkout"><span class="btn-label">${esc(T('checkout'))}</span></a>`}
      <a class="ket-cart__view" href="${esc(root.dataset.cartUrl)}">${esc(T('view'))}</a>`;
  }

  async function load() { if (!(await zid())) return; try { cart = await window.zid.cart.get(); badge(cart); render(); } catch (e) {} }

  function open(added) {
    justAdded = !!added; lastFocus = document.activeElement;
    render(); load();
    drawer.classList.add('is-open'); scrim.classList.add('is-open'); drawer.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('ket-cart-open'); if (window.lenis && window.lenis.stop) window.lenis.stop();
    setTimeout(() => drawer.querySelector('[data-cart-close].icon-btn')?.focus({ preventScroll: true }), 60);
  }
  function close() {
    drawer.classList.remove('is-open'); scrim.classList.remove('is-open'); drawer.setAttribute('aria-hidden', 'true');
    document.documentElement.classList.remove('ket-cart-open'); if (window.lenis && window.lenis.start) window.lenis.start();
    justAdded = false; lastFocus?.focus?.({ preventScroll: true });
  }
  window.ketCart = { open, close };

  // quantity and removal (one change at a time; the drawer redraws from Zid's answer)
  root.addEventListener('click', async e => {
    if (e.target.closest('[data-cart-close]')) { close(); return; }
    const line = e.target.closest('[data-line]'); if (!line || busy) return;
    const step = e.target.closest('[data-d]'), rm = e.target.closest('[data-rm]'); if (!step && !rm) return;
    const p = (cart.products || []).find(x => String(x.id) === line.dataset.line); if (!p || !(await zid())) return;
    busy = true; line.classList.add('is-busy');
    try {
      const q = (+p.quantity || 1) + (step ? +step.dataset.d : 0);
      if (rm || q < 1) await window.zid.cart.removeProduct({ product_id: p.id }, { showErrorNotification: true });
      else await window.zid.cart.updateProduct({ product_id: p.id, quantity: q }, { showErrorNotification: true });
      cart = await window.zid.cart.get(); justAdded = false; badge(cart); render();
      window.dispatchEvent(new CustomEvent('ket:cart-changed'));
    } catch (err) { line.classList.remove('is-busy'); }
    busy = false;
  });

  // the bag in the header opens the drawer instead of leaving the page
  document.addEventListener('click', e => {
    const a = e.target.closest('a.cart-btn'); if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault(); open(false);
  });
  document.addEventListener('keydown', e => {
    if (!drawer.classList.contains('is-open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'Tab') {   // keep focus inside the open drawer
      const f = [...drawer.querySelectorAll('button:not([disabled]), a[href]')].filter(x => x.offsetParent !== null); if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f.at(-1).focus(); }
      else if (!e.shiftKey && document.activeElement === f.at(-1)) { e.preventDefault(); f[0].focus(); }
    }
  });
  // something was added anywhere on the site: show it in the drawer
  window.addEventListener('cart:updated', e => { if ((e.detail || {}).action === 'add') open(true); });
})();
