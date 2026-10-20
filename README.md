# KET · Tuwaiq Chair product page (concept)

Live: https://ahmadallan243.github.io/ket-tuwaiq-chair/

## Edit `src/`, not the files at the root

The files at the repo root (`index.html`, `ket-hero.js`, `models/`) are **build output** served by
GitHub Pages. They are regenerated on every build, so edits made to them directly are lost.

| Path | What it is |
|---|---|
| `src/ket-product.html` | The product page source: all sections, data (`STORE`), styles and scripts |
| `src/ket-hero/` | The 3D scroll hero (React Three Fiber + Vite) and the build/test tools |
| `src/ket-hero/assets-src/` | Model sources (`chair2-source.glb`), fabric photo, mascot drawings |

## Build

Requires Node 18+, Python 3 with Pillow, and Google Chrome (used headless).

```bash
cd src/ket-hero && npm install
# serve src/ on :5178 (the build pre-renders the page from there)
python3 -m http.server 5178 -d ..   # in a second terminal
tools/build-model.sh                # only when the 3D model changes
tools/build-site.sh "$PWD/../site-preview"
```

`build-site.sh` builds the hero bundle, pre-renders the page (so it reads fully in previews that
don't run JavaScript, like the iPhone file preview), embeds the product photos, and writes the
finished site to `src/site-preview/`. Preview it at `http://localhost:5178/site-preview/`.

## Publish

Copy `src/site-preview/index.html`, `ket-hero.js` and `models/tuwaiq-chair.glb` to the repo root,
then commit **both** the `src/` changes and the root files together.

## Checks

`src/ket-hero/tools/` has headless-Chrome checks (`test-hero`, `test-pins`, `test-counters`,
`test-story`, `test-moments`, …) that capture screenshots and report errors.
