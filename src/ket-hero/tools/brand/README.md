# Brand asset tools (client round 2, Oct 2026)

- `trace_logo.py` traces the ket wordmark, the TANASOUB lockup and the smile from the client's logo sheet (`assets-src/brand/logo_crop.png`) with potrace (`pip install potracer`).
- `gazelles.py` turns the client's grey-wash gazelle drawings into black line art plus one brand colour (output in `assets-src/mascot/colour/`). `python3 gazelles.py ../../assets-src/mascot <out>`
- `make_assets.py` packs the logo paths, the three trust shapes (`icons.json`), the gazelles and the inspiration illustration into the `const BRAND = {...}` block that is inlined in `ket-product.html`.
- `patch_brand.py` is the one-off patch that added this round to `ket-product.html` (kept for reference; already applied).

The traced logo is close but not the master file. If the client sends an SVG of the ket wordmark, swap the paths in `BRAND.KET`.

## Round 3 (Oct 2026): black-and-white gazelles that actually move

- `rig_arhab.py` cuts the client's "ارحبوووو" drawing (`assets-src/mascot/new/arhab.jpg`) into vector parts
  (body, ears, head, mouth, eyes, paws; each with its black ink and white fill) → `assets-src/mascot/rigs/arhab.json`.
  Ears that touch the head and antlers are split along the ink from seed points, so they move without leaving a doubled line.
- `gazelle-rigs.js` is the animator (no libraries), inlined in `ket-product.html`:
  `welcome()` = the edge line draws in, the paws grip it, the head slides out, looks around and blinks, then says ارحبوووو;
  `walk('walk' | 'hop' | 'sit', line, small, link)` = the same head on a drawn body with four legs that walks, hops or sits along
  the bottom with ear flops, blinks, a wagging tail and a talking mouth. Open `gazelle-lab.html` (served from the repo root) to try them.
- `box_bw.py` makes the delivery gazelle: the client's black-and-white box drawing with a coloured outline around the box only.
- `patch_round3.py` is the one-off patch that applied this round (story blur, mobile story photo, footer, accordion cards, …).
- Client rule from now on: every gazelle is black and white; colour only as an outline around the box or the gazelle; no cloud or
  bubble behind what a gazelle says.
