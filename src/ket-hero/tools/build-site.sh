#!/bin/zsh
# Usage: tools/build-site.sh <out-dir>   (needs the source page served on :5178)
set -e
HERE=${0:A:h}/..; ROOT=$HERE/..; OUT=${1:?out dir}
cd $HERE && npx vite build --logLevel warn
cp dist/ket-hero.js $ROOT/ket-hero.js && mkdir -p $ROOT/models && cp dist/models/tuwaiq-chair.glb $ROOT/models/
node tools/prerender.cjs http://localhost:5178/ket-product.html /tmp/ket-prerendered.$$.html
mkdir -p $OUT/models
python3 tools/embed.py /tmp/ket-prerendered.$$.html $OUT/index.html
cp dist/ket-hero.js $OUT/ && cp dist/models/tuwaiq-chair.glb $OUT/models/
cp $OUT/index.html $ROOT/ket-tuwaiq-chair.html
echo "site ready in $OUT"
