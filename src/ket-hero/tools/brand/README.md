# Brand asset tools (client round 2, Oct 2026)

- `trace_logo.py` traces the ket wordmark, the TANASOUB lockup and the smile from the client's logo sheet (`assets-src/brand/logo_crop.png`) with potrace (`pip install potracer`).
- `gazelles.py` turns the client's grey-wash gazelle drawings into black line art plus one brand colour (output in `assets-src/mascot/colour/`). `python3 gazelles.py ../../assets-src/mascot <out>`
- `make_assets.py` packs the logo paths, the three trust shapes (`icons.json`), the gazelles and the inspiration illustration into the `const BRAND = {...}` block that is inlined in `ket-product.html`.
- `patch_brand.py` is the one-off patch that added this round to `ket-product.html` (kept for reference; already applied).

The traced logo is close but not the master file. If the client sends an SVG of the ket wordmark, swap the paths in `BRAND.KET`.
