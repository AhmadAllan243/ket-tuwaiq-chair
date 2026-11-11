"""
Local preview of the KET home section (sections/ket-home.jinja) inside the theme layout, without a Zid store.
Same stubs as ket/preview.py; the deals use real Zid product photos so the cut-out can be checked.

usage: python3 ket/preview_home.py [en]      (run from src/zid-theme; writes .preview/home.html)
then open http://localhost:5178/zid-theme/.preview/home.html with the "ket" dev server running
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'preview.py')).read()
src = src[:src.index("html = env.get_template('templates/product.jinja')")]
exec(compile(src, 'preview.py', 'exec'))

AR = LANG == 'ar'
deal = lambda i, name, price, sale, qty: {'id': f'd{i}', 'name': name, 'slug': f'd{i}', 'price': price, 'sale_price': sale,
    'formatted_price': f'{price:,.2f} ر.س', 'formatted_sale_price': f'{sale:,.2f} ر.س' if sale else None, 'quantity': qty, 'is_infinite': False,
    'has_options': False, 'main_image': {'image': {'large': IMG + IMAGES[i % len(IMAGES)] + '.png'}}}
sec = obj({
    'dept_tables': {'id': 444477, 'slug': 'tables', 'name': 'الطاولات' if AR else 'Tables', 'products_count': 20},
    'dept_lamps': {'id': 444478, 'slug': 'lamps', 'name': 'الأبجورات' if AR else 'Lamps', 'products_count': 14},
    'deals': {'results': [deal(0, 'كرسي طويق', 1560, 696, 8), deal(2, 'طاولة TM', 750, 296, 4), deal(3, 'قطعة بدون خصم', 400, None, 0)]},
    'deals_stock_scale': 30,
})
env.globals['url_for'] = lambda name, **k: '/products/' + k.get('slug', '')
page = env.from_string('{% extends "layout.jinja" %}{% block content %}{% with settings=sec %}{% include "sections/ket-home.jinja" %}{% endwith %}{% endblock %}')
html = page.render(sec=sec)
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'home.html'), 'w').write(html)
print('wrote', os.path.join(OUT, 'home.html'), len(html), 'bytes')
