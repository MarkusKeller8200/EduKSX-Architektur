# Modulregister der EduKSX-Plattform

Stand: 13.11.2026 · Verantwortlich: Markus Keller · Status: **BESCHLOSSEN** 13.11.2026

Einzige Quelle für die **Modulschlüssel**. DB-Standard (E1) und API-Standard (G2) verweisen hierher. Änderungen nur per
Pull Request.

## Regeln

- **Schlüssel intern, englisch, unveränderlich:** Kleinbuchstaben, ohne Bindestrich, englisch (DB A1). Der Schlüssel
  benennt Schema, Datenbankzugänge, Löschregister, Ereignisse (`<key>.<objekt>.<verb>`), Fehlertypen, Token-Präfixe,
  MCP-Werkzeuge und API-Pfade. Ist er einmal vergeben, ändert er sich nie.
- **Marketingname frei:** Wie ein Modul gegenüber Kundinnen und Kunden heisst, wird situativ festgelegt und darf sich
  ändern, ohne dass Code, Datenbank oder API angepasst werden. Die Spalte «Marketingname» ist nur ein Hinweis.
- **Status:** `aktiv` (Repo vorhanden), `geplant` (Schlüssel vergeben, noch kein Repo), `reserviert` (für die
  Produktfamilie freigehalten, noch kein Modul).

## Register

| Schlüssel | Modul (intern) | Marketingname (Stand) | Repo | Betriebsart | Status |
| --- | --- | --- | --- | --- | --- |
| `core` | gemeinsame Bibliothek `eduksx/core` (kein Dienst, Plattform 4.3) | Teil von «EduKSX-Core» | EduKSX-Core | Paket | aktiv (0.1.0) |
| `ident` | Anmeldung, Konten, Organisationen, Rollen | Teil von «EduKSX-Core» | – | zentral | geplant |
| `ops` | Leitstand: Kunden, Instanzen, Versionen, Updates, Zustand | Teil von «EduKSX-Core» | – | intern | geplant |
| `glossary` | Glossar | EduKSX-Glossary | EduKSX-Glossary | zentral | aktiv |
| `codex` | Rechtssammlung | EduKSX-Codex | EduKSX-Codex | zentral | aktiv |
| `intranet` | Intranet einer Schule | Intranet | sek-intranet | isoliert | aktiv |
| `timetable` | Stundenplan | Stundenplan | – | isoliert | geplant |
| `portal`, `connect`, `licence`, `shop`, `sign`, `time`, `services` | Produktfamilie | – | – | – | reserviert |

## Umbenennungen

| Datum | bisher | neu | Grund |
| --- | --- | --- | --- |
| 13.11.2026 | `recht` (DB-Standard) | `codex` | Widerspruch DB/API bereinigt; englisch (API-E35) |
| 13.11.2026 | `stundenplan` | `timetable` | interne Bezeichnungen englisch |
| 13.11.2026 | `leitstand` | `ops` | interne Bezeichnungen englisch |

Alle drei Module hatten noch kein Repo und keine Daten; die Umbenennung war ohne Migration möglich.
