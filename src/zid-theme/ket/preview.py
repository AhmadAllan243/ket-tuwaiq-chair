"""
Local preview of the theme's product page, without a Zid store.

Renders templates/product.jinja (with layout, header and footer) through plain Jinja2 with the
Vitrin-only parts stubbed: {% vitrin_head %} / {% vitrin_body %} and "vitrin:" includes render
nothing, url_for / image_url return plain URLs, _() reads the Arabic .po file. The product is the
Tuwaiq chair from the prototype. Zid's own scripts (cart, lightbox) do not run here, and the
Growth styles come from assets/styles.css (run `npm run build` first), so this is for checking the KET layout and
motion only; the real check is `vitrin preview` on a development store.

usage: python3 ket/preview.py [en]      (run from src/zid-theme; writes .preview/index.html)
then open http://localhost:5178/zid-theme/.preview/ with the "ket" dev server running
"""
import json, os, re, sys
from jinja2 import Environment, FileSystemLoader, BaseLoader, TemplateNotFound, nodes
from jinja2.ext import Extension

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, '.preview')
LANG = sys.argv[1] if len(sys.argv) > 1 else 'ar'


class Loader(BaseLoader):
    """Theme files from disk; Zid platform includes ("vitrin:...") are empty."""
    def __init__(self):
        self.fs = FileSystemLoader(ROOT)

    def get_source(self, env, name):
        if name.startswith('vitrin:'):
            return f'<!-- {name} (Zid platform include) -->', None, lambda: True
        return self.fs.get_source(env, name)


class VitrinTags(Extension):
    tags = {'vitrin_head', 'vitrin_body'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        return nodes.Output([nodes.TemplateData('')], lineno=lineno)


def po_catalog():
    if LANG != 'ar':
        return {}
    s = open(os.path.join(ROOT, 'locale/ar/LC_MESSAGES/messages.po')).read()
    return {m.group(1): m.group(2) for m in re.finditer(r'msgid "(.*)"\nmsgstr "(.*)"', s) if m.group(2)}


CAT = po_catalog()


class Null:
    """a missing platform field: falsy, empty, and chainable (store.settings.menus.main_menu.items)"""
    def __getattr__(self, k): return NULL
    def __getitem__(self, k): return NULL
    def __call__(self, *a, **k): return NULL
    def __bool__(self): return False
    def __iter__(self): return iter(())
    def __len__(self): return 0
    def __str__(self): return ''
    def __html__(self): return ''
    def __eq__(self, o): return o is None or isinstance(o, Null) or o == '' or o is False
    def __hash__(self): return 0
    def __lt__(self, o): return False
    __gt__ = __le__ = __ge__ = __lt__
    def __int__(self): return 0
    def __float__(self): return 0.0


NULL = Null()


class Obj(dict):
    """dict with attribute access; missing keys are a chainable empty value, like the platform's objects"""
    def __getattr__(self, k):
        return self[k] if k in self else NULL

    def __getitem__(self, k):
        return dict.__getitem__(self, k) if k in self else NULL

    def get(self, k, d=None):
        return dict.get(self, k, d)


def obj(x):
    if isinstance(x, dict):
        return Obj({k: obj(v) for k, v in x.items()})
    if isinstance(x, list):
        return [obj(v) for v in x]
    return x


def safeget(o, path, default=None):
    for p in path.split('.'):
        o = o.get(p) if isinstance(o, dict) else getattr(o, p, None)
        if o is None:
            return default
    return o


IMG = 'https://media.zid.store/3d020177-292e-4bbd-8716-c86b494643f5/'
IMAGES = ['f64968d0-f94f-4451-92c0-1cd14c7a7e97', '7cdd8e0e-a3f3-4cc3-8175-755ebaa52d26', 'e09fc8d7-8afb-4a5d-87fb-139065934cc2',
          'cfc5e61b-953a-4e89-88f7-855583b80073', 'dcfa343f-8d7a-49e5-8072-48425603d9e7', 'e325edf2-a03d-4afe-928a-4b08d2063965',
          '255be32d-a8a5-48d8-b874-31208f331b04']
AR = LANG == 'ar'
product = obj({
    'id': 'tuwaiq', 'name': 'كرسي طويق' if AR else 'Tuwaiq Chair', 'sku': 'TC-2030', 'slug': 'tuwaiq',
    'short_description': '<p>' + ('نقوش نجد والحجاز وعسير، في تصميم واحد.' if AR else 'Najd, Hijaz and Asir patterns, in one chair.') + '</p>',
    'description': '<p>' + ('كرسي بنقوش تراثية متعددة الألوان، بمقعد وظهر محشوّين، ومساند يدين من الخشب الطبيعي، وهيكل معدني أسود نحيف.' if AR
                            else 'A heritage-pattern chair with a padded seat and back, natural wood arms and a slim black metal frame.') + '</p>',
    'formatted_price': '1,560.00 ر.س' if AR else 'SAR 1,560.00', 'formatted_sale_price': '696.00 ر.س' if AR else 'SAR 696.00',
    'discount_percentage': 55.4, 'is_taxable': True, 'in_stock': True, 'is_infinite': False, 'quantity': 80,
    'sold_products_count': 1653, 'has_options': False, 'has_fields': False,
    'images': [{'image': {'large': IMG + i + '.png'}, 'alt_text': ''} for i in IMAGES],
    'selected_product': {'id': 'tuwaiq-1', 'in_stock': True, 'is_infinite': False, 'quantity': 80, 'sold_products_count': 1653},
    'rating': {'average': 5.0, 'total_count': 326, 'ratings_5': {'count': 313}, 'ratings_4': {'count': 13}},
    'reviews': {'results': [
        {'rating': 5, 'comment': 'الكرسي أجمل من الصور، والقماش ألوانه ثابتة.' if AR else 'Even nicer than the photos, and the colours hold.', 'customer': {'name': 'نورة' if AR else 'Noura'}},
        {'rating': 5, 'comment': 'مريح جدًا ووصل بسرعة.' if AR else 'Very comfortable and arrived fast.', 'customer': {'name': 'عبدالله' if AR else 'Abdullah'}},
        {'rating': 5, 'comment': 'تغليف ممتاز وجودة عالية.' if AR else 'Great packaging and quality.', 'customer': {'name': 'سارة' if AR else 'Sara'}},
    ]},
    'metafields': [
        {'key': 'model_3d', 'data_type': 'file', 'name': {'ar': 'نموذج ثلاثي الأبعاد', 'en': '3D model'}, 'value': {'url': '/models/tuwaiq-chair.glb'}},
        {'key': 'width', 'data_type': 'number', 'name': {'ar': 'العرض', 'en': 'Width'}, 'value': 60},
        {'key': 'height', 'data_type': 'number', 'name': {'ar': 'الارتفاع', 'en': 'Height'}, 'value': 70},
        {'key': 'story_title', 'data_type': 'text', 'name': {'ar': 'عنوان الحكاية', 'en': 'Story title'}, 'value': {'ar': 'طويق', 'en': 'TUWAIQ'}},
        {'key': 'story_text', 'data_type': 'text', 'name': {'ar': 'نص الحكاية', 'en': 'Story text'},
         'value': {'ar': 'من مثلثات نجد، وشبك رواشين الحجاز، وألوان القط العسيري؛ جمعنا تنوّع النقوش السعودية في قطعة واحدة.',
                   'en': 'Najdi triangles, the lattice of Hijazi rawasheen, the colour of Asiri Al-Qatt, brought together in one piece.'}},
    ],
    'related_products': [], 'categories': [],
})
layout = json.load(open(os.path.join(ROOT, 'layout.json')))[LANG]
store = obj({'name': 'ket', 'settings': {'products': {'reviews_enabled': True, 'is_metafields_enabled': True, 'low_stock_label_enabled': True,
                                                      'low_stock_quantity_threshold': 100, 'questions_enabled': False},
                                         'checkout': {'show_checkout_as_popup': True, 'is_loyalty_enabled': False, 'gift_order_settings': {}},
                                         'general': {}}})
session = obj({'lang': LANG, 'template': 'product_details', 'is_guest': True,
               'locale': {'language': {'direction': 'rtl' if AR else 'ltr', 'code': LANG}}})

from jinja2 import ChainableUndefined
env = Environment(loader=Loader(), extensions=[VitrinTags, 'jinja2.ext.do'], autoescape=True, undefined=ChainableUndefined)
env.globals.update(_=lambda s: CAT.get(s, s), url_for=lambda *a, **k: '#', image_url=lambda src, **k: src, safeget=safeget,
                   settings=obj(layout), store=store, session=session, request=obj({}), user_custom_css=None)
env.filters['asset_url'] = lambda p: '../assets/' + p

html = env.get_template('templates/product.jinja').render(product=product)
# Growth's Tailwind classes, compiled in the browser (preview only; the real theme ships assets/styles.css)
# Growth styles: assets/styles.css (npm run build) is linked by the layout itself
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w').write(html)
print('wrote', os.path.join(OUT, 'index.html'), len(html), 'bytes')
