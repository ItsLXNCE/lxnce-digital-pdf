#!/usr/bin/env bash
# Lädt die unveränderten WASM-, OCR- und Schriftpakete von npm und legt sie in vendor/ ab.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)"; V="$HERE/vendor"
rm -rf "$V"; mkdir -p "$V"/wasm/{pymupdf,gs,cpdf,ocr/core,ocr/lang-data,ocr/fonts} "$V"/fonts/embedpdf/fonts-latin@1.0.0
cd "$T"
npm pack @bentopdf/pymupdf-wasm@0.11.16 @bentopdf/gs-wasm@0.1.1 coherentpdf@2.5.5 tesseract.js@7.0.0 tesseract.js-core@7.0.0 \
  @tesseract.js-data/eng@1.0.0 @tesseract.js-data/deu@1.0.0 @embedpdf/fonts-latin@1.0.0 >/dev/null
tar xzf bentopdf-pymupdf-wasm-0.11.16.tgz -C "$V/wasm/pymupdf" --strip-components=1
mkdir gs cp ts fl; tar xzf bentopdf-gs-wasm-0.1.1.tgz -C gs; cp -r gs/package/assets/* "$V/wasm/gs/"
tar xzf coherentpdf-2.5.5.tgz -C cp; cp -r cp/package/dist/* "$V/wasm/cpdf/"
tar xzf tesseract.js-7.0.0.tgz -C ts; cp ts/package/dist/worker.min.js "$V/wasm/ocr/"
tar xzf tesseract.js-core-7.0.0.tgz -C "$V/wasm/ocr/core" --strip-components=1
for l in eng deu; do mkdir "$l"; tar xzf "tesseract.js-data-$l-1.0.0.tgz" -C "$l"; cp "$l/package/4.0.0_best_int/$l.traineddata.gz" "$V/wasm/ocr/lang-data/"; done
tar xzf embedpdf-fonts-latin-1.0.0.tgz -C fl; cp -r fl/package/fonts "$V/fonts/embedpdf/fonts-latin@1.0.0/"; cp fl/package/fonts/NotoSans-Regular.ttf "$V/wasm/ocr/fonts/"
echo "vendor/ bereit."
