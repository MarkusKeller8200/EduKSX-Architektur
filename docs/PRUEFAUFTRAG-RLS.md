# Prüfauftrag: Row-Level Security in PostgreSQL (#13)

Stand: 13.11.2026 · Verantwortlich: Markus Keller · Status: **ZU PRÜFEN** – Vorgehen und Empfehlung liegen vor; der
Prototyp entsteht ausserhalb dieses Repos (Nichtziel: kein Anwendungscode), z. B. mit Glossary #191 (PostgreSQL).

Betrifft [DB-Standard B1 Regel 4, B5 und DB-E5](KONZEPT-DB-GUIDELINE.md).

## 1. Frage

Wird Row-Level Security (RLS) als **zweite Schicht** der Mandantentrennung in zentralen Diensten Pflicht – zusätzlich
zum globalen Scope im Modell (B1 Regel 1)? Zu klären sind Laravel, der Verbindungspool (PgBouncer im
Transaktionsmodus), Jobs und der Aufwand.

## 2. Vorgeschlagene Umsetzung (für den Prototyp)

```sql
ALTER TABLE glossary.custom_terms ENABLE ROW LEVEL SECURITY;
ALTER TABLE glossary.custom_terms FORCE ROW LEVEL SECURITY;   -- gilt auch für den Eigentümer
CREATE POLICY organization_isolation ON glossary.custom_terms
  USING (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid)
  WITH CHECK (organization_id = NULLIF(current_setting('app.organization_id', true), '')::uuid);
```

- Ohne gesetzten Kontext liefert die Richtlinie **keine** Zeilen (NULL vergleicht nie wahr) – sicherer Ausfall wie
  Regel 1.
- Die Anwendung setzt den Kontext **in derselben Transaktion** wie die Abfragen:
  `SELECT set_config('app.organization_id', ?, true)` (entspricht `SET LOCAL`, aber mit Parameter). Darum laufen
  Anfragen auf Tabellen «Organisation» in einer Transaktion: Middleware für HTTP, Job-Middleware für Warteschlangen,
  ein Helfer für Befehle.
- `SET` ohne `LOCAL` ist verboten: im Transaktionsmodus von PgBouncer bliebe der Wert an der Verbindung hängen und
  gälte für die nächste Anfrage einer anderen Organisation.
- Rollen nach B5: `<modul>_runtime` und `<modul>_readonly` unterliegen RLS, `<modul>_migrate` ist Eigentümer;
  mandantenübergreifende Plattform-Abfragen über eine eigene Rolle mit `BYPASSRLS` und Protokoll (B1 Regel 2).
- Prepared Statements mit PgBouncer im Transaktionsmodus: ab PgBouncer 1.21 mit `max_prepared_statements`, sonst
  `PDO::ATTR_EMULATE_PREPARES` – im Prototyp festlegen.
- Index auf `organization_id` (ohnehin Pflicht, DB A3), damit die Richtlinie die Abfragen nicht verlangsamt.

## 3. Prototyp

| # | Prüfung | Abnahme |
|---|---|---|
| R1 | Zwei Organisationen, Tabelle «Organisation», Abfrage **ohne** Scope im Code | keine Zeile der fremden Organisation; ohne Kontext gar keine |
| R2 | Schreiben mit falscher `organization_id` | von `WITH CHECK` abgewiesen |
| R3 | PgBouncer im Transaktionsmodus, parallele Anfragen zweier Organisationen (Lasttest) | kein Übersprechen; Kontext nie ausserhalb der Transaktion sichtbar |
| R4 | Job einer Organisation, danach Job der anderen auf demselben Worker | Kontext je Job korrekt, nichts bleibt hängen |
| R5 | Leistung: typische Liste mit und ohne RLS (je 1000 Abrufe) | Unterschied gemessen und notiert |
| R6 | Aufwand: Middleware, Job-Middleware, Migrationen-Helfer | als Baustein für `eduksx/core` (Kandidat Core 0.2) beschrieben |

## 4. Empfehlung

- **Pflicht für zentrale Dienste mit Daten der Klasse «vertraulich» oder höher**, wenn R1–R4 bestehen und R5 unter
  etwa 10 % Mehraufwand bleibt; für die übrigen zentralen Dienste empfohlen. Isolierte Instanzen brauchen RLS nicht
  (B1). EMPFOHLEN.
- Die Helfer (Richtlinie in der Migration, Kontext setzen) gehören nach `eduksx/core`, damit kein Modul sie selbst baut
  (Core-Grundsatz: erst nach dem Prototyp).
- SQLite kennt kein RLS; für SQLite gilt allein Regel 1 – deshalb bleibt der Test mit zwei Organisationen (B1 Regel 5)
  in jedem Modul Pflicht.

## 5. Offene Prüfpunkte

- [ ] Prototyp R1–R6 (Glossary #191 oder eigenes Prototyp-Repo)
- [ ] Entscheid DB-E5 im DB-Standard nachführen (B1 Regel 4)

## 6. Verlauf

- 13.11.2026: Vorgehen und Empfehlung beschrieben; Entscheid nach dem Prototyp.
