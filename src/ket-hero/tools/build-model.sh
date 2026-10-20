#!/bin/zsh
# Repairs the AI-generated chair model and compresses it for the web.
# Sources live in assets-src/ (chair2-source.glb from the designer, fabric-photo.png = product photo 7).
set -e
cd ${0:A:h}/..
python3 tools/repair_chair.py assets-src/chair2-source.glb assets-src/chair-fixed.glb assets-src/fabric-photo.png
npx -y @gltf-transform/cli@4 optimize assets-src/chair-fixed.glb public/models/tuwaiq-chair.glb \
  --compress meshopt --texture-compress webp --texture-size 2048 --join false --instance false --flatten false --simplify false
