#!/usr/bin/env bash
# Baut den LXNCE E-Mail-Signatur-Generator aus einem frischen antonreshetov/mysigmail-Checkout.
# Aufruf: ./build.sh <checkout>   Ergebnis: <checkout>/dist  (Inhalt nach public_html/signatur/ hochladen)
set -euo pipefail
SRC="$(cd "$1" && pwd)"; HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$SRC"
git checkout -q . && git clean -fdq public src
python3 "$HERE/patch.py" .
[ -d node_modules ] || npm install --no-audit --no-fund
npx vite build --base /signatur/
cp "$HERE/assets/htaccess" dist/.htaccess
cp LICENSE dist/quellcode/LICENSE.txt
( cd "$HERE/.." && rm -f "$SRC/dist/quellcode/lxnce-signatur-anpassungen.zip" && zip -qr "$SRC/dist/quellcode/lxnce-signatur-anpassungen.zip" "$(basename "$HERE")" )
echo "fertig: $SRC/dist"
