# Konzept: DB-Standard der EduKSX-Plattform (#9, #11, #20)

Stand: 20.11.2026 (Version 1.3) · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** – Version 1.3 abgenommen am 20.11.2026
(Version 1.2 am 13.11.2026, Version 1.0 und 1.1 am 12.11.2026)

Verbindlicher Datenbank-Standard für **alle** EduKSX-Module (Glossary, Rechtssammlung, Intranet, Stundenplan …) – für
Menschen und KI-Agenten. Er enthält nur Regeln, die für jedes Modul gelten. Fachliche Tabellen, Befehle und
modulspezifische Entscheide stehen im Datenmodell des jeweiligen Moduls, das auf diesen Standard verweist (für das
Glossary: `docs/KONZEPT-DB-GUIDELINE.md` im Repo EduKSX-Glossary).

**Verbindlichkeit** (Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md)): Alle Regeln sind **BESCHLOSSEN**
(12.11.2026 bzw. – für Teil E und B7–B14 – 13.11.2026), ausser sie sind ausdrücklich als **ZU PRÜFEN** gekennzeichnet.

Der Standard ist in fünf Teile gegliedert:

| Teil | Inhalt |
| --- | --- |
| [A · Grundregeln](#a--grundregeln) | Namen, Normalisierung, Schlüssel, Typen, Migrationen, Transaktionen, Sperren, Historie |
| [B · Sicherheit und Datenschutz](#b--sicherheit-und-datenschutz) | Geltungsbereiche und Mandanten, Datenklassen, Löschen und Löschregister, Identitäten, Datenbankzugänge, Rechtsrahmen, Betroffenenrechte, Zweck, Folgenabschätzung, Zugriffsprotokoll, Testdaten |
| [C · Betrieb](#c--betrieb) | Plattform SQLite/PostgreSQL, Sicherung und Wiederherstellung, RPO/RTO, Tests |
| [D · Sprachen](#d--sprachen) | Mehrsprachigkeit, Datum und Zeit, Sortierung und Suche |
| [E · Modularität und Zusammenführbarkeit](#e--modularität-und-zusammenführbarkeit) | Modulschlüssel, Schema je Modul, Plattform-IDs, Versionsbindung, Konformitätstests, Zusammenlegen |

## Grundsätze

1. **Technik englisch, Anzeige deutsch** – übersetzt wird nur über Labels im Code, nie in der Datenbank. Jeder englische
   Name hat im Datenmodell eine deutsche Beschreibung (A8). BESCHLOSSEN
2. **Kein Datenverlust** – jede Änderung überführt bestehende Daten, zählt vorher und nachher und bricht bei Abweichung
   ab. BESCHLOSSEN
3. **Öffentlich, Organisation und persönlich strikt getrennt** – technisch, nicht nur per Konvention. BESCHLOSSEN
4. **Nachvollziehbar** – jede Datenänderung ist mit wer, wann, was belegt. BESCHLOSSEN
5. **Ein fachliches Modell, datenbankspezifische Umsetzung erlaubt** – SQLite und PostgreSQL werden beide geprüft.
   BESCHLOSSEN
6. **Konzept vor Code** – Schemaänderungen, die vom Standard abweichen, kommen zuerst als Konzept-PR zur Abnahme.
   BESCHLOSSEN
7. **Eigenständig, aber zusammenführbar** – jedes Modul läuft mit eigener Datenbank in eigenem Repo; Namen und
   Schlüssel sind so gewählt, dass Datenbanken später ohne Konflikte zusammengelegt werden können (Teil E).
   BESCHLOSSEN 13.11.2026
8. **Strengstes Datenschutzrecht** – umgesetzt wird jeweils die strengste Regel aus IDG, DSG und DSGVO (B7).
   BESCHLOSSEN 13.11.2026

---

## A · Grundregeln

### A1 Namen (BESCHLOSSEN)

Alle Namen in der Datenbank sind englisch und `snake_case`.

| Regel | Element | Muster | Richtig | Falsch |
| --- | --- | --- | --- | --- |
| N1 | Sprache | englisch, `snake_case` | `short_description` | `kurzbeschreibung`, `shortDescription` |
| N2 | Tabelle | Plural | `documents`, `proposals` | `document` |
| N2 | Verknüpfung | `<besitzer_singular>_<ziel_plural>` | `document_categories`, `user_roles` | `categories_documents` |
| N2 | Protokoll | `<objekt>_audit` (unveränderlich), `<objekt>_events` (Verlauf) | `user_audit`, `proposal_events` | `user_audits` |
| N3 | Primärschlüssel | immer `id` | `id` | `document_id` als PK |
| N4 | Fremdschlüssel | `<ziel>_id` bzw. `<rolle>_id` | `responsible_user_id` | `responsible` |
| N4 | handelnde Person | `<verb>_by_id` | `approved_by_id` | `approved_by` |
| N6 | Zeitpunkt | `<x>_at` | `published_at` | `published` |
| N6 | Datum | `<x>_on` | `retrieved_on` | `retrieved_at` für ein Datum |
| N6 | Zeitraum | `valid_from` / `valid_until` | `valid_from` | `start_date` |
| N7 | Ja/Nein | `is_<x>` / `has_<x>`, nie verneint | `is_active` | `is_not_hidden` |
| N8 | Status / Art | `status` bzw. `<x>_type` | `relation_type` | `kind`, `typ` |
| N9 | Übersetzung | `<objekt>_translations` mit `locale` | `document_translations` | `documents_fr` |
| N10 | Abweichung | `<feld>_override` in `*_overrides` | `name_override` | `own_name` |
| N11 | Index | Laravel-Standard `<tabelle>_<spalten>_index` / `_unique` / `_foreign` | `document_categories_category_id_index` | `idx_cat` |
| N12 | JSON-Spalte | sprechender Name für Abbild/Liste | `snapshot`, `changes`, `details`, `scopes` | `data`, `json` |
| N13 | Mandant | `organization_id` | `organization_id` | `tenant`, `school_id` |

Darum herum: Klassen, Methoden, Variablen englisch; Werte von Status und Arten englisch `snake_case` – identisch in
Datenbank, API und Maschinen-Exporten; Routen der Website deutsch, der API englisch; Excel- und PDF-Spalten deutsch.

### A2 Normalisierung (BESCHLOSSEN)

Standard ist die **dritte Normalform**: Jede Information steht an genau einer Stelle.

1. **Eine Information, eine Stelle:** Jede Spalte hängt vollständig und nur vom Schlüssel ihrer Tabelle ab.
2. **Keine Listen in einem Feld:** keine kommagetrennten Werte, keine wiederholten Spalten (`alias_1`, `alias_2`).
   Mehrfachwerte bekommen eine eigene Tabelle, n:m-Bezüge eine Verknüpfungstabelle.
3. **Abgeleitete Werte werden berechnet, nicht gespeichert** (Summen, Zähler, Anzeigetexte).
4. **Auswahlwerte:** feste, vom Code bestimmte Werte als Enum mit CHECK-Regel; Werte, die eine Redaktion pflegt, als
   eigene Stammdatentabelle mit Übersetzungen.
5. **Gemeinsam, Organisation und persönlich getrennt:** Abweichungen je Organisation oder Person nie in der
   Haupttabelle, sondern in `*_overrides` (N10).
6. **Sprachen getrennt:** Übersetzungen nur in `*_translations` (D1), nie als Sprachspalten.
7. **Doppelte Speicherung nur als Ausnahme:** für unveränderliche Abbilder, Historie, Namen als Text für die
   Pseudonymisierung – für Performance nur mit Messung. Jedes Modul führt eine **Ausnahmetabelle** (Wo, was doppelt,
   Grund, wie aktuell gehalten) in seinem Datenmodell. Eine Ausnahme ohne Eintrag ist ein Fehler im Review.

### A3 Schlüssel, Fremdschlüssel, Indizes

**Primärschlüssel (BESCHLOSSEN):** Fachobjekte und Konten (sichtbar in API, Sync, Links) haben UUID v7, Protokolle,
Ereignisse und reine Hilfstabellen eine fortlaufende Zahl. Öffentliche Kurzcodes (Permalinks) sind zusätzlich eindeutig,
ersetzen aber nie die `id`. Dass UUID v7 den Erstellungszeitpunkt erkennen lässt, ist bewusst in Kauf genommen
(Entscheid 12.11.2026). Alles, was später über Modulgrenzen zusammengeführt werden kann (Historie, Löschregister,
Ereignisse für den Leitstand), trägt zusätzlich eine UUID (`event_id`); fortlaufende Zahlen gelten nur innerhalb
eines Moduls (E4, BESCHLOSSEN 13.11.2026).

**Fremdschlüssel (BESCHLOSSEN):**

| Fall | Constraint | `ON DELETE` |
| --- | --- | --- |
| Normaler Bezug | ja | passend zum Fachfall (`cascade` bei abhängigen Daten) |
| Optionaler Bezug auf Person | ja | `set null` |
| Verweis muss das Löschen einer Person oder Organisation überleben (Journal, Audit, Ereignisse) | nein, nur Index | – |

Wo der Bezug ohne Constraint bleibt, wird die Person zusätzlich als Text gespeichert (`actor_label`), damit der Eintrag
nach der Pseudonymisierung lesbar bleibt.

**Zugehörigkeit absichern (BESCHLOSSEN):** Zeigt ein Verweis auf einen Datensatz, der zum **selben** übergeordneten Objekt
gehören muss (z. B. «veröffentlichte Revision» eines Dokuments, Kind einer Organisation), wird das mit einem
zusammengesetzten Fremdschlüssel gesichert – `(document_id, published_revision_id)` → `revisions(document_id, id)` mit
UNIQUE auf `revisions(document_id, id)`. Wo das nicht geht, prüft der Service und ein Test.

**Indizes:** jede Fremdschlüssel-Spalte ist indexiert, auch ohne Constraint (SQLite und PostgreSQL legen keinen von
selbst an) – BESCHLOSSEN. Weitere Indizes nur, wenn eine konkrete, häufige Abfrage sie braucht (mit `EXPLAIN` belegt);
ungenutzte werden entfernt – BESCHLOSSEN.

### A4 Datentypen, Enums, CHECK-Regeln (BESCHLOSSEN)

| Inhalt | Laravel | SQLite (STRICT) | PostgreSQL | Grenze |
| --- | --- | --- | --- | --- |
| Kurzer Text | `string` | `TEXT` | `text` | Länge über Validierung + CHECK |
| Langer Text | `text` | `TEXT` | `text` | – |
| Zeitpunkt | `timestampTz` | `TEXT` (ISO 8601, UTC) | `timestamptz` | Spalte `_at` |
| Datum | `date` | `TEXT` (ISO 8601) | `date` | Spalte `_on` |
| Ja/Nein | `boolean` | `INTEGER` | `boolean` | 0/1 |
| UUID | `uuid` | `TEXT` | `uuid` | 36 Zeichen |
| Zähler | `integer` | `INTEGER` | `integer`/`bigint` | nie `float` |
| Geldbetrag | `integer` (Rappen) | `INTEGER` | `bigint` | nie `float` |

- **Enums:** jedes Status- oder Art-Feld ist ein PHP-Backed-Enum mit deutschem Label, in der Datenbank als Text, **ab
  Beginn auf beiden Datenbanken mit CHECK-Regel**. Neue Werte brauchen eine Migration, die die Regel erweitert.
- **SQLite `STRICT`:** neue Tabellen werden strikt angelegt. STRICT kennt nur `INTEGER`, `REAL`, `TEXT`, `BLOB`, `ANY`;
  ein gemeinsamer Migrations-Helfer (in `eduksx/core`) bildet die Laravel-Typen darauf ab.
- **CHECK-Regeln** für Enums, Ja/Nein, Längen und Zeiträume gehören in die erste Migration der Tabelle (SQLite kann sie
  nachträglich nur mit Neuaufbau setzen).
- **JSON** nur für Abbilder, Protokolle und Listen ohne eigene Abfrage; sobald gefiltert oder verknüpft wird, wird der
  Wert eine Spalte.

### A5 Migrationen

- **Erweitern – umstellen – aufräumen** über zwei Versionen: in Version n nichts entfernen oder umbenennen, was Version
  n−1 noch liest. Ein Test pro Modul prüft das; bewusste Ausnahmen tragen den Vermerk
  `abwaertskompatibel: <Grund>`. BESCHLOSSEN
- **Ausnahme vor dem ersten produktiven Release (BESCHLOSSEN):** Solange ein Modul nie produktiv ausgeliefert war, darf es
  seine Migrationen einmal zu einem bereinigten Anfangsstand zusammenfassen und direkt umbenennen – nur mit Vermerk und
  Überführung der bestehenden Test-/dev-Daten. Danach gilt die Regel ohne Ausnahme.
- Pflichtteile jeder Migration: Sicherung und Probelauf auf einer Kopie; Datenüberführung zählt vorher/nachher und bricht
  bei Abweichung ab; entfallende Daten werden archiviert (siehe B3, Archiv); `down()` stellt Struktur und Daten wieder
  her, soweit möglich; keine Modellklassen in Migrationen; Daten in Blöcken (`chunkById`); ein Test je Migration.
  BESCHLOSSEN
- **Datenbankspezifisch erlaubt (BESCHLOSSEN):** Das fachliche Modell ist eines; die Umsetzung darf je Datenbank abweichen
  (z. B. STRICT nur SQLite, `uuid`/`timestamptz`/RLS nur PostgreSQL). Abweichungen stehen gebündelt im Helfer bzw. in
  einer Weiche `if ($driver === 'pgsql')` mit Kommentar – nicht verstreut.

### A6 Transaktionen und konkurrierende Speicherung (BESCHLOSSEN)

- Alles, was zusammengehört, läuft in **einer** Transaktion; bei einem Fehler wird die **gesamte** Transaktion
  zurückgerollt. Seiteneffekte (Mails, Webhooks, Dateien, Jobs) erst nach dem Commit (`afterCommit`).
- **Obergrenzen:** eine Transaktion bleibt unter rund **5 Sekunden** bzw. **10 000 geänderten Zeilen**. Was grösser ist,
  läuft über Staging-Tabellen (prüfen, dann in einer Transaktion übernehmen) oder in Blöcken mit eigenem
  Fortschrittsprotokoll, das sich fortsetzen oder vollständig zurücknehmen lässt. BESCHLOSSEN
- **Optimistisches Sperren:** änderbare Fachtabellen haben `lock_version`; gespeichert wird mit
  `WHERE id = ? AND lock_version = ?`; 0 getroffene Zeilen ergibt Konflikt (HTTP 409), nichts wird überschrieben.
  Umsetzung als kleines Trait in `eduksx/core`, kein Fremdpaket.
- Zähler atomar in der Datenbank (`increment()`), Eindeutigkeit über UNIQUE-Index, nicht über vorherige Abfrage.
- SQLite: WAL, `busy_timeout` 5000 ms, kurze Schreibtransaktionen; bei `database is locked` den ganzen Ablauf
  wiederholen.

### A7 Änderungshistorie (BESCHLOSSEN)

Jede Datenänderung – Anlegen, Ändern, Löschen, Wiederherstellen – wird mit wer, wann, was festgehalten, in **derselben
Transaktion** wie die Änderung. Module mit eigenem Revisionssystem nutzen dieses; alle anderen Tabellen schreiben in eine
zentrale Tabelle `data_changes`.

| Spalte | Inhalt | Stufe |
| --- | --- | --- |
| `id` | fortlaufende Zahl | BESCHLOSSEN |
| `event_id` | UUID, eindeutig auch über Module und Exporte hinweg | BESCHLOSSEN |
| `subject_type`, `subject_id` | Tabelle und `id` des Datensatzes (ohne Constraint, mit Index) | BESCHLOSSEN |
| `organization_id` | Mandant des Datensatzes, leer bei globalen Daten | BESCHLOSSEN |
| `action` | `created`, `updated`, `deleted`, `restored` | BESCHLOSSEN |
| `changes` | Feld → `{old, new}` nach den Regeln der Datenklasse (B2) | BESCHLOSSEN, angepasst |
| `actor_type`, `actor_id`, `actor_label` | wer | BESCHLOSSEN |
| `source` | `web`, `api`, `import`, `mcp`, `job`, `system`, `migration` | BESCHLOSSEN |
| `transaction_id` | gemeinsame Kennung aller Einträge einer Transaktion | BESCHLOSSEN |
| `request_id` | Anfrage-ID aus dem Protokoll | BESCHLOSSEN |
| `schema_version` | Stand des Schemas, um alte Einträge richtig zu lesen | BESCHLOSSEN |
| `occurred_at` | wann, UTC | BESCHLOSSEN |

- **Erfassung:** über ein Trait im Modell **und** verbindlich über die Service-Schicht. Schreibende Zugriffe am Service
  vorbei (`DB::table()->update()`, Migrationen, Importe) schreiben die Historie selbst oder einen Sammeleintrag mit
  Anzahl. Ein Test pro Modul sucht nach Schreibzugriffen ausserhalb der Services. BESCHLOSSEN
- **Trigger** nur, wenn ein Weg am Code vorbei anders nicht abzusichern ist – dann für beide Datenbanken, dokumentiert,
  getestet und gepflegt. BESCHLOSSEN
- **Manipulationsschutz:** Einträge sind unveränderlich (keine Updates ausser Pseudonymisierung). Für das
  **Sicherheitsprotokoll** (Rollen, Rechte, Anmeldungen, Löschungen) zusätzlich eine Hash-Verkettung, deren Prüfpunkte
  täglich ausserhalb der Datenbank abgelegt werden (Protokollierung im Leitstand). Für fachliche Historie keine
  Hash-Verkettung. BESCHLOSSEN

### A8 Deutsche Beschreibungen (BESCHLOSSEN 20.11.2026, DB-E13)

Namen bleiben englisch (A1). Damit Fachleute, Datenschutz und Betrieb das Modell ohne Übersetzung lesen können, trägt
**jeder englische Name eine deutsche Beschreibung** – im Datenmodell des Moduls, verbindlich für alle EduKSX-Projekte
(Module und Prototypen).

| Element | Pflichtangaben (deutsch) | Beispiel |
| --- | --- | --- |
| **Tabelle** | Kurzbeschreibung (was eine Zeile ist), Geltungsbereich (B1), Herkunft bzw. Verwendung | `classes` – «Klasse eines Schuljahrs» · Organisation · erfasst in «Klassen», Grundlage für VZE und Lektionen |
| **Spalte** | deutscher Begriff (wie in Oberfläche und Excel), Herkunft bzw. Verwendung, Datenklasse (B2) | `student_count` – «Schülerzahl» · Eingabe in «Klassen», für Klassengrösse und VZE · intern |
| **Status- und Art-Wert** | deutsches Label je Wert (dasselbe wie im PHP-Enum, A4) | `status` = `submitted` → «eingereicht» |

- **Begriff:** das Wort, das Benutzerinnen und Benutzer sehen (Feldname in der Maske, Spalte in Excel/PDF), in
  Schweizer Schreibweise. Für Status und Arten ist es das Label des Enums.
- **Herkunft bzw. Verwendung:** woher der Wert stammt (Eingabe in welcher Ansicht, Import, anderes Modul,
  Rechtsgrundlage, berechnet aus …) oder wofür er gebraucht wird. Mindestens eines von beiden; gilt es für alle
  Spalten einer Tabelle gleich, genügt die Angabe bei der Tabelle.
- **Standardspalten** (`id`, `organization_id`, `created_at`, `created_by_id`, `updated_at`, `updated_by_id`,
  `lock_version`, `deleted_at`, `deleted_by_id`, `event_id`) haben feste Beschreibungen aus `eduksx/core` und werden im
  Modul nicht wiederholt. Fremdschlüssel nennen das Ziel («Verweis auf …»), der Begriff steht trotzdem.
- **Form:** Die Beschreibungen stehen im Datenmodell des Moduls (Tabelle «Spalte | Typ | Deutsch | Herkunft/Verwendung |
  Datenklasse», handgeschrieben oder aus dem Schema erzeugt). In PostgreSQL schreibt der Migrations-Helfer sie
  zusätzlich als `COMMENT ON TABLE/COLUMN` im Format «Begriff – Herkunft/Verwendung»; SQLite hat keine Kommentare.
- **Gleiche Texte in der API:** Felder der API, die einer Spalte entsprechen, übernehmen Begriff und Beschreibung
  unverändert (API A8). Es gibt nur eine Quelle je Begriff.
- Keine Entscheidnummern und keine echten Personen- oder Organisationsnamen in Beschreibungen; Freitext kurz (eine
  Zeile).
- Der Konformitätstest (E5) prüft, dass jede Tabelle, Spalte und jeder Enum-Wert eine deutsche Beschreibung hat.

---

## B · Sicherheit und Datenschutz

### B1 Geltungsbereiche und Mandantentrennung (BESCHLOSSEN)

Jede Tabelle hat genau einen Geltungsbereich; er steht im Datenmodell des Moduls.

| Geltungsbereich | Beispiel | Mandantenspalte | Regel |
| --- | --- | --- | --- |
| **Global** | öffentliche Glossary-Begriffe, Rechtstexte | keine | gehört keiner Organisation; Änderungen nur über die Redaktion |
| **Organisation** | eigene Bezeichnungen einer Schule, Mitglieder | `organization_id` NOT NULL | sieht und ändert nur die eigene Organisation |
| **Persönlich** | persönliche Anpassungen, Einstellungen | `user_id` NOT NULL, `organization_id` falls an eine Organisation gebunden | sieht nur die Person selbst |

Technische Absicherung in **zentralen** Diensten (eine Datenbank für viele Organisationen):

1. **Jede** Abfrage auf Tabellen «Organisation» ist auf den Mandanten eingeschränkt – über einen globalen Scope im
   Modell, der ohne gesetzten Mandantenkontext eine Exception wirft (statt alles zu liefern).
2. Der Mandantenkontext wird auch in **Jobs, Befehlen, Importen und Administrationsabfragen** ausdrücklich gesetzt; Jobs
   tragen die `organization_id` in ihrer Nutzlast. Mandantenübergreifende Abfragen (Plattform-Administration) laufen
   über einen eigenen, protokollierten Weg.
3. **Kinder einer Organisation** verweisen über zusammengesetzte Fremdschlüssel `(organization_id, parent_id)`, damit
   ein Datensatz nie an ein Objekt einer anderen Organisation gehängt werden kann.
4. **PostgreSQL Row-Level Security** als zweite Schicht auf allen Tabellen «Organisation»: die Anwendung setzt je Anfrage
   `SET LOCAL app.organization_id`, die Richtlinie lässt nur passende Zeilen zu. ZU PRÜFEN (Prototyp, #13): Aufwand mit Laravel und
   Verbindungspool.
5. Ein Test je Modul legt zwei Organisationen an und prüft, dass keine Abfrage, kein Export und kein Job Daten der
   anderen liefert.

**Isolierte** Instanzen (eigene Datenbank je Kunde) brauchen die Regeln 1–4 nicht für die Trennung, führen die Spalte
`organization_id` aber **ebenfalls in jeder Tabelle «Organisation»** – sonst liessen sich die Daten verschiedener
Organisationen nach einem Zusammenlegen nicht mehr trennen (E3, BESCHLOSSEN 13.11.2026).

Ob persönliche Anpassungen organisationsübergreifend gelten oder je Organisation verschieden sein dürfen, entscheidet
jedes Modul und hält es im Datenmodell fest.

### B2 Datenklassen je Feld (BESCHLOSSEN)

Jede Spalte bekommt im Datenmodell des Moduls eine Datenklasse; daraus folgen Historie, Export und Löschung.

| Klasse | Beispiele | In der Historie (`changes`) | Beim Löschen der Person |
| --- | --- | --- | --- |
| **öffentlich** | Begriff, Beschreibung | alter und neuer Wert | bleibt |
| **intern** | Status, Notiz der Redaktion | alter und neuer Wert | bleibt |
| **personenbezogen** | Name, E-Mail, Anzeigename, Freitext einer Person | nur `"changed"`, kein Wert | Bezug pseudonymisieren |
| **besonders schützenswert** | Gesundheit, Massnahmen, Beurteilungen | nur `"changed"`, nie ein Wert | sofort löschen |
| **geheim** | Passwort-Hash, Token, 2FA-Geheimnis | nur `"changed"` | löschen |

Damit enthält die Historie keine Personendaten mehr, die beim Löschen gesucht werden müssten – auch nicht der «letzte
Stand» bei `deleted`. Abbilder (Revisionen, Snapshots als JSON) enthalten nur Felder der Klassen öffentlich und intern.

### B3 Löschen, Wiederherstellungsfrist und Löschregister

**Papierkorb (BESCHLOSSEN 12.11.2026, Geltung präzisiert in 1.1):** Hauptobjekte der Fachdaten und
Organisationsdaten werden zuerst vorläufig gelöscht (`deleted_at`, `deleted_by_id`) und nach einer Frist endgültig.
**Nicht** im Papierkorb: Verknüpfungs-, Hilfs- und Protokolltabellen – sie folgen ihrem Hauptobjekt. Fristen und das
Recht zum Wiederherstellen stellen **nur Super-Admins** ein; Vorgabe [30 Tage].

**Konten (BESCHLOSSEN 12.11.2026):** ebenfalls zuerst vorläufig gelöscht (Anmeldung gesperrt, Sitzungen und Tokens
beendet), Wiederherstellung während der Frist durch Super-Admins. **Ausnahme:** Verlangt eine Person die sofortige
Löschung nach Datenschutzrecht, wird sofort gelöscht. Fristen rechtlich prüfen (ZU PRÜFEN).

**Löschregister (BESCHLOSSEN):** Ein Zurückspielen einer Sicherung darf gelöschte Personen nicht wiederbeleben.

1. Jede endgültige Löschung von Personendaten wird zusätzlich in ein **Löschregister ausserhalb der Datenbank**
   geschrieben: nur Art, `id`, Zeitpunkt und Grund – keine Personendaten.
2. Ablage nur anhängend (append-only), verschlüsselt, mit eigener Aufbewahrung, getrennt von den Datenbanksicherungen
   (z. B. eigener Objektspeicher-Bucket mit Objektsperre).
3. Nach jeder Wiederherstellung wendet der Dienst das Register **vor dem Start** automatisch an; erst danach nimmt er
   Anfragen an. Ohne erreichbares Register startet er nicht; einziger Ausweg ist der protokollierte Notfallweg N3 nach
   [KONZEPT-NOTFALL.md](KONZEPT-NOTFALL.md) (neues Register ab Stichtag, ältere Sicherungen gesperrt; 22.11.2026).
4. Ein Test spielt eine ältere Sicherung zurück und prüft, dass danach keine registrierten Personendaten mehr vorhanden
   sind – in Tabellen, Historie, Archiven und Suchindex.

**Überall löschen:** Löschpflichtige Daten werden auch aus Archiven, Exporten, Staging-Tabellen, Caches und
Suchindizes entfernt. In Sicherungen bleiben sie bis zu deren Ablauf, unbenutzt; das Register verhindert ihre Rückkehr.

**Archive (BESCHLOSSEN):** Archivierte Daten (z. B. bei Migrationen entfallende Werte) tragen ihre Datenklasse, eine Frist
und werden verschlüsselt abgelegt; personenbezogene Werte nur, wenn nötig und mit Löschregel.

### B4 Identitäten und Rechte (BESCHLOSSEN)

- **Plattformidentität** kommt aus EduKSX-Ident (OIDC). Ein Modul speichert sie als `issuer` + `subject` (zusammen
  eindeutig) – nie die E-Mail als Schlüssel, nie `subject` allein.
- **Lokale Benutzerreferenz:** Das Modul hält nur, was es tatsächlich braucht (Anzeigename, Sprache, Zeitpunkt der
  letzten Anmeldung als Datum); alles andere liest es aus Ident.
- **Rollen und Rechte gelten je Modul und Organisation:** Zuordnung mit `(user_id, organization_id, role)` im Modul;
  Admin im Glossary ist nicht Admin in der Rechtssammlung. Geprüft wird auf Rechte, nicht auf Rollennamen.
- **Super-Admin** ist eine Plattformrolle aus Ident mit zweitem Faktor; welche Rechte sie im Modul gibt, legt das Modul
  fest. Bis ein Modul an Ident angeschlossen ist, übernimmt seine höchste geschützte Rolle diese Aufgabe (im Glossary:
  Developer). BESCHLOSSEN 12.11.2026
- **Servicekonten** sind eigene Identitäten (Client-Credentials), nie Benutzerkonten.

### B5 Datenbankzugänge (BESCHLOSSEN, PostgreSQL)

| Zugang | Rechte | Verwendet von |
| --- | --- | --- |
| `<modul>_runtime` | Lesen/Schreiben auf Tabellen, keine DDL, unterliegt RLS | Anwendung, Jobs |
| `<modul>_migrate` | DDL und Daten, nicht Besitzer anderer Module | Migrationen beim Update |
| `<modul>_readonly` | nur Lesen, unterliegt RLS | Auswertungen, Support |

Jedes Modul hat eine eigene Datenbank bzw. ein eigenes Schema; kein Modul liest Tabellen eines anderen (Austausch nur
über APIs). Für SQLite entfällt dieser Abschnitt – die Datei ist nur für den Dienst lesbar.

### B6 Geheimnisse und Verschlüsselung (BESCHLOSSEN)

Tokens nur gehasht, 2FA-Geheimnisse und Zugangsdaten verschlüsselt (Laravel-Cast `encrypted`); Felder der Klasse
«besonders schützenswert» zusätzlich verschlüsselt gespeichert (BESCHLOSSEN).

### B7 Rechtsrahmen (BESCHLOSSEN 13.11.2026)

| Recht | Gilt für | Bedeutung für die Datenbank |
| --- | --- | --- |
| **IDG Kanton Zürich** | Schulen, Schulgemeinden und Gemeinden als öffentliche Organe (Verantwortliche) | Folgenabschätzung, Vorabkontrolle bei besonderen Risiken, Informationssicherheit, Bekanntgabe nur mit Grundlage |
| **DSG (Schweiz)** | Betreiberin der Plattform, private Kunden | Verzeichnis der Bearbeitungstätigkeiten, Auskunft, Datenherausgabe, Meldung von Verletzungen |
| **DSGVO** | nur bei Bezug zur EU (Niederlassung oder Angebot an Personen in der EU) | Meldung innerhalb von 72 Stunden, Recht auf Einschränkung |

Umgesetzt wird jeweils die **strengste** Regel; so ist ein Modul ohne Umbau für alle drei geeignet. Die Plattform
bearbeitet Daten der Schulen im Auftrag – der Auftragsbearbeitungsvertrag regelt Zweck, Ort (Schweiz) und Löschung.
Dieser Standard ist keine Rechtsberatung; Fristen und Folgenabschätzungen prüft eine Fachperson (siehe Glossary #278).

### B8 Auskunft und Datenherausgabe (BESCHLOSSEN 13.11.2026)

- Jedes Modul bietet die Funktion **«alle Daten einer Person»**: Sie findet über den Personenbezug und die Datenklassen
  (B2) alle Zeilen in allen Tabellen – auch Historie, Vorschläge, Archive – und exportiert sie maschinenlesbar (JSON,
  Felder englisch, Labels deutsch) für Auskunft und Datenherausgabe.
- Der Export ist für die Person selbst («Meine Daten») und für die Administration (Anfrage per Brief) verfügbar; jeder
  Aufruf steht im Sicherheitsprotokoll.
- Berichtigung ändert die Daten mit Historie; die Historie enthält personenbezogene Werte ohnehin nicht (B2).
- Ein Test legt Daten einer Person in jeder Tabelle an und prüft, dass der Export alles und nichts von anderen enthält.

### B9 Zweck und Rechtsgrundlage je Tabelle (BESCHLOSSEN 13.11.2026)

Neben der Datenklasse je Spalte (B2) hält jedes Modul im Code je Tabelle **Zweck**, **Rechtsgrundlage** bzw.
Auftrag, **Geltungsbereich** (B1) und **Löschfrist** fest. Daraus wird das Verzeichnis der Bearbeitungen des Moduls
erzeugt (Plattformkonzept, Prüfliste); ein Test schlägt fehl, wenn eine Tabelle diese Angaben nicht hat. Eine neue
Tabelle ohne Zweck wird nicht gemergt.

### B10 Folgenabschätzung und Vorabkontrolle (BESCHLOSSEN 13.11.2026)

- Ein Modul, das Daten der Klasse **besonders schützenswert** bearbeitet oder Personendaten online für viele Personen
  zugänglich macht, geht erst produktiv, wenn eine **Datenschutz-Folgenabschätzung** vorliegt – für Kunden im Kanton
  Zürich nach der Vorlage des Kantons; bei besonderen Risiken legt der Kunde das Vorhaben der Datenschutzbeauftragten
  zur **Vorabkontrolle** vor.
- Die Folgenabschätzung liegt im Repo des Moduls und wird bei jeder neuen Datenklasse «besonders schützenswert» oder
  neuen Bekanntgabe nachgeführt.

### B11 Protokoll der Lesezugriffe (BESCHLOSSEN 13.11.2026)

Zugriffe auf Felder der Klasse **besonders schützenswert** werden auch beim **Lesen** protokolliert (wer, wann,
welcher Datensatz, welcher Zweck; nicht der Inhalt) – im Sicherheitsprotokoll (A7) mit Aufbewahrung nach Löschkonzept.
Für die übrigen Klassen genügt das Protokoll der Änderungen.

### B12 Kopien für Entwicklung und Test (BESCHLOSSEN 13.11.2026)

Produktive Daten kommen nur **anonymisiert** nach dev oder test: ein Befehl je Modul ersetzt alle Felder der Klassen
personenbezogen, besonders schützenswert und geheim, erhält aber Schlüssel, Bezüge und Mengen. Ein nicht
anonymisierter Dump wird auf dev und test beim Einspielen abgewiesen. Testdaten in Repos, Issues und Bildschirmfotos
sind immer erfunden.

### B13 Einschränkung der Bearbeitung und Verletzungen (BESCHLOSSEN 13.11.2026)

- Konten haben ein Merkmal `is_processing_restricted`: Die Daten bleiben gespeichert, werden aber nicht mehr angezeigt,
  exportiert oder geändert (z. B. während eine Berichtigung strittig ist).
- Bei einer **Datenschutzverletzung** muss sich rasch bestimmen lassen, wer betroffen ist: über Datenklassen, Zweck je
  Tabelle (B9) und Protokolle. Meldung nach Recht (DSG: bei voraussichtlich hohem Risiko; DSGVO: innerhalb von 72
  Stunden) – Ablauf im Betriebskonzept.

### B14 Zusammenlegen als neue Bearbeitung (BESCHLOSSEN 13.11.2026)

- Module **desselben Kunden** zusammenzulegen ist eine neue Bearbeitung: Vorher wird geprüft, ob die Zwecke vereinbar
  sind; Verzeichnis und Datenschutzerklärung werden nachgeführt.
- **Isolierte Instanzen verschiedener Kunden** werden nur mit Zustimmung bzw. Vertrag jedes Kunden in einen zentralen
  Dienst überführt; danach gilt die Mandantentrennung (B1).
- Fristen, Löschregister und Einschränkungen der Herkunft gelten nach dem Zusammenlegen unverändert weiter.

---

## C · Betrieb

### C1 SQLite und PostgreSQL (BESCHLOSSEN)

| Thema | SQLite (isolierte, kleine Instanzen; Glossary bis zum Wechsel) | PostgreSQL (zentrale Dienste) |
| --- | --- | --- |
| Einstellungen | WAL, `busy_timeout` 5000 ms, `foreign_keys` an, STRICT | Verbindungspool, Lesekopien, RLS |
| Schreiben | ein Schreiber zur Zeit, kurze Transaktionen | parallel, Sperren auf Zeilenebene |
| Typen | `TEXT`/`INTEGER` über Helfer | `uuid`, `timestamptz`, `text`, `jsonb` |
| Sicherung | Litestream + `VACUUM INTO` | Base Backup + WAL-Archivierung (PITR), `pg_dump` nur für logische Exporte |

**Prototypen (BESCHLOSSEN 12.11.2026):** Für Prototypen ist Speicherung in JSON-Dateien erlaubt. Auch dann gelten
Namen, Mehrsprachigkeit und Historie dieses Standards; Schreibzugriffe sind gesperrt (Datei-Lock) und atomar (temporäre
Datei, dann umbenennen); der Zugriff läuft über ein Repository, damit der Wechsel auf die Datenbank nur diese Schicht
betrifft. Vor dem produktiven Einsatz wird auf eine Datenbank umgestellt.

**Beide Datenbanken in der CI ab sofort:** Jedes Modul, das PostgreSQL unterstützen soll, lässt seine Tests und alle
Migrationen in der CI gegen SQLite **und** PostgreSQL laufen – nicht erst beim Wechsel.

### C2 Sicherung und Wiederherstellung

| Regel | Umsetzung | Stufe |
| --- | --- | --- |
| Laufend | SQLite: Litestream in einen S3-kompatiblen Speicher (z. B. Swiss Backup). PostgreSQL: Base Backup + WAL-Archivierung (z. B. WAL-G oder pgBackRest nach S3; Werkzeug legt der Betrieb fest) | BESCHLOSSEN |
| Zeitpunkt wählbar | Wiederherstellung auf jeden Zeitpunkt der Aufbewahrung (PITR) – `pg_dump` allein genügt dafür nicht | BESCHLOSSEN |
| Einzelsnapshot | vor jedem Update, jeder Migration, grossen Importen; Dateiname mit Zeitstempel und Version; Prüfsumme und Zeilen je Tabelle | BESCHLOSSEN |
| Verschlüsselt | alle Sicherungen verschlüsselt; Schlüssel getrennt vom gesicherten System und von der Sicherung aufbewahrt (Geheimnisspeicher), Notfallkopie offline | BESCHLOSSEN |
| Getestet | Wiederherstellung mindestens monatlich auf einer Kopie, Dauer messen und mit RTO vergleichen | BESCHLOSSEN |
| Nach dem Zurückspielen | Migrationen, Löschregister (B3), Löschfristen – erst dann Anfragen annehmen | BESCHLOSSEN |

**RPO und RTO (BESCHLOSSEN 12.11.2026):** verbindliche Ziele je Dienstart:

| Dienstart | RPO (höchster Datenverlust) | RTO (höchste Ausfallzeit) |
| --- | --- | --- |
| zentral (Glossary, Rechtssammlung) | 1 Minute | 4 Stunden |
| isoliert (Intranet, Stundenplan) | 15 Minuten | 1 Arbeitstag |
| Ident | 1 Minute | 1 Stunde |

### C3 Tests (BESCHLOSSEN, ergänzt)

Jedes Modul hat mindestens: Migrationstest je Migration (Daten vorher, nachher prüfen); Abwärtskompatibilität der
Migrationen; Schemaprüfung (STRICT, CHECK, `integrity_check`, `foreign_key_check`); Veröffentlichungsgrenze (nichts
Privates in öffentlichen Ausgaben); **Mandantentrennung** mit zwei Organisationen (B1); Papierkorb und Fristen;
**Löschung nach Wiederherstellung** mit Löschregister (B3); Historie für alle vier Aktionen; Rollback einer
mehrteiligen Änderung. Seit 1.2 zusätzlich: **Auskunft/Export** einer Person (B8), **Zweck je Tabelle** (B9),
**Anonymisierung** (B12) und die **Konformitätstests** aus `eduksx/core` (E5).

---

## D · Sprachen

### D1 Mehrsprachigkeit (BESCHLOSSEN 12.11.2026, präzisiert)

| Art des Textes | Umsetzung |
| --- | --- |
| **Fachliche Inhalte** (Bezeichnungen, Beschreibungen, Stammdaten) | **immer** mehrsprachig ab Start: Grundsprache in der Haupttabelle, **nur die übrigen Sprachen** in `<objekt>_translations` (`locale` = `fr`, `it`, `en`; eindeutig je Objekt und Sprache). Die Grundsprache steht nie zusätzlich in der Übersetzungstabelle. |
| **Technische Texte** (Oberfläche, Labels von Enums, Fehlermeldungen) | Übersetzungsdateien im Code (Laravel `lang/`, Frontend-i18n), nie in der Datenbank |
| **Persönliche Daten und Freitexte einer Person** (persönliche Anpassungen, Notizen, Kommentare) | **keine** Übersetzung – gespeichert in der Sprache, in der sie erfasst wurden |

Fehlt eine Übersetzung, gilt die Grundsprache (`de`). Sprachcodes nach ISO 639-1.

### D2 Datum und Uhrzeit (BESCHLOSSEN 12.11.2026)

Anzeige für Menschen: Datum `DD.MM.YYYY`, Uhrzeit `HH:MM:SS` (24 Stunden), Zeitzone Europe/Zurich. Gespeichert und in
Maschinenformaten: ISO 8601 in UTC. Formatiert wird an einer Stelle im Code, nie in der Abfrage.

### D3 Sortierung, Suche, Unicode (BESCHLOSSEN)

- Texte werden beim Speichern in **Unicode NFC** normalisiert.
- Für die Suche führt jede durchsuchte Tabelle eine normalisierte Suchspalte (klein, NFC, ohne Akzente – «Ecole» findet
  «École»); gesucht wird nur darin.
- Sortierung für Menschen nach Schweizer Regeln: PostgreSQL mit ICU-Kollation `de-CH-x-icu` (bzw. `fr-CH`, `it-CH` je
  Sprache); SQLite sortiert in der Anwendung (PHP `Collator`), weil es keine passende Kollation mitbringt.
- Volltextsuche über die Datenbank (PostgreSQL `tsvector` je Sprache) oder einen Suchdienst; Suchindizes zählen zu den
  Orten, aus denen gelöscht werden muss (B3).

---

## E · Modularität und Zusammenführbarkeit

Datenbanken werden je Modul in eigenen Repos entwickelt und laufen eigenständig. Damit sie später ohne Konflikte
zusammengelegt werden können, gelten diese Regeln (alle BESCHLOSSEN 13.11.2026).

### E1 Modulschlüssel

Jedes Modul hat einen festen, kurzen **Modulschlüssel** (Kleinbuchstaben, ohne Bindestrich), vergeben in der Tabelle
unten und nie geändert. Er benennt Schema, Datenbankzugänge (B5), Einträge im Löschregister und Ereignisse.

Die Schlüssel stehen im [Modulregister](REGISTER-MODULE.md); es gilt für DB- und API-Standard gemeinsam.
Schlüssel sind englisch (A1) und unabhängig vom Marketingnamen des Moduls.

### E2 Schema je Modul

- Auf PostgreSQL liegen alle Tabellen eines Moduls in einem **eigenen Schema mit dem Modulschlüssel** (`glossary.terms`,
  `intranet.users`), auch wenn das Modul allein in seiner Datenbank läuft. Laravel-Tabellen (`migrations`, `jobs`,
  `cache`, `sessions` …) liegen im selben Schema.
- Tabellennamen bekommen **keine Präfixe**; gleiche Namen in verschiedenen Modulen (`users`, `settings`) sind erlaubt,
  weil sie durch das Schema getrennt sind.
- SQLite kennt keine Schemas: Die Datei heisst `<modulschlüssel>.sqlite`; beim Überführen nach PostgreSQL wird sie in
  das Schema des Moduls geladen.
- Kein Modul greift auf das Schema eines anderen zu, auch nicht nach dem Zusammenlegen (Austausch nur über APIs).

### E3 Plattform-IDs für Organisationen und Personen

- **Organisationen** tragen die ID aus EduKSX-Ident. Bis ein Modul an Ident angeschlossen ist, erzeugt es eine UUID v7
  und führt die Spalte `platform_id` (UUID, eindeutig, leer erlaubt), die später mit der ID aus Ident befüllt wird.
- **Personen** werden über Modulgrenzen nur mit `issuer` + `subject` (B4) bzw. `platform_id` referenziert, nie mit der
  lokalen `users.id`.
- `organization_id` steht in jeder Tabelle «Organisation», auch in isolierten Instanzen (B1).

### E4 Schlüssel, die das Zusammenlegen überstehen

UUID v7 für Fachobjekte (A3) und `event_id` für alles Modulübergreifende; fortlaufende Zahlen nur modulintern. Enum-Werte,
Rollen und Einstellungen gelten je Modul und werden beim Zusammenlegen nicht vermischt. Gemeinsame Stammdaten (z. B.
Sprachen, Schulstufen) werden nicht in mehreren Modulen gepflegt, sondern – wenn nötig – als Plattformdienst angeboten.

### E5 Versionsbindung und Konformitätstests

- Jedes Modul nennt in seinem Datenmodell, nach welcher **Version dieses Standards** es arbeitet (z. B. «DB-Standard
  1.2»). Eine neue Version gilt für ein Modul erst, wenn es sie übernommen hat; die Übernahme ist ein Issue im Modul.
- Die prüfbaren Regeln stehen als **Konformitätstests** in `eduksx/core` und laufen in der CI jedes Moduls: Namen,
  STRICT und CHECK, Index auf Fremdschlüsseln, Datenklasse und Zweck je Spalte bzw. Tabelle, deutsche Beschreibung je
  Tabelle, Spalte und Enum-Wert (A8), Schema = Modulschlüssel,
  `organization_id` in Tabellen «Organisation».
- Hilfen (Migrations-Helfer, Traits für Sperren und Historie, Anonymisierung, Export) liegen ebenfalls in
  `eduksx/core`, nicht kopiert in den Modulen.

### E6 Zusammenlegen üben

- `eduksx/core` enthält ein Werkzeug, das eine SQLite-Datenbank eines Moduls in das Schema des Moduls in PostgreSQL
  überführt (Zählung je Tabelle vorher/nachher, Prüfsummen).
- Ein CI-Test der Plattform lädt die Testdatenbanken mindestens zweier Module in **eine** PostgreSQL-Datenbank und
  prüft: keine Namenskonflikte, alle Fremdschlüssel gültig, Mandantentrennung intakt, Löschregister anwendbar.
- Vor einem echten Zusammenlegen gilt zusätzlich B14.

---

## Checkliste für Pull Requests mit DB-Änderung

- [ ] Standard deckt die Änderung ab – sonst zuerst Konzept-PR
- [ ] Namen nach A1, dritte Normalform nach A2, Ausnahme in der Ausnahmetabelle des Moduls
- [ ] Deutsche Beschreibung für jede neue Tabelle, Spalte und jeden Enum-Wert (A8); API-Texte gleich
- [ ] Geltungsbereich der Tabelle (global / Organisation / persönlich) und Datenklasse jeder Spalte im Datenmodell
- [ ] Mandantenscope und zusammengesetzte Fremdschlüssel bei Tabellen «Organisation»; Test mit zwei Organisationen
- [ ] Primärschlüssel, Fremdschlüssel mit Index, Zugehörigkeit gesichert (A3)
- [ ] SQLite STRICT, CHECK-Regeln in der ersten Migration, Typen nach A4
- [ ] Migration abwärtskompatibel, zählt vorher/nachher, Test vorhanden; läuft in der CI auf SQLite und PostgreSQL
- [ ] Transaktion vollständig zurückrollbar, Obergrenzen beachtet; optimistisches Sperren
- [ ] Historie für alle Aktionen, `changes` nach Datenklasse, in derselben Transaktion
- [ ] Löschen: Papierkorb nur für Hauptobjekte, Löschregister, alle Orte (Archiv, Export, Suchindex)
- [ ] Fachtexte mit Übersetzungstabelle (ohne Grundsprache), persönliche Texte ohne
- [ ] Anzeige `DD.MM.YYYY` / `HH:MM:SS`, Speicherung ISO 8601 UTC; Suchspalte normalisiert
- [ ] Sicherung vor der Migration, Wiederherstellung geprüft
- [ ] Tabelle im Schema des Moduls; Zweck, Rechtsgrundlage, Geltungsbereich und Löschfrist im Code (B9, E2)
- [ ] Personenbezug für Auskunft/Export erfasst (B8); Felder «besonders schützenswert» mit Lese-Protokoll (B11)
- [ ] Anonymisierung deckt neue personenbezogene Felder ab (B12)
- [ ] Modulübergreifende Bezüge nur über Plattform-IDs (E3); Konformitätstests aus `eduksx/core` grün (E5)

## Entscheide

| Nr. | Frage | Entscheid | Status |
| --- | --- | --- | --- |
| DB-E1 | Aufteilung in Plattform-Standard und Modul-Datenmodell | Standard hier, Fachliches im Modul | BESCHLOSSEN 12.11.2026 |
| DB-E2 | Mehrsprachigkeit für persönliche Daten | nein | BESCHLOSSEN 12.11.2026 |
| DB-E3 | UUID v7 trotz erkennbarem Erstellungszeitpunkt | ja | BESCHLOSSEN 12.11.2026 |
| DB-E4 | RPO/RTO je Dienstart | Werte in C2 | BESCHLOSSEN 12.11.2026 |
| DB-E5 | Row-Level Security in PostgreSQL | als zweite Schicht vorgesehen; Prototyp mit PostgreSQL, Laravel und Verbindungspool (Entscheid 12.11.2026, #13); Vorgehen und Empfehlung: [Prüfauftrag RLS](PRUEFAUFTRAG-RLS.md); Entscheid #34 | ZU PRÜFEN |
| DB-E6 | Super-Admin als Plattformrolle aus Ident | ja; bis zum Anschluss an Ident die höchste geschützte Rolle des Moduls | BESCHLOSSEN 12.11.2026 |
| DB-E7 | Hash-Verkettung nur für das Sicherheitsprotokoll | ja, A7 | BESCHLOSSEN 12.11.2026 |
| DB-E8 | Neue Regeln aus dem Architekturreview (Version 1.1) | alle übernommen, RLS zu prüfen | BESCHLOSSEN 12.11.2026 |
| DB-E9 | Module eigenständig in eigenen Repos, später zusammenlegbar | Teil E: Modulschlüssel, Schema je Modul, Plattform-IDs, Versionsbindung, Konformitätstests | BESCHLOSSEN 13.11.2026 |
| DB-E10 | Datenschutz nach IDG, DSG und DSGVO | strengste Regel; B7–B14 | BESCHLOSSEN 13.11.2026 |
| DB-E11 | Modulschlüssel englisch, ein gemeinsames Register | [REGISTER-MODULE.md](REGISTER-MODULE.md); `recht` → `codex`, `stundenplan` → `timetable`, `leitstand` → `ops` | BESCHLOSSEN 13.11.2026 |
| DB-E13 | Deutsche Beschreibungen zu englischen Namen | je Tabelle Kurzbeschreibung, Geltungsbereich, Herkunft/Verwendung; je Spalte Begriff, Herkunft/Verwendung, Datenklasse; je Enum-Wert Label (A8); gleiche Texte in der API | BESCHLOSSEN 20.11.2026 |
| DB-E12 | Gemeinsame Tabellen über `eduksx/core` | Core liefert Migrationen für Standardtabellen (z. B. lokale Personenreferenz, Organisationen, Mitgliedschaften, `data_changes`, Einstellungen); jedes Modul installiert sie im eigenen Schema (E2); Stammdaten von Personen und Organisationen führt Ident | BESCHLOSSEN 13.11.2026 |

Entscheide heissen ab 1.2.1 `DB-E<n>`, damit sie nicht mit den Abschnitten E1–E6 und den Entscheiden des API-Standards
(`API-E<n>`) verwechselt werden.

## Verlauf

- 12.11.2026: Version 1.0 (DB-Entwickler-Guideline, aus dem Glossary) abgenommen (#9).
- 12.11.2026: Version 1.1 nach Architekturreview abgenommen: Aufteilung Plattform/Modul, Mandantentrennung, Datenklassen,
  Löschregister, Identitäten, Datenbankzugänge, PITR/RPO/RTO, Sprachregeln (#11).
- 13.11.2026: Version 1.2 abgenommen – Teil E (Modularität und Zusammenführbarkeit) und B7–B14 (Rechtsrahmen, Auskunft,
  Zweck je Tabelle, Folgenabschätzung, Lesezugriffe, anonymisierte Kopien, Einschränkung, Zusammenlegen) (#20).
- 13.11.2026: Version 1.2.1 redaktionell – Modulschlüssel ins gemeinsame [Modulregister](REGISTER-MODULE.md) verschoben
  und englisch (DB-E11), Entscheide als `DB-E<n>` nummeriert, Core-Tabellen festgehalten (DB-E12).
- 20.11.2026: Version 1.3 abgenommen – A8 deutsche Beschreibungen zu englischen Namen (DB-E13), verbindlich für alle
  EduKSX-Projekte (#65).
