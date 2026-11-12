"""
Local preview of the KET departments page (templates/categories.jinja) and the search results (templates/products.jinja).
usage: python3 ket/preview_pages.py [en]      (run from src/zid-theme; writes .preview/categories.html, .preview/search.html)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'preview.py')).read()
src = src[:src.index("html = env.get_template('templates/product.jinja')")]
exec(compile(src, 'preview.py', 'exec'))
AR = LANG == 'ar'
cats = [{'id': 445400, 'name': 'تخفيضات' if AR else 'Discounts section', 'slug': 'sale'},
        {'id': 444476, 'name': 'قسم النباتات الصناعية' if AR else 'Industrial Plants', 'slug': 'plants'},
        {'id': 444477, 'name': 'قسم الطاولات' if AR else 'Tables Section', 'slug': 'tables'},
        {'id': 444478, 'name': 'قسم الإضاءات' if AR else 'Lighting Section', 'slug': 'lights'},
        {'id': 444490, 'name': 'قسم السجاد' if AR else 'Carpet Section', 'slug': 'rugs'},
        {'id': 444491, 'name': 'قسم مستلزمات المنزل' if AR else 'Decorating supplies', 'slug': 'home'}]
env.globals['url_for'] = lambda name, **k: '/categories/%s/%s' % (k.get('category_id'), k.get('slug')) if name == 'category_details' else '/products/' + k.get('slug', '') if name == 'product_details' else '#'
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'categories.html'), 'w').write(env.get_template('templates/categories.jinja').render(categories=[obj(c) for c in cats]))
prods = [obj({'id': f'p{i}', 'name': n, 'slug': f'p{i}', 'price': pr, 'sale_price': sp, 'has_options': False,
              'formatted_price': f'{pr:,.2f} ر.س', 'formatted_sale_price': f'{sp:,.2f} ر.س' if sp else None,
              'main_image': {'image': {'large': IMG + IMAGES[i % len(IMAGES)] + '.png'}}})
         for i, (n, pr, sp) in enumerate([('كرسي طويق', 1400, 696), ('طاولة TM', 750, 296), ('أبجورة ARKAN', 349, None), ('شجرة فيكس', 454, None), ('سجادة', 500, 390)])]
session.query_params = obj({'q': 'طاولة'})
open(os.path.join(OUT, 'search.html'), 'w').write(env.get_template('templates/products.jinja').render(products=obj({'results': prods, 'count': 5, 'page': 1})))
print('wrote categories.html, search.html')
