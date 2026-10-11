# Garagentor-Konfigurator – Projektordner

Aktuelle Version: **V4** (`template_v4.html` → `Garagentor-Konfigurator-V4.html`).
V1–V3 sind Archivstände; Quelle von V3: `template_v3.html`.

## Bauen und prüfen
    ./build_v4.sh          # baut V4, 132 Rechentests + 70 Bildvergleiche
    python3 tools/mutate.py template_v4.html   # Mutationstest (prüft, ob die Tests Fehler finden)
    node tools/format.mjs template_v4.html     # einheitliche Formatierung (Prettier)
    python3 regress/report.py                  # Prüfliste als HTML

Voraussetzungen: Python 3 mit Pillow, Node.js, Playwright mit Chromium,
in `tools/`: `npm install` (acorn, acorn-walk, postcss, prettier).

## Aufbau
- `template_v4.html` – Quelle (HTML, CSS, JS) mit Platzhaltern `__PRICES__` usw.
- `build.py` – setzt Daten ein: `prices.json`, `ral.txt`, `win_thumbs.json`, `brief.json`, `besch.json`,
  `zubimg.json`, `fassaden.json`, `plz.txt`, `teilorte/teilorte-deutschland.json`, `libs/` (PDF)
- `regress/` – Testfälle (`cases.js`), Referenz (`baseline.json`, `visual/ref`), Prüfliste
- `tools/` – Analyse-, Zerlege-, Formatier- und Mutationswerkzeuge
- `teilorte/` – Aufbereitung GeoNames → Teilorte
- Git-Verlauf in `.git` (jeder Aufräumschritt einzeln)

## Datenquellen
PLZ/Orte: © OpenStreetMap-Mitwirkende (ODbL), OpenPLZ API · Teilorte: GeoNames (CC BY 4.0)
