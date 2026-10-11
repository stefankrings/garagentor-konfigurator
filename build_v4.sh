#!/bin/sh
# V4: eigenständige Quelle template_v4.html (kein Patch-Stapel mehr). Bauen + Rechentests.
set -e; cd "$(dirname "$0")"
python3 build.py template_v4.html Garagentor-Konfigurator-V4.html
APP=Garagentor-Konfigurator-V4.html node regress/run.js
APP=Garagentor-Konfigurator-V4.html node regress/visual.js
