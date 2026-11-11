#!/bin/zsh
# Builds the zip for Zid's "upload theme" (dashboard → themes → ⋮ → تعديل): vitrin build, minus the
# developer-only folders, with the editor thumbnails shrunk so it stays under 10 MB.
# usage: zsh ket/make-upload-zip.sh [out.zip]      (from src/zid-theme)
set -e
cd ${0:A:h}/..
OUT=${1:-${0:A:h}/../../../../ket-theme-home.zip}
npx -y @zidsa/vitrin-cli@1.4.0 --no-color build . < /dev/null > /dev/null
Z=$(ls -t zid-theme-*.zip | head -1)
mv "$Z" "$OUT"
zip -q -d "$OUT" "ket/*" "docs/*" "tests/*" playwright.config.js || true
T=$(mktemp -d); (cd $T && unzip -q "$OUT" "sections/*.png" && python3 -c "
from PIL import Image; import glob
for f in glob.glob('sections/*.png'):
    im = Image.open(f); im.thumbnail((640, 640)); im.save(f, optimize=True)" && zip -q "$OUT" sections/*.png); rm -rf $T
ls -la "$OUT"
