#!/usr/bin/env python3
"""Entfernt die bentopdf.com-eigenen Seiten (Über uns, Blog, Datenschutz, AGB, Lizenzkauf ...)
aus dem Build, ergänzt .htaccess und bereinigt die Sitemap."""
import re, sys, shutil, pathlib
dist = pathlib.Path(sys.argv[1]); here = pathlib.Path(__file__).resolve().parent
PAGES = ['about', 'contact', 'faq', 'licensing', 'privacy', 'terms', 'kura']
removed = 0
for d in [dist] + [p for p in dist.iterdir() if p.is_dir() and re.fullmatch(r'[a-z]{2}(-[A-Z]{2})?', p.name)]:
    for name in PAGES:
        for ext in ('.html', '.html.br', '.html.gz'):
            f = d / (name + ext)
            if f.exists(): f.unlink(); removed += 1
    if (d / 'blog').is_dir(): shutil.rmtree(d / 'blog'); removed += 1
sm = dist / 'sitemap.xml'
if sm.exists():
    s = sm.read_text()
    s = re.sub(r'<url>(?:(?!</url>).)*?/(?:[a-z]{2}(?:-[A-Z]{2})?/)?(?:%s|blog[^<]*)(?:\.html)?</loc>.*?</url>\s*' % '|'.join(PAGES), '', s, flags=re.S)
    sm.write_text(s)
# vorkomprimierte Kopien entfernen (Apache/Cloudflare komprimieren selbst); echte .gz-Originale bleiben
pre = 0
for f in list(dist.rglob('*')):
    if f.is_file() and f.suffix in ('.br', '.gz') and f.with_suffix('').exists():
        f.unlink(); pre += 1
print('vorkomprimierte Kopien entfernt:', pre)
# Markenname in allen Seiten (Titel, Meta-Tags, SEO-Texte); Quellenangabe im Footer bleibt erhalten
ATTR = '>BentoPDF</a>'
n = 0
for f in dist.rglob('*.html'):
    if 'quellcode' in f.parts: continue
    t = f.read_text(encoding='utf-8')
    if 'BentoPDF' not in t: continue
    t2 = re.sub(r'\s*<meta name="twitter:(site|creator)" content="@BentoPDF">', '', t)
    t2 = t2.replace(ATTR, '>\x00</a>').replace('content="BentoPDF"', 'content="LXNCE Digital"')
    t2 = t2.replace("BentoPDF's", 'LXNCE PDF').replace('BentoPDF', 'LXNCE PDF').replace('>\x00</a>', ATTR)
    if t2 != t: f.write_text(t2, encoding='utf-8'); n += 1
print('Seiten umbenannt:', n)
# Startseiten: aussagekräftiger Titel und Beschreibung (statt generischem "PDF Tools")
HOME = {
    'de': ('PDF-Werkzeuge kostenlos online – zusammenfügen, bearbeiten, umwandeln | LXNCE PDF',
           'Über 100 kostenlose PDF-Werkzeuge: PDFs zusammenfügen, komprimieren, bearbeiten, unterschreiben und in Word umwandeln. Alles im Browser, ohne Upload, ohne Anmeldung.'),
    '': ('Free PDF tools online – merge, edit, convert | LXNCE PDF',
         'More than 100 free PDF tools: merge, compress, edit, sign and convert PDFs. Runs entirely in your browser, no uploads, no signup.'),
}
for sub_dir, (title, desc) in HOME.items():
    f = dist / sub_dir / 'index.html'
    if not f.exists(): continue
    t = f.read_text(encoding='utf-8')
    t = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', t, count=1)
    t = re.sub(r'<meta name="title" content="[^"]*">', f'<meta name="title" content="{title}">', t, count=1)
    t = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', t, count=1)
    f.write_text(t, encoding='utf-8')
shutil.copy(here / 'assets/htaccess', dist / '.htaccess')
print('entfernt:', removed)
