# Konzept: DB-Standard der EduKSX-Plattform (#9, #11)

Stand: 12.11.2026 (Version 1.1) · Verantwortlich: Markus Keller · Status: **ENTWURF** (Version 1.0 abgenommen am
12.11.2026)

Verbindlicher Datenbank-Standard für **alle** EduKSX-Module (Glossary, Rechtssammlung, Intranet, Stundenplan …) – für
Menschen und KI-Agenten. Er enthält nur Regeln, die für jedes Modul gelten. Fachliche Tabellen, Befehle und
modulspezifische Entscheide stehen im Datenmodell des jeweiligen Moduls, das auf diesen Standard verweist (für das
Glossary: `docs/KONZEPT-DB-GUIDELINE.md` im Repo EduKSX-Glossary).

**Verbindlichkeit** (Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md)): **BESCHLOSSEN** = Version 1.0 bzw.
Vorgabe von Projektverantwortlicher:m mit Datum · **EMPFOHLEN** = neu in 1.1 aus dem Architekturreview vom 12.11.2026,
noch nicht bestätigt · **OFFEN** = vor der Umsetzung zu entscheiden.

Der Standard ist in vier Teile gegliedert:

| Teil | Inhalt |
| --- | --- |
| [A · Grundregeln](#a--grundregeln) | Namen, Normalisierung, Schlüssel, Typen, Migrationen, Transaktionen, Sperren, Historie |
| [B · Sicherheit und Datenschutz](#b--sicherheit-und-datenschutz) | Geltungsbereiche und Mandanten, Datenklassen, Löschen und Löschregister, Identitäten, Datenbankzugänge |
| [C · Betrieb](#c--betrieb) | Plattform SQLite/PostgreSQL, Sicherung und Wiederherstellung, RPO/RTO, Tests |
| [D · Sprachen](#d--sprachen) | Mehrsprachigkeit, Datum und Zeit, Sortierung und Suche |

## Grundsätze

1. **Technik englisch, Anzeige deutsch** – übersetzt wird nur über Labels im Code, nie in der Datenbank. BESCHLOSSEN
2. **Kein Datenverlust** – jede Änderung überführt bestehende Daten, zählt vorher und nachher und bricht bei Abweichung
   ab. BESCHLOSSEN
3. **Öffentlich, Organisation und persönlich strikt getrennt** – technisch, nicht nur per Konvention. EMPFOHLEN
4. **Nachvollziehbar** – jede Datenänderung ist mit wer, wann, was belegt. BESCHLOSSEN
5. **Ein fachliches Modell, datenbankspezifische Umsetzung erlaubt** – SQLite und PostgreSQL werden beide geprüft.
   EMPFOHLEN
6. **Konzept vor Code** – Schemaänderungen, die vom Standard abweichen, kommen zuerst als Konzept-PR zur Abnahme.
   BESCHLOSSEN

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
(Entscheid 12.11.2026).

**Fremdschlüssel (BESCHLOSSEN):**

| Fall | Constraint | `ON DELETE` |
| --- | --- | --- |
| Normaler Bezug | ja | passend zum Fachfall (`cascade` bei abhängigen Daten) |
| Optionaler Bezug auf Person | ja | `set null` |
| Verweis muss das Löschen einer Person oder Organisation überleben (Journal, Audit, Ereignisse) | nein, nur Index | – |

Wo der Bezug ohne Constraint bleibt, wird die Person zusätzlich als Text gespeichert (`actor_label`), damit der Eintrag
nach der Pseudonymisierung lesbar bleibt.

**Zugehörigkeit absichern (EMPFOHLEN):** Zeigt ein Verweis auf einen Datensatz, der zum **selben** übergeordneten Objekt
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
- **Ausnahme vor dem ersten produktiven Release (EMPFOHLEN):** Solange ein Modul nie produktiv ausgeliefert war, darf es
  seine Migrationen einmal zu einem bereinigten Anfangsstand zusammenfassen und direkt umbenennen – nur mit Vermerk und
  Überführung der bestehenden Test-/dev-Daten. Danach gilt die Regel ohne Ausnahme.
- Pflichtteile jeder Migration: Sicherung und Probelauf auf einer Kopie; Datenüberführung zählt vorher/nachher und bricht
  bei Abweichung ab; entfallende Daten werden archiviert (siehe B3, Archiv); `down()` stellt Struktur und Daten wieder
  her, soweit möglich; keine Modellklassen in Migrationen; Daten in Blöcken (`chunkById`); ein Test je Migration.
  BESCHLOSSEN
- **Datenbankspezifisch erlaubt (EMPFOHLEN):** Das fachliche Modell ist eines; die Umsetzung darf je Datenbank abweichen
  (z. B. STRICT nur SQLite, `uuid`/`timestamptz`/RLS nur PostgreSQL). Abweichungen stehen gebündelt im Helfer bzw. in
  einer Weiche `if ($driver === 'pgsql')` mit Kommentar – nicht verstreut.

### A6 Transaktionen und konkurrierende Speicherung (BESCHLOSSEN, Obergrenzen EMPFOHLEN)

- Alles, was zusammengehört, läuft in **einer** Transaktion; bei einem Fehler wird die **gesamte** Transaktion
  zurückgerollt. Seiteneffekte (Mails, Webhooks, Dateien, Jobs) erst nach dem Commit (`afterCommit`).
- **Obergrenzen:** eine Transaktion bleibt unter rund **5 Sekunden** bzw. **10 000 geänderten Zeilen**. Was grösser ist,
  läuft über Staging-Tabellen (prüfen, dann in einer Transaktion übernehmen) oder in Blöcken mit eigenem
  Fortschrittsprotokoll, das sich fortsetzen oder vollständig zurücknehmen lässt. EMPFOHLEN
- **Optimistisches Sperren:** änderbare Fachtabellen haben `lock_version`; gespeichert wird mit
  `WHERE id = ? AND lock_version = ?`; 0 getroffene Zeilen ergibt Konflikt (HTTP 409), nichts wird überschrieben.
  Umsetzung als kleines Trait in `eduksx/core`, kein Fremdpaket.
- Zähler atomar in der Datenbank (`increment()`), Eindeutigkeit über UNIQUE-Index, nicht über vorherige Abfrage.
- SQLite: WAL, `busy_timeout` 5000 ms, kurze Schreibtransaktionen; bei `database is locked` den ganzen Ablauf
  wiederholen.

### A7 Änderungshistorie (BESCHLOSSEN, Erweiterungen EMPFOHLEN)

Jede Datenänderung – Anlegen, Ändern, Löschen, Wiederherstellen – wird mit wer, wann, was festgehalten, in **derselben
Transaktion** wie die Änderung. Module mit eigenem Revisionssystem nutzen dieses; alle anderen Tabellen schreiben in eine
zentrale Tabelle `data_changes`.

| Spalte | Inhalt | Stufe |
| --- | --- | --- |
| `id` | fortlaufende Zahl | BESCHLOSSEN |
| `event_id` | UUID, eindeutig auch über Module und Exporte hinweg | EMPFOHLEN |
| `subject_type`, `subject_id` | Tabelle und `id` des Datensatzes (ohne Constraint, mit Index) | BESCHLOSSEN |
| `organization_id` | Mandant des Datensatzes, leer bei globalen Daten | EMPFOHLEN |
| `action` | `created`, `updated`, `deleted`, `restored` | BESCHLOSSEN |
| `changes` | Feld → `{old, new}` nach den Regeln der Datenklasse (B2) | BESCHLOSSEN, angepasst |
| `actor_type`, `actor_id`, `actor_label` | wer | BESCHLOSSEN |
| `source` | `web`, `api`, `import`, `mcp`, `job`, `system`, `migration` | EMPFOHLEN |
| `transaction_id` | gemeinsame Kennung aller Einträge einer Transaktion | EMPFOHLEN |
| `request_id` | Anfrage-ID aus dem Protokoll | EMPFOHLEN |
| `schema_version` | Stand des Schemas, um alte Einträge richtig zu lesen | EMPFOHLEN |
| `occurred_at` | wann, UTC | BESCHLOSSEN |

- **Erfassung:** über ein Trait im Modell **und** verbindlich über die Service-Schicht. Schreibende Zugriffe am Service
  vorbei (`DB::table()->update()`, Migrationen, Importe) schreiben die Historie selbst oder einen Sammeleintrag mit
  Anzahl. Ein Test pro Modul sucht nach Schreibzugriffen ausserhalb der Services. BESCHLOSSEN/EMPFOHLEN
- **Trigger** nur, wenn ein Weg am Code vorbei anders nicht abzusichern ist – dann für beide Datenbanken, dokumentiert,
  getestet und gepflegt. BESCHLOSSEN
- **Manipulationsschutz:** Einträge sind unveränderlich (keine Updates ausser Pseudonymisierung). Für das
  **Sicherheitsprotokoll** (Rollen, Rechte, Anmeldungen, Löschungen) zusätzlich eine Hash-Verkettung, deren Prüfpunkte
  täglich ausserhalb der Datenbank abgelegt werden (Protokollierung im Leitstand). Für fachliche Historie keine
  Hash-Verkettung. EMPFOHLEN

---

## B · Sicherheit und Datenschutz

### B1 Geltungsbereiche und Mandantentrennung (EMPFOHLEN)

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
   `SET LOCAL app.organization_id`, die Richtlinie lässt nur passende Zeilen zu. ZU PRÜFEN: Aufwand mit Laravel und
   Verbindungspool.
5. Ein Test je Modul legt zwei Organisationen an und prüft, dass keine Abfrage, kein Export und kein Job Daten der
   anderen liefert.

**Isolierte** Instanzen (eigene Datenbank je Kunde) brauchen die Regeln 1–4 nicht für die Trennung, behalten aber die
Spalte `organization_id` dort, wo Daten mit dem zentralen Dienst abgeglichen werden.

Ob persönliche Anpassungen organisationsübergreifend gelten oder je Organisation verschieden sein dürfen, entscheidet
jedes Modul und hält es im Datenmodell fest.

### B2 Datenklassen je Feld (EMPFOHLEN)

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

**Papierkorb (BESCHLOSSEN 12.11.2026, Geltung EMPFOHLEN präzisiert):** Hauptobjekte der Fachdaten und
Organisationsdaten werden zuerst vorläufig gelöscht (`deleted_at`, `deleted_by_id`) und nach einer Frist endgültig.
**Nicht** im Papierkorb: Verknüpfungs-, Hilfs- und Protokolltabellen – sie folgen ihrem Hauptobjekt. Fristen und das
Recht zum Wiederherstellen stellen **nur Super-Admins** ein; Vorgabe [30 Tage].

**Konten (BESCHLOSSEN 12.11.2026):** ebenfalls zuerst vorläufig gelöscht (Anmeldung gesperrt, Sitzungen und Tokens
beendet), Wiederherstellung während der Frist durch Super-Admins. **Ausnahme:** Verlangt eine Person die sofortige
Löschung nach Datenschutzrecht, wird sofort gelöscht. Fristen rechtlich prüfen (ZU PRÜFEN).

**Löschregister (EMPFOHLEN):** Ein Zurückspielen einer Sicherung darf gelöschte Personen nicht wiederbeleben.

1. Jede endgültige Löschung von Personendaten wird zusätzlich in ein **Löschregister ausserhalb der Datenbank**
   geschrieben: nur Art, `id`, Zeitpunkt und Grund – keine Personendaten.
2. Ablage nur anhängend (append-only), verschlüsselt, mit eigener Aufbewahrung, getrennt von den Datenbanksicherungen
   (z. B. eigener Objektspeicher-Bucket mit Objektsperre).
3. Nach jeder Wiederherstellung wendet der Dienst das Register **vor dem Start** automatisch an; erst danach nimmt er
   Anfragen an. Ohne erreichbares Register startet er nicht.
4. Ein Test spielt eine ältere Sicherung zurück und prüft, dass danach keine registrierten Personendaten mehr vorhanden
   sind – in Tabellen, Historie, Archiven und Suchindex.

**Überall löschen:** Löschpflichtige Daten werden auch aus Archiven, Exporten, Staging-Tabellen, Caches und
Suchindizes entfernt. In Sicherungen bleiben sie bis zu deren Ablauf, unbenutzt; das Register verhindert ihre Rückkehr.

**Archive (EMPFOHLEN):** Archivierte Daten (z. B. bei Migrationen entfallende Werte) tragen ihre Datenklasse, eine Frist
und werden verschlüsselt abgelegt; personenbezogene Werte nur, wenn nötig und mit Löschregel.

### B4 Identitäten und Rechte (EMPFOHLEN)

- **Plattformidentität** kommt aus EduKSX-Ident (OIDC). Ein Modul speichert sie als `issuer` + `subject` (zusammen
  eindeutig) – nie die E-Mail als Schlüssel, nie `subject` allein.
- **Lokale Benutzerreferenz:** Das Modul hält nur, was es tatsächlich braucht (Anzeigename, Sprache, Zeitpunkt der
  letzten Anmeldung als Datum); alles andere liest es aus Ident.
- **Rollen und Rechte gelten je Modul und Organisation:** Zuordnung mit `(user_id, organization_id, role)` im Modul;
  Admin im Glossary ist nicht Admin in der Rechtssammlung. Geprüft wird auf Rechte, nicht auf Rollennamen.
- **Super-Admin** ist eine Plattformrolle aus Ident mit zweitem Faktor; welche Rechte sie im Modul gibt, legt das Modul
  fest. OFFEN: Verhältnis zur Rolle «Developer» im Glossary.
- **Servicekonten** sind eigene Identitäten (Client-Credentials), nie Benutzerkonten.

### B5 Datenbankzugänge (EMPFOHLEN, PostgreSQL)

| Zugang | Rechte | Verwendet von |
| --- | --- | --- |
| `<modul>_runtime` | Lesen/Schreiben auf Tabellen, keine DDL, unterliegt RLS | Anwendung, Jobs |
| `<modul>_migrate` | DDL und Daten, nicht Besitzer anderer Module | Migrationen beim Update |
| `<modul>_readonly` | nur Lesen, unterliegt RLS | Auswertungen, Support |

Jedes Modul hat eine eigene Datenbank bzw. ein eigenes Schema; kein Modul liest Tabellen eines anderen (Austausch nur
über APIs). Für SQLite entfällt dieser Abschnitt – die Datei ist nur für den Dienst lesbar.

### B6 Geheimnisse und Verschlüsselung (BESCHLOSSEN/EMPFOHLEN)

Tokens nur gehasht, 2FA-Geheimnisse und Zugangsdaten verschlüsselt (Laravel-Cast `encrypted`); Felder der Klasse
«besonders schützenswert» zusätzlich verschlüsselt gespeichert (EMPFOHLEN).

---

## C · Betrieb

### C1 SQLite und PostgreSQL (EMPFOHLEN)

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
| Laufend | SQLite: Litestream in einen S3-kompatiblen Speicher (z. B. Swiss Backup). PostgreSQL: Base Backup + WAL-Archivierung (z. B. CloudNativePG/Barman) | BESCHLOSSEN / EMPFOHLEN |
| Zeitpunkt wählbar | Wiederherstellung auf jeden Zeitpunkt der Aufbewahrung (PITR) – `pg_dump` allein genügt dafür nicht | EMPFOHLEN |
| Einzelsnapshot | vor jedem Update, jeder Migration, grossen Importen; Dateiname mit Zeitstempel und Version; Prüfsumme und Zeilen je Tabelle | BESCHLOSSEN |
| Verschlüsselt | alle Sicherungen verschlüsselt; Schlüssel getrennt vom gesicherten System und von der Sicherung aufbewahrt (Geheimnisspeicher), Notfallkopie offline | EMPFOHLEN |
| Getestet | Wiederherstellung mindestens monatlich auf einer Kopie, Dauer messen und mit RTO vergleichen | BESCHLOSSEN |
| Nach dem Zurückspielen | Migrationen, Löschregister (B3), Löschfristen – erst dann Anfragen annehmen | EMPFOHLEN |

**RPO und RTO (OFFEN):** verbindliche Ziele je Dienstart. Vorschlag:

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
mehrteiligen Änderung.

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

### D3 Sortierung, Suche, Unicode (EMPFOHLEN)

- Texte werden beim Speichern in **Unicode NFC** normalisiert.
- Für die Suche führt jede durchsuchte Tabelle eine normalisierte Suchspalte (klein, NFC, ohne Akzente – «Ecole» findet
  «École»); gesucht wird nur darin.
- Sortierung für Menschen nach Schweizer Regeln: PostgreSQL mit ICU-Kollation `de-CH-x-icu` (bzw. `fr-CH`, `it-CH` je
  Sprache); SQLite sortiert in der Anwendung (PHP `Collator`), weil es keine passende Kollation mitbringt.
- Volltextsuche über die Datenbank (PostgreSQL `tsvector` je Sprache) oder einen Suchdienst; Suchindizes zählen zu den
  Orten, aus denen gelöscht werden muss (B3).

---

## Checkliste für Pull Requests mit DB-Änderung

- [ ] Standard deckt die Änderung ab – sonst zuerst Konzept-PR
- [ ] Namen nach A1, dritte Normalform nach A2, Ausnahme in der Ausnahmetabelle des Moduls
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

## Entscheide

| Nr. | Frage | Entscheid | Status |
| --- | --- | --- | --- |
| E1 | Aufteilung in Plattform-Standard und Modul-Datenmodell | Standard hier, Fachliches im Modul | BESCHLOSSEN 12.11.2026 |
| E2 | Mehrsprachigkeit für persönliche Daten | nein | BESCHLOSSEN 12.11.2026 |
| E3 | UUID v7 trotz erkennbarem Erstellungszeitpunkt | ja | BESCHLOSSEN 12.11.2026 |
| E4 | RPO/RTO je Dienstart | Vorschlag in C2 | OFFEN |
| E5 | Row-Level Security in PostgreSQL | als zweite Schicht vorgesehen | ZU PRÜFEN |
| E6 | Super-Admin als Plattformrolle aus Ident | Vorschlag in B4 | OFFEN |
| E7 | Hash-Verkettung nur für das Sicherheitsprotokoll | Vorschlag in A7 | EMPFOHLEN |

## Verlauf

- 12.11.2026: Version 1.0 (DB-Entwickler-Guideline, aus dem Glossary) abgenommen (#9).
- 12.11.2026: Version 1.1 nach Architekturreview: Aufteilung Plattform/Modul, Mandantentrennung, Datenklassen,
  Löschregister, Identitäten, Datenbankzugänge, PITR/RPO/RTO, Sprachregeln (#11).
