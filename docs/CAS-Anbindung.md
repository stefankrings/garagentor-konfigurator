# Anbindung CAS genesisWorld (REST)

Stand: 2026-10-14. Ziel: Konfigurator/Belegtool soll Kunden aus CAS genesisWorld lesen und später Belege als Dokumente mit GUID nach CAS schreiben.

## Zugang
- Basis-URL: `https://gwapp.kringsdesign.de/genesisrest.svc/v7.0` (nur Version 7.0 wird unterstützt)
- Anmeldung: HTTP Basic Auth (CAS-Benutzer + dessen genesisWorld-Passwort) **plus** Header `X-CAS-PRODUCT-KEY`.
- Zugangsdaten liegen als **Netzwerk-Secret** in der claude.ai/code-Umgebung „Default“ (ein Secret mit zwei Headern: `Authorization: Basic …` und `X-CAS-PRODUCT-KEY`). Der Proxy hängt sie automatisch an, sie sind in der Sitzung nicht lesbar. Pro Host wird nur ein Secret angewendet.
- Netzwerk: Domain `gwapp.kringsdesign.de` muss in der Umgebung freigegeben sein (Network access: Custom).
- Test 2026-10-14: `GET /ping` → 200 `pong`. Anmeldung (Basic + Key) noch nicht mit einer geschützten Abfrage geprüft.

## Regeln
- Nie Schlüssel/Passwörter in Chat, Code oder Repository.
- Eigener API-Benutzer mit minimalen Rechten, zunächst reine Leserechte; erst Testmandant.
- Zunächst **nur lesen** (ping, databases, query). Kein Anlegen/Ändern/Löschen ohne ausdrückliche Freigabe.
- Keine Kundendaten ins Repository (Testfälle nur mit Musterkunden).

## Endpunkte laut Schnittstellenbeschreibung (mpl, v7.0)
- `GET /ping`, `GET /databases`
- `POST /type/query` mit `{"query":"SELECT GGUID, Compname, Street1 FROM address WHERE ..."}`
- `GET /type/address/{GGUID}` (liefert ETag im Header)
- `POST /type/address` mit `{"fields":{...}}` → 201, GGUID im Location-Header
- `PUT /type/address/{GGUID}` mit Header `If-Match: <ETag>`
- `POST /type/{T1}/{GGUID1}/dossier?gguid2=…&object-type2=…&attribute=…` für Verknüpfungen
- `DELETE /type/address/{GGUID}` (nicht verwenden)
- Adressfelder u. a.: COMPNAME, STREET1, ZIP1, TOWN1, COUNTRY1, GWISCOMPANY, GWISCONTACT

## Nächste Schritte
1. Geschützte Lese-Abfrage (z. B. `/databases`, dann kleine `query` auf `address`) → Anmeldung bestätigen.
2. Prototyp „Kunde aus CAS wählen“ (Suche nach Name/PLZ) im Konfigurator, nur lesend.
3. Später: Beleg-PDF als CAS-Dokument mit GUID und Button im Dokumentdatensatz.
