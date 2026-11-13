# Schnittstellen der EduKSX-Plattform als Schemas (#3)

Stand: 13.11.2026 (Meilenstein 0.2.0) · Status: **BESCHLOSSEN** – Schemas v1 und Festlegungen SP1–SP8 abgenommen am
13.11.2026 (#3). Grundlage: [Plattform §5](../docs/KONZEPT-PLATTFORM.md), [API-Standard](../docs/KONZEPT-API-GUIDELINE.md)
B7, C1, D3, D6.

Die Schnittstellen S1–S8 sind im Plattform-Konzept beschrieben. Hier stehen die Teile, die zwischen Ident, Leitstand
und Modulen ausgetauscht werden, **maschinenlesbar**, damit jedes Modul und `eduksx/core` dagegen prüfen kann. Kein Code
für einzelne Module.

## Inhalt

| Datei | Schnittstelle | Inhalt |
| --- | --- | --- |
| [v1/oidc-claims.schema.json](v1/oidc-claims.schema.json) | S1 | Claims im ID-Token: Standard-Claims, `acr`/`amr`, `eduksx_orgs`, `eduksx_roles` |
| [v1/event.schema.json](v1/event.schema.json) | S4 | Ereignis als CloudEvents 1.0 (JSON) mit den Arten aus Ident und ihren Daten |
| [v1/signature.schema.json](v1/signature.schema.json) | S4 | Kopfzeile `EduKSX-Signature` |
| [v1/module-manifest.schema.json](v1/module-manifest.schema.json) | S5 | Steckbrief `/.well-known/eduksx-module.json`, mit Abschnitt `ui` für Plugins ([KONZEPT-PLUGINS.md](../docs/KONZEPT-PLUGINS.md)) |
| [v1/health.schema.json](v1/health.schema.json) | S5 | Antwort von `/health` |
| [v1/ops-instances.openapi.json](v1/ops-instances.openapi.json) | S6 | Heartbeat und Aufträge zwischen Instanz und Leitstand (OpenAPI 3.1); Anmeldung per Client Credentials oder Instanz-Token |

Beispiele liegen unter `v1/examples/<name>/valid|invalid/` (bei OpenAPI `v1/examples/<datei>/<Schema>/…`). Alle Werte sind
erfunden; Adressen nur unter `.example`. Der Steckbrief des Glossary bleibt ein **Entwurf** – die Werte (Version, Rollen,
Ereignisse) übernimmt das Glossary mit Glossary #189.

S2 (Client Credentials, JWT) und S3 (SCIM 2.0) sind Standards ohne eigene Erweiterung; ihre Profile folgen mit dem
Konzept Ident ([KONZEPT-IDENT.md](../docs/KONZEPT-IDENT.md)). S7 (`/api/v1/me/modules`) und S8 (Daten-APIs) beschreibt
jeweils das anbietende Modul in seiner eigenen OpenAPI-Datei (API D3).

## Festlegungen

| Nr. | Frage | Entscheid | Status |
| --- | --- | --- | --- |
| SP1 | Ablage | Quelle der Plattform-Schemas ist dieses Verzeichnis; `eduksx/core` übernimmt die Dateien je Release unverändert (Core C11). Das präzisiert API D3 («gemeinsame Schemas in `eduksx/core`»): Core liefert aus, hier wird gepflegt. | BESCHLOSSEN 13.11.2026 |
| SP2 | Format | JSON Schema Draft 2020-12; HTTP-Schnittstellen als OpenAPI 3.1 (dessen Schemas sind JSON Schema 2020-12) | BESCHLOSSEN 13.11.2026 |
| SP3 | Namen | Felder englisch, `snake_case` (API A2); Arten der Ereignisse `<modul>.<objekt>.<verb>` (API B7) | BESCHLOSSEN (API A2, B7) |
| SP4 | Ereignisarten von Ident | mit Modulschlüssel: `ident.user.*`, `ident.organization.*`, `ident.membership.*`, `ident.role.changed`. Plattform S4 nannte sie ohne Präfix; angeglichen an API B7 | BESCHLOSSEN 13.11.2026 |
| SP5 | Rolle in `eduksx_orgs` | Feld heisst `role` (Plattform S1 schrieb «rolle»); Werte `admin`, `member` | BESCHLOSSEN 13.11.2026 |
| SP6 | Signatur S4 | `EduKSX-Signature: t=<Unix-Sekunden>,v1=<hex>`; HMAC-SHA256 über `<t>.<roher Body>`; mehrere `v1=` beim Schlüsselwechsel; Abweisung nach 300 s; Vergleich in konstanter Zeit | BESCHLOSSEN 13.11.2026 |
| SP7 | Personendaten in Ereignissen und Heartbeat | keine – nur IDs; Schemas verbieten zusätzliche Felder (`additionalProperties: false`) | BESCHLOSSEN (API B7, Plattform S6) |
| SP8 | Aufträge S6 | signiert als JWS mit abgetrenntem Inhalt; Images nur mit `@sha256:`-Digest | BESCHLOSSEN 13.11.2026 |

## Versionierung

- Der Ordner ist die **Hauptversion** (`v1`) und entspricht der Version der Schnittstelle (Plattform §5). Die `$id`
  lautet `https://docs.eduksx.ch/spec/v<n>/<datei>`.
- **Innerhalb von `v1` nur abwärtskompatibel:** neue optionale Felder, neue Ereignisarten, neue Enum-Werte nur dort,
  wo Empfänger Unbekanntes ignorieren dürfen (bei Ereignisarten ja, bei `role` nein). Pflichtfelder, Muster und
  Bedeutungen ändern sich nicht.
- **Brüche** (Feld entfernt, Pflichtfeld neu, Muster enger) nur in `v2`, parallel zu `v1` mit Übergangszeit nach API D1;
  Ident und Leitstand liefern beide Versionen, bis alle Module umgestellt sind (Steckbrief `api_versions`).
- Jede Änderung steht im CHANGELOG dieses Repos; `eduksx/core` nimmt sie mit der nächsten Minor-Version auf (Core C9).
- Felder für Bindungen (`x-eduksx-*`) folgen API D3.

## Prüfung

`python3 -m unittest discover -s tests` (benötigt `pip install -r requirements-pruefung.txt`):

- jedes Schema ist gültig (Draft 2020-12) und trägt die richtige `$id`;
- jede OpenAPI-Datei ist 3.1, hat Lizenz, Modulschlüssel, eindeutige `operationId` und `security` je Operation;
- je Schema mindestens ein gültiges und ein ungültiges Beispiel, beide werden geprüft; Beispiele in der
  OpenAPI-Datei ebenso;
- in Beispielen nur Adressen unter `.example`.

Formate (`uuid`, `email`) werden geprüft, soweit `jsonschema` sie ohne Zusatzpakete kennt. Die volle Prüfung von
OpenAPI (Spectral-Regelsatz `eduksx`) kommt mit `eduksx/core` (API D3).
