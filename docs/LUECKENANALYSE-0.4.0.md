# Lückenanalyse: Grundlagen der EduKSX-Plattform

Stand 22.11.2026. Geprüft gegen das Repo EduKSX-Architektur (Konzept 0.3.0, eingefroren) und als Referenzmodul
EduKSX-Glossary 0.18.0-beta.1. Reine Analyse, keine Konzeptänderung. Die Lücken werden im Meilenstein «0.4.0 – Konzept erweitert» mit Label
`konzept-erweiterung` geschlossen (#70), jeweils nach Freigabe.

Bewertung: **geregelt** = beschlossen und konkret genug zum Umsetzen · **teilweise** = Grundsatz vorhanden, aber
Regeln fehlen oder widersprechen sich · **Lücke** = kein Konzept.

## 1. Ergebnis auf einen Blick

| Nr. | Thema | Stand | Wo geregelt | Was fehlt |
| --- | --- | --- | --- | --- |
| 1 | API-First | teilweise | API-Standard Grundsatz 1, D3 «Vertrag zuerst» | Begriff nicht ausgeführt; offen, ob eigene Oberflächen die API nutzen oder nur dieselben Services |
| 2 | Datenbank-Design | geregelt | DB-Standard A1–A6, B1, E1–E6 | – (nur Kleinigkeiten, siehe 2.2) |
| 3 | Mehrsprachigkeit | geregelt, Details offen | DB D1, API A4, A8 | Sprachenliste je Modul, Übersetzungsstatus, Abkürzungen je Sprache |
| 4 | Historie | geregelt | DB A7, B2, B11 | Aufbewahrungsfrist der Historie; Archivpflicht (siehe 9) |
| 5 | Sicherung und Wiederherstellung | teilweise | DB C2, Glossary D6, Operation | Widerspruch RPO 1 Min. ↔ täglicher Dump (Operation #27 offen); Restore-Test noch nicht nachgewiesen |
| 6 | GUI und Theme | Lücke auf Plattformebene | nur Prüfliste («Design-System aus Core»), Plugins P5 | Plattform-Konzept Design-System, Themes, Bausteine, Paket `@eduksx/ui` |
| 7 | Debugging und Logs | teilweise | API C7 (nur EMPFOHLEN), Plattform §6, Operation (VictoriaLogs) | Konzept Protokollierung und Fehlersuche: Stufen, Fristen je Art, Tracing, Fehler-Tracking, Support-Zugriff |
| 8 | Rollenkonzept | teilweise | DB B4, API C2, Plattform S1, Ident | Plattformweiter Rollenkatalog, Namensschema für Rechte, Rechte auf Feld- bzw. Datenebene, Stellvertretung |
| 9 | Datenschutz nach DSB Kanton Zürich | weitgehend geregelt | DB B7–B14, API C9, Vorlagen DSFA/Verzeichnis | Klassifizierung nach IVSV, Vertrag nach § 25 IDV, Anbietepflicht Archiv, Prüfung durch Fachperson (#22) |

Die allgemeine Liste (Bereiche 1–9) ist in Abschnitt 3 Punkt für Punkt geprüft. Dort zusätzlich offen:
UI-Bausteine in Core, einheitlicher Stack (Frontend, Versionen), Performance- und Verfügbarkeitsziele, Wartbarkeitsziele,
Feature-Schalter.

## 2. Die neun Punkte im Einzelnen

### 2.1 API-First – was heisst das?

**Heute:** Grundsatz 1 sagt: jede Funktion, die ein anderes System braucht, gibt es zuerst als API; Website, Intranet
und MCP nutzen **dieselben Services**. D3 verlangt «Vertrag zuerst» (OpenAPI-Datei vor dem Code, Test Route ↔
Beschreibung, Linter, `oasdiff`).

**Unklar:** Das ist eher «Service-First» als API-First. Das Glossary baut seine Website mit Inertia direkt auf den
Services, nicht über die eigene API. Beides ist vertretbar, muss aber ausdrücklich entschieden sein.

**Vorschlag für eine klare Regel:**

| Stufe | Bedeutung | Bewertung |
| --- | --- | --- |
| A · Vertrag zuerst | Jede Schnittstelle nach aussen steht zuerst in OpenAPI, wird geprüft und dann gebaut | heute beschlossen |
| B · Funktion zuerst als API | Jede fachliche Funktion (lesen, ändern, freigeben, exportieren) gibt es als API-Operation, nicht nur in der Oberfläche | nur für Funktionen «die ein anderes System braucht» beschlossen → auf alle Fachfunktionen ausweiten? |
| C · Eigene Oberfläche als API-Client | Website und Administration rufen nur die eigene API auf (headless) | heute nicht verlangt; teuer, bringt aber echte Gleichheit |

Empfehlung: A und B verbindlich, C nicht verlangen. Ein Test stellt sicher, dass jede schreibende Aktion der
Oberfläche eine API-Operation mit demselben Service und derselben Policy hat. Dazu festhalten: interne APIs
(`/api/sync`) folgen denselben Regeln, sind aber nicht öffentlich dokumentiert.

### 2.2 Datenbank-Design

**Geregelt (DB-Standard 1.3):**

- Normalisierung: dritte Normalform, Ausnahmetabelle je Modul (A2).
- Namen: englisch, `snake_case`, Tabellen im Plural, Verknüpfungen, Protokolle, Zeitpunkte `_at`, Daten `_on`, Ja/Nein `is_`/`has_`, Übersetzungen, Overrides, Indizes, Mandant `organization_id` (A1).
- PK: `id`; UUID v7 für Fachobjekte und Konten, Zahl für Protokolle; `event_id` für Modulübergreifendes (A3, E4).
- FK: Constraint mit `ON DELETE` je Fall, ohne Constraint für Protokolle mit `actor_label`; zusammengesetzte FK für Zugehörigkeit (A3).
- Indizes: jede FK-Spalte, weitere nur mit `EXPLAIN` belegt (A3).
- Felder und Typen: Tabelle A4, Enums mit CHECK, STRICT, Geld in Rappen.
- Geltungsbereich (Scope) je Tabelle: global, Organisation, persönlich (B1).
- Mehrere Module: Modulschlüssel, eigenes Schema, keine Präfixe, Plattform-IDs, Zusammenlegen geübt (E1–E6).
- Deutsche Beschreibung jeder Tabelle, Spalte und jedes Enum-Werts (A8).

**Kleinigkeiten:**

- Standardspalten sind in A8 aufgezählt, aber nicht als Pflichtsatz je Geltungsbereich (welche Spalten **jede** Fachtabelle hat). Eine kleine Tabelle «Pflichtspalten» würde Diskussionen sparen.
- Namensschema für gemeinsame Stammdaten (Sprachen, Schulstufen) als Plattformdienst ist angedeutet (E4), aber kein Dienst zugeordnet.

### 2.3 Mehrsprachigkeit

**Geregelt:** Fachliche Inhalte immer mehrsprachig ab Start (Grundsprache in der Haupttabelle, übrige in
`*_translations`), technische Texte im Code, persönliche Freitexte ohne Übersetzung, Rückfall auf `de`, ISO 639-1
(D1); Sortierung und Suche je Sprache (D3); API mit `Accept-Language` (A4).

**Offen bzw. zu präzisieren:**

- **Abkürzungen je Sprache:** Eine Abkürzung ist nicht immer eine Übersetzung (z. B. eine deutsche Abkürzung ohne Entsprechung). Regel: Abkürzung, Langform, Beschreibung und Erklärungstext sind alle übersetzbare Felder; eine fehlende Übersetzung zeigt die Grundsprache **mit Sprachkennzeichnung**.
- **Übersetzungsstatus:** Feld `translation_status` (z. B. `machine`, `reviewed`) und wer prüft. Ohne das sind maschinelle Übersetzungen nicht erkennbar.
- **Sprachenliste:** welche Sprachen ein Modul anbietet (de, fr, it, en; Rätoromanisch?) gehört in den Steckbrief.
- **Oberflächensprache:** Wahl der Person (Claim `locale`) vs. Einstellung der Organisation.

### 2.4 Historie für lückenlose Nachvollziehbarkeit

**Geregelt (A7):** jede Änderung in derselben Transaktion; zentrale Tabelle `data_changes` mit `event_id`,
`actor_*`, `source`, `transaction_id`, `request_id`, `schema_version`; Werte nach Datenklasse (B2); unveränderlich;
Hash-Verkettung für das Sicherheitsprotokoll; Test gegen Schreibzugriffe am Service vorbei; Lesezugriffe auf besonders
schützenswerte Daten protokolliert (B11).

**Offen:**

- **Aufbewahrungsfrist der Historie** je Modul (B9 verlangt Fristen je Tabelle, für `data_changes` ist keine Vorgabe gesetzt).
- **Archivpflicht** vor dem Löschen (siehe 2.9).
- **Anzeige:** Gibt es eine einheitliche Ansicht «Verlauf» in allen Modulen (Baustein in Core)?

### 2.5 Sicherung und Wiederherstellung

**Geregelt (DB C2):** laufend (Litestream bzw. Base Backup + WAL), PITR, Einzelsnapshot vor Updates,
verschlüsselt, Schlüssel getrennt, monatlicher Restore-Test, Löschregister vor dem Start; RPO/RTO je Dienstart
(zentral 1 Min./4 h, isoliert 15 Min./1 Arbeitstag, Ident 1 Min./1 h).

**Widerspruch (bekannt, offen):** Operation sichert mit Backrest/restic täglich (Dump). Damit ist RPO 1 Minute für
PostgreSQL nicht erreichbar; das Glossary sichert auf PostgreSQL ebenfalls täglich (`taeglich.zip`). Prüfauftrag
MarKusSX-Operation #27. Entweder WAL-Archivierung in Operation aufnehmen oder RPO für PostgreSQL-Dienste senken.

**Zu ergänzen:**

- Nachweis des Restore-Tests (Protokoll, gemessene Dauer gegen RTO) als Teil von `/health` oder Leitstand.
- Wiederherstellung **einer** Organisation aus einer zentralen Datenbank (nicht nur ganze Datenbank).
- Wiederherstellung von Dateien (Object Storage) zusammen mit der Datenbank.

### 2.6 GUI und Theme-Design

**Heute:** Plattform-Prüfliste «Design-System und Kopfzeile mit Modulwechsel aus `eduksx/core`», WCAG 2.1 AA
(eCH-0059); Plugins übernehmen Farben über CSS-Variablen `--eduksx-*`, später `@eduksx/ui`. Inhaltlich liegt alles in
anderen Repos: Marke im CI-Manual (markussxch), Bausteine und Themes im sek-intranet (`KONZEPT-THEMES.md`,
`GUI-KOMPONENTEN.md`), Übernahme im Glossary (`KONZEPT-DESIGN.md`).

**Lücke:** kein Plattform-Konzept. Der Core-Fahrplan (0.1–0.3) enthält keinen UI-Baustein. Festzulegen:

- Quelle der Design-Tokens (Farben, Schrift, Abstände, Radien) und wie sie verteilt werden (npm-Paket `@eduksx/ui`).
- Themes: hell/dunkel, hoher Kontrast, Farbe je Modul, Branding je Organisation (Logo, Primärfarbe) – was ist erlaubt.
- Gemeinsame Bausteine (Kopfzeile, Modulwechsel, Tabellen/Data-Grid, Dialoge, Formulare, Verlauf, Hilfe nach Rolle).
- Schreibweise und Texte (Schweizer Schreibweise, Datumsformat D2, keine Entscheidnummern).
- Prüfung: Barrierefreiheit automatisch (axe) in der CI, Kontrast je Theme.

### 2.7 Debugging und Logs

**Heute:** Anfrage-ID, JSON-Protokolle ohne Personendaten, Warnmuster, Hash-Verkettung (API C7, nur EMPFOHLEN);
Plattform §6: JSON auf stdout, `/metrics`; Betrieb mit VictoriaLogs (Operation); Fehler ohne Stacktraces (API A6);
API-Protokolle 90 Tage (C9).

**Lücke:** kein zusammenhängendes Konzept. Festzulegen:

| Thema | Frage |
| --- | --- |
| Protokollarten | Anwendung, Zugriff, Sicherheit, Audit, Job – je Art Ort, Frist, Zugriff |
| Stufen | was ist `debug`/`info`/`warning`/`error`; Standard je Umgebung |
| Fehlersuche in prod | `APP_DEBUG` immer aus; zeitlich begrenztes Debug je Organisation oder Anfrage, protokolliert |
| Korrelation | `X-Request-Id` bzw. W3C `traceparent` über S2, S4 und Jobs weitergeben |
| Fehler-Tracking | Werkzeug (selbst gehostet, Schweiz) oder nur Logs; Alarmierung |
| Personendaten | Maskierung im Code (Core), nicht nur Konvention; Test |
| Support | wer darf Kundenprotokolle sehen, wie protokolliert |
| Selbst-Hosting | wie ein Kunde Protokolle für den Support bereitstellt |

Empfehlung: API C7 auf BESCHLOSSEN heben und als Abschnitt «Protokollierung und Fehlersuche» im Plattform-Konzept
ausbauen; Bausteine (Logger-Format, Maskierung, Weitergabe der IDs) in Core.

### 2.8 Rollenkonzept (Zugriff auf Funktionen und Daten)

**Geregelt:** Rollen je Modul und Organisation `(user_id, organization_id, role)`; geprüft wird auf Rechte, nicht
Rollennamen (DB B4); Scopes `<modul>:<ressource>.<aktion>` begrenzen Tokens (API C2); Org-Rollen `admin`/`member`
und Modulrollen über Claims (S1); Rollen im Steckbrief (S5); MFA für privilegierte Rollen; Super-Admin aus Ident;
Datenzugriff über Geltungsbereiche (B1) und Datenklassen (B2).

**Lücken:**

- **Rollenkatalog der Plattform:** welche Personengruppen es gibt (Schulleitung, Verwaltung, Lehrperson, Schülerin/Schüler, Eltern, IT, Extern) und welche Standardrollen jedes Modul mindestens anbietet (z. B. `reader`, `editor`, `admin`).
- **Namensschema für Rechte:** `x-eduksx-ability` ist verlangt, aber das Format nicht festgelegt (Vorschlag analog Scopes: `<ressource>.<aktion>` plus Fachrechte wie `terms.publish`).
- **Daten-Ebene:** Rechte auf Feldgruppen (z. B. besonders schützenswerte Felder nur für bestimmte Rollen) und auf Teilmengen (eigene Klasse, eigenes Schulhaus).
- **Zeit und Stellvertretung:** befristete Rollen, Stellvertretung, Entzug beim Austritt (Ereignis aus Ident).
- **Minderjährige:** Rechte von Eltern und Schülerinnen/Schülern, Altersgrenzen.
- **Nachweis:** Rollen-Rechte-Matrix je Modul als Datei (aus dem Code erzeugt), Rezertifizierung (wer prüft jährlich).

### 2.9 Datenschutz nach Vorgaben der DSB Kanton Zürich

**Geregelt:** strengste Regel aus IDG, DSG, DSGVO (B7); Datenklassen je Feld (B2); Zweck, Rechtsgrundlage und
Frist je Tabelle mit Test (B9); Folgenabschätzung nach Vorlage des Kantons und Vorabkontrolle (B10); Auskunft und
Export (B8, API C9); Löschregister (B3); Lesezugriffe protokolliert (B11); nur anonymisierte Kopien für dev/test
(B12); Einschränkung und Verletzungen (B13); Datenort Schweiz/EU; Vorlagen Folgenabschätzung und Verzeichnis.

**Lücken bzw. zu prüfen:**

1. **Klassifizierung:** Die Verwaltung des Kantons Zürich klassifiziert in vier Stufen: öffentlich, intern, vertraulich, geheim. EduKSX nutzt zwei andere Schemata: DB B2 (öffentlich, intern, personenbezogen, besonders schützenswert, geheim) und Plattform §6 (öffentlich, intern, vertraulich, besonders schützenswert). Es braucht **eine** Zuordnung beider auf die vier Stufen des Kantons, damit Schulen ihre Klassifizierung übernehmen können.
2. **Bearbeiten im Auftrag:** Für Schulen als öffentliche Organe ist der Betrieb durch EduKSX ein Bearbeiten im Auftrag (§ 6 IDG, § 25 IDV). Die DSB stellt dafür den «Leitfaden Bearbeiten im Auftrag» mit Checklisten bereit. Fehlt: Vertragsvorlage für Kunden, die § 25 IDV abdeckt, und ein Abgleich der Plattform mit den Checklisten des Leitfadens (Informationssicherheitsmassnahmen, Vertragskriterien).
3. **Cloud-Vorgaben:** Merkblatt Cloud Computing und Leitfaden Verschlüsselung: Anbieter (Infomaniak, Hostinger für dev, Cloudflare) mit Risikoanalyse dokumentieren; CLOUD-Act-Fragen bei Cloudflare.
4. **Archivierung:** Öffentliche Organe im Kanton Zürich müssen Unterlagen vor der Vernichtung dem zuständigen Archiv anbieten (Archivgesetz, IVSV). Das Löschkonzept kennt nur Löschen. Für Module mit Geschäftsunterlagen (Codex, Intranet, Sign, Staffing) braucht es eine Regel «anbieten, dann löschen» bzw. einen Export für das Archiv.
5. **Leitfaden Informationssicherheit in Volksschulen:** Die DSB verlangt von Schulen ein ISMS; EduKSX sollte zeigen, welche Anforderungen die Plattform für die Schule erfüllt (Nachweisdokument je Modul).
6. **Prüfung durch Fachperson:** API C9 und DB B3 tragen noch ZU PRÜFEN (#22, Glossary #278).

## 3. Die allgemeine Liste (Bereiche 1–9)

Die neun Bereiche aus der allgemeinen Liste «Was ist zu Beginn festzulegen», Punkt für Punkt.

| Bereich | Punkt | Stand | Wo geregelt bzw. was fehlt |
| --- | --- | --- | --- |
| 1 Grundsatzentscheide | Schnitt der Module | geregelt | Modulübersicht; Kriterium «auch einzeln sinnvoll» |
| | Architekturstil | geregelt | eigenständige Module je Repo, zusammenlegbar (DB Grundsatz 7, Teil E); kein Kubernetes |
| | Abhängigkeitsregeln | geregelt | kein Zugriff auf fremde DB, Austausch nur über API/Ereignisse (API Grundsatz 2, DB B5/E2) |
| | Betriebsmodell | geregelt | zentral/isoliert (Plattform 4.2), Selbst-Hosting (#40), Stufen §7 |
| 2 Schnittstellen | API-Richtlinie | geregelt | API-Standard A–D |
| | Maschinenlesbare Verträge | geregelt | OpenAPI 3.1, `spec/v1`, Linter, `oasdiff` (D3) |
| | Ereignisse | geregelt | S4, CloudEvents, Signatur (B7) |
| | Plugin-Modell | geregelt | Plugins P1–P5, Steckbrief S5 |
| 3 Identität | Anmeldung, IdP | geregelt | Ident/Zitadel, S1; Ausnahme Selbst-Hosting |
| | Berechtigungsmodell | teilweise | siehe 2.8 |
| | Technische Identitäten | geregelt | Servicekonten, Client Credentials (DB B4, S2) |
| | Stabile IDs | geregelt | UUID v7, `issuer`+`subject`, `platform_id` (A3, B4, E3) |
| 4 Daten | Datenhoheit | geregelt | Schema je Modul (E2) |
| | DB-Richtlinie | geregelt | siehe 2.2 |
| | Datenschutz | weitgehend | siehe 2.9 |
| | Mandantenfähigkeit | geregelt | B1, `organization_id` auch isoliert; RLS ZU PRÜFEN (#34) |
| 5 Core | Umfang, Versionierung, Verteilung | geregelt | Core 0.1–0.3, Paket mit SemVer, Versionsbindung (E5) |
| | Kein zu grosser Core | geregelt | «kommt, sobald ein Modul es braucht» (Core 4.1) |
| | UI-Bausteine in Core | **Lücke** | siehe 2.6 |
| 6 Technologie-Stack | Einheitlicher Stack | **teilweise** | Backend Laravel nur über die Modulvorlage festgelegt; Frontend (React/Inertia, Tailwind), Versionen und Support-Fenster nicht plattformweit beschlossen |
| | Prüfbefehl | teilweise | im Glossary (`composer ci:check`), Konformitätstests aus Core; kein gemeinsamer Befehl in der Modulvorlage beschrieben |
| | Lizenzpolitik | geregelt | MIT/AGPL, `third-party.json` |
| 7 Entwicklungsprozess | Repo-Struktur, Vorlage | geregelt | ein Repo je Modul, Blueprint, Modulvorlage |
| | Versionierung, Releases | geregelt | SemVer, Beta/Stable, CHANGELOG |
| | Branching, Reviews | geregelt | GITHUB-ABLAUF, PR-Pflicht, Squash |
| | Entscheide dokumentieren | geregelt | Entscheidtabellen, Konzept-Vorlage, Konzepte als PR |
| 8 Auslieferung, Betrieb | Ein Build, ein Image | geregelt | Plattform §6, Glossary D1 |
| | Umgebungen, Datenfluss | geregelt | dev/test/prod, anonymisierte Kopien (B12), Glossary DEC-041 |
| | Konfiguration, Geheimnisse | geregelt | Plattform §6, DB B6, Operation (1Password) |
| | Health, Rollback | geregelt | `/up`, `/health`, Glossary D5 |
| | Sicherung | teilweise | siehe 2.5 |
| | Monitoring | teilweise | `/metrics`, VictoriaLogs in Operation; siehe 2.7 |
| | Supply-Chain | teilweise | SBOM, Signatur, Dependabot, CodeQL beschlossen; Image-Scan im Glossary noch nicht umgesetzt |
| 9 Qualitätsziele | Sicherheit | geregelt | ASVS L2, ZAP, Pentest (API C10) |
| | Barrierefreiheit | teilweise | Ziel WCAG 2.1 AA, automatische Prüfung fehlt (siehe 2.6) |
| | RPO/RTO | geregelt, Widerspruch | DB C2; siehe 2.5 |
| | **Performance, Verfügbarkeit** | **Lücke** | keine Antwortzeiten (z. B. p95), keine Verfügbarkeit je Dienstart, keine Lastannahmen |
| | **Wartbarkeit** | **Lücke** | keine plattformweiten Ziele (PHPStan-Stufe, Testabdeckung, Support-Fenster der Versionen) |
| | Einfachheit Selbst-Hosting | geregelt | Installation unter 15 Minuten ohne Docker-Kenntnisse (Selbst-Hosting Ziel) |
| zusätzlich | Feature-Schalter | teilweise | Einstellungen je Modul, aber kein gemeinsames Muster (Glossary hat Schalter mit env-Sperre) |

## 4. Vorschlag Reihenfolge

1. **Sicherung:** Widerspruch RPO ↔ Operation #27 entscheiden (betrifft prod des Glossary direkt).
2. **Datenschutz ZH:** Klassifizierung abbilden, Vertragsvorlage § 25 IDV, Archivregel – vor dem ersten Kunden.
3. **Rollenkonzept:** Rollenkatalog und Rechte-Namensschema – bevor weitere Module (Intranet, Staffing) Rollen anlegen.
4. **API-First:** Begriff entscheiden (Stufen A/B) – kleiner Aufwand, verhindert Uneinheitlichkeit.
5. **Protokollierung und Fehlersuche:** C7 beschliessen und ausbauen.
6. **Design-System:** Plattform-Konzept und `@eduksx/ui`, sobald ein zweites Modul eine Oberfläche bekommt.
7. Stack plattformweit festhalten (Frontend, Versionen, Support-Fenster) und Qualitätsziele ergänzen (Performance,
   Verfügbarkeit, Wartbarkeit).
8. Mehrsprachigkeit und Historie präzisieren.

## 5. Issues (Meilenstein «0.4.0 – Konzept erweitert»)

| Issue | Thema | Abschnitt |
| --- | --- | --- |
| #70 | Regel Konzept-Erweiterung (README, CONTRIBUTING) | – |
| #71 | Gesamtprüfung: Widersprüche, veraltete Stellen, Verweise | alle |
| #72 | API-First: Begriff und Stufen | 2.1 |
| #73 | DB-Standard 1.4: Pflichtspalten, Frist der Historie, Mehrsprachigkeit | 2.2–2.4 |
| #74 | Sicherung: RPO/RTO mit Operation, Restore-Nachweis | 2.5 |
| #75 | Design-System und Themes | 2.6 |
| #76 | Protokollierung und Fehlersuche | 2.7 |
| #77 | Rollen und Rechte | 2.8 |
| #78 | Datenschutz DSB Kanton Zürich | 2.9 |
| #79 | Technologie-Stack und gemeinsame Muster | 3 (Bereich 6) |
| #80 | Qualitätsziele | 3 (Bereich 9) |

Umsetzung je Issue erst nach Freigabe.

## Quellen

- Repo EduKSX-Architektur: `docs/KONZEPT-DB-GUIDELINE.md` (1.3), `docs/KONZEPT-API-GUIDELINE.md`, `docs/KONZEPT-PLATTFORM.md`, `docs/KONZEPT-CORE.md`, `docs/KONZEPT-IDENT.md`, `docs/KONZEPT-PLUGINS.md`, `docs/UEBERGABE.md`, `spec/v1/`
- Repo EduKSX-Glossary: `docs/KONZEPT-DEPLOYMENT.md`, `docs/KONZEPT-DESIGN.md`, `docs/SELBST-HOSTEN.md`
- DSB Kanton Zürich: [Leitfaden Bearbeiten im Auftrag](https://docs.datenschutz.ch/u/d/publikationen/leitfaeden/leitfaden_bearbeiten_im_auftrag.pdf), [Merkblatt Cloud Computing](https://docs.datenschutz.ch/u/d/publikationen/formulare-merkblaetter/merkblatt_cloud_computing.pdf), [Leitfaden Nutzung externer Cloud-Dienste](https://docs.datenschutz.ch/u/d/publikationen/leitfaeden/leitfaden_nutzung_externer_cloud_dienste.pdf), [Leitfaden Informationssicherheit in Volksschulen](https://docs.datenschutz.ch/u/d/informationssicherheit/schulen/leitfaden_informationssicherheit_volksschulen.pdf)
- Kanton Zürich: [Leitfaden Informationsverwaltung und Archivierung für Gemeinden](https://internet.zh.ch/content/dam/zhweb/bilder-dokumente/themen/politik-staat/informationsverwaltung/bereich-gemeindearchive/leitfaden_informationsverwaltung_archivierung_fuer_gemeinden.pdf), Klassifizierung öffentlich/intern/vertraulich/geheim z. B. [Vorlage Richtlinie Dokumentenlenkung Schulen (MBA)](https://help.mba.zh.ch/images/InformationssicherheitDatenschutz/Vorlage_Richtlinie_Dokumentenlenkung_Schulen.docx)

Keine Rechtsberatung; die Punkte in 2.9 prüft eine Fachperson.
