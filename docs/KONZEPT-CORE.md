# Konzept: Gemeinsame Bibliothek `eduksx/core` (#27)

Stand: 13.11.2026 (Meilenstein 0.2.0) · Verantwortlich: Markus Keller · Status: **ENTWURF**

Konkretisiert [Plattform 4.3](KONZEPT-PLATTFORM.md), [DB-Standard](KONZEPT-DB-GUIDELINE.md) (E5, DB-E12) und
[API-Standard G3](KONZEPT-API-GUIDELINE.md). Modulschlüssel `core` laut [Modulregister](REGISTER-MODULE.md).

**Verbindlichkeit:** Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md). Umgesetzt wird erst, was als Issue mit
`_1 bereit` freigegeben ist.

## 1. Ziel

Was jedes Modul gleich macht, baut kein Modul selbst. `eduksx/core` bündelt diese Bausteine als PHP-Paket, damit
Glossary, Intranet und alle weiteren Module dieselben Regeln mit demselben Code einhalten und die Konformitätstests
der Standards überhaupt laufen können.

Grundsatz (API G3, BESCHLOSSEN): **nichts auf Vorrat.** Ein Baustein kommt erst in Core, wenn mindestens ein Modul ihn
braucht und er im Glossary oder Intranet schon erprobt ist. Core 0.1 wird **herausgelöst, nicht neu erfunden**.

**Nichtziele:**
- kein Dienst, keine eigene Datenbank, keine eigene Oberfläche (Plattform 4.3, DB-E12)
- keine Stammdaten von Personen oder Organisationen (gehören Ident)
- kein Fachcode eines Moduls; keine Konfiguration einzelner Kunden

## 2. Ablauf

So arbeitet ein Modul mit Core:

1. `composer require eduksx/core:^0.1` – der Service-Provider registriert sich selbst (Laravel Package Discovery).
2. Das Modul setzt seinen Schlüssel aus dem Register: `EDUKSX_MODULE=glossary`. Daraus leitet Core Präfixe für
   Fehlertypen, Tokens, Ereignisse und MCP-Werkzeuge ab.
3. Migrationen nutzen die Helfer (`StrictSchema`), Controller die Antwort-Bausteine (Fehler, Cursor, ETag).
4. In der CI läuft der Konformitätstest aus Core (`EduKSX\Core\Testing\ConformanceTest`) und der Spectral-Regelsatz
   gegen die OpenAPI-Beschreibung des Moduls.
5. Ein neues Core-Release wird per Dependabot vorgeschlagen; Minor-Versionen sind abwärtskompatibel (SemVer).

## 3. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
|---|---|---|---|---|
| C1 | Bibliothek oder Dienst? | Bibliothek / Dienst | Bibliothek mit Standardtabellen je Modul-Schema | BESCHLOSSEN 13.11.2026 (DB-E12) |
| C2 | Wo entsteht Core? | eigenes Repo / im Glossary | eigenes Repo **EduKSX-Core** | BESCHLOSSEN 13.11.2026 |
| C3 | Lizenz | MIT / intern / AGPL | **MIT** wie das Glossary | BESCHLOSSEN 13.11.2026 |
| C4 | Unterstützte Versionen 0.1 | nur aktuell / auch ältere | **PHP 8.4, Laravel 13** | BESCHLOSSEN 13.11.2026 |
| C5 | Verteilung | Packagist / GitHub als Composer-Repository | Packagist (öffentlich, MIT; kein Token in den Modulen nötig) | EMPFOHLEN |
| C6 | Namensraum | `EduKSX\Core\…` / `Eduksx\Core\…` | `EduKSX\Core\…`, Paket `eduksx/core` | EMPFOHLEN |
| C7 | Standardtabellen (Personenreferenz, Organisationen, Mitgliedschaften) | in 0.1 / mit Ident in 0.2 | **mit Ident (Core 0.2)** – ihre Spalten (`issuer`, `subject`, `platform_id`) hängen vom PoC #25 ab | EMPFOHLEN |
| C8 | Module, die Core-Tabellen schon haben (Glossary) | neu anlegen / übernehmen | Übernahme-Migration prüft Spalten, Typen und CHECKs und passt nur Abweichungen an | EMPFOHLEN |
| C9 | Bindung an die Standards | lose / fest | Core erklärt in `composer.json` (`extra.eduksx.standards`) die Versionen, die es umsetzt (0.1: DB 1.2.1, API 1.1.1); neue Standard-Version → neue Core-Minor | EMPFOHLEN |
| C10 | Gemeinsame Oberfläche (npm-Paket mit React-Komponenten) | jetzt / später | später, eigenes Paket `@eduksx/ui`, erst wenn ein zweites Modul mit Inertia/React entsteht | EMPFOHLEN |

## 4. Umsetzung

### 4.1 Umfang Core 0.1

Reihenfolge nach API G3 (Basis → Listen → Prüfungen). Quelle = heutiger Ort im Glossary.

| Gruppe | Baustein | Quelle im Glossary | Regel |
|---|---|---|---|
| HTTP-Basis | Fehler als `application/problem+json`, Typ-URL mit Modulschlüssel | `bootstrap/app.php` (Fehlerbehandlung) | API A6 |
| | `X-Request-Id` annehmen oder erzeugen, in Antwort und Protokoll | neu (heute nur gelesen in `app/Data/DataChanges.php`) | API C7 |
| | Sicherheitskopfzeilen | `app/Http/Middleware/SecurityHeaders.php` | API C6, Plattform §6 |
| | Abruflimit `api` (Standard 120/Min., konfigurierbar) | `app/Providers/AppServiceProvider.php` | API C5 |
| | CORS-Voreinstellung für öffentliche Lese-APIs | `config/cors.php` | API C6 |
| DB-Basis | `StrictSchema` (STRICT, CHECK, Fremdschlüssel; SQLite und PostgreSQL) | `app/Database/StrictSchema.php` | DB A4, A6 |
| | Trait für `lock_version` (optimistisches Sperren) | Modelle `Term`, `Category`, `Organization` | DB A6, API B2 |
| Listen | Cursor-Pagination (`next_cursor`, `has_more`) | `GlossaryApiController` (Feed `changes`) | API A5 |
| | Starker ETag mit `If-None-Match`/`If-Match`, 304/412 | `GlossaryApiController` | API B2, B5 |
| Prüfungen | Spectral-Regelsatz `eduksx` (zuerst als Warnung) | neu | API D3 |
| | Konformitätstest: Tabellen- und Spaltennamen englisch, STRICT/CHECK, Index auf Fremdschlüsseln, Präfixe mit Modulschlüssel | neu | DB E5, API D8 |

**Nicht in 0.1** (kommt, sobald ein Modul es braucht): OIDC-Client und Token-/JWT-Prüfung (mit Ident, 0.2),
Standardtabellen (C7), Historie `data_changes` mit Datenklassen (heute `app/Data/DataChanges.php`,
`DataClasses.php` – Kandidat für 0.2), Anonymisierung, Export, Idempotenz-Speicher, Webhook-Signatur, HTTP-Client mit
SSRF-Schutz, Werkzeug SQLite → PostgreSQL (DB E6), Steckbrief und `/health` (Plattform S5).

### 4.2 Herauslöse-Plan

1. **Repo anlegen** (Projektverantwortliche:r): `EduKSX-Core`, MIT, mit my-github-blueprint (CI, Releases, Dependabot).
2. **Bausteine übernehmen:** Code aus dem Glossary mit seinen Tests nach `EduKSX\Core\…`; Glossary-Bezüge entfernen,
   Modulschlüssel aus der Konfiguration. Tests laufen gegen SQLite **und** PostgreSQL.
3. **Core 0.1.0 veröffentlichen** (nach Freigabe).
4. **Glossary stellt um** (Issue im Glossary, verknüpft mit Glossary #193): eigene Klassen durch Core ersetzen,
   Verhalten unverändert (gleiche API-Antworten, bestehende Tests grün).
5. **Intranet stellt um** (zweiter Abnehmer): `problem+json` statt `{"message": …}` und Cursor statt `limit/offset`
   (Abweichungen laut API-Standard). Was das Intranet anders braucht, fliesst als Verbesserung in Core zurück.

Erst wenn beide Module Core 0.1 nutzen, gilt ein Baustein als bewährt; Ausnahmen nur über das Ausnahmeregister (API D8).

### 4.3 Sicherheit und Datenschutz

- Core verarbeitet keine Personendaten selbst; Protokolle maskieren nach Datenklasse (API C7).
- Abhängigkeiten von Core sind minimal (nur Laravel); jede neue Abhängigkeit mit Lizenz- und Pflegeprüfung.
- Sicherheitslücken in Core betreffen alle Module: eigenes `SECURITY.md`, Patch-Releases ohne Wartezeit.

### 4.4 Tests

- Einheitstests je Baustein; Konformitätstest an einem Beispielmodul in Core selbst.
- Matrix PHP 8.4 × SQLite/PostgreSQL in der CI.
- Glossary und Intranet behalten ihre API-Tests; sie belegen, dass die Umstellung nichts verändert.

## 5. Issues

| Issue | Inhalt | Status |
|---|---|---|
| #27 | Dieses Konzept | `_2 in Arbeit` |
| (folgt) | EduKSX-Core: Grundgerüst und Bausteine 0.1 | erst nach Abnahme des Konzepts |
| Glossary #193 | Bausteine abgrenzen – wird zur Umstellung auf Core 0.1 | `triage` |

## 6. Verlauf

- 13.11.2026: Entwurf angelegt; C1–C4 im Chat entschieden.
