#!/usr/bin/env bash
# Baut LXNCE PDF aus einem frischen alam00000/bentopdf-Checkout. Aufruf: ./build.sh <checkout>
set -euo pipefail
SRC="$(cd "$1" && pwd)"; HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$SRC"
git checkout -q . && git clean -fdq public src
python3 "$HERE/patch.py" .
[ -d node_modules ] || npm ci --no-audit --no-fund
export SIMPLE_MODE=true DISABLE_GITHUB_STARS=true \
  VITE_BRAND_NAME="LXNCE PDF" VITE_DEFAULT_LANGUAGE=de SITE_URL=https://pdf.lxnce.digital \
  VITE_WASM_PYMUPDF_URL=/wasm/pymupdf/ VITE_WASM_GS_URL=/wasm/gs/ VITE_WASM_CPDF_URL=/wasm/cpdf/ \
  VITE_TESSERACT_WORKER_URL=/wasm/ocr/worker.min.js VITE_TESSERACT_CORE_URL=/wasm/ocr/core \
  VITE_TESSERACT_LANG_URL=/wasm/ocr/lang-data VITE_TESSERACT_AVAILABLE_LANGUAGES=eng,deu \
  VITE_OCR_FONT_BASE_URL=/wasm/ocr/fonts VITE_EMBEDPDF_FONTS_URL=/fonts/embedpdf
# wie "npm run build", aber ohne den SEO-Audit von bentopdf.com
node scripts/generate-blog.mjs && node scripts/generate-static-tool-links.mjs && npx tsc && npx vite build \
  && node scripts/enhance-seo-pages.mjs && NODE_OPTIONS='--max-old-space-size=3072' node scripts/generate-i18n-pages.mjs \
  && node scripts/generate-sitemap.mjs && node scripts/generate-security-headers.mjs
python3 "$HERE/postbuild.py" dist
# Quellcode der Anpassungen für die AGPL-Quellcode-Seite mitliefern
( cd "$HERE/.." && rm -f "$SRC/dist/quellcode/lxnce-pdf-anpassungen.zip" && zip -qr "$SRC/dist/quellcode/lxnce-pdf-anpassungen.zip" "$(basename "$HERE")" -x "$(basename "$HERE")/vendor/*" )
cp LICENSE dist/quellcode/LICENSE.txt
