# Konzept: Rollen und Rechte (0.4.0, #77)

Stand: 25.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 25.11.2026 (Chat, Entscheide RO1–RO4);
Abschnitte mit **EMPFOHLEN** gelten, bis das erste Modul sie umsetzt; **ZU PRÜFEN** klärt die Fachperson (#22).

Baut auf der bestehenden Mechanik auf: Rollen je Modul und Organisation, geprüft wird auf Rechte (DB B4); Scopes
`<modul>:<ressource>.<aktion>` (API C2); Rollen über den Claim `eduksx_roles` (Plattform S1); Rollen im Steckbrief (S5).
Grundlage: [Lückenanalyse](LUECKENANALYSE-0.4.0.md) 2.8, Widerspruch W7 der [Gesamtprüfung](GESAMTPRUEFUNG-0.4.0.md).
Verbindlichkeit: Stufen nach [KONZEPT-VORLAGE.md](KONZEPT-VORLAGE.md).

## 1. Ziel

Wer in einem Modul eine Rolle vergibt, findet in jedem Modul dieselben Grundrollen, dieselbe Schreibweise der Rechte und
dieselben Regeln für Befristung, Stellvertretung und Austritt. Eine Schule kann jährlich nachweisen, wer was darf.

**Nichtziele:**
- keine Rollen über Module hinweg («Admin überall»); Ausnahme bleibt der Super-Admin aus Ident
- keine Rollenlogik im Client; geprüft wird immer serverseitig (API C2)

## 2. Personengruppen (BESCHLOSSEN)

Personengruppen beschreiben, **wer** jemand ist; sie geben keine Rechte. Rechte kommen nur aus Rollen.

| Gruppe | Quelle | Typische Rollen |
| --- | --- | --- |
| Schulleitung | Ident / Connect | `admin` in Intranet, Staffing, Timetable |
| Verwaltung | Ident / Connect | `editor` bzw. `admin` in Verwaltungsmodulen |
| Lehrperson | Ident / Connect (Edulog-Rolle Lehrperson) | `reader`, `editor` in fachlichen Modulen |
| Schülerin, Schüler | Connect (Edulog `pupil`) | nur nach RO4 |
| Eltern, Erziehungsberechtigte | Connect (Edulog `legal_guardian`) | nur nach RO4, nur über Portal |
| IT | Ident | `admin`; Super-Admin nur aus Ident mit zweitem Faktor |
| Extern (Ärztin, Zahnarzt, Behörde, Anbieter) | Portal bzw. Servicekonto | nur Portal bzw. Scopes |

## 3. Standardrollen (BESCHLOSSEN, RO1)

Jedes Modul bietet **mindestens** diese drei Rollen an; die Namen sind in allen Modulen gleich.

| Rolle | Bedeutung | Mindestens |
| --- | --- | --- |
| `reader` | liest alles, was die Organisation im Modul sehen darf | alle `*.read` ausser besonders schützenswerten Feldern |
| `editor` | bearbeitet Fachdaten | `reader` + `*.write` der Fachdaten |
| `admin` | verwaltet das Modul in der Organisation: Einstellungen, Rollen, Importe | `editor` + `*.admin`; zweiter Faktor Pflicht |

- **Fachrollen** sind zusätzlich erlaubt (z. B. `moderator` im Glossary), mit Namen nach Steckbrief-Schema
  (`^[a-z][a-z0-9_]*$`).
- **Super-Admin** bleibt Plattformrolle aus Ident (DB B4); bis zum Anschluss an Ident die höchste geschützte Rolle des
  Moduls. Er ist keine Standardrolle und nicht über die Administration vergebbar.
- Rollen sind kombinierbar; die effektiven Rechte sind die Vereinigung aller Rollen (Vorbild Glossary).

## 4. Namensschema der Rechte (BESCHLOSSEN, RO2)

- Ein Recht heisst **`<ressource>.<aktion>`**, ohne Modulschlüssel; das Modul ergibt sich aus dem Ort (Steckbrief,
  `x-eduksx-ability` in der API-Beschreibung).
- **Ressource** wie im Scope und im Pfad (Plural; Schreibweise wie das Steckbrief-Schema: Kleinbuchstaben, Ziffern,
  `_`). **Aktion:** `read`, `write`, `delete`, `admin` oder eine **Fachaktion** (z. B. `publish`, `moderate`,
  `export`, `report`, `read_sensitive`).
- Jede Fachaktion ist einer Scope-Aktion zugeordnet (z. B. `terms.publish` → `write`), damit ein Token mit
  `glossary:terms.write` sie überhaupt erreichen kann; der Scope begrenzt, das Recht entscheidet (API C2).
- Muster: `^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$`. Der Steckbrief (S5) listet die Rechte unter `abilities` mit
  Scope-Aktion (Schema `module-manifest`, ab dieser Version).
- Beispiele: `terms.read`, `terms.publish`, `proposals.write`, `instances.report`, `people.read_sensitive`.

## 5. Rechte auf Datenebene (BESCHLOSSEN, RO3)

**Feldgruppen:** Felder der Datenklasse «besonders schützenswert» (DB B2, Stufe «vertraulich» nach
[KONZEPT-DATENSCHUTZ-ZH.md](KONZEPT-DATENSCHUTZ-ZH.md)) liest und ändert nur, wer das eigene Recht
`<ressource>.read_sensitive` bzw. `<ressource>.write_sensitive` hat. `reader` und `editor` haben es nicht von selbst;
jeder Lesezugriff wird protokolliert (DB B11).

**Teilmengen:** Eine Rollenzuweisung hat einen **Geltungsbereich**:

| Geltungsbereich | Bedeutung | Beispiel |
| --- | --- | --- |
| `organization` | ganze Organisation (Vorgabe) | Schulleitung im Intranet |
| `unit` | eine Einheit der Organisation | Schulhaus Hinterbirch |
| `group` | eine Gruppe | Klasse 2b, Fachschaft |
| `self` | nur eigene Daten | Lehrperson in Time |

Die Zuweisung ist `(user_id, organization_id, role, scope_type, scope_id, valid_from, valid_until, granted_by)`.
Einheiten und Gruppen kommen aus `connect` (Stammdaten, DB E4). Die Prüfung macht ein **Policy-Baustein in
`eduksx/core`**; Module schreiben keine eigene Logik für Geltungsbereiche. RLS in PostgreSQL bleibt die zweite Schicht
(DB-E5, #34).

**Reihenfolge in Core (BESCHLOSSEN 26.11.2026, API G3 «nichts auf Vorrat»):** zuerst Rechte aus Rollen
(`reader`·`editor`·`admin` und Fachrollen), `abilities` im Steckbrief und die Matrix (§8). Geltungsbereiche
(`unit`, `group`, `self`), Befristung, Stellvertretung und `*_sensitive` folgen, sobald das erste Modul sie braucht
(voraussichtlich Time bzw. Intranet).

## 6. Befristung, Stellvertretung, Austritt (EMPFOHLEN)

- **Befristet:** `valid_until` ist bei jeder Zuweisung möglich; abgelaufene Zuweisungen wirken nicht mehr und bleiben im
  Protokoll.
- **Stellvertretung:** eine befristete Zuweisung mit `granted_by` = vertretene Person; sie gibt nie mehr als die
  vertretene Person hat und nie `admin`. Ende spätestens mit der Rückkehr bzw. `valid_until`.
- **Austritt:** Das Ereignis `ident.user.deleted` bzw. die Deaktivierung aus Ident (S4) beendet alle Zuweisungen in
  allen Modulen sofort; `ident.role.changed` gleicht Rollen aus Ident ab. Ohne Ident: Austritt in der Administration
  des Moduls, gleiche Wirkung.
- **Letzter Admin:** Die letzte wirksame Verwaltungsrolle einer Organisation lässt sich nicht entziehen oder sperren
  (Vorbild Glossary).

## 7. Minderjährige (BESCHLOSSEN, RO4 – löst W7)

- **Schülerinnen und Schüler** sehen nur **eigene** Daten (`self`) und nur in Modulen, die das im Steckbrief freigeben.
- **Eltern und Erziehungsberechtigte** sehen nur Daten **ihrer Kinder** (Beziehung aus `connect`) und nur über das
  **Portal**, nie über das Intranet.
- Die Edulog-Rollen `pupil` und `legal_guardian` bleiben gesperrt, bis ein Modul sie im Steckbrief freigibt
  (`audiences` ZU PRÜFEN bei der Umsetzung von Portal bzw. Timetable).
- ZU PRÜFEN (#22): Altersgrenzen (z. B. ab wann Jugendliche selbst entscheiden, was Eltern sehen) und das Ende des
  Zugriffs der Eltern mit der Volljährigkeit.

## 8. Nachweis und Rezertifizierung (EMPFOHLEN)

- **Rollen-Rechte-Matrix je Modul** als Datei `docs/ROLLEN-RECHTE.md`, **aus dem Code erzeugt** (Befehl
  `eduksx:rollen-rechte` in `eduksx/core`, BESCHLOSSEN 26.11.2026); `--check` in der CI prüft, dass Datei und Code
  übereinstimmen.
- **Jährliche Rezertifizierung:** Der `admin` jeder Organisation bestätigt einmal im Jahr die Liste der Zuweisungen;
  nicht bestätigte Zuweisungen von `admin` und `*_sensitive` laufen nach [30 Tagen] ab. Bestätigung im Protokoll.
- Die Matrix ist Teil des Nachweises für das ISMS der Schule (KONZEPT-DATENSCHUTZ-ZH §6).

## 9. Beispielmatrix: Glossary

Übersetzung der heutigen Rechte des Glossary (`docs/KONZEPT-BENUTZER.md` dort) in das Schema; die Umstellung im
Glossary ist ein Folgeauftrag (#83).

| Recht (heute) | Recht (neu) | Scope-Aktion | `reader` (Gast) | Benutzer | `moderator` | `editor` | `admin` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| – | `terms.read` | read | ✓ | ✓ | ✓ | ✓ | ✓ |
| `export` | `terms.export` | read | | ✓ | ✓ | ✓ | ✓ |
| `propose` | `proposals.write` | write | | ✓ | ✓ | ✓ | ✓ |
| `moderate` | `proposals.moderate` | write | | | ✓ | | ✓ |
| `edit-terms` | `terms.write` | write | | | ✓ | ✓ | ✓ |
| `publish` | `terms.publish` | write | | | | | ✓ |
| `edit-official` | `official_terms.write` | write | | | | | ✓ |
| `manage-users` | `users.admin` | admin | | | | | ✓ |
| `import`, `lists` | `imports.write`, `lists.write` | write | | | | | ✓ |
| `service-tokens` | `service_tokens.admin` | admin | | | | | ✓ |
| `system` | `system.admin` | admin | Super-Admin (heute Developer) | | | | |

«Benutzer» und `moderator` bleiben Fachrollen des Glossary. `editor` bearbeitet Begriffe, moderiert aber keine
Vorschläge; ob der bisherige Moderator zu `moderator` + `editor` wird, ist ZU PRÜFEN bei der Umstellung.

## 10. Entscheide

| Nr. | Frage | Optionen | Entscheid | Status |
| --- | --- | --- | --- | --- |
| RO1 | Standardrollen je Modul | reader·editor·admin / fünf Stufen / keine Vorgabe | `reader`, `editor`, `admin`; Fachrollen zusätzlich | BESCHLOSSEN 25.11.2026 |
| RO2 | Namensschema der Rechte | `<ressource>.<aktion>` mit Fachaktionen / nur vier Aktionen / mit Modul | `<ressource>.<aktion>`, Fachaktionen mit Zuordnung zu einer Scope-Aktion | BESCHLOSSEN 25.11.2026 |
| RO3 | Datenebene | Feldgruppen + Teilmengen / nur Teilmengen / je Modul | Feldgruppen (`*_sensitive`) und Geltungsbereiche, Policy-Baustein in Core | BESCHLOSSEN 25.11.2026 |
| RO4 | Minderjährige | Freigabe je Modul / vorerst kein Zugang / Eltern auch im Intranet | SuS nur eigene Daten, Eltern nur Kinder und nur über Portal, Freigabe je Modul; löst W7 | BESCHLOSSEN 25.11.2026 |

## 11. Verlauf

- 25.11.2026: Konzept angelegt (#77), RO1–RO4 im Chat entschieden.
- 26.11.2026: Befehl `eduksx:rollen-rechte` beschlossen; Reihenfolge der Umsetzung in Core nach API G3.
