"""
Local preview of the KET category page (templates/category.jinja) without a Zid store; same stubs as ket/preview.py,
real Zid product photos. usage: python3 ket/preview_category.py [en]  → .preview/category.html
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'preview.py')).read()
exec(compile(src[:src.index("html = env.get_template('templates/product.jinja')")], 'preview.py', 'exec'))

AR = LANG == 'ar'
subs = [{'id': 11, 'name': 'طاولات قهوة' if AR else 'Coffee tables', 'slug': 'coffee'}, {'id': 12, 'name': 'طاولات جانبية' if AR else 'Side tables', 'slug': 'side'},
        {'id': 13, 'name': 'أطقم' if AR else 'Sets', 'slug': 'sets'}]
NAMES = ['طاولة قهوة مدار', 'طاولة خدمة BELLO', 'طقم طاولات لينك', 'طاولة لاكسي A', 'طاولة TM الرئيسية', 'طاولة تراس - كونسول', 'طاولة قهوة كادن', 'طاولة غولدن ليفز', 'طاولة جانبية سولا']
prods = [{'id': f'p{i}', 'name': NAMES[i], 'slug': f'p{i}', 'price': 800 + i * 70, 'sale_price': (400 + i * 30) if i % 3 else None,
          'has_options': i == 4, 'categories': [{'id': subs[i % 3]['id']}], 'main_image': {'image': {'large': IMG + IMAGES[i % len(IMAGES)] + '.png'}}} for i in range(9)]
TREES = 'trees' in sys.argv   # python3 ket/preview_category.py [en] [trees] → .preview/trees.html
category = obj({'id': 444476, 'name': 'قسم النباتات الصناعية' if AR else 'Industrial Plants', 'description': '', 'sub_categories': []}) if TREES else obj({'id': 444477, 'name': 'قسم الطاولات' if AR else 'Tables', 'description': '', 'sub_categories': []})
products = obj({'results': prods, 'count': 30, 'page': 1})
env.globals['url_for'] = lambda name, **k: '/products/' + k.get('slug', '')
env.globals['session'] = obj({**session, 'query_params': {}, 'url': {}})
html = env.get_template('templates/category.jinja').render(category=category, products=products)
name = 'trees.html' if TREES else 'category.html'
open(os.path.join(OUT, name), 'w').write(html)
print('wrote', os.path.join(OUT, name), len(html), 'bytes')
