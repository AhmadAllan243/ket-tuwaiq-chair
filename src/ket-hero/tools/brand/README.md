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

## Round 4 (Oct 2026): the peeking gazelle is the client's own animation

The hand-built walkers and the traced ارحبوووو rig were dropped (they didn't look good enough). The peek is now the
client's "hello" video (`assets-src/mascot/new/hello-reference.mp4`), trimmed before its speech bubble and cropped past the pole,
so the gazelle grips the screen edge itself:

```
F="trim=end=5.5,setpts=PTS-STARTPTS,crop=500:760:26:110,curves=all='0/0 0.86/0.88 0.93/1 1/1'"
ffmpeg -i hello-reference.mp4 -vf "$F" -an -c:v libx264 -preset slow -crf 27 -pix_fmt yuv420p -movflags +faststart media/gazelle-peek.mp4
ffmpeg -i hello-reference.mp4 -vf "$F" -an -c:v libvpx-vp9 -b:v 0 -crf 40 -row-mt 1 media/gazelle-peek.webm
ffmpeg -sseof -0.1 -i media/gazelle-peek.mp4 -frames:v 1 -c:v libwebp -quality 80 media/gazelle-peek-end.webp   # reduced motion
```

`gazellePeek()` in `ket-product.html` plays it (muted, inline, `mix-blend-mode:multiply` removes the white background) and puts
the line in plain bold text above the gazelle once it smiles (~4 s). Used for the welcome ارحبوووو (left edge, after the box),
the buy box and the reviews. `media/` must ship next to `index.html`. `patch_round4.py` applied this round.
