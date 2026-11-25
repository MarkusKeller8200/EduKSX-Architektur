# Konzept: Vorlage für neue Module (#28)

Stand: 13.11.2026 (Meilenstein 0.2.0) · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** – abgenommen am 13.11.2026 (#28); Blueprint-Profil und
Probe-Modul folgen mit #37

Ein neues Modul soll nicht bei null beginnen und vom ersten Commit an die [Prüfliste der Plattform](KONZEPT-PLATTFORM.md)
§6, den [DB-Standard](KONZEPT-DB-GUIDELINE.md) und den [API-Standard](KONZEPT-API-GUIDELINE.md) (Stufe 1 «Kern»)
erfüllen. Bausteine aus [Core](KONZEPT-CORE.md), Schemas aus [spec/](../spec/README.md).

**Verbindlichkeit:** Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Ziel

Mit einem Befehl entsteht ein Modul-Repository, das baut, getestet wird, den Konformitätstest besteht und im
Modulregister eingetragen ist – ohne Fachcode.

**Nichtziele:**
- keine Fachlogik, keine Beispieldaten ausser erfundenen Testdaten
- keine eigene Kopie von Workflows oder Regeln, die der my-github-blueprint bereits liefert (AGENTS.md)
- keine Oberflächen-Komponenten in der Vorlage selbst – sie kommen aus `@eduksx/ui` ([Design](KONZEPT-DESIGN.md))

## 2. Ablauf «neues Modul anlegen»

1. **Schlüssel vergeben:** Pull Request in diesem Repo, Eintrag im [Modulregister](REGISTER-MODULE.md) mit Status
   `geplant` (englisch, `[a-z][a-z0-9]{1,15}`, unveränderlich).
2. **Repo anlegen** (Projektverantwortliche:r): `EduKSX-<Name>`, leer.
3. **Blueprint anwenden:** `python3 ../my-github-blueprint/.github/blueprint/start.py --ziel .` (Steckbrief
   `docs/PROJEKTSTART.md`), danach `apply.py --ziel . --probelauf` und ohne `--probelauf`. Neu dazu kommt ein Profil
   `eduksx-modul` (M1, muss im Blueprint noch entstehen), das Modulschlüssel, Betriebsart (`central`/`isolated`) und
   höchste Datenklasse abfragt.
4. **Laravel-Gerüst:** `composer create-project laravel/laravel .`, dann `composer require eduksx/core:^0.1` und
   `php artisan eduksx:module-init` (aus Core, siehe 4.2) – legt die Dateien aus 4.1 an.
5. **Vertrag zuerst:** `openapi/<modul>-v1.json` ergänzen (API D3), erst dann Routen.
6. **Prüfen:** `composer test` (inkl. Konformitätstest) und CI grün; Steckbrief besteht
   [module-manifest.schema.json](../spec/v1/module-manifest.schema.json).
7. **Datenschutz:** Verzeichnis der Bearbeitungen und – falls nötig – Folgenabschätzung aus den Vorlagen (4.3) ausfüllen.
8. **Register nachführen:** Status `aktiv`, Repo eintragen (Pull Request hier).

## 3. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
|---|---|---|---|---|
| M1 | Wo liegt die Vorlage? | eigenes Template-Repo / Profil im my-github-blueprint + Befehl in Core | **Profil `eduksx-modul` im my-github-blueprint** (Ablauf, CI, Repo-Regeln) **plus** `php artisan eduksx:module-init` in Core (Laravel-Teile); kein drittes Template-Repo, das veraltet | BESCHLOSSEN 13.11.2026 |
| M2 | Datenschutz-Vorlagen | im Blueprint / hier | hier unter `docs/vorlagen/` (plattformweit gleich), das Profil kopiert sie ins Modul | BESCHLOSSEN 13.11.2026 |
| M3 | Erster Stand des Konformitätstests | alle Stufen / Stufe 1 | Stufe 1 «Kern» Pflicht, Stufe 2 als Warnung bis vor dem ersten produktiven Release | BESCHLOSSEN 13.11.2026 |
| M4 | Datenbank im neuen Modul | SQLite / PostgreSQL | SQLite für Entwicklung und kleine isolierte Instanzen, Tests in der CI gegen **beide** (DB C1); `central` startet mit PostgreSQL | BESCHLOSSEN 13.11.2026 |
| M5 | Probe-Modul für den Test der Vorlage | eigenes Repo / temporär in der CI | temporär: ein Workflow im Blueprint erzeugt `probe` und lässt dessen Tests laufen; kein dauerhaftes Repo | BESCHLOSSEN 13.11.2026 |

## 4. Umsetzung

### 4.1 Inhalt eines neuen Moduls

| Datei / Bereich | Inhalt | Regel |
|---|---|---|
| `.github/` | aus dem Blueprint: Issues mit Freigabe, Labels, Meilensteine, `pruefungen`, Release, Dependabot, CodeQL | Plattform §6 «Ablauf» |
| `config/eduksx.php` | `module` = Schlüssel, Betriebsart, Datenklasse, Standards (`db`, `api`) | API G2, DB E5 |
| `routes/api.php` | nur `/api/v1/…`; Gruppe mit Core-Middleware (`request_id`, Kopfzeilen, Abruflimit) | API A1, C5–C7 |
| `openapi/<modul>-v1.json` | Grundgerüst OpenAPI 3.1 mit `info.x-eduksx-module`, Lizenz, `Problem`, Sicherheitsschema | API D3 |
| `/.well-known/eduksx-module.json` | aus `config/eduksx.php` erzeugt | S5, [Schema](../spec/v1/module-manifest.schema.json) |
| `/up`, `/health` | Laravel-Health plus Core-Prüfungen | S5, [Schema](../spec/v1/health.schema.json) |
| `database/migrations` | erste Migration mit `StrictSchema`, Schema = Modulschlüssel | DB A4, E2 |
| `app/Data/Purposes.php` | Zweck, Rechtsgrundlage, Geltungsbereich, Löschfrist je Tabelle | DB B9 |
| `tests/` | Konformitätstest (Core), Mandantentest mit zwei Organisationen (DB B1 Regel 5), Export «alle Daten einer Person» (DB B8) als Gerüst | DB C3, API D7 |
| `.spectral.yaml` | erweitert den Regelsatz `eduksx` aus Core | API D3 |
| `Dockerfile` | aus dem Blueprint; Rollen web/worker/scheduler | Plattform §6 «Betrieb» |
| `docs/DATENSCHUTZ-VERZEICHNIS.md`, `docs/DATENSCHUTZ-FOLGENABSCHAETZUNG.md` | aus `docs/vorlagen/` | DB B9, B10; API C9 |
| `docs/NACHWEIS-ISMS.md` | Nachweis für das ISMS der Schule, aus `docs/vorlagen/AUFTRAGSBEARBEITUNG-ZH.md` Teil D | KONZEPT-DATENSCHUTZ-ZH §6 |
| `docs/third-party.json` | Laravel, `eduksx/core` mit Lizenz | AGENTS.md |
| `composer.json` | `php` ≥ Mindestversion, Skript `ci:check` (Stil, Analyse, Typen, Tests auf SQLite und PostgreSQL, Spectral, axe-core) | [KONZEPT-STACK.md](KONZEPT-STACK.md) §3, §5 |
| `package.json`, CI | Inertia, React, TypeScript, Tailwind, `@eduksx/ui`; Node nach Mindestversion | KONZEPT-STACK §2, §3 |

### 4.2 Teil in `eduksx/core`

`php artisan eduksx:module-init` schreibt nur Dateien, die es noch nicht gibt, und meldet Abweichungen bei
bestehenden (wiederholbar). Er kommt in Core erst, wenn das erste neue Modul ihn braucht (Core: «nichts auf Vorrat») –
voraussichtlich mit `codex` oder `timetable`; bis dahin gilt dieser Abschnitt als Checkliste.

### 4.3 Datenschutz-Vorlagen

- [Verzeichnis der Bearbeitungen](vorlagen/DATENSCHUTZ-VERZEICHNIS.md) – je Modul, aus DB B9 und API C9 befüllt
- [Datenschutz-Folgenabschätzung](vorlagen/DATENSCHUTZ-FOLGENABSCHAETZUNG.md) – Pflicht nach DB B10 bei Datenklasse
  «besonders schützenswert» oder Online-Zugang für viele Personen; bei Kunden im Kanton Zürich gilt zusätzlich die
  Vorlage des Kantons

Die Vorlagen sind Arbeitshilfen, keine Rechtsberatung; die Prüfung durch eine Fachperson bleibt (#22).

### 4.4 Tests der Vorlage

- Workflow im Blueprint (M5): Probe-Modul erzeugen, `composer test`, Konformitätstest, Steckbrief gegen das Schema.
- Dieses Repo prüft nur, dass die Vorlagen und Verweise vorhanden sind (`tests/`).

## 5. Issues

| Issue | Inhalt | Status |
|---|---|---|
| #28 | Dieses Konzept und die Datenschutz-Vorlagen | `_3 Beta-Test` |
| #37 (0.3.0) | Profil `eduksx-modul` im my-github-blueprint und Probe-Modul (M1, M5) | `triage` |
| (folgt, EduKSX-Core) | Befehl `eduksx:module-init` (4.2) | mit dem ersten neuen Modul |

## 6. Verlauf

- 25.11.2026: Stack, Mindestversionen und `ci:check` aus [KONZEPT-STACK.md](KONZEPT-STACK.md) aufgenommen (#79).
- 13.11.2026: Abgenommen, M1–M5 beschlossen; Probe-Modul nach #37 abgespalten.
- 13.11.2026: Konzept angelegt mit Ablauf, Inhalt und Datenschutz-Vorlagen.
