#!/usr/bin/env python3
"""LXNCE-Anpassungen für MySigMail (antonreshetov/mysigmail).
Aufruf: python3 patch.py <checkout>   (auf einen frischen Checkout anwenden)"""
import re, sys, shutil, pathlib

root = pathlib.Path(sys.argv[1])
src = root / 'src'
here = pathlib.Path(__file__).resolve().parent
BASE = 'https://tools.lxnce.digital/signatur'


def rd(rel):
    return (root / rel).read_text(encoding='utf-8')


def wr(rel, s):
    (root / rel).write_text(s, encoding='utf-8')


def sub(rel, old, new, count=1, regex=False):
    s = rd(rel)
    if regex:
        s2, n = re.subn(old, new, s, count=count, flags=re.S)
    else:
        n = s.count(old)
        s2 = s.replace(old, new) if count == 0 else s.replace(old, new, count)
    if n == 0:
        sys.exit(f'PATCH FEHLGESCHLAGEN: {rel}: {old[:70]!r} nicht gefunden')
    wr(rel, s2)


# ---------------------------------------------------------------- Technik
# Router unter /signatur/
sub('src/router/index.ts', 'createWebHistory()', 'createWebHistory(import.meta.env.BASE_URL)')
# Bilder in der Signatur brauchen absolute Adressen (sie werden in E-Mails geladen)
for f in list(src.rglob('*.vue')) + list(src.rglob('*.ts')):
    if 'shadcn' in f.parts:
        continue
    s = f.read_text(encoding='utf-8')
    s2 = s.replace('${cdnUrl}/signature/assets/', f'{BASE}/assets/')
    s2 = re.sub(r"(['\"`])/assets/", lambda m: m.group(1) + BASE + '/assets/', s2)
    if s2 != s:
        f.write_text(s2, encoding='utf-8')
# Google Analytics entfernen
sub('src/components/preview/header/UpdateDialog.vue', r"\nconst \{ gtag \} = useGtag\(\)\n", '\n', regex=True)
sub('src/components/preview/header/UpdateDialog.vue', r"\s*gtag\('event'.*?\}\)\n", '\n', regex=True)
# Bild-Upload (Amazon S3 mit Schlüsseln im Browser) ausblenden
sub('src/components/ui/upload/Upload.vue', ':disabled="!isUploadAvailable"', 'v-if="isUploadAvailable"')

# ---------------------------------------------------------------- Farben (LXNCE-Orange)
sub('src/style.css', '--primary: oklch(0.557 0.183 263.711);', '--primary: #ff5119;')
sub('src/style.css', '--primary-foreground: oklch(0.985 0.004 264.052);', '--primary-foreground: #ffffff;')
sub('src/style.css', '--primary: oklch(0.637 0.203 263.711);', '--primary: #ff6a3a;')
sub('src/style.css', '--primary-foreground: oklch(0.224 0.022 266.109);', '--primary-foreground: #ffffff;')

# ---------------------------------------------------------------- Kopf und Fuß
wr('src/components/header/Header.vue', '''<template>
  <div
    data-header
    class="p-3 pr-6 flex justify-between items-center"
  >
    <RouterLink to="/basic">
      <div class="w-[var(--sidebar-width)] flex items-center gap-2">
        <img
          src="/lxnce-logo-dunkel.png"
          alt="LXNCE Digital"
          class="h-7 w-auto dark:hidden"
        >
        <img
          src="/lxnce-logo-hell.png"
          alt="LXNCE Digital"
          class="h-7 w-auto hidden dark:block"
        >
      </div>
    </RouterLink>
    <div class="flex items-center gap-4">
      <span class="hidden md:inline text-sm font-semibold">E-Mail-Signatur-Generator</span>
      <UiButton variant="link" as-child>
        <a href="https://tools.lxnce.digital/">Alle Tools</a>
      </UiButton>
      <UiButton as-child>
        <a href="https://lxnce.digital/" target="_blank" rel="noopener">lxnce.digital</a>
      </UiButton>
      <HeaderColorMode />
    </div>
  </div>
</template>
''')
wr('src/components/preview/Footer.vue', '''<script setup lang="ts">
import { version } from '../../../package.json'
</script>

<template>
  <div
    data-footer
    class="text-xs text-muted-foreground text-right space-y-1"
  >
    <div>
      Ein kostenloser Service von
      <a class="underline" href="https://lxnce.digital/" target="_blank" rel="noopener">LXNCE Digital</a>
      ·
      <a class="underline" href="https://lxnce.digital/impressum.php" target="_blank" rel="noopener">Impressum</a>
      ·
      <a class="underline" href="https://lxnce.digital/datenschutz.php" target="_blank" rel="noopener">Datenschutz</a>
    </div>
    <div>
      Alle Eingaben bleiben in Ihrem Browser und werden nicht an uns übertragen.
    </div>
    <div>
      Basiert auf
      <a class="underline" href="https://github.com/antonreshetov/mysigmail" target="_blank" rel="noopener">MySigMail</a>
      v{{ version }} von Anton Reshetov · Lizenz
      <a class="underline" href="https://www.gnu.org/licenses/agpl-3.0.html" target="_blank" rel="noopener">AGPL-3.0</a>
      ·
      <a class="underline" href="https://tools.lxnce.digital/signatur/quellcode/">Quellcode dieser Version</a>
    </div>
  </div>
</template>
''')
sub('index.html', '<html lang="en">', '<html lang="de">')
sub('index.html', '<title>MySigMail</title>',
    '<title>E-Mail-Signatur-Generator – kostenlos | LXNCE Tools</title>\n'
    '    <meta name="description" content="Kostenlos eine professionelle E-Mail-Signatur für Outlook, Gmail, Apple Mail und Thunderbird erstellen – mit Logo, Social-Media-Links und Pflichtangaben. Direkt im Browser, ohne Anmeldung." />\n'
    f'    <link rel="canonical" href="{BASE}/" />\n'
    '    <meta name="theme-color" content="#ff5119" />')

# ---------------------------------------------------------------- Beispieldaten (deutsch)
T = 'src/data/templates.ts'
for old, new in [
    ("label: 'Avatar',\n        type: 'image',\n        main: true,\n        value: '',",
     f"label: 'Foto / Logo',\n        type: 'image',\n        main: true,\n        value: '{BASE}/assets/avatar.png',"),
    ("label: 'Full Name',", "label: 'Name',"), ("value: 'John Doe',", "value: 'Max Mustermann',"),
    ("label: 'Job Title',", "label: 'Position',"), ("value: 'Frontend developer',", "value: 'Geschäftsführer',"),
    ("label: 'Company',", "label: 'Firma',"), ("value: 'JohnDoe LLC',", "value: 'Musterfirma GmbH',"),
    ("value: 'https://example.com',\n      },\n      {\n        id: nanoid(8),\n        label: 'Email',",
     "value: 'https://www.example.de',\n      },\n      {\n        id: nanoid(8),\n        label: 'E-Mail',"),
    ("value: 'johndoe@example.com',", "value: 'max@example.de',"),
    ("label: 'Phone',", "label: 'Telefon',"), ("value: '+ 1 123 456 7890',", "value: '+49 30 1234567',"),
    ("mainColor: '#396BDD',\n      secondaryColor: '#396BDD',\n      bgColor: '#3D6693',",
     "mainColor: '#ff5119',\n      secondaryColor: '#141414',\n      bgColor: '#141414',"),
]:
    sub(T, old, new)
sub(T, r"    addons: \[\n      \{\n        label: 'Disclaimer',.*?\] as AddonTool\[\],",
    "    addons: [\n      {\n        label: 'Pflichtangaben / Hinweis',\n        type: 'disclaimer',\n        isNew: false,\n        value:\n"
    "          'Musterfirma GmbH · Musterstraße 1 · 10115 Berlin · Geschäftsführer: Max Mustermann · Amtsgericht Berlin-Charlottenburg HRB 123456 · USt-IdNr. DE123456789',\n"
    "      },\n    ] as AddonTool[],", regex=True)
sub(T, r"    socials: \[\n.*?\] as SocialTool\[\],",
    "    socials: [\n      { icon: 'linkedin', value: 'https://www.linkedin.com/', label: 'LinkedIn' },\n"
    "      { icon: 'instagram', value: 'https://www.instagram.com/', label: 'Instagram' },\n"
    "      { icon: 'facebook', value: 'https://www.facebook.com/', label: 'Facebook' },\n    ] as SocialTool[],", regex=True)
sub(T, r"label: 'Template #(\d+)'", r"label: 'Vorlage \1'", count=0, regex=True)
if (root / 'src/data/presets.ts').exists():
    sub('src/data/presets.ts', r"label: 'Preset #(\d+)'", r"label: 'Beispiel \1'", count=0, regex=True)

wr('src/data/disclaimer-pressets.ts', '''export const disclaimerPresets = [
  {
    label: 'Pflichtangaben (GmbH)',
    value:
      '[Firma] GmbH · [Straße Nr.] · [PLZ Ort] · Geschäftsführer: [Name] · Registergericht: Amtsgericht [Ort] HRB [Nummer] · USt-IdNr. [DE…]',
  },
  {
    label: 'Pflichtangaben (Einzelunternehmen)',
    value:
      '[Vorname Nachname] · [Firmenname] · [Straße Nr.] · [PLZ Ort] · USt-IdNr. [DE…] (falls vorhanden)',
  },
  {
    label: 'Vertraulichkeit',
    value:
      'Diese E-Mail kann vertrauliche und/oder rechtlich geschützte Informationen enthalten. Wenn Sie nicht der richtige Adressat sind oder diese E-Mail irrtümlich erhalten haben, informieren Sie bitte sofort den Absender und vernichten Sie diese E-Mail. Das unerlaubte Kopieren sowie die unbefugte Weitergabe dieser E-Mail ist nicht gestattet.',
  },
  {
    label: 'Datenschutz (DSGVO)',
    value:
      'Informationen zur Verarbeitung Ihrer personenbezogenen Daten gemäß Art. 13 DSGVO finden Sie in unserer Datenschutzerklärung: [Link zur Datenschutzerklärung]',
  },
  {
    label: 'Umwelt',
    value: 'Bitte denken Sie an die Umwelt, bevor Sie diese E-Mail ausdrucken.',
  },
]
''')

# ---------------------------------------------------------------- Oberfläche übersetzen
TEXT = {  # Textknoten in Vue-Vorlagen
    'Upload JSON': 'JSON laden', 'Get Signature': 'Signatur übernehmen', 'Copy as Select': 'Signatur kopieren',
    'Copy as HTML': 'Als HTML kopieren', 'Download JSON': 'Als JSON speichern',
    'Signature is too large': 'Signatur ist sehr groß',
    'The HTML code for the signature exceeds 10,000 characters, which may be too much for some email clients (e.g., Outlook or Gmail). We recommend reducing the size: remove unnecessary add-ons or shorten the text.':
        'Der HTML-Code der Signatur ist länger als 10.000 Zeichen. Das kann für manche E-Mail-Programme (z. B. Outlook oder Gmail) zu viel sein. Entfernen Sie nicht benötigte Erweiterungen oder kürzen Sie den Text.',
    'Add Custom Field': 'Eigenes Feld hinzufügen', 'Add Field': 'Feld hinzufügen', 'Installed': 'Aktiv',
    'No addons installed': 'Keine Erweiterungen aktiv', 'Addons': 'Verfügbar',
    'Write your disclaimer text or select a preset.': 'Eigenen Text eingeben oder eine Vorlage auswählen.',
    'Color': 'Farbe', 'Column Size': 'Spaltenbreite', 'Font': 'Schrift', 'Other': 'Sonstiges', 'Photo / Logo': 'Foto / Logo',
    'Name': 'Name', 'Rename': 'Umbenennen', 'Save': 'Speichern', 'Preview': 'Vorschau', 'Upload': 'Hochladen',
    'Upload Image': 'Bild hochladen', 'Crop image to the desired size.': 'Bild auf die gewünschte Größe zuschneiden.',
}
ATTR = {  # label=, placeholder=, description= …
    'Image': 'Bild', 'Link': 'Link', 'Width': 'Breite', 'Text': 'Text', 'Type': 'Typ', 'Value': 'Wert', 'Label': 'Bezeichnung',
    'You can upload image or paste the public link to image.':
        'Fügen Sie die öffentliche Adresse Ihres Bildes ein, z. B. das Logo auf Ihrer Website (Rechtsklick → Bildadresse kopieren).',
    'https://example.com/image.png': 'https://www.ihre-website.de/logo.png',
    'Background Color': 'Hintergrundfarbe', 'Enable Image': 'Bild statt Text', 'Text Color': 'Textfarbe',
    'Select a preset': 'Vorlage auswählen', 'Select a type': 'Typ auswählen', 'Select a timezone': 'Zeitzone auswählen',
    'Background': 'Hintergrund', 'Background text': 'Text auf Hintergrund', 'Column 1': 'Spalte 1', 'Family': 'Schriftart',
    'Job separator': 'Trenner Position/Firma', 'Main': 'Hauptfarbe', 'Secondary': 'Zweitfarbe', 'Select a value': 'Auswählen',
    'Shape': 'Form', 'Show': 'Anzeigen', 'Size': 'Größe', 'Aspect Ratio': 'Seitenverhältnis', 'Resize to': 'Skalieren auf',
}
PROP = {  # label: '…' / title: '…' usw. in TypeScript
    'Basic signature details': 'Angaben zur Signatur', 'Social media links': 'Social-Media-Links',
    'Signature options': 'Darstellung', 'Signature addons': 'Erweiterungen', 'Templates': 'Vorlagen',
    'Basic': 'Angaben', 'Social': 'Social Media', 'Options': 'Darstellung', 'Addons': 'Extras',
    'Dark': 'Dunkel', 'Light': 'Hell', 'System': 'System',
    'Mobile App': 'App-Links', 'Disclaimer': 'Pflichtangaben / Hinweis', 'Banner': 'Banner', 'Video Conference': 'Videokonferenz',
    'CTA': 'Button (Call-to-Action)', 'Logo': 'Logo',
    'Meet me on Google Hangouts': 'Termin per Videocall vereinbaren',
    'Get your coupon for a 20% discount': 'Jetzt Termin vereinbaren',
    'Email': 'E-Mail', 'Phone': 'Telefon', 'Text': 'Text', 'Link': 'Link', 'New line': 'Neue Zeile',
    'Small': 'Klein', 'Medium': 'Mittel', 'Large': 'Groß', 'Square': 'Eckig', 'Round': 'Rund', 'Rounded corners': 'Abgerundet',
    'Free': 'Frei', 'Success': 'Erledigt', 'Error': 'Fehler', 'Oops! Something went wrong.': 'Hoppla, da ist etwas schiefgelaufen.',
    'Signature copied to clipboard.': 'Signatur in die Zwischenablage kopiert. Jetzt im E-Mail-Programm einfügen (Strg + V).',
    'You need to allow clipboard access to copy the signature.': 'Bitte erlauben Sie den Zugriff auf die Zwischenablage, um die Signatur zu kopieren.',
    'Signature uploaded successfully': 'Signatur geladen', 'Image uploaded successfully': 'Bild hochgeladen',
    'Failed to upload image': 'Bild konnte nicht hochgeladen werden', 'Invalid JSON format': 'Ungültige JSON-Datei',
    'Full Name': 'Name', 'Job Title': 'Position', 'Company': 'Firma', 'Website': 'Website', 'Avatar': 'Foto / Logo',
}
props = r'(label|title|description|text|name|presetName)'
for f in list(src.rglob('*.vue')) + list(src.rglob('*.ts')):
    if 'shadcn' in f.parts or f.name in ('analytics.ts', 'socials.ts'):
        continue
    s = f.read_text(encoding='utf-8'); s0 = s
    if f.suffix == '.vue':
        for en, de in TEXT.items():
            pat = r'>(\s*)' + r'\s+'.join(map(re.escape, en.split())) + r'(\s*)<'
            s = re.sub(pat, lambda m: f'>{m.group(1)}{de}{m.group(2)}<', s)
        for en, de in ATTR.items():
            s = re.sub(r'\b(label|placeholder|description|title)="' + re.escape(en) + '"', lambda m: f'{m.group(1)}="{de}"', s)
    for en, de in PROP.items():
        s = re.sub(r"\b" + props + r"(\s*:\s*)'" + re.escape(en) + "'", lambda m: f"{m.group(1)}{m.group(2)}'{de}'", s)
    if s != s0:
        f.write_text(s, encoding='utf-8')

sub('src/components/options/Form.vue', '`Width in percentage. Current: ${avatarSize[0]}%`', '`Größe in Pixel. Aktuell: ${avatarSize[0]} px`')
for f in ('src/components/options/Form.vue', 'src/components/addons/Cta.vue', 'src/components/addons/Banner.vue'):
    sub(f, '`Width in percentage. Current: ', '`Breite in Prozent. Aktuell: ', count=0)

sub('src/data/addons.ts', "colorBg: '#ffa500',", "colorBg: '#ff5119',")

# ---------------------------------------------------------------- Grafiken, Icons, Quellcode-Seite
for f in (here / 'assets/public').iterdir():
    shutil.copy(f, root / 'public' / f.name)
shutil.copytree(here / 'assets/quellcode', root / 'public/quellcode', dirs_exist_ok=True)
for f in (here / 'assets/replace').glob('*'):
    shutil.copy(f, root / 'public/assets' / f.name)

print('LXNCE-Signatur-Patch angewendet.')
