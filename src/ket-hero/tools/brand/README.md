# Brand asset tools (client round 2, Oct 2026)

- `trace_logo.py` traces the ket wordmark, the TANASOUB lockup and the smile from the client's logo sheet (`assets-src/brand/logo_crop.png`) with potrace (`pip install potracer`).
- `gazelles.py` turns the client's grey-wash gazelle drawings into black line art plus one brand colour (output in `assets-src/mascot/colour/`). `python3 gazelles.py ../../assets-src/mascot <out>`
- `make_assets.py` packs the logo paths, the three trust shapes (`icons.json`), the gazelles and the inspiration illustration into the `const BRAND = {...}` block that is inlined in `ket-product.html`.
- `patch_brand.py` is the one-off patch that added this round to `ket-product.html` (kept for reference; already applied).

The traced logo is close but not the master file. If the client sends an SVG of the ket wordmark, swap the paths in `BRAND.KET`.

## Round 3 (Oct 2026): black-and-white gazelles that actually move

- `box_bw.py` makes the delivery gazelle: the client's black-and-white box drawing with a coloured outline around the box only.
- `patch_round3.py` is the one-off patch that applied this round (story blur, mobile story photo, footer, accordion cards, …).
- Client rule from now on: every gazelle is black and white; colour only as an outline around the box or the gazelle; no cloud or
  bubble behind what a gazelle says.

## Round 4 (Oct 2026): gazelles that move, without looking homemade

The hand-built SVG walkers and the traced ارحبوووو rig were dropped (they looked amateur).

**Peeking gazelle (welcome ارحبوووو, reviews)** = the client's own "hello" animation (`assets-src/mascot/new/hello-reference.mp4`),
trimmed before its speech bubble, cropped past the pole so the gazelle grips the screen edge, and turned into a
transparent, play-once animated WebP (`media/gazelle-peek.webp`, 12 fps). `peek_alpha4.py` does it: the white
background is flood-filled from the top and right edges, so the gazelle's own white stays solid. Frames come from:
`ffmpeg -i hello-reference.mp4 -vf "trim=end=5.5,setpts=PTS-STARTPTS,fps=12,crop=500:760:26:110,scale=300:-1" peekfr3/f_%03d.png`.

**Walking gazelle (buy box, dimensions)** = modelled and animated in Blender 5.2 (file kept on Mohammed's Mac at
`~/ket-gazelle/ket-gazelle.blend`): white emission materials plus an inverted-hull outline (solidify, flipped normals, black
back faces) give the thick black cartoon line. Body side-on, head turned to camera. Two 48-frame loops at 24 fps:
walk (lateral gait, knees lift on the swing, body bob, ear flop, tail wag, blink) and idle (head tilt, ear flick, blink).
Rendered with a transparent film to `assets-src/mascot/3d/{walk,idle}/f_*.webp`; `gz_webp.py` crops them and makes
`media/gazelle-walk.webp` / `gazelle-idle.webp` (on twos, 12 fps). `gazelleWalk()` slides it in at the stride speed
(160 render px per second) so the hooves don't skate, swaps to idle while it talks, then turns and walks out.

Text above every gazelle is plain bold text with a white letter outline (no cloud or bubble, per the client).
`patch_round4.py` / `patch_round4b.py` applied this round. `media/` must ship next to `index.html`.

## Oct 24: pop-ups off, sofa illustration moves

- All pop-up gazelles (welcome, walkers, peeks, idle) are switched off with `GAZELLE_POPUPS = false` in `ket-product.html`
  while they are refined; set it to `true` to bring them all back. The cart gazelles are unaffected.
- `illus_fx.py` splits the sofa illustration into base / steam / gazelle layers (`assets-src/brand/illus-*.webp`) and packs
  them as `ILLUS_FX`: the coffee steam sways and the sleeping gazelle breathes (CSS, off with reduced motion).
