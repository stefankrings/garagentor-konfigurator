#!/bin/sh
# V3: eigenständige Quelle template_v3.html (kein Patch-Stapel mehr). Bauen + Rechentests.
set -e; cd "$(dirname "$0")"
python3 build.py template_v3.html Garagentor-Konfigurator-V3.html
APP=Garagentor-Konfigurator-V3.html node regress/run.js
node regress/visual.js
