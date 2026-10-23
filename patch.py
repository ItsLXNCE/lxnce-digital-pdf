#!/usr/bin/env python3
"""LXNCE-Branding für BentoPDF (alam00000/bentopdf). Aufruf: python3 patch.py <checkout>
Auf einen frischen Checkout anwenden (git checkout . && git clean -fd public vorher)."""
import re, sys, shutil, pathlib

root = pathlib.Path(sys.argv[1])
here = pathlib.Path(__file__).resolve().parent


def sub(rel, old, new, count=1, regex=False):
    p = root / rel
    s = p.read_text(encoding='utf-8')
    if regex:
        s2, n = re.subn(old, new, s, count=count, flags=re.S)
    else:
        n = s.count(old)
        s2 = s.replace(old, new) if count == 0 else s.replace(old, new, count)
    if n == 0:
        sys.exit(f'PATCH FEHLGESCHLAGEN: {rel}: {old[:70]!r} nicht gefunden')
    p.write_text(s2, encoding='utf-8')


# 1) Akzentfarbe Indigo -> LXNCE-Orange (Tailwind-Theme-Variablen)
ORANGE = {
    50: '#fff4ef', 100: '#ffe5d9', 200: '#ffc7b0', 300: '#ffa07e', 400: '#ff7a4c',
    500: '#ff5119', 600: '#ff5119', 700: '#e0400a', 800: '#b3330b', 900: '#7f2810', 950: '#451106',
}
block = ''.join(f'  --color-indigo-{k}: {v};\n' for k, v in ORANGE.items())
sub('src/css/styles.css',
    r"  --color-indigo-300: #a5b4fc;\n  --color-indigo-400: #818cf8;\n  --color-indigo-500: #6366f1;\n  --color-indigo-600: #6366f1;\n  --color-indigo-700: #4f46e5;\n",
    block, regex=True)

# 2) Kopfzeile (Simple Mode): LXNCE-Logo, Titel, Links zu Website und Tools
sub('src/partials/navbar-simple.html', r'<div class="flex justify-start items-center h-16">.*?\n    </div>\n  </div>\n</nav>',
    '''<div class="flex justify-between items-center h-16 gap-4">
      <a href="{{baseUrl}}" class="flex items-center gap-3 min-w-0" aria-label="LXNCE PDF Startseite">
        <img id="nav-logo" src="{{baseUrl}}images/lxnce-logo-hell.png" alt="LXNCE Digital" class="h-8 w-auto" width="128" height="32" />
        <span id="nav-brand" class="text-white font-bold text-lg border-l border-gray-600 pl-3 whitespace-nowrap">PDF<span class="text-indigo-500">.</span></span>
      </a>
      <div class="flex items-center gap-2 text-sm">
        <a href="https://tools.lxnce.digital/" class="hidden sm:inline-block text-gray-300 hover:text-white px-3 py-2 rounded-md">Weitere Tools</a>
        <a href="https://lxnce.digital/" class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-3 py-2 rounded-md whitespace-nowrap">lxnce.digital</a>
      </div>
    </div>
  </div>
</nav>''', regex=True)

# 3) Fußzeile (Simple Mode): Anbieter, Impressum, Datenschutz, AGPL-Quellcode
sub('src/partials/footer-simple.html', r'<div>\n        <div class="flex items-center mb-2">.*?</p>\n      </div>',
    '''<div>
        <div class="flex items-center mb-2">
          <img id="footer-logo" src="{{baseUrl}}images/lxnce-logo-hell.png" alt="LXNCE Digital" class="h-7 w-auto mr-3" width="112" height="28" />
          <span id="footer-brand" class="text-white font-bold text-lg">PDF</span>
        </div>
        <p id="footer-copyright" class="text-gray-400 text-sm">
          Ein kostenloser Service von <a href="https://lxnce.digital/" class="text-indigo-400 hover:underline">LXNCE Digital</a>, IT-Service &amp; Webdesign aus Berlin.
          Alle Dateien werden ausschließlich in Ihrem Browser verarbeitet.
        </p>
        <p class="text-gray-400 text-sm mt-2">
          <a href="https://lxnce.digital/impressum.php" class="hover:text-white underline">Impressum</a> ·
          <a href="https://lxnce.digital/datenschutz.php" class="hover:text-white underline">Datenschutz</a> ·
          <a href="https://tools.lxnce.digital/" class="hover:text-white underline">Weitere Tools</a>
        </p>
        <p class="text-gray-500 text-xs mt-2">
          Basiert auf <a href="https://github.com/Alam00000/bentopdf" class="underline hover:text-gray-300">BentoPDF</a>
          <span id="app-version">{{appVersion}}</span> · Lizenz <a href="https://www.gnu.org/licenses/agpl-3.0.html" class="underline hover:text-gray-300">AGPL-3.0</a> ·
          <a href="https://pdf.lxnce.digital/quellcode/" class="underline hover:text-gray-300">Quellcode dieser Version</a>
        </p>
      </div>''', regex=True)

# 3b) Startseite im Simple Mode nutzt eigene Kopf-/Fußzeile -> auf die Partials umstellen
sub('simple-index.html', r'<!-- Simple Mode Navbar -->\s*<nav.*?</nav>', '<!-- Simple Mode Navbar -->\n    {{> navbar-simple }}', regex=True)
sub('simple-index.html', r'<!-- Simple mode footer -->\s*<footer.*?</footer>', '<!-- Simple mode footer -->\n    {{> footer-simple }}', regex=True)

# 3c) Markenname in strukturierten Daten, Seitentiteln und Texten
sub('scripts/enhance-seo-pages.mjs', "name: 'BentoPDF',\n    alternateName: ['Bento PDF', 'BentoPDF.com'],", "name: 'LXNCE PDF',\n    alternateName: ['LXNCE Digital PDF-Tools'],")
sub('scripts/generate-i18n-pages.mjs', r"name: 'BentoPDF',\n    url: SITE_URL,\n    logo: `\$\{SITE_URL\}/images/favicon.svg`,\n    sameAs: \[.*?\],",
    "name: 'LXNCE Digital',\n    url: 'https://lxnce.digital',\n    logo: `${SITE_URL}/images/favicon-512x512.png`,\n    sameAs: ['https://tools.lxnce.digital/'],", regex=True)
sub('scripts/generate-i18n-pages.mjs', "`${tools[translationKey].name} - BentoPDF`", "`${tools[translationKey].name} - LXNCE PDF`")
for loc in (root / 'public/locales').glob('*/*.json'):
    t = loc.read_text(encoding='utf-8')
    if 'BentoPDF' in t:
        loc.write_text(t.replace('BentoPDF', 'LXNCE PDF'), encoding='utf-8')

# 4) Logos, Favicons, Quellcode-Seite, Webserver-Konfiguration
for f in (here / 'assets/images').iterdir():
    shutil.copy(f, root / 'public/images' / f.name)
for f in ('favicon.ico',):
    shutil.copy(here / 'assets' / f, root / 'public' / f)

import json
mf = root / 'public/site.webmanifest'
m = json.loads(mf.read_text())
m.update(name='LXNCE PDF', short_name='LXNCE PDF', theme_color='#ff5119',
         description='Kostenlose PDF-Werkzeuge von LXNCE Digital – alles läuft direkt im Browser.')
mf.write_text(json.dumps(m, indent=4, ensure_ascii=False))

# 5) Selbst gehostete WASM-, OCR- und Schriftdateien (keine Aufrufe an fremde CDNs)
shutil.copytree(here / 'assets/quellcode', root / 'public/quellcode', dirs_exist_ok=True)
for d in ('wasm', 'fonts'):
    shutil.copytree(here / 'vendor' / d, root / 'public' / d, dirs_exist_ok=True)

print('LXNCE-PDF-Patch angewendet.')
