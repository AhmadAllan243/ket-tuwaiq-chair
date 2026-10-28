#!/bin/zsh
# Preview the theme on the KET Test dev store with test-only settings (sample customer moments).
# ket/test-store-settings.json is merged into layout.json just for the upload and layout.json is
# restored right after, so the samples never become the theme's defaults for a real store.
# usage: zsh ket/preview-test-store.sh      (from src/zid-theme; needs `vitrin login`)
set -e
cd ${0:A:h}/..
cp layout.json .layout.json.bak
trap 'mv .layout.json.bak layout.json' EXIT
python3 - <<'PY'
import json
d = json.load(open('layout.json')); t = json.load(open('ket/test-store-settings.json'))
for l in t: d.setdefault(l, {}).update(t[l])
json.dump(d, open('layout.json', 'w'), indent=2, ensure_ascii=False)
PY
npx -y @zidsa/vitrin-cli@1.4.0 --no-color preview 3276734 . < /dev/null
