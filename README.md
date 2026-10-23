# LXNCE PDF

**Live:** https://pdf.lxnce.digital · **Quellcode-Seite:** https://pdf.lxnce.digital/quellcode/

Angepasste Version von [BentoPDF](https://github.com/alam00000/bentopdf) für **https://pdf.lxnce.digital**,
einen kostenlosen Service von [LXNCE Digital](https://lxnce.digital). Alle PDF-Werkzeuge laufen
vollständig im Browser; es werden keine Dateien hochgeladen und keine fremden Server (CDNs) aufgerufen.

Lizenz: **GNU AGPL-3.0** (wie BentoPDF).

## Was geändert ist

- Farben (LXNCE-Orange), Logo, Favicons, Vorschaubilder
- Kopf- und Fußzeile mit Impressum, Datenschutz und Quellcode-Hinweis
- Markenname „LXNCE PDF“ in Seitentiteln und Texten
- Simple Mode, Standardsprache Deutsch
- WASM-Module (PyMuPDF, Ghostscript, CoherentPDF), OCR (Tesseract, Deutsch + Englisch) und Schriften
  werden vom eigenen Server ausgeliefert statt von jsDelivr/githack
- Strenge Content-Security-Policy (`.htaccess`): nur Inhalte vom eigenen Server
- bentopdf.com-eigene Seiten (Über uns, Blog, Datenschutz, AGB, Lizenzkauf) werden entfernt

## Bauen

```bash
git clone https://github.com/alam00000/bentopdf.git
git -C bentopdf checkout dafb6f8e188591bf5838728542d4cd234b8d4a75
./fetch-vendor.sh                 # lädt die unveränderten WASM-/OCR-Pakete von npm
./build.sh ./bentopdf             # Ergebnis: bentopdf/dist/
```

Den Inhalt von `bentopdf/dist/` (inklusive `.htaccess`) auf einen Apache-Webserver hochladen.

## Dateien

- `patch.py`: wendet alle Änderungen auf einen BentoPDF-Checkout an
- `build.sh`: Patch + Build mit den passenden Umgebungsvariablen
- `postbuild.py`: entfernt bentopdf.com-Seiten, benennt die Marke um, legt `.htaccess` ab
- `fetch-vendor.sh`: lädt die WASM-, OCR- und Schriftpakete
- `assets/`: Logos, Icons, Quellcode-Seite, Apache-Konfiguration
