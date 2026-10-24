# LXNCE E-Mail-Signatur-Generator

Angepasste Version von [MySigMail](https://github.com/antonreshetov/mysigmail) (Anton Reshetov) für
**https://tools.lxnce.digital/signatur/**. Lizenz: **GNU AGPL-3.0**.

Änderungen: deutsche Oberfläche und Beispieldaten, LXNCE-Farben und -Logo, Kopf- und Fußzeile
(Impressum, Datenschutz, Quellcode), Google Analytics entfernt, S3-Bild-Upload ausgeblendet,
Bilder/Icons mit absoluten Adressen vom eigenen Server, App unter `/signatur/`.

## Bauen

```bash
git clone https://github.com/antonreshetov/mysigmail.git
./build.sh ./mysigmail        # Ergebnis: mysigmail/dist → nach public_html/signatur/ hochladen
```
